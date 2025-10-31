# arca_extract_post_images.py
import json
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright
from arcacfg import CDP_ENDPOINT

OUT_DIR = Path("out")
OUT_DIR.mkdir(parents=True, exist_ok=True)
SEARCH_URLS_FILE = OUT_DIR / "search_urls.jsonl"
LINKS_JSONL = OUT_DIR / "links.jsonl"

ALLOWED_DOMAIN = "ac-o.namu.la"


def extract_images_from_post(page, post_url: str) -> list:
    """
    게시물 페이지에서 이미지 URL을 추출합니다.

    Args:
        page: Playwright 페이지 객체
        post_url: 게시물 URL

    Returns:
        이미지 URL 리스트
    """
    page.goto(post_url, wait_until="domcontentloaded")

    # 방어로직: 페이지가 완전히 로딩되었는지 확인
    # 1. 콘텐츠 컨테이너가 로딩될 때까지 대기
    try:
        page.wait_for_selector("div.fr-view.article-content", timeout=15000)
        print("  [DEBUG] article-content 요소 로딩 완료")
    except Exception:
        print("  [DEBUG] article-content를 찾을 수 없음 (링크가 없을 수 있음)")
        return []

    # 2. <a> 태그 중 자식으로 <img> 포함하는 앵커 모두 추출
    try:
        page.wait_for_selector("a:has(img)", timeout=15000)
        print("  [DEBUG] a:has(img) 요소 감지")
    except Exception:
        print("  [DEBUG] a:has(img) 요소를 찾을 수 없음 (이미지가 없을 수 있음)")
        return []

    # 3. 충분한 <a:has(img)> 요소가 나타날 때까지 대기
    # 스크롤 또는 동적 로딩으로 인해 링크가 계속 추가될 수 있으므로 안정화 대기
    previous_count = 0
    stable_count = 0
    max_retries = 5

    for attempt in range(max_retries):
        current_count = page.locator("a:has(img)").count()
        if current_count == previous_count and current_count > 0:
            stable_count += 1
            if stable_count >= 2:  # 2회 연속 개수가 동일하면 로딩 완료로 판단
                print(f"  [DEBUG] 링크 개수 안정화됨: {current_count}개 (시도: {attempt + 1})")
                break
        else:
            stable_count = 0

        previous_count = current_count
        print(f"  [DEBUG] 현재 링크 개수: {current_count}개 (시도: {attempt + 1}/{max_retries})")
        page.wait_for_timeout(1000)  # 1초 대기 후 다시 확인

    links = page.locator("a:has(img)").evaluate_all(
        """els => Array.from(
               new Set(
                 els.map(a => a.getAttribute('href') || a.href)
                    .filter(h => !!h)
               )
             )"""
    )

    # 절대주소화(필요 시) 및 필터링
    links = [h for h in links if h.lower().startswith("http")]

    # ac-o.namu.la 도메인만 필터링
    links = [h for h in links if ALLOWED_DOMAIN in h.lower()]

    return links


def process_search_urls():
    """
    search_urls.jsonl에서 URL을 읽고 각 게시물에서 이미지를 추출합니다.
    """
    if not SEARCH_URLS_FILE.exists():
        print(f"[ERROR] 파일을 찾을 수 없습니다: {SEARCH_URLS_FILE}")
        print("[INFO] 먼저 arca_search_urls.py를 실행하세요.")
        return

    # search_urls.jsonl 읽기
    print(f"[INFO] 읽는 파일: {SEARCH_URLS_FILE.resolve()}")

    with open(SEARCH_URLS_FILE, "r", encoding="utf-8") as f:
        search_data = json.loads(f.read())

    post_urls = search_data.get("urls", [])
    print(f"[INFO] 총 {len(post_urls)}개의 게시물에서 이미지 추출 시작\n")

    # 브라우저 연결
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()

        # 각 게시물 URL 처리
        for idx, post_url in enumerate(post_urls, 1):
            print(f"[{idx}/{len(post_urls)}] 처리 중: {post_url}")

            try:
                # 게시물에서 이미지 URL 추출
                image_urls = extract_images_from_post(page, post_url)

                # JSONL 레코드 저장
                record = {
                    "source_url": post_url,
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "count": len(image_urls),
                    "download_status": "미처리",
                    "links": image_urls,
                }

                with LINKS_JSONL.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")

                print(f"  [INFO] 추출된 이미지 수: {len(image_urls)}")

            except Exception as e:
                print(f"  [ERROR] 처리 중 오류 발생: {e}")
                continue

        page.close()

    print(f"\n[INFO] 완료 → {LINKS_JSONL.resolve()}")


if __name__ == "__main__":
    process_search_urls()
