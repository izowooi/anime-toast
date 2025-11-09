#!/usr/bin/env python3
"""
PNG to WebP Converter
Recursively converts PNG files to WebP format while maintaining directory structure.
"""

import argparse
from pathlib import Path
from typing import List, Tuple
from PIL import Image


def find_png_files(input_path: Path) -> List[Path]:
    """
    Recursively find all PNG files in the given directory.

    Args:
        input_path: Root directory to search for PNG files

    Returns:
        List of Path objects for all PNG files found
    """
    return list(input_path.rglob("*.png")) + list(input_path.rglob("*.PNG"))


def convert_image(input_file: Path, output_file: Path, quality: int = 80) -> Tuple[bool, int, int]:
    """
    Convert a single PNG file to WebP format.

    Args:
        input_file: Path to input PNG file
        output_file: Path to output WebP file
        quality: WebP quality (0-100)

    Returns:
        Tuple of (success, original_size, converted_size)
    """
    try:
        # Get original file size
        original_size = input_file.stat().st_size

        # Open and convert image
        with Image.open(input_file) as img:
            # Convert RGBA to RGB if necessary (WebP supports both, but RGB is smaller)
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
            img.save(output_file, 'WEBP', quality=quality, method=6)

        # Get converted file size
        converted_size = output_file.stat().st_size

        return True, original_size, converted_size
    except Exception as e:
        print(f"오류 발생: {input_file} - {str(e)}")
        return False, 0, 0


def main():
    """Main function to handle the conversion process."""
    parser = argparse.ArgumentParser(
        description='PNG 파일을 WebP 형식으로 변환합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  %(prog)s                           # 기본 경로(input/character_images/) 사용
  %(prog)s input/other_path/         # 커스텀 경로 지정
  %(prog)s -q 90 input/images/       # Quality 90으로 변환
        """
    )
    parser.add_argument(
        'input_path',
        nargs='?',
        default='input/character_images/',
        help='입력 경로 (기본값: input/character_images/)'
    )
    parser.add_argument(
        '-o', '--output',
        default='output/',
        help='출력 경로 (기본값: output/)'
    )
    parser.add_argument(
        '-q', '--quality',
        type=int,
        default=80,
        help='WebP 품질 (0-100, 기본값: 80)'
    )

    args = parser.parse_args()

    # Convert to Path objects
    input_path = Path(args.input_path)
    output_path = Path(args.output)
    quality = args.quality

    # Validate input path
    if not input_path.exists():
        print(f"오류: 입력 경로를 찾을 수 없습니다: {input_path}")
        return 1

    if not input_path.is_dir():
        print(f"오류: 입력 경로가 디렉토리가 아닙니다: {input_path}")
        return 1

    # Find all PNG files
    print(f"PNG 파일 검색 중: {input_path}")
    png_files = find_png_files(input_path)

    if not png_files:
        print("변환할 PNG 파일이 없습니다.")
        return 0

    print(f"총 {len(png_files)}개의 PNG 파일을 찾았습니다.\n")

    # Statistics
    converted_count = 0
    skipped_count = 0
    failed_count = 0
    total_original_size = 0
    total_converted_size = 0

    # Process each file
    for idx, png_file in enumerate(png_files, 1):
        # Calculate relative path from input to maintain directory structure
        relative_path = png_file.relative_to(input_path)

        # Create output file path with .webp extension
        output_file = output_path / relative_path.with_suffix('.webp')

        # Create output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Check if WebP already exists
        if output_file.exists():
            print(f"[{idx}/{len(png_files)}] 건너뜀 (이미 존재): {relative_path}")
            skipped_count += 1
            continue

        # Convert the file
        print(f"[{idx}/{len(png_files)}] 변환 중: {relative_path}")
        success, original_size, converted_size = convert_image(png_file, output_file, quality)

        if success:
            converted_count += 1
            total_original_size += original_size
            total_converted_size += converted_size

            # Show size reduction
            reduction = 100 * (1 - converted_size / original_size) if original_size > 0 else 0
            print(f"    완료: {original_size:,} bytes → {converted_size:,} bytes ({reduction:.1f}% 감소)")
        else:
            failed_count += 1

    # Print summary
    print("\n" + "="*60)
    print("변환 완료!")
    print("="*60)
    print(f"총 파일 수:     {len(png_files):,}")
    print(f"변환 완료:      {converted_count:,}")
    print(f"건너뜀:         {skipped_count:,}")
    print(f"실패:           {failed_count:,}")

    if converted_count > 0:
        print(f"\n원본 크기:      {total_original_size:,} bytes ({total_original_size / 1024 / 1024:.2f} MB)")
        print(f"변환 후 크기:   {total_converted_size:,} bytes ({total_converted_size / 1024 / 1024:.2f} MB)")
        saved_size = total_original_size - total_converted_size
        saved_percent = 100 * (1 - total_converted_size / total_original_size)
        print(f"절약된 용량:    {saved_size:,} bytes ({saved_size / 1024 / 1024:.2f} MB, {saved_percent:.1f}%)")

    return 0


if __name__ == '__main__':
    exit(main())
