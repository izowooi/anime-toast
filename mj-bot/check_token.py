import os
import urllib.request
import urllib.error
import json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN", "")

print("[1] 토큰 로딩 확인")
print(f"    길이: {len(token)} 문자")
print(f"    앞 3자: {repr(token[:3])} / 뒤 3자: {repr(token[-3:])}")

if not token:
    print("[✗] DISCORD_TOKEN이 .env에 없거나 비어 있습니다.")
    exit(1)

if token != token.strip():
    print("[!] 경고: 토큰에 앞뒤 공백/개행이 포함되어 있습니다. 자동으로 strip() 적용.")
    token = token.strip()

print("\n[2] Discord API 요청 중...")

req = urllib.request.Request(
    "https://discord.com/api/v10/users/@me",
    headers={
        "Authorization": token,
        "User-Agent": "Mozilla/5.0",
    }
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        print(f"[✓] 토큰 유효! 사용자: {data.get('username')}#{data.get('discriminator')} (id: {data.get('id')})")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"[✗] HTTP {e.code} 에러: {body}")
    if e.code == 401:
        print("    → 토큰이 만료되었거나 잘못되었습니다. Discord에서 토큰을 다시 발급받으세요.")
except urllib.error.URLError as e:
    print(f"[✗] 네트워크 에러: {e.reason}")
