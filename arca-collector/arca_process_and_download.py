# arca_process_and_download.py
"""
통합 이미지 추출 및 다운로드 모듈

동작 방식:
1. search_urls.jsonl에서 게시글 URL 읽기
2. 각 게시글 방문 → 이미지 URL 추출 → 즉시 다운로드
3. 다음 게시글로 이동 → 반복

이렇게 하면 이미지 URL이 expire 되기 전에 다운로드할 수 있습니다.
"""

import json
import time
import requests
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
from arcacfg import CDP_ENDPOINT

# 파일 경로
OUT_DIR = Path("out")
OUT_DIR.mkdir(parents=True, exist_ok=True)
SEARCH_URLS_FILE = OUT_DIR / "search_urls.jsonl"
IMAGES_DIR = OUT_DIR / "images"
PROGRESS_FILE = OUT_DIR / "progress.jsonl"

# 설정
ALLOWED_DOMAIN = "ac-o.namu.la"
REQUEST_TIMEOUT = 30
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def extract_post_id_from_url(source_url: str) -> str:
    """게시물 URL에서 게시물 ID를 추출합니다."""
    return source_url.split("/")[-1]


def extract_images_from_post(page, post_url: str) -> list:
    """
    게시물 페이지에서 이미지 URL을 추출합니다.

    Args:
        page: Playwright 페이지 객체
        post_url: 게시물 URL

    Returns:
        이미지 URL 리스트
    """
    try:
        print(f"  [이미지 추출] {post_url}")
        page.goto(post_url, wait_until="domcontentloaded")

        # 콘텐츠 컨테이너 로딩 대기
        try:
            page.wait_for_selector("div.fr-view.article-content", timeout=15000)
            print("    → article-content 요소 발견")
        except Exception:
            print("    → article-content 없음 (이미지 없을 수 있음)")
            return []

        # <img> 태그를 포함한 <a> 요소 로딩 대기
        try:
            page.wait_for_selector("a:has(img)", timeout=15000)
            print("    → a:has(img) 요소 발견")
        except Exception:
            print("    → a:has(img) 없음 (이미지 없음)")
            return []

        # 링크 개수 안정화 대기 (동적 로딩 완료)
        previous_count = 0
        stable_count = 0
        max_retries = 5

        for attempt in range(max_retries):
            current_count = page.locator("a:has(img)").count()
            if current_count == previous_count and current_count > 0:
                stable_count += 1
                if stable_count >= 2:
                    print(f"    → 링크 {current_count}개 안정화")
                    break
            else:
                stable_count = 0

            previous_count = current_count
            page.wait_for_timeout(1000)

        # 링크 추출
        links = page.locator("a:has(img)").evaluate_all(
            """els => Array.from(
                   new Set(
                     els.map(a => a.getAttribute('href') || a.href)
                        .filter(h => !!h)
                   )
                 )"""
        )

        # 필터링: HTTP로 시작하고 ALLOWED_DOMAIN 포함
        links = [h for h in links if h.lower().startswith("http")]
        links = [h for h in links if ALLOWED_DOMAIN in h.lower()]

        print(f"    → {len(links)}개 이미지 추출 완료")
        return links

    except Exception as e:
        print(f"    [ERROR] {e}")
        return []


def download_image(image_url: str, save_path: Path) -> bool:
    """이미지를 다운로드합니다."""
    try:
        response = requests.get(image_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(response.content)

        return True

    except requests.exceptions.RequestException as e:
        print(f"      [ERROR] 다운로드 실패: {e}")
        return False


def download_images_for_post(image_urls: list, post_id: str) -> tuple:
    """
    게시물의 이미지들을 다운로드합니다.

    Returns:
        (성공 개수, 실패 개수)
    """
    if not image_urls:
        return 0, 0

    post_dir = IMAGES_DIR / post_id
    post_dir.mkdir(parents=True, exist_ok=True)

    downloaded_count = 0
    failed_count = 0

    for idx, image_url in enumerate(image_urls, 1):
        # 파일명 추출
        parsed_url = urlparse(image_url)
        path_parts = parsed_url.path.split("/")
        filename_with_params = path_parts[-1]
        filename = filename_with_params.split("?")[0]

        if not filename:
            filename = f"image_{idx}"

        save_path = post_dir / filename

        # 이미 다운로드된 파일 스킵
        if save_path.exists():
            print(f"      [{idx}/{len(image_urls)}] 이미 존재: {filename}")
            downloaded_count += 1
            continue

        print(f"      [{idx}/{len(image_urls)}] 다운로드: {filename}")
        if download_image(image_url, save_path):
            downloaded_count += 1
            print(f"        ✓")
        else:
            failed_count += 1
            if save_path.exists():
                save_path.unlink()

        time.sleep(0.3)  # 서버 부하 완화

    return downloaded_count, failed_count


def save_progress(post_url: str, status: str, images_found: int = 0, images_downloaded: int = 0, images_failed: int = 0):
    """진행 상황을 progress.jsonl에 저장합니다."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "post_url": post_url,
        "status": status,
        "images_found": images_found,
        "images_downloaded": images_downloaded,
        "images_failed": images_failed,
    }

    with open(PROGRESS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def get_processed_urls() -> set:
    """이미 처리된 URL을 읽습니다."""
    processed = set()
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        record = json.loads(line)
                        if record.get("status") == "completed":
                            processed.add(record.get("post_url"))
        except Exception as e:
            print(f"[WARNING] progress 파일 읽기 실패: {e}")
    return processed


def process_and_download():
    """
    메인 처리 함수:
    1. search_urls.jsonl에서 게시글 URL 읽기
    2. 각 게시글 방문 → 이미지 추출 → 즉시 다운로드
    3. 다음 게시글 진행
    """
    # 필수 파일 확인
    if not SEARCH_URLS_FILE.exists():
        print(f"[ERROR] 파일을 찾을 수 없습니다: {SEARCH_URLS_FILE}")
        print("[INFO] 먼저 arca_search_urls.py를 실행하세요.")
        return

    print(f"[INFO] 시작 시간: {datetime.now(timezone.utc).isoformat()}")
    print(f"[INFO] 읽는 파일: {SEARCH_URLS_FILE.resolve()}\n")

    # search_urls.jsonl 읽기
    try:
        with open(SEARCH_URLS_FILE, "r", encoding="utf-8") as f:
            search_data = json.loads(f.read())
    except Exception as e:
        print(f"[ERROR] search_urls.jsonl 읽기 실패: {e}")
        return

    post_urls = search_data.get("urls", [])
    print(f"[INFO] 총 {len(post_urls)}개의 게시물 처리 시작\n")

    # 이미 처리된 URL 확인
    processed_urls = get_processed_urls()
    pending_urls = [url for url in post_urls if url not in processed_urls]

    if pending_urls:
        print(f"[INFO] 미처리: {len(pending_urls)}개 / 완료: {len(processed_urls)}개\n")
    else:
        print(f"[INFO] 모든 URL이 이미 처리되었습니다.\n")
        return

    # 브라우저 연결
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()

        # 각 게시물 처리
        for idx, post_url in enumerate(pending_urls, 1):
            total = len(pending_urls)
            print(f"[{idx}/{total}] 처리 중: {post_url}")

            try:
                # 1. 게시물에서 이미지 URL 추출
                image_urls = extract_images_from_post(page, post_url)

                # 2. 즉시 다운로드
                post_id = extract_post_id_from_url(post_url)
                downloaded, failed = download_images_for_post(image_urls, post_id)

                # 3. 진행 상황 저장
                save_progress(
                    post_url,
                    "completed",
                    images_found=len(image_urls),
                    images_downloaded=downloaded,
                    images_failed=failed,
                )

                print(f"  [완료] 추출: {len(image_urls)}개, 다운로드: {downloaded}개, 실패: {failed}개")
                print()

            except Exception as e:
                print(f"  [ERROR] {e}\n")
                save_progress(post_url, "failed")
                continue

        page.close()

    print(f"\n[완료] 끝 시간: {datetime.now(timezone.utc).isoformat()}")
    print(f"[INFO] 이미지 저장 위치: {IMAGES_DIR.resolve()}")
    print(f"[INFO] 진행 상황: {PROGRESS_FILE.resolve()}")


if __name__ == "__main__":
    process_and_download()
