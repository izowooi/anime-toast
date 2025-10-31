# arca_download_images.py
import json
import time
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime, timezone
import requests

OUT_DIR = Path("out")
LINKS_JSONL = OUT_DIR / "links.jsonl"
IMAGES_DIR = OUT_DIR / "images"

# 요청 타임아웃 (초)
REQUEST_TIMEOUT = 30

# 요청 헤더 (일반적인 브라우저 헤더)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def extract_post_id_from_url(source_url: str) -> str:
    """
    source_url에서 게시물 ID를 추출합니다.
    예: https://arca.live/b/aiart/150865554 → 150865554

    Args:
        source_url: 원본 URL

    Returns:
        게시물 ID
    """
    return source_url.split("/")[-1]


def download_image(image_url: str, save_path: Path) -> bool:
    """
    URL에서 이미지를 다운로드합니다.

    Args:
        image_url: 다운로드할 이미지 URL
        save_path: 저장할 파일 경로

    Returns:
        성공 여부
    """
    try:
        response = requests.get(image_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        with open(save_path, "wb") as f:
            f.write(response.content)

        return True

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] 다운로드 실패 ({image_url}): {e}")
        return False


def process_record(record: dict) -> bool:
    """
    단일 JSONL 레코드를 처리합니다.
    이미지를 다운로드하고 상태를 업데이트합니다.

    Args:
        record: JSONL 레코드 딕셔너리

    Returns:
        처리 성공 여부
    """
    # 이미 처리된 레코드는 건너뜁니다
    if record.get("download_status") == "작업 완료":
        print(f"[SKIP] 이미 처리됨: {record['source_url']}")
        return True

    source_url = record.get("source_url")
    links = record.get("links", [])

    if not links:
        print(f"[INFO] 링크 없음: {source_url}")
        record["download_status"] = "작업 완료"
        return True

    # 게시물 ID로 폴더 생성
    post_id = extract_post_id_from_url(source_url)
    post_dir = IMAGES_DIR / post_id
    post_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[START] 다운로드 시작: {source_url}")
    record["download_status"] = "작업 중"
    print(f"[DEBUG] 상태 변경: 작업 중")

    # 이미지 다운로드 (순차 처리)
    downloaded_count = 0
    failed_count = 0

    for idx, image_url in enumerate(links, 1):
        # 파일명 생성 (URL의 마지막 부분에서 확장자 추출)
        parsed_url = urlparse(image_url)
        path_parts = parsed_url.path.split("/")
        filename_with_params = path_parts[-1]
        # 쿼리 파라미터 제거
        filename = filename_with_params.split("?")[0]
        save_path = post_dir / filename

        # 이미 다운로드된 파일은 건너뜁니다
        if save_path.exists():
            print(f"  [{idx}/{len(links)}] 이미 존재함: {filename}")
            downloaded_count += 1
            continue

        # 다운로드 시도
        print(f"  [{idx}/{len(links)}] 다운로드 중: {filename}")

        if download_image(image_url, save_path):
            downloaded_count += 1
            print(f"    ✓ 완료")
        else:
            failed_count += 1
            # 실패한 파일 제거
            if save_path.exists():
                save_path.unlink()

        # 서버에 부하를 주지 않기 위해 지연
        time.sleep(0.5)

    # 결과 출력 및 상태 업데이트
    print(
        f"[RESULT] 완료: {source_url}"
        f"\n  - 성공: {downloaded_count}/{len(links)}"
        f"\n  - 실패: {failed_count}"
        f"\n  - 저장 위치: {post_dir.resolve()}"
    )

    record["download_status"] = "작업 완료"
    record["download_completed_at"] = datetime.now(timezone.utc).isoformat()
    record["download_count"] = downloaded_count
    record["download_failed_count"] = failed_count

    return True


def update_jsonl_record(original_line: str, updated_record: dict) -> str:
    """
    JSONL 라인을 업데이트합니다.

    Args:
        original_line: 원본 JSONL 라인
        updated_record: 업데이트된 레코드 딕셔너리

    Returns:
        업데이트된 JSONL 라인
    """
    return json.dumps(updated_record, ensure_ascii=False) + "\n"


def download_all_images():
    """
    out/links.jsonl의 모든 미처리 레코드에서 이미지를 다운로드합니다.
    """
    if not LINKS_JSONL.exists():
        print(f"[ERROR] 파일을 찾을 수 없습니다: {LINKS_JSONL}")
        return

    print(f"[INFO] 시작 시간: {datetime.now(timezone.utc).isoformat()}")
    print(f"[INFO] 읽는 파일: {LINKS_JSONL.resolve()}")

    # 모든 레코드를 읽고 처리합니다
    all_records = []
    with open(LINKS_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                all_records.append(json.loads(line))

    print(f"[INFO] 총 {len(all_records)}개의 레코드 발견\n")

    # 각 레코드 처리
    for idx, record in enumerate(all_records, 1):
        print(f"[{idx}/{len(all_records)}] 처리 중...")
        process_record(record)

    # 업데이트된 내용을 다시 저장
    with open(LINKS_JSONL, "w", encoding="utf-8") as f:
        for record in all_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"\n[INFO] 완료 시간: {datetime.now(timezone.utc).isoformat()}")
    print(f"[INFO] 업데이트된 JSONL 저장 완료: {LINKS_JSONL.resolve()}")


if __name__ == "__main__":
    download_all_images()
