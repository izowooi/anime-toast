# arcacfg.py
import os

# CDP(Remote Debugging) 접속 포트 (필요 시 바꾸세요)
CDP_PORT = int(os.environ.get("ARCA_CDP_PORT", "9222"))
CDP_ENDPOINT = f"http://127.0.0.1:{CDP_PORT}"

# 사용자 데이터 디렉터리: 같은 경로를 쓰면 로그인/쿠키가 유지됩니다.
USER_DATA_DIR = os.path.abspath(os.environ.get(
    "ARCA_USER_DATA_DIR",
    os.path.join(os.path.expanduser("~"), ".arca_profile")
))

# 대상 페이지
ARCA_HOME = "https://arca.live"
TARGET_URL = "https://arca.live/b/aiart/150865554"
#TARGET_URL = "https://arca.live/b/aiart/145949734"
