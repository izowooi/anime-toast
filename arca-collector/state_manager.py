# state_manager.py
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional


class StateManager:
    """파이프라인의 상태를 추적하고 저장하는 클래스"""

    def __init__(self, state_file: Path = Path("state.json")):
        """
        Args:
            state_file: 상태를 저장할 JSON 파일 경로
        """
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        """상태 파일을 로드합니다."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARNING] 상태 파일 로드 실패: {e}")
                return self._get_initial_state()
        return self._get_initial_state()

    def _get_initial_state(self) -> Dict[str, Any]:
        """초기 상태를 반환합니다."""
        return {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_updated_at": datetime.now(timezone.utc).isoformat(),
            "current_step": None,
            "steps_completed": [],
            "search": {
                "status": "pending",
                "urls_found": 0,
                "started_at": None,
                "completed_at": None,
            },
            "extract": {
                "status": "pending",
                "processed": 0,
                "total": 0,
                "current_url": None,
                "started_at": None,
                "completed_at": None,
            },
            "download": {
                "status": "pending",
                "processed": 0,
                "total": 0,
                "successful": 0,
                "failed": 0,
                "started_at": None,
                "completed_at": None,
            },
        }

    def save(self) -> None:
        """현재 상태를 파일에 저장합니다."""
        self.state["last_updated_at"] = datetime.now(timezone.utc).isoformat()
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def start_step(self, step_name: str) -> None:
        """특정 단계를 시작합니다."""
        self.state["current_step"] = step_name
        if step_name in self.state:
            self.state[step_name]["status"] = "in_progress"
            self.state[step_name]["started_at"] = datetime.now(timezone.utc).isoformat()
        self.save()
        print(f"[STATE] {step_name} 시작")

    def complete_step(self, step_name: str) -> None:
        """특정 단계를 완료합니다."""
        if step_name in self.state:
            self.state[step_name]["status"] = "completed"
            self.state[step_name]["completed_at"] = datetime.now(timezone.utc).isoformat()

        if step_name not in self.state["steps_completed"]:
            self.state["steps_completed"].append(step_name)

        self.state["current_step"] = None
        self.save()
        print(f"[STATE] {step_name} 완료")

    def fail_step(self, step_name: str, error_msg: str) -> None:
        """특정 단계를 실패로 표시합니다."""
        if step_name in self.state:
            self.state[step_name]["status"] = "failed"
            self.state[step_name]["error"] = error_msg
            self.state[step_name]["failed_at"] = datetime.now(timezone.utc).isoformat()

        self.state["current_step"] = None
        self.save()
        print(f"[STATE] {step_name} 실패: {error_msg}")

    def update_progress(
        self, step_name: str, processed: int = None, total: int = None, **kwargs
    ) -> None:
        """단계의 진행 상황을 업데이트합니다."""
        if step_name in self.state:
            if processed is not None:
                self.state[step_name]["processed"] = processed
            if total is not None:
                self.state[step_name]["total"] = total

            # 추가 필드 업데이트
            for key, value in kwargs.items():
                self.state[step_name][key] = value

        self.save()

    def set_search_results(self, urls_found: int) -> None:
        """검색 결과를 저장합니다."""
        self.state["search"]["urls_found"] = urls_found
        self.save()

    def get_last_completed_step(self) -> Optional[str]:
        """마지막으로 완료된 단계를 반환합니다."""
        if self.state["steps_completed"]:
            return self.state["steps_completed"][-1]
        return None

    def is_step_completed(self, step_name: str) -> bool:
        """특정 단계가 완료되었는지 확인합니다."""
        return step_name in self.state["steps_completed"]

    def get_step_status(self, step_name: str) -> Dict[str, Any]:
        """특정 단계의 상태를 반환합니다."""
        return self.state.get(step_name, {})

    def print_status(self) -> None:
        """현재 전체 상태를 출력합니다."""
        print("\n" + "=" * 60)
        print("📊 파이프라인 상태")
        print("=" * 60)

        # 검색 상태
        search = self.state["search"]
        search_status = "✓" if search["status"] == "completed" else "✗" if search["status"] == "failed" else "⏳"
        print(f"\n[1] 검색 {search_status}")
        print(f"    상태: {search['status']}")
        if search["urls_found"] > 0:
            print(f"    발견된 URL: {search['urls_found']}개")

        # 추출 상태
        extract = self.state["extract"]
        extract_status = "✓" if extract["status"] == "completed" else "✗" if extract["status"] == "failed" else "⏳"
        print(f"\n[2] 이미지 추출 {extract_status}")
        print(f"    상태: {extract['status']}")
        if extract["total"] > 0:
            progress = (extract["processed"] / extract["total"]) * 100
            print(f"    진행: {extract['processed']}/{extract['total']} ({progress:.1f}%)")

        # 다운로드 상태
        download = self.state["download"]
        download_status = "✓" if download["status"] == "completed" else "✗" if download["status"] == "failed" else "⏳"
        print(f"\n[3] 다운로드 {download_status}")
        print(f"    상태: {download['status']}")
        if download["total"] > 0:
            progress = (download["processed"] / download["total"]) * 100
            print(f"    진행: {download['processed']}/{download['total']} ({progress:.1f}%)")
            print(f"    성공: {download['successful']} | 실패: {download['failed']}")

        print("\n" + "=" * 60 + "\n")

    def reset(self) -> None:
        """상태를 초기화합니다."""
        self.state = self._get_initial_state()
        self.save()
        print("[STATE] 상태 초기화 완료")

    def export(self) -> Dict[str, Any]:
        """상태를 딕셔너리로 반환합니다."""
        return self.state.copy()
