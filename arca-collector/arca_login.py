# arca_login.py
import os, sys, time, subprocess, shutil
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
    # 사용자 데이터 디렉터리 생성
    Path(USER_DATA_DIR).mkdir(parents=True, exist_ok=True)
    # 크롬/엣지 실행 (원격 디버깅 포트 + 전용 프로필)
    cmd = [
        browser_path,
        f"--remote-debugging-port={CDP_PORT}",
        f"--user-data-dir={USER_DATA_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        "--new-window",
        "about:blank",
    ]
    # 브라우저는 이 프로세스와 별개로 계속 실행됩니다.
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    browser_path = find_browser()
    print(f"[INFO] Using browser: {browser_path}")
    print(f"[INFO] USER_DATA_DIR: {USER_DATA_DIR}")
    print(f"[INFO] Launching browser on CDP {CDP_ENDPOINT} ...")
    launch_chromium(browser_path)
    # 브라우저 기동 대기
    time.sleep(1.5)

    with sync_playwright() as p:
        # 실행 중인 Chromium에 접속
        # (Chromium 계열에서만 지원됩니다)
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)  # :contentReference[oaicite:4]{index=4}
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()
        page.goto(ARCA_HOME, wait_until="domcontentloaded")
        print(f"[INFO] 열람 페이지: {page.url}")

        print(
            "\n[작업 안내]\n"
            "  1) 브라우저 창에서 직접 로그인(OTP 포함)하세요.\n"
            "  2) 로그인 완료 후 이 콘솔로 돌아와 Enter를 누르세요.\n"
            "     (브라우저 창은 닫지 마세요)\n"
        )
        input("로그인 완료 후 Enter ▶ ")

        # (선택) 인증 상태를 파일로 백업하고 싶다면 주석 해제:
        # state = context.storage_state(path="state.json")  # :contentReference[oaicite:5]{index=5}
        # print("[INFO] storage state 저장: state.json")

        print(
            "\n[다음 단계]\n"
            "  - 이제 수집 스크립트를 실행하세요.\n"
            "    예) uv run python arca_collect.py\n"
            "  - 수집이 끝날 때까지 브라우저 창은 계속 열어 두세요.\n"
        )

if __name__ == "__main__":
    main()
