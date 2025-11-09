#!/usr/bin/env python3
"""
Character Repeater - 파일의 각 캐릭터 이름을 지정된 횟수만큼 반복합니다.
"""

import argparse
import sys
from pathlib import Path


def repeat_characters(file_path: str, repeat_count: int) -> None:
    """
    파일의 각 캐릭터를 지정된 횟수만큼 반복하여 파일을 수정합니다.

    Args:
        file_path: 캐릭터 목록이 있는 파일 경로
        repeat_count: 각 캐릭터를 반복할 횟수
    """
    try:
        # 파일 경로 객체 생성
        path = Path(file_path)

        # 파일 존재 확인
        if not path.exists():
            print(f"❌ 오류: '{file_path}' 파일을 찾을 수 없습니다.")
            sys.exit(1)

        # 파일이 실제 파일인지 확인
        if not path.is_file():
            print(f"❌ 오류: '{file_path}'는 파일이 아닙니다.")
            sys.exit(1)

        # 파일 읽기
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            print(f"❌ 오류: '{file_path}' 파일을 UTF-8로 읽을 수 없습니다.")
            sys.exit(1)

        # 빈 파일 확인
        if not lines:
            print(f"⚠️  경고: '{file_path}' 파일이 비어있습니다.")
            return

        # 반복된 내용 생성
        repeated_lines = []
        for line in lines:
            # 줄바꿈 제거하고 다시 추가 (일관성 유지)
            line_content = line.rstrip('\n')
            if line_content:  # 빈 줄은 건너뛰기
                for _ in range(repeat_count):
                    repeated_lines.append(line_content + '\n')

        # 파일에 다시 쓰기
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.writelines(repeated_lines)

            # 성공 메시지
            print(f"✅ 성공: {len(lines)}개의 캐릭터를 각각 {repeat_count}번 반복했습니다.")
            print(f"📁 파일: {file_path}")
            print(f"📊 총 라인 수: {len(repeated_lines)}")

        except IOError as e:
            print(f"❌ 오류: 파일 쓰기 실패 - {e}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        sys.exit(1)


def main():
    """메인 함수 - CLI 인터페이스 처리"""

    # 파서 생성
    parser = argparse.ArgumentParser(
        description="📝 Character Repeater - 캐릭터 목록 파일의 각 이름을 지정된 횟수만큼 반복합니다.",
        epilog="예시: python character_repeater.py characters.txt 32",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # 인자 추가
    parser.add_argument(
        'file_path',
        help='캐릭터 목록이 포함된 파일 경로'
    )

    parser.add_argument(
        'repeat_count',
        type=int,
        help='각 캐릭터를 반복할 횟수 (양의 정수)'
    )

    # 버전 정보 추가
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    # 인자 파싱
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(1)

    # 반복 횟수 유효성 검사
    if args.repeat_count <= 0:
        print(f"❌ 오류: 반복 횟수는 1 이상의 양의 정수여야 합니다. (입력값: {args.repeat_count})")
        sys.exit(1)

    if args.repeat_count > 10000:
        response = input(f"⚠️  경고: {args.repeat_count}번 반복하면 파일이 매우 커질 수 있습니다. 계속하시겠습니까? (y/N): ")
        if response.lower() != 'y':
            print("작업을 취소했습니다.")
            sys.exit(0)

    # 메인 함수 실행
    repeat_characters(args.file_path, args.repeat_count)


if __name__ == "__main__":
    main()