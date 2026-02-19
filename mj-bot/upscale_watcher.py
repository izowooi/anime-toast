"""
Midjourney 업스케일 감시 + 자동 클릭 스크립트

동작 흐름:
  1. 채널을 감시하며 MJ Bot의 완성된 4-grid 이미지 메시지 대기
  2. 이미지 URL과 프롬프트를 터미널에 출력
  3. 사용자가 U1~U4 중 선택 입력 (q=건너뜀)
  4. 해당 버튼 자동 클릭 → 업스케일 완성 메시지 감지
  5. 업스케일 이미지 자동 다운로드 → ./output/upscaled/

Usage:
    python upscale_watcher.py
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

TOKEN      = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
SERVER_ID  = int(os.getenv("SERVER_ID", "0"))

MJ_BOT_USER_ID = 1022952195194359889
UPSCALE_OUTPUT_DIR = Path("./output/upscaled")

# 업스케일 대기 중인 작업: {message_id: {"prompt": str, "choice": str}}
pending_upscale: dict[int, dict] = {}


client = discord.Client()


@client.event
async def on_ready():
    print(f"[✓] 로그인: {client.user} (ID: {client.user.id})")
    UPSCALE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"\n[*] 채널 감시 시작 (채널 ID: {CHANNEL_ID})")
    print("[*] MJ Bot의 완성 이미지가 감지되면 U1~U4를 선택하세요.")
    print("[*] 종료: Ctrl+C\n")


@client.event
async def on_message(message: discord.Message):
    if message.author.id != MJ_BOT_USER_ID:
        return
    if message.channel.id != CHANNEL_ID:
        return

    content = message.content or ""

    # ── 4-grid 완성 메시지 감지 (U1~U4 버튼 있음) ──
    has_attachment = len(message.attachments) > 0
    is_in_progress = bool(re.search(r'\(\d+%\)', content))

    # U1/U2/U3/U4 버튼이 있는지 확인
    upscale_buttons = _find_upscale_buttons(message)
    if has_attachment and upscale_buttons and not is_in_progress:
        url = message.attachments[0].url
        print(f"\n{'='*60}")
        print(f" [새 이미지 완성]")
        print(f" 프롬프트: {content[:100]}...")
        print(f" 미리보기: {url[:80]}...")
        print(f"{'='*60}")

        # 비동기로 사용자 입력 처리 (메인 이벤트 루프 블로킹 방지)
        asyncio.get_event_loop().create_task(
            _handle_upscale_choice(message, upscale_buttons)
        )

    # ── 업스케일 완성 감지 (버튼 없음, 단일 이미지) ──
    if has_attachment and not upscale_buttons and not is_in_progress:
        # pending_upscale에 부모 메시지 ID가 있으면 업스케일 완성
        ref_id = _get_reference_message_id(message)
        if ref_id and ref_id in pending_upscale:
            info = pending_upscale.pop(ref_id)
            url = message.attachments[0].url
            print(f"\n[✓] 업스케일 완성! ({info['choice']})")
            print(f"    URL: {url[:80]}...")
            asyncio.get_event_loop().create_task(
                _download_upscaled(url, info)
            )


@client.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    await on_message(after)


def _find_upscale_buttons(message: discord.Message) -> dict[str, object]:
    """U1~U4 버튼을 찾아서 {label: component} 딕셔너리 반환"""
    buttons = {}
    for row in message.components:
        children = getattr(row, "children", [])
        for component in children:
            label = getattr(component, "label", "") or ""
            if re.match(r'^U[1-4]$', label):
                buttons[label] = component
    return buttons


def _get_reference_message_id(message: discord.Message) -> int | None:
    """메시지의 참조(reply) 메시지 ID 반환"""
    if message.reference:
        return message.reference.message_id
    return None


async def _handle_upscale_choice(message: discord.Message, buttons: dict):
    """터미널에서 업스케일 선택 받아서 버튼 클릭"""
    valid = sorted(buttons.keys())  # ["U1", "U2", "U3", "U4"]
    print(f" 선택: {', '.join(valid)}  또는  q=건너뜀")

    loop = asyncio.get_event_loop()
    choice = await loop.run_in_executor(None, _get_user_input, f" 입력 > ")
    choice = choice.strip().upper()

    if choice == "Q" or choice == "":
        print("[→] 건너뜀")
        return

    if choice not in buttons:
        print(f"[!] 잘못된 입력: {choice} (유효: {', '.join(valid)})")
        return

    print(f"[→] {choice} 클릭 중...")
    try:
        component = buttons[choice]
        await component.click()
        pending_upscale[message.id] = {
            "choice": choice,
            "prompt": message.content[:80],
            "original_url": message.attachments[0].url if message.attachments else "",
            "timestamp": datetime.now().isoformat(),
        }
        print(f"[✓] {choice} 클릭 완료. 업스케일 완성 대기 중...")
    except Exception as e:
        print(f"[✗] 버튼 클릭 실패: {e}")


def _get_user_input(prompt: str) -> str:
    """동기 입력 (run_in_executor용)"""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return "q"


async def _download_upscaled(url: str, info: dict):
    """업스케일 이미지 다운로드"""
    choice = info["choice"].lower()  # "u1", "u2" 등
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 원본 프롬프트에서 slug 생성
    prompt_slug = re.sub(r'[^\w-]', '_', info["prompt"][:40].strip())
    filename = f"{ts}_{prompt_slug}_{choice}.png"
    path = UPSCALE_OUTPUT_DIR / filename

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(path, "wb") as f:
                    await f.write(await resp.read())
                print(f"[↓] 업스케일 저장: {path}")
            else:
                print(f"[✗] 다운로드 실패: HTTP {resp.status}")


# ───── 진입점 ─────
if __name__ == "__main__":
    missing = []
    if not TOKEN:     missing.append("DISCORD_TOKEN")
    if not CHANNEL_ID: missing.append("CHANNEL_ID")

    if missing:
        print(f"[✗] .env에 다음 값이 없습니다: {', '.join(missing)}")
        raise SystemExit(1)

    print("[…] Discord에 연결 중...")
    client.run(TOKEN)
