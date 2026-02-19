"""
스토리보드 JSON → Midjourney 배치 실행 스크립트

Usage:
    python run_storyboard.py storyboard/act1_daily_life.json
    python run_storyboard.py storyboard/act1_daily_life.json 1 3 5   # 특정 shot만
"""

import json
import sys
from pathlib import Path

import mj_selfbot


def build_prompts(json_path: Path, shot_filter: list[int] | None = None) -> list[dict]:
    """
    storyboard JSON에서 프롬프트 목록 생성.
    shot_filter가 있으면 해당 shot_number만 포함.
    """
    data = json.loads(json_path.read_text(encoding="utf-8"))
    act_num = data["act_number"]
    act_title = data.get("act_title", "")
    shots = data.get("shots", [])

    prompts = []
    for shot in shots:
        shot_num = shot["shot_number"]
        if shot_filter and shot_num not in shot_filter:
            continue

        prompt = shot.get("niji_prompt_hint", "")
        if not prompt:
            print(f"[!] act{act_num} shot{shot_num}: niji_prompt_hint 없음, 건너뜀")
            continue

        shot_type = shot.get("shot_type", "XX")
        mood = shot.get("mood", "unknown")
        filename = f"act{act_num:02d}_shot{shot_num:02d}_{shot_type}_{mood}"

        prompts.append({"prompt": prompt, "filename": filename})

    return prompts


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_storyboard.py <storyboard_json> [shot_number ...]")
        print("  예: python run_storyboard.py storyboard/act1_daily_life.json")
        print("  예: python run_storyboard.py storyboard/act1_daily_life.json 1 3 5")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    if not json_path.exists():
        print(f"[✗] 파일을 찾을 수 없음: {json_path}")
        sys.exit(1)

    shot_filter = [int(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else None

    prompts = build_prompts(json_path, shot_filter)
    if not prompts:
        print("[✗] 실행할 프롬프트가 없습니다.")
        sys.exit(1)

    output_dir = Path(f"./output/{json_path.stem}")

    print(f"[*] 스토리보드: {json_path.name}")
    print(f"[*] 실행할 shot: {len(prompts)}개")
    print(f"[*] 출력 디렉토리: {output_dir}")
    if shot_filter:
        print(f"[*] 필터링된 shot: {shot_filter}")
    print()

    for i, p in enumerate(prompts, 1):
        print(f"  [{i}] {p['filename']}")
        print(f"      {p['prompt'][:80]}...")
    print()

    mj_selfbot.main(prompts=prompts, output_dir=output_dir)


if __name__ == "__main__":
    main()
