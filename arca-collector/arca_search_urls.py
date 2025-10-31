# arca_search_urls.py
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, quote
import yaml
from playwright.sync_api import sync_playwright
from arcacfg import CDP_ENDPOINT

OUT_DIR = Path("out")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "search_urls.jsonl"
PROGRESS_FILE = OUT_DIR / "progress.jsonl"

BASE_DOMAIN = "https://arca.live"


def load_config():
    """
    config.yaml 파일을 읽어 검색 설정을 로드합니다.
    """
    config_path = Path("config.yaml")
    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def get_processed_urls():
    """
    progress.jsonl에서 이미 처리 완료된 URL 목록을 읽어옵니다.

    Returns:
        이미 처리 완료된 URL들의 set
    """
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
            print(f"[WARNING] progress.jsonl 읽기 실패: {e}")
    return processed


def build_search_urls(keyword, target, pages):
    """
    config.yaml의 설정값으로 검색 URL 리스트를 동적으로 생성합니다.

    Args:
        keyword: 검색 키워드
        target: 검색 대상 (nic, kname 등)
        pages: 검색 페이지 리스트

    Returns:
        생성된 검색 URL 리스트
    """
    urls = []
    encoded_keyword = quote(keyword)

    for page in pages:
        url = f"{BASE_DOMAIN}/b/aiart?target={target}&keyword={encoded_keyword}&p={page}"
        urls.append(url)

    return urls


def extract_post_ids(href: str) -> str | None:
    """
    href에서 /b/aiart/xxxxxxxxx 패턴을 추출합니다.

    Args:
        href: a 태그의 href 속성값

    Returns:
        추출된 패턴 또는 None
    """
    match = re.search(r"/b/aiart/\d+", href)
    return match.group(0) if match else None


def collect_search_urls():
    """
    config.yaml의 설정을 참조하여 검색 페이지들을 순차적으로 방문하고 게시물 URL을 수집합니다.
    """
    # config.yaml에서 설정 로드
    config = load_config()
    search_config = config.get("search", {})
    keyword = search_config.get("keyword", "")
    target = search_config.get("target", "nic")
    pages = search_config.get("pages", [1])

    # 동적으로 검색 URL 생성
    search_urls = build_search_urls(keyword, target, pages)

    all_urls = []

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_ENDPOINT)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = context.new_page()

        for search_url in search_urls:
            print(f"\n[INFO] 페이지 방문: {search_url}")
            page.goto(search_url, wait_until="domcontentloaded")

            # 페이지 로딩 완료 대기
            page.wait_for_load_state("networkidle", timeout=10000)
            print("[DEBUG] 네트워크 유휴 상태 도달")

            # vrow column 클래스를 가진 a 태그 모두 찾기
            page.wait_for_selector("a.vrow.column", timeout=10000)
            links = page.locator("a.vrow.column").evaluate_all(
                """els => els.map(a => a.getAttribute('href')).filter(h => !!h)"""
            )

            print(f"[DEBUG] 현재 페이지에서 찾은 링크 수: {len(links)}")

            # 각 href에서 /b/aiart/xxxxxxxxx 패턴 추출
            page_urls = []
            for href in links:
                post_id = extract_post_ids(href)
                if post_id:
                    full_url = urljoin(BASE_DOMAIN, post_id)
                    page_urls.append(full_url)
                    print(f"  {full_url}")

            all_urls.extend(page_urls)

        page.close()

    # 중복 제거
    unique_urls = list(set(all_urls))
    print(f"\n[INFO] 검색된 URL: {len(unique_urls)}개")

    # 이미 처리된 URL 필터링
    processed_urls = get_processed_urls()
    filtered_urls = [url for url in unique_urls if url not in processed_urls]

    print(f"[INFO] 이미 처리됨: {len(unique_urls) - len(filtered_urls)}개 (제외)")
    print(f"[INFO] 새로운 URL: {len(filtered_urls)}개")

    # JSONL 형식으로 저장 (search_params는 config.yaml의 실제 값 사용)
    record = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "search_params": {
            "target": target,
            "keyword": keyword,
            "pages": pages,
        },
        "total_count": len(filtered_urls),
        "urls": filtered_urls,
    }

    with OUT_FILE.open("w", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"[INFO] 저장 완료 → {OUT_FILE.resolve()}")


if __name__ == "__main__":
    collect_search_urls()
