#!/usr/bin/env python3
"""
PNG to WebP In-Place Replacement
Converts PNG files to WebP format and deletes the original PNG files.
Searches up to 2 levels deep in the directory structure.
"""

import argparse
from pathlib import Path
from typing import List, Tuple
from PIL import Image


def find_png_files(root_path: Path, max_depth: int = 2) -> List[Path]:
    """
    Find all PNG files up to max_depth levels deep.

    Args:
        root_path: Root directory to search
        max_depth: Maximum depth to search (0 = root only, 1 = root + 1 level, etc.)

    Returns:
        List of Path objects for all PNG files found
    """
    png_files = []

    def search_directory(current_path: Path, current_depth: int):
        if current_depth > max_depth:
            return

        try:
            for item in current_path.iterdir():
                if item.is_file() and item.suffix.lower() == '.png':
                    png_files.append(item)
                elif item.is_dir() and current_depth < max_depth:
                    search_directory(item, current_depth + 1)
        except PermissionError:
            print(f"경고: 권한 없음 - {current_path}")

    search_directory(root_path, 0)
    return png_files


def convert_and_replace(png_file: Path, quality: int = 80) -> Tuple[bool, int, int, str]:
    """
    Convert a PNG file to WebP and delete the original PNG.

    Args:
        png_file: Path to PNG file
        quality: WebP quality (0-100)

    Returns:
        Tuple of (success, original_size, converted_size, message)
    """
    webp_file = png_file.with_suffix('.webp')

    # Check if WebP already exists
    if webp_file.exists():
        return False, 0, 0, "WebP already exists"

    try:
        # Get original file size
        original_size = png_file.stat().st_size

        # Open and convert image
        with Image.open(png_file) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA'):
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                else:
                    background.paste(img, mask=img.split()[1])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # Save as WebP
            img.save(webp_file, 'WEBP', quality=quality, method=6)

        # Get converted file size
        converted_size = webp_file.stat().st_size

        # Delete original PNG
        png_file.unlink()

        return True, original_size, converted_size, "Success"

    except Exception as e:
        # If conversion failed and WebP was created, remove it
        if webp_file.exists():
            try:
                webp_file.unlink()
            except:
                pass
        return False, 0, 0, f"Error: {str(e)}"


def main():
    """Main function to handle the conversion process."""
    parser = argparse.ArgumentParser(
        description='PNG 파일을 WebP로 변환하고 원본 PNG를 삭제합니다 (2depth까지 탐색).',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  %(prog)s                           # 현재 디렉토리에서 실행
  %(prog)s input/images/             # 특정 경로 지정
  %(prog)s -q 90 input/images/       # Quality 90으로 변환
  %(prog)s --yes input/images/       # 확인 프롬프트 건너뛰기

경고: 이 스크립트는 원본 PNG 파일을 삭제합니다!
      변환 전에 백업을 권장합니다.
        """
    )
    parser.add_argument(
        'input_path',
        nargs='?',
        default='.',
        help='입력 경로 (기본값: 현재 디렉토리)'
    )
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=80,
        help='WebP 품질 (0-100, 기본값: 80)'
    )
    parser.add_argument(
        '-d', '--depth',
        type=int,
        default=2,
        help='탐색할 최대 depth (기본값: 2)'
    )
    parser.add_argument(
        '-y', '--yes',
        action='store_true',
        help='확인 프롬프트 건너뛰기'
    )

    args = parser.parse_args()

    # Convert to Path object
    input_path = Path(args.input_path)
    quality = args.quality
    max_depth = args.depth

    # Validate input path
    if not input_path.exists():
        print(f"오류: 입력 경로를 찾을 수 없습니다: {input_path}")
        return 1

    if not input_path.is_dir():
        print(f"오류: 입력 경로가 디렉토리가 아닙니다: {input_path}")
        return 1

    # Find all PNG files
    print(f"PNG 파일 검색 중 (최대 {max_depth}depth): {input_path.absolute()}")
    png_files = find_png_files(input_path, max_depth)

    if not png_files:
        print("변환할 PNG 파일이 없습니다.")
        return 0

    print(f"\n총 {len(png_files)}개의 PNG 파일을 찾았습니다.\n")

    # Show warning and ask for confirmation
    if not args.yes:
        print("=" * 60)
        print("경고: 이 작업은 원본 PNG 파일을 삭제합니다!")
        print("=" * 60)
        print(f"변환될 파일 수: {len(png_files)}")
        print(f"품질 설정: {quality}")
        print("\n처음 10개 파일:")
        for i, f in enumerate(png_files[:10], 1):
            print(f"  {i}. {f.relative_to(input_path)}")
        if len(png_files) > 10:
            print(f"  ... 외 {len(png_files) - 10}개")
        print()

        response = input("계속하시겠습니까? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("취소되었습니다.")
            return 0
        print()

    # Statistics
    converted_count = 0
    skipped_count = 0
    failed_count = 0
    total_original_size = 0
    total_converted_size = 0

    # Process each file
    for idx, png_file in enumerate(png_files, 1):
        relative_path = png_file.relative_to(input_path) if png_file.is_relative_to(input_path) else png_file

        print(f"[{idx}/{len(png_files)}] {relative_path}")

        success, original_size, converted_size, message = convert_and_replace(png_file, quality)

        if success:
            converted_count += 1
            total_original_size += original_size
            total_converted_size += converted_size

            reduction = 100 * (1 - converted_size / original_size) if original_size > 0 else 0
            print(f"    ✓ 변환 완료: {original_size:,} → {converted_size:,} bytes ({reduction:.1f}% 감소)")
            print(f"    ✓ PNG 파일 삭제됨")
        elif message == "WebP already exists":
            skipped_count += 1
            print(f"    ⊘ 건너뜀: WebP 파일이 이미 존재합니다")
        else:
            failed_count += 1
            print(f"    ✗ 실패: {message}")
            print(f"    ✓ PNG 파일 유지됨 (안전)")

    # Print summary
    print("\n" + "=" * 60)
    print("변환 완료!")
    print("=" * 60)
    print(f"총 파일 수:     {len(png_files):,}")
    print(f"변환 완료:      {converted_count:,}")
    print(f"건너뜀:         {skipped_count:,}")
    print(f"실패:           {failed_count:,}")

    if converted_count > 0:
        print(f"\n원본 크기:      {total_original_size:,} bytes ({total_original_size / 1024 / 1024:.2f} MB)")
        print(f"변환 후 크기:   {total_converted_size:,} bytes ({total_converted_size / 1024 / 1024:.2f} MB)")
        saved_size = total_original_size - total_converted_size
        saved_percent = 100 * (1 - total_converted_size / total_original_size) if total_original_size > 0 else 0
        print(f"절약된 용량:    {saved_size:,} bytes ({saved_size / 1024 / 1024:.2f} MB, {saved_percent:.1f}%)")
        print(f"\n{converted_count}개의 PNG 파일이 삭제되었습니다.")

    return 0


if __name__ == '__main__':
    exit(main())
