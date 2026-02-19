"""
Midjourney Discord Selfbot — 제대로 된 구현
discord.py-self의 SlashCommand를 통해 /imagine 전송

필요 패키지:
    pip install discord.py-self aiohttp aiofiles python-dotenv
"""

import asyncio
import os
import re
import aiohttp
import aiofiles
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import discord

load_dotenv()

# ───── 설정값 ─────
TOKEN      = os.getenv("DISCORD_TOKEN")   # .env 파일에서 로드
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
SERVER_ID  = int(os.getenv("SERVER_ID", "0"))   # 채널이 속한 서버(Guild) ID

# 각 항목: {"prompt": str, "filename": str}
# filename은 확장자 없는 파일명. 없으면 타임스탬프+프롬프트 slug로 자동 생성
PROMPTS = [
    {
        "prompt": "close-up of traffic light blinking, soft bokeh background with girl silhouette, warm afternoon glow, anime style --ar 16:9 --niji 6",
        "filename": "",
    }
]

DELAY_BETWEEN = 8      # 프롬프트 제출 간격 (초) — 너무 빠르면 rate limit
TIMEOUT       = 600    # 이미지 대기 타임아웃 (초, 기본 10분)
OUTPUT_DIR    = Path("./output")

# MJ Bot 공식 Application ID
MJ_BOT_APP_ID = 1022952195194359889
MJ_BOT_USER_ID = 1022952195194359889


# ───── 상태 컨테이너 ─────
class JobState:
    def __init__(self):
        self.current_prompt = ""
        self.current_filename = ""
        self.waiting = False
        self.done_event = asyncio.Event()
        self.results: list[dict] = []

    def reset(self, prompt: str, filename: str = ""):
        self.current_prompt = prompt
        self.current_filename = filename
        self.waiting = True
        self.done_event = asyncio.Event()

    def complete(self, url: str):
        self.results.append({
            "prompt": self.current_prompt,
            "filename": self.current_filename,
            "url": url,
            "timestamp": datetime.now().isoformat(),
        })
        self.waiting = False
        self.done_event.set()

    def fail(self, reason: str):
        self.results.append({
            "prompt": self.current_prompt,
            "filename": self.current_filename,
            "url": None,
            "error": reason,
            "timestamp": datetime.now().isoformat(),
        })
        self.waiting = False
        self.done_event.set()


job = JobState()
client = discord.Client()


# ───── 이벤트 핸들러 ─────

@client.event
async def on_ready():
    print(f"[✓] 로그인: {client.user} (ID: {client.user.id})")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    asyncio.get_event_loop().create_task(run_batch())


@client.event
async def on_message(message: discord.Message):
    """MJ Bot의 완성 메시지 감지"""
    if not job.waiting:
        return
    if message.author.id != MJ_BOT_USER_ID:
        return
    if message.channel.id != CHANNEL_ID:
        return

    content = message.content or ""

    # ── 완성 조건 분석 ──
    # MJ Bot 메시지 패턴:
    #   진행중: "**{prompt}** - <@!uid> (10%)" — 첨부파일 있음(저해상도)
    #   완성:   "**{prompt}** - <@!uid>" — 첨부파일 있음(고해상도), 버튼 컴포넌트 있음
    #   완성2:  embed 방식도 있음

    has_attachment = len(message.attachments) > 0
    has_components = len(message.components) > 0  # U1 U2 U3 U4 버튼 = 완성 신호
    is_in_progress = bool(re.search(r'\(\d+%\)', content))  # "(xx%)" 패턴 = 진행중

    prompt_lower = job.current_prompt.split("--")[0].strip().lower()
    # MJ는 프롬프트를 **굵게** 표시함
    content_lower = content.lower()
    prompt_mentioned = any(
        word in content_lower
        for word in prompt_lower.split()[:5]  # 앞 5단어만 확인
    )

    if has_attachment and has_components and not is_in_progress and prompt_mentioned:
        url = message.attachments[0].url
        print(f"\n[✓] 이미지 완성 감지!")
        print(f"    URL: {url[:80]}...")

        # 이미지 다운로드
        await download_image(url, job.current_filename, job.current_prompt)
        job.complete(url)


@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    """
    MJ Bot은 메시지를 업데이트하면서 진행률을 표시함.
    최종 완성도 message_edit로 오는 경우가 많음.
    """
    await on_message(after)


# ───── 핵심: 슬래시 커맨드 전송 ─────

async def send_imagine(channel: discord.TextChannel, prompt: str):
    """
    /imagine 슬래시 커맨드를 Discord API로 직접 전송.
    discord.py-self는 use_application_commands()를 지원.
    """
    guild = channel.guild

    try:
        # Application Commands 방식
        commands = await guild.application_commands()
        imagine_cmd = next(
            (cmd for cmd in commands if cmd.name == "imagine"),
            None
        )

        if imagine_cmd is None:
            print("[✗] /imagine 커맨드를 찾을 수 없음. MJ Bot이 이 서버에 있는지 확인하세요.")
            return False

        # 슬래시 커맨드 실행
        await imagine_cmd(channel, prompt=prompt)
        print(f"[→] /imagine 전송 완료: {prompt[:50]}...")
        return True

    except AttributeError:
        # discord.py-self 버전에 따라 API가 다를 수 있음
        # fallback: HTTP 직접 호출
        print("[!] slash command API 실패, HTTP fallback 시도...")
        return await send_imagine_http(channel, prompt)

    except Exception as e:
        print(f"[✗] 슬래시 커맨드 전송 실패: {e}")
        return False


async def send_imagine_http(channel: discord.TextChannel, prompt: str):
    """
    Discord Interaction API를 HTTP로 직접 호출하는 fallback.
    /imagine의 command_id는 서버마다 다를 수 있으나 보통 고정.
    """
    command_id = await fetch_imagine_command_id(channel.guild)
    if not command_id:
        print("[✗] command_id 조회 실패")
        return False

    payload = {
        "type": 2,  # APPLICATION_COMMAND
        "application_id": str(MJ_BOT_APP_ID),
        "guild_id": str(channel.guild.id),
        "channel_id": str(channel.id),
        "session_id": "selfbot_session",  # 임의값
        "data": {
            "version": "1166847114203123795",  # /imagine 버전 ID (고정)
            "id": str(command_id),
            "name": "imagine",
            "type": 1,
            "options": [
                {
                    "type": 3,  # STRING
                    "name": "prompt",
                    "value": prompt,
                }
            ],
            "application_command": {
                "id": str(command_id),
                "application_id": str(MJ_BOT_APP_ID),
                "name": "imagine",
                "description": "Create images with Midjourney",
                "type": 1,
            },
            "attachments": [],
        },
        "nonce": str(int(datetime.now().timestamp() * 1000)),
    }

    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://discord.com/api/v9/interactions",
            json=payload,
            headers=headers,
        ) as resp:
            if resp.status == 204:
                print(f"[→] HTTP 방식으로 /imagine 전송 완료")
                return True
            else:
                text = await resp.text()
                print(f"[✗] HTTP 전송 실패: {resp.status} — {text[:200]}")
                return False


async def fetch_imagine_command_id(guild: discord.Guild) -> int | None:
    """
    서버에 등록된 MJ Bot의 슬래시 커맨드 ID를 동적으로 조회.
    서버마다 ID가 다를 수 있음.
    """
    headers = {
        "Authorization": TOKEN,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    }
    url = f"https://discord.com/api/v9/guilds/{guild.id}/application-command-search"
    params = {
        "type": 1,
        "application_id": MJ_BOT_APP_ID,
        "query": "imagine",
        "limit": 10,
        "include_applications": False,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            commands = data.get("application_commands", [])
            imagine = next((c for c in commands if c["name"] == "imagine"), None)
            return int(imagine["id"]) if imagine else None


# ───── 이미지 다운로드 ─────

async def download_image(url: str, filename: str = "", prompt: str = ""):
    """
    filename이 제공되면 그대로 사용 (.png 자동 추가).
    없으면 타임스탬프 + 프롬프트 slug로 자동 생성.
    """
    if filename:
        safe = re.sub(r'[^\w\-]', '_', filename)
        path = OUTPUT_DIR / f"{safe}.png"
    else:
        safe = re.sub(r'[^\w-]', '_', prompt[:40].strip())
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = OUTPUT_DIR / f"{ts}_{safe}.png"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(path, "wb") as f:
                    await f.write(await resp.read())
                print(f"[↓] 저장: {path}")
            else:
                print(f"[✗] 다운로드 실패: HTTP {resp.status}")


# ───── 배치 실행 루프 ─────

async def run_batch():
    await client.wait_until_ready()

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"[✗] 채널 {CHANNEL_ID}를 찾을 수 없음.")
        await client.close()
        return

    print(f"\n{'='*50}")
    print(f" Batch 시작: {len(PROMPTS)}개 프롬프트")
    print(f" 채널: #{channel.name}")
    print(f" 출력 디렉토리: {OUTPUT_DIR}")
    print(f"{'='*50}\n")

    for i, item in enumerate(PROMPTS, 1):
        prompt = item["prompt"] if isinstance(item, dict) else item
        filename = item.get("filename", "") if isinstance(item, dict) else ""

        print(f"[{i}/{len(PROMPTS)}] {prompt[:60]}...")
        if filename:
            print(f"         파일명: {filename}.png")

        job.reset(prompt, filename)

        # 슬래시 커맨드 전송
        success = await send_imagine(channel, prompt)
        if not success:
            job.fail("커맨드 전송 실패")
            continue

        # 결과 대기
        try:
            await asyncio.wait_for(job.done_event.wait(), timeout=TIMEOUT)
            r = job.results[-1]
            if r.get("url"):
                print(f"[{i}/{len(PROMPTS)}] ✓ 완료")
            else:
                print(f"[{i}/{len(PROMPTS)}] ✗ 실패: {r.get('error')}")
        except asyncio.TimeoutError:
            print(f"[{i}/{len(PROMPTS)}] ✗ 타임아웃 ({TIMEOUT}초)")
            job.fail("timeout")

        # 다음 프롬프트 전 대기
        if i < len(PROMPTS):
            print(f"    → {DELAY_BETWEEN}초 후 다음 프롬프트...")
            await asyncio.sleep(DELAY_BETWEEN)

    # ── 결과 요약 ──
    print(f"\n{'='*50}")
    print(" 결과 요약")
    print(f"{'='*50}")
    success_count = sum(1 for r in job.results if r.get("url"))
    print(f" 성공: {success_count} / {len(PROMPTS)}")
    for r in job.results:
        icon = "✓" if r.get("url") else "✗"
        label = r.get("filename") or r["prompt"][:55]
        print(f" {icon} {label}")
    print()

    await client.close()


# ───── 진입점 (외부 import용) ─────

def main(prompts=None, output_dir=None):
    """
    외부 스크립트에서 호출 가능한 진입점.
    prompts: list[dict] — [{"prompt": str, "filename": str}, ...]
    output_dir: str 또는 Path
    """
    global PROMPTS, OUTPUT_DIR

    if prompts is not None:
        PROMPTS = prompts
    if output_dir is not None:
        OUTPUT_DIR = Path(output_dir)

    missing = []
    if not TOKEN:     missing.append("DISCORD_TOKEN")
    if not CHANNEL_ID: missing.append("CHANNEL_ID")
    if not SERVER_ID:  missing.append("SERVER_ID")

    if missing:
        print(f"[✗] .env에 다음 값이 없습니다: {', '.join(missing)}")
        print("    .env.example을 참고하세요.")
        raise SystemExit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("[…] Discord에 연결 중...")
    client.run(TOKEN)


if __name__ == "__main__":
    main()
