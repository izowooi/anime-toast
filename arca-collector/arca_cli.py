#!/usr/bin/env python3
# arca_cli.py
"""
ARCA Collector 통합 CLI 도구 (v2 - 통합 처리 방식)

새로운 동작 방식:
1. login: 초기 로그인 및 브라우저 실행
2. collect-urls: 게시글 URL 수집 (search_urls.jsonl)
3. process: 각 게시글 방문 → 이미지 추출 → 즉시 다운로드 (통합)

이전의 extract와 download가 분리된 방식은 더 이상 사용하지 않습니다.

사용법:
    python arca_cli.py login                    # 초기 로그인
    python arca_cli.py collect-urls             # URL 수집
    python arca_cli.py process                  # 이미지 추출 + 다운로드 (통합)
    python arca_cli.py status                   # 상태 확인
    python arca_cli.py reset                    # 상태 초기화
"""

import argparse
import sys
import yaml
import subprocess
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from state_manager import StateManager


class ArcaCLI:
    """ARCA Collector CLI 메인 클래스"""

    def __init__(self):
        self.config_file = Path("config.yaml")
        self.state_manager = StateManager(Path("state.json"))
        self.config = self._load_config()
        self.out_dir = Path(self.config.get("paths", {}).get("output_dir", "out"))

    def _load_config(self) -> dict:
        """config.yaml을 로드합니다."""
        if not self.config_file.exists():
            print(f"[ERROR] {self.config_file}를 찾을 수 없습니다.")
            sys.exit(1)

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[ERROR] 설정 파일 로드 실패: {e}")
            sys.exit(1)

    def _save_config(self) -> None:
        """현재 설정을 저장합니다."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            print(f"[INFO] 설정 저장 완료: {self.config_file}")
        except Exception as e:
            print(f"[ERROR] 설정 저장 실패: {e}")
            sys.exit(1)

    def cmd_login(self, args) -> None:
        """초기 로그인 명령어 (arca_init.py 실행)"""
        print("\n" + "=" * 60)
        print("🔐 ARCA Collector 초기화 및 로그인")
        print("=" * 60)
        print("\n[INFO] 초기화 및 로그인 스크립트 실행 중...\n")

        try:
            result = subprocess.run(
                ["python", "arca_init.py"],
                check=False,
                timeout=600,  # 10분
            )

            if result.returncode == 0:
                print("\n" + "=" * 60)
                print("✅ 로그인 완료!")
                print("=" * 60)
                print("\n다음 단계: python arca_cli.py collect-urls\n")
            else:
                print("\n[ERROR] 로그인 실패")
                sys.exit(1)

        except subprocess.TimeoutExpired:
            print("[ERROR] 로그인 시간 초과")
            sys.exit(1)
        except Exception as e:
            print(f"[ERROR] 로그인 중 오류: {e}")
            sys.exit(1)

    def cmd_config(self, args) -> None:
        """설정 명령어"""
        if args.action == "get":
            self._config_get(args)
        elif args.action == "set":
            self._config_set(args)
        elif args.action == "show":
            self._config_show()
        else:
            print("[ERROR] 알 수 없는 설정 명령어")
            sys.exit(1)

    def _config_show(self) -> None:
        """현재 설정을 표시합니다."""
        print("\n" + "=" * 60)
        print("⚙️  설정 정보")
        print("=" * 60)

        search = self.config.get("search", {})
        print(f"\n🔍 검색 설정:")
        print(f"   검색어: {search.get('keyword', 'N/A')}")
        print(f"   대상: {search.get('target', 'N/A')}")
        print(f"   페이지: {search.get('pages', [])}")

        download = self.config.get("download", {})
        print(f"\n⬇️  다운로드 설정:")
        print(f"   허용 도메인: {download.get('allowed_domain', 'N/A')}")
        print(f"   타임아웃: {download.get('timeout_seconds', 'N/A')}초")
        print(f"   지연: {download.get('delay_seconds', 'N/A')}초")

        paths = self.config.get("paths", {})
        print(f"\n📁 경로 설정:")
        print(f"   출력: {paths.get('output_dir', 'N/A')}")
        print(f"   로그: {paths.get('logs_dir', 'N/A')}")

        print("\n" + "=" * 60 + "\n")

    def _config_get(self, args) -> None:
        """특정 설정값을 조회합니다."""
        key_path = args.key.split(".")
        value = self.config

        try:
            for key in key_path:
                value = value[key]
            print(f"{args.key} = {value}")
        except KeyError:
            print(f"[ERROR] 설정 '{args.key}'를 찾을 수 없습니다.")

    def _config_set(self, args) -> None:
        """설정값을 변경합니다."""
        key_path = args.key.split(".")
        value = args.value

        # 타입 변환 시도
        if value.lower() in ("true", "false"):
            value = value.lower() == "true"
        elif value.startswith("[") and value.endswith("]"):
            try:
                value = json.loads(value)
            except:
                pass
        elif value.isdigit():
            value = int(value)
        elif "." in value and all(c.isdigit() or c == "." for c in value):
            try:
                value = float(value)
            except:
                pass

        # 중첩된 키에 값 설정
        config = self.config
        for key in key_path[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[key_path[-1]] = value
        self._save_config()
        print(f"[INFO] {args.key} = {value}")

    def cmd_collect_urls(self, args) -> None:
        """URL 수집 명령어 (search_urls.jsonl 생성)"""
        print("\n" + "=" * 60)
        print("🔗 게시글 URL 수집")
        print("=" * 60)

        self.state_manager.start_step("search")

        try:
            print("\n[INFO] 검색 URL 수집 중...\n")
            self._run_search()

            self.state_manager.complete_step("search")

            print("\n" + "=" * 60)
            print("✅ 게시글 URL 수집 완료!")
            print("=" * 60)

            # 수집된 URL 개수 표시
            search_file = self.out_dir / "search_urls.jsonl"
            if search_file.exists():
                with open(search_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    urls_count = len(data.get("urls", []))
                    print(f"\n📊 수집 현황:")
                    print(f"   • 게시글 수: {urls_count}개")

            print(f"\n다음 단계: python arca_cli.py process\n")

        except Exception as e:
            print(f"\n[ERROR] 수집 중 오류: {e}")
            self.state_manager.fail_step("search", str(e))
            sys.exit(1)

    def _run_search(self) -> None:
        """검색 단계 실행"""
        try:
            result = subprocess.run(
                ["python", "arca_search_urls.py"],
                check=True,
                timeout=3600,  # 1시간
            )

            # search_urls.jsonl에서 URL 개수 읽기
            search_file = self.out_dir / "search_urls.jsonl"
            if search_file.exists():
                with open(search_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    urls_found = len(data.get("urls", []))
                    self.state_manager.update_progress(
                        "search",
                        processed=urls_found,
                        total=urls_found,
                    )
                    self.state_manager.state["search"]["status"] = "completed"

        except subprocess.CalledProcessError as e:
            raise Exception(f"검색 스크립트 실패: {e}")


    def cmd_process(self, args) -> None:
        """통합 이미지 추출 및 다운로드 명령어"""
        print("\n" + "=" * 60)
        print("🔄 이미지 추출 및 다운로드 (통합)")
        print("=" * 60)

        # 필수 파일 확인
        search_urls_file = self.out_dir / "search_urls.jsonl"
        if not search_urls_file.exists():
            print("\n[ERROR] search_urls.jsonl을 찾을 수 없습니다.")
            print("[INFO] 먼저 'python arca_cli.py collect-urls'를 실행하세요.")
            sys.exit(1)

        self.state_manager.start_step("extract")

        print("\n[INFO] 각 게시글에서 이미지 추출 및 다운로드 중...\n")
        print("(이 과정은 시간이 오래 걸릴 수 있습니다)\n")

        try:
            result = subprocess.run(
                ["python", "arca_process_and_download.py"],
                check=True,
                timeout=86400,  # 24시간
            )

            # 진행 상황 통계 읽기
            progress_file = self.out_dir / "progress.jsonl"
            if progress_file.exists():
                with open(progress_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    completed = 0
                    total_images = 0
                    failed_posts = 0

                    for line in lines:
                        data = json.loads(line)
                        if data.get("status") == "completed":
                            completed += 1
                            total_images += data.get("images_downloaded", 0)
                        elif data.get("status") == "failed":
                            failed_posts += 1

                    self.state_manager.update_progress(
                        "extract",
                        processed=completed,
                        total=completed + failed_posts,
                    )

            self.state_manager.complete_step("extract")

            print("\n" + "=" * 60)
            print("✅ 이미지 추출 및 다운로드 완료!")
            print("=" * 60)
            print("\n📊 처리 현황:")
            print(f"   • 완료된 게시물: {completed}개")
            print(f"   • 다운로드된 이미지: {total_images}개")
            if failed_posts > 0:
                print(f"   • 실패한 게시물: {failed_posts}개")
            print(f"\n📁 저장 위치: {self.out_dir.resolve()}/images/\n")

        except subprocess.CalledProcessError as e:
            print(f"\n[ERROR] 처리 중 오류: {e}")
            self.state_manager.fail_step("extract", str(e))
            sys.exit(1)

    def cmd_status(self, args) -> None:
        """상태 확인 명령어"""
        self.state_manager.print_status()

    def cmd_reset(self, args) -> None:
        """상태 초기화 명령어"""
        if not args.force:
            response = input("[경고] 상태를 초기화하시겠습니까? (yes/no): ")
            if response.lower() != "yes":
                print("[INFO] 취소됨")
                return

        self.state_manager.reset()
        print("[INFO] 상태가 초기화되었습니다.")


def main():
    parser = argparse.ArgumentParser(
        description="ARCA Collector 통합 CLI 도구 (v2 - 통합 처리)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📋 명령어 목록:

[초기 설정]
  python arca_cli.py login              # 초기화 및 로그인 (최초 1회)

[작업 실행]
  python arca_cli.py collect-urls       # 게시글 URL 수집 (search_urls.jsonl)
  python arca_cli.py process            # 이미지 추출 및 다운로드 (통합)

[유틸리티]
  python arca_cli.py status             # 현재 상태 확인
  python arca_cli.py reset              # 상태 초기화

📝 기본 동작 흐름:
  1. python arca_cli.py login           # 브라우저 실행 및 로그인
  2. python arca_cli.py collect-urls    # 게시글 URL 수집
  3. python arca_cli.py process         # 각 게시글 방문 → 이미지 추출 → 즉시 다운로드

⚠️  주의사항:
  - 로그인 후에는 브라우저 창을 닫지 마세요.
  - process 명령은 시간이 오래 걸립니다.
  - 이미지 URL은 collect-urls 실행 후 process 실행 전에 expire 될 수 있으므로
    즉시 process를 실행하세요.
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="실행할 명령어")

    # login 명령어
    subparsers.add_parser("login", help="초기화 및 로그인 (최초 1회)")

    # collect-urls 명령어
    subparsers.add_parser(
        "collect-urls",
        help="게시글 URL 수집 (search_urls.jsonl 생성)",
    )

    # process 명령어
    subparsers.add_parser(
        "process",
        help="이미지 추출 및 다운로드 (통합) - search_urls.jsonl에서 읽음",
    )

    # status 명령어
    subparsers.add_parser("status", help="파이프라인 상태 확인")

    # reset 명령어
    reset_parser = subparsers.add_parser("reset", help="상태 초기화")
    reset_parser.add_argument("--force", action="store_true", help="확인 없이 초기화")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    # CLI 인스턴스 생성 및 명령어 실행
    cli = ArcaCLI()

    try:
        if args.command == "login":
            cli.cmd_login(args)
        elif args.command == "collect-urls":
            cli.cmd_collect_urls(args)
        elif args.command == "process":
            cli.cmd_process(args)
        elif args.command == "status":
            cli.cmd_status(args)
        elif args.command == "reset":
            cli.cmd_reset(args)
        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\n[INFO] 사용자에 의해 중단됨")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
