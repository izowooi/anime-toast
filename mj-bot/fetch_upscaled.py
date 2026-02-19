"""
Midjourney 업스케일 이미지 일괄 다운로드 스크립트

이미 Discord에서 수동으로 U1~U4 업스케일을 완료한 경우,
채널 히스토리를 조회해서 업스케일된 이미지만 골라 다운로드합니다.

판별 기준:
  - MJ Bot이 보낸 메시지
  - 첨부파일 있음 (이미지)
  - "(xx%)" 진행중 표시 없음
  - U1/U2/U3/U4 버튼 없음 (있으면 4-grid이므로 제외)

Usage:
    python fetch_upscaled.py               # 최근 100개 메시지 조회
    python fetch_upscaled.py --limit 200   # 최근 200개
    python fetch_upscaled.py --hours 24    # 최근 24시간 이내
"""

import argparse
import asyncio
import os
import re
import aiohttp
import aiofiles
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dotenv import load_dotenv
import discord

load_dotenv()

TOKEN      = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

MJ_BOT_USER_ID = 1022952195194359889
OUTPUT_DIR = Path("./output/upscaled")


def parse_args():
    parser = argparse.ArgumentParser(description="MJ 업스케일 이미지 다운로드")
    parser.add_argument("--limit", type=int, default=100,
                        help="조회할 최대 메시지 수 (기본: 100)")
    parser.add_argument("--hours", type=float, default=None,
                        help="최근 N시간 이내 메시지만 조회 (예: --hours 24)")
    return parser.parse_args()


args = parse_args()
client = discord.Client()


@client.event
async def on_ready():
    print(f"[✓] 로그인: {client.user} (ID: {client.user.id})")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"[✗] 채널 {CHANNEL_ID}를 찾을 수 없음.")
        await client.close()
        return

    # 시간 필터
    cutoff = None
    if args.hours:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=args.hours)
        print(f"[*] 최근 {args.hours}시간 이내 메시지 조회 중...")
    else:
        print(f"[*] 최근 {args.limit}개 메시지 조회 중...")

    found = 0
    skipped = 0

    async for message in channel.history(limit=args.limit, after=cutoff, oldest_first=False):
        if not _is_upscaled(message):
            continue

        url = message.attachments[0].url
        filename = _make_filename(message)
        path = OUTPUT_DIR / filename

        # 이미 다운로드된 파일 건너뜀
        if path.exists():
            print(f"[=] 이미 존재: {filename}")
            skipped += 1
            continue

        print(f"[↓] 다운로드: {filename}")
        print(f"    프롬프트: {(message.content or '')[:80]}...")
        await _download(url, path)
        found += 1

    print(f"\n{'='*50}")
    print(f" 완료: {found}개 다운로드, {skipped}개 이미 존재")
    print(f" 저장 위치: {OUTPUT_DIR.resolve()}")
    print(f"{'='*50}")

    await client.close()


def _is_upscaled(message: discord.Message) -> bool:
    """업스케일 이미지 메시지인지 판별"""
    if message.author.id != MJ_BOT_USER_ID:
        return False
    if not message.attachments:
        return False
    # 진행중 메시지 제외
    if re.search(r'\(\d+%\)', message.content or ""):
        return False
    # U1~U4 버튼이 있으면 4-grid → 제외
    for row in message.components:
        for comp in getattr(row, "children", []):
            label = getattr(comp, "label", "") or ""
            if re.match(r'^U[1-4]$', label):
                return False
    return True


def _make_filename(message: discord.Message) -> str:
    """message_id + 프롬프트 slug로 중복 없는 파일명 생성"""
    content = message.content or ""
    # MJ 프롬프트는 **굵게** 표시됨. 별표 제거
    clean = re.sub(r'\*+', '', content)
    # "--ar" 이후 MJ 파라미터 제거
    clean = clean.split("--")[0].strip()
    # 특수문자 → 언더스코어
    slug = re.sub(r'[^\w]', '_', clean[:50]).strip("_")
    ts = message.created_at.strftime("%Y%m%d_%H%M%S")
    return f"{ts}_{slug}.png"


async def _download(url: str, path: Path):
    """URL에서 이미지 다운로드"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(path, "wb") as f:
                    await f.write(await resp.read())
            else:
                print(f"    [✗] 다운로드 실패: HTTP {resp.status}")


if __name__ == "__main__":
    missing = []
    if not TOKEN:     missing.append("DISCORD_TOKEN")
    if not CHANNEL_ID: missing.append("CHANNEL_ID")

    if missing:
        print(f"[✗] .env에 다음 값이 없습니다: {', '.join(missing)}")
        raise SystemExit(1)

    print("[…] Discord에 연결 중...")
    client.run(TOKEN)
