#!/usr/bin/env python3
"""
파일명 일괄 증가 스크립트
특정 번호부터 마지막 파일까지 파일명을 +1 증가시킵니다.
"""

import os
import argparse
import re
from pathlib import Path


def rename_files(folder_path, start_number):
    """
    지정된 폴더에서 start_number부터 마지막까지 파일명을 +1 증가시킵니다.

    Args:
        folder_path: 파일들이 있는 폴더 경로
        start_number: 변경을 시작할 번호 (예: 165)
    """
    folder = Path(folder_path)

    if not folder.exists():
        print(f"오류: 폴더 '{folder_path}'가 존재하지 않습니다.")
        return

    if not folder.is_dir():
        print(f"오류: '{folder_path}'는 폴더가 아닙니다.")
        return

    # 모든 PNG 파일 찾기
    png_files = []
    pattern = re.compile(r'^(\d{5})\.png$')

    for file in folder.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match:
                number = int(match.group(1))
                png_files.append((number, file))

    if not png_files:
        print(f"폴더에 00000.png 형식의 파일이 없습니다.")
        return

    # start_number 이상인 파일들만 필터링
    files_to_rename = [(num, file) for num, file in png_files if num >= start_number]

    if not files_to_rename:
        print(f"{start_number:05d}.png 이상의 파일이 없습니다.")
        return

    # 역순으로 정렬 (큰 번호부터 처리하여 충돌 방지)
    files_to_rename.sort(reverse=True)

    print(f"총 {len(files_to_rename)}개 파일을 변경합니다.")
    print(f"범위: {files_to_rename[-1][0]:05d}.png ~ {files_to_rename[0][0]:05d}.png")
    print()

    # 파일명 변경
    renamed_count = 0
    for number, file in files_to_rename:
        new_number = number + 1
        new_name = f"{new_number:05d}.png"
        new_path = folder / new_name

        try:
            file.rename(new_path)
            print(f"{file.name} -> {new_name}")
            renamed_count += 1
        except Exception as e:
            print(f"오류: {file.name} 변경 실패 - {e}")

    print()
    print(f"완료: {renamed_count}개 파일이 변경되었습니다.")


def main():
    parser = argparse.ArgumentParser(
        description='특정 번호부터 마지막까지 파일명을 +1 증가시킵니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python rename_files.py /path/to/folder 165

  위 명령은 00165.png부터 마지막 파일까지 파일명을 1씩 증가시킵니다.
  (00165.png -> 00166.png, 00166.png -> 00167.png, ...)
        """
    )

    parser.add_argument('folder_path', help='파일들이 있는 폴더 경로')
    parser.add_argument('start_number', type=int, help='변경을 시작할 번호 (예: 165)')

    args = parser.parse_args()

    rename_files(args.folder_path, args.start_number)


if __name__ == '__main__':
    main()
