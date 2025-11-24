#!/usr/bin/env python3
"""
파일을 캐릭터 폴더별로 재배치하는 스크립트
지정된 개수씩 파일을 묶어서 각 캐릭터 폴더로 이동합니다.
"""

import os
import argparse
import shutil
from pathlib import Path


def read_character_folders(character_file_path):
    """
    character_folder.txt 파일을 읽어서 캐릭터 이름 목록을 반환합니다.

    Args:
        character_file_path: character_folder.txt 파일 경로

    Returns:
        캐릭터 이름 리스트
    """
    characters = []

    try:
        with open(character_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:  # 빈 줄이 아닌 경우만 추가
                    characters.append(line)
    except FileNotFoundError:
        print(f"오류: '{character_file_path}' 파일을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"오류: 파일 읽기 실패 - {e}")
        return []

    return characters


def get_sorted_files(folder_path):
    """
    폴더의 png와 webp 파일만 정렬하여 반환합니다.

    Args:
        folder_path: 파일이 있는 폴더 경로

    Returns:
        정렬된 파일 경로 리스트 (png, webp만)
    """
    folder = Path(folder_path)

    if not folder.exists():
        print(f"오류: 폴더 '{folder_path}'가 존재하지 않습니다.")
        return []

    if not folder.is_dir():
        print(f"오류: '{folder_path}'는 폴더가 아닙니다.")
        return []

    # 모든 파일 찾기 (하위 폴더 제외, png와 webp만)
    allowed_extensions = {'.png', '.webp'}
    files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in allowed_extensions]

    # 파일명으로 정렬
    files.sort(key=lambda x: x.name)

    return files


def distribute_files(source_folder, output_folder, files_per_group, character_file_path):
    """
    파일들을 캐릭터 폴더별로 재배치합니다.

    Args:
        source_folder: 원본 파일이 있는 폴더 경로
        output_folder: 출력 폴더 경로
        files_per_group: 그룹당 파일 개수
        character_file_path: character_folder.txt 파일 경로
    """
    # 캐릭터 목록 읽기
    characters = read_character_folders(character_file_path)

    if not characters:
        print("캐릭터 목록을 읽을 수 없습니다.")
        return

    print(f"총 {len(characters)}명의 캐릭터를 찾았습니다.")
    print()

    # 파일 목록 가져오기
    files = get_sorted_files(source_folder)

    if not files:
        print("이동할 파일이 없습니다.")
        return

    print(f"총 {len(files)}개의 파일을 찾았습니다.")
    print()

    # 원본 폴더에서 하위 폴더명 추출 (예: input/pose -> pose)
    source_path = Path(source_folder)
    subfolder_name = source_path.name

    # 파일 그룹별로 처리
    moved_count = 0
    for i, character in enumerate(characters):
        start_idx = i * files_per_group
        end_idx = start_idx + files_per_group

        # 해당 그룹의 파일들
        group_files = files[start_idx:end_idx]

        if not group_files:
            break  # 더 이상 파일이 없으면 종료

        # 대상 폴더 생성 (예: kousaka-honoka/pose)
        target_folder = Path(output_folder) / Path(character) / subfolder_name
        target_folder.mkdir(parents=True, exist_ok=True)

        print(f"[{character}] {len(group_files)}개 파일 이동 중...")

        # 파일 이동
        for file in group_files:
            target_path = target_folder / file.name
            try:
                shutil.move(str(file), str(target_path))
                print(f"  {file.name} -> {target_folder}/")
                moved_count += 1
            except Exception as e:
                print(f"  오류: {file.name} 이동 실패 - {e}")

        print()

    print(f"완료: 총 {moved_count}개 파일이 이동되었습니다.")


def main():
    parser = argparse.ArgumentParser(
        description='파일을 캐릭터 폴더별로 재배치합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  python distribute_files.py input/pose output 15

  위 명령은 input/pose 폴더의 파일들을 15개씩 묶어서
  output/kousaka-honoka/pose, output/ayase-eli/pose 등의 폴더로 이동합니다.

  character_folder.txt 파일은 input/character_folder.txt 경로에 있어야 합니다.
        """
    )

    parser.add_argument('source_folder', help='원본 파일이 있는 폴더 경로 (예: input/pose)')
    parser.add_argument('output_folder', help='출력 폴더 경로 (예: output)')
    parser.add_argument('files_per_group', type=int, help='그룹당 파일 개수 (예: 15)')
    parser.add_argument(
        '--character-file',
        default='input/character_folder.txt',
        help='캐릭터 목록 파일 경로 (기본값: input/character_folder.txt)'
    )

    args = parser.parse_args()

    if args.files_per_group <= 0:
        print("오류: 그룹당 파일 개수는 1 이상이어야 합니다.")
        return

    distribute_files(args.source_folder, args.output_folder, args.files_per_group, args.character_file)


if __name__ == '__main__':
    main()
