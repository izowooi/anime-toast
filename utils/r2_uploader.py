import os
import json
import boto3
from pathlib import Path
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# 1. 환경 변수 로드
load_dotenv()

# 설정 값 가져오기
ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID")
SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
PUBLIC_DOMAIN = os.getenv("R2_PUBLIC_DOMAIN", "")  # 없으면 빈 문자열

# 경로 설정
SOURCE_DIR = Path("./input/r2/fan-gallery")  # 이미지가 있는 폴더
MANIFEST_FILE = Path("./input/r2/images.json")  # React 프로젝트 내의 json 위치라고 가정
R2_FOLDER_PREFIX = "fan-gallery/"  # R2 버킷 내에 저장될 폴더명


def get_r2_client():
    return boto3.client(
        service_name='s3',
        endpoint_url=f'https://{ACCOUNT_ID}.r2.cloudflarestorage.com',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name='auto'
    )


def file_exists_in_r2(s3_client, bucket, key):
    """R2에 파일이 이미 존재하는지 메타데이터(Head)만 조회하여 확인"""
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            # 404 외의 에러는 실제 문제이므로 출력
            print(f"⚠️ Error checking {key}: {e}")
            raise e


def load_manifest():
    """기존 JSON 파일을 로드하거나 없으면 빈 딕셔너리 반환"""
    if MANIFEST_FILE.exists():
        try:
            with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 기존에 리스트 형식이었다면 빈 딕셔너리로 변환
                if isinstance(data, list):
                    print("⚠️ Converting old list format to new dict format...")
                    return {}
                return data
        except json.JSONDecodeError:
            print("⚠️ JSON file corrupted. Starting with empty dict.")
            return {}
    return {}


def save_manifest(data):
    """JSON 파일 저장 (디렉토리가 없으면 생성)"""
    MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Manifest saved to {MANIFEST_FILE}")


def collect_registered_files(manifest_dict):
    """재귀적으로 manifest에서 모든 파일 경로를 수집"""
    registered = set()

    def traverse(data):
        if isinstance(data, list):
            # 리스트면 모든 항목을 등록
            for item in data:
                registered.add(item)
        elif isinstance(data, dict):
            # 딕셔너리면 모든 값을 재귀적으로 탐색
            for value in data.values():
                traverse(value)

    traverse(manifest_dict)
    return registered


def main():
    s3 = get_r2_client()
    manifest = load_manifest()

    # 이미 JSON에 등록된 파일들을 Set으로 만들어 검색 속도 향상
    registered_files = collect_registered_files(manifest)

    # 새로 추가될 항목들을 담을 임시 리스트
    new_entries = []

    # 소스 디렉토리 순회 (이미지 파일만, 재귀적으로)
    extensions = {'.png', '.jpg', '.jpeg', '.webp'}
    files = [f for f in SOURCE_DIR.rglob('*') if f.is_file() and f.suffix.lower() in extensions]

    print(f"📂 Found {len(files)} files in {SOURCE_DIR}...")

    for file_path in files:
        # 파일의 상대 경로를 계산 (폴더 구조 유지)
        relative_path = file_path.relative_to(SOURCE_DIR)
        # R2에 저장될 Key (경로 + 상대 경로, Windows 호환성을 위해 슬래시로 통일)
        r2_key = f"{R2_FOLDER_PREFIX}{str(relative_path).replace(chr(92), '/')}"
        r2_key_normalized = r2_key.replace('\\', '/')

        # 1. R2 업로드 체크
        # 파일이 로컬에 있고 R2에 없는 경우에만 업로드
        if file_exists_in_r2(s3, BUCKET_NAME, r2_key):
            print(f"⏭️  Skipping upload (Exists in R2): {relative_path}")
        else:
            print(f"⬆️  Uploading: {relative_path}")
            try:
                s3.upload_file(str(file_path), BUCKET_NAME, r2_key)
            except Exception as e:
                print(f"❌ Failed to upload {relative_path}: {e}")
                continue  # 업로드 실패 시 JSON 추가 건너뜀

        # 2. JSON 데이터 갱신 (계층 구조로)
        # 업로드 여부와 관계없이, JSON에 정보가 없으면 추가
        if r2_key_normalized not in registered_files:
            # 경로를 분리 (예: character/asaka-karin/pose/00316.webp)
            parts = str(relative_path).replace('\\', '/').split('/')

            # 최소 3단계 깊이가 필요 (category/name/type/filename)
            if len(parts) >= 3:
                category = parts[0]  # "character"
                name = parts[1]      # "asaka-karin"
                type_key = parts[2]  # "pose"

                # 딕셔너리 구조 생성 (없으면 생성)
                if category not in manifest:
                    manifest[category] = {}
                if name not in manifest[category]:
                    manifest[category][name] = {}
                if type_key not in manifest[category][name]:
                    manifest[category][name][type_key] = []

                # 배열에 R2 전체 경로 추가
                manifest[category][name][type_key].append(r2_key_normalized)
                registered_files.add(r2_key_normalized)
                new_entries.append(r2_key_normalized)
            else:
                # 깊이가 부족한 경우 경고
                print(f"⚠️  Skipping (insufficient path depth): {relative_path}")

    # 변경사항이 있을 때만 JSON 저장
    if new_entries:
        print(f"📝 Adding {len(new_entries)} new entries to JSON...")
        save_manifest(manifest)
    else:
        print("✨ No new entries to add to JSON.")


if __name__ == "__main__":
    # 소스 폴더가 없으면 에러 처리
    if not SOURCE_DIR.exists():
        print(f"❌ Error: Source directory '{SOURCE_DIR}' not found.")
    else:
        main()