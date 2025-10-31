# arca_init.py
"""
초기화 및 로그인 모듈
- 브라우저 실행
- 사용자 로그인 (OTP 포함)
- 로그인 상태 유지
"""

import os
import sys
import time
import subprocess
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
from arcacfg import CDP_PORT, CDP_ENDPOINT, USER_DATA_DIR, ARCA_HOME

# OS별 크롬/엣지 실행 파일 후보
CANDIDATES = [
    # Windows Chrome/Edge
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    # macOS Chrome/Edge
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    # Linux
    shutil.which("google-chrome"),
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
    shutil.which("msedge"),
]


def find_browser():
    """브라우저 실행 파일 경로를 찾습니다."""
    env = os.environ.get("ARCA_BROWSER")
    if env and Path(env).exists():
        return env
    for c in CANDIDATES:
        if c and Path(c).exists():
            return c
    raise FileNotFoundError(
        "Chrome/Edge 실행 파일을 찾지 못했습니다. "
        "환경변수 ARCA_BROWSER에 브라우저 경로를 지정하세요."
    )


def launch_chromium(browser_path: str):
    """브라우저를 실행합니다 (원격 디버깅 포트 활성화)."""
    Path(USER_DATA_DIR).mkdir(parents=True, exist_ok=True)
    cmd = [
        browser_path,
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={USER_DATA_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        "--new-window",
        "about:blank",
    ]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def initialize_and_login():
    """
    브라우저를 실행하고 사용자 로그인을 진행합니다.
    로그인 후에는 브라우저가 계속 실행 상태로 유지됩니다.
    """
    try:
        browser_path = find_browser()
        print(f"[INFO] 브라우저: {browser_path}")
        print(f"[INFO] 사용자 데이터 디렉터리: {USER_DATA_DIR}")
        print(f"[INFO] CDP 엔드포인트: {CDP_ENDPOINT}")
        print(f"[INFO] 브라우저 실행 중...\n")

        launch_chromium(browser_path)
        time.sleep(2)  # 브라우저 기동 대기

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = context.new_page()
            page.goto(ARCA_HOME, wait_until="domcontentloaded")

            print(f"[INFO] 페이지: {page.url}\n")
            print("[안내]")
            print("  1) 브라우저 창에서 직접 로그인 (OTP 포함)")
            print("  2) 로그인 완료 후 이 콘솔로 돌아와 Enter 키 입력")
            print("  3) 브라우저 창은 닫지 말 것 (백그라운드에서 계속 실행)\n")

            input(">>> 로그인 완료 후 Enter 입력: ")

            print("\n[완료]")
            print("  - 로그인 상태가 저장되었습니다.")
            print("  - 이제 다음 단계를 실행할 수 있습니다.")
            print("  - 브라우저는 계속 열어두세요.\n")

            return True

    except Exception as e:
        print(f"[ERROR] 초기화 중 오류: {e}")
        return False


if __name__ == "__main__":
    success = initialize_and_login()
    sys.exit(0 if success else 1)
