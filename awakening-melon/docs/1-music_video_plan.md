# AI 뮤직비디오 제작 완벽 가이드

## 📋 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [필요한 도구 및 준비사항](#필요한-도구-및-준비사항)
3. [단계별 제작 워크플로우](#단계별-제작-워크플로우)
4. [자동화 스크립트](#자동화-스크립트)
5. [품질 체크리스트](#품질-체크리스트)
6. [문제 해결 가이드](#문제-해결-가이드)

---

## 프로젝트 개요

### 목표
AI를 활용하여 주제 선정부터 최종 영상 편집까지 완성도 높은 뮤직비디오를 제작합니다.

### 전체 워크플로우
```
주제 선정 → 가사 생성 → 음악 제작 → 콘티 작성 
→ 키프레임 이미지 생성 → 동영상 변환 → 최종 편집
```

### 예상 소요 시간
- **초기 제작**: 6-8시간
- **자동화 구축 후**: 3-4시간

---

## 필요한 도구 및 준비사항

### 1. AI 서비스 (모두 구독 중)
- **Suno AI**: 음악 생성
- **Nijijourney**: 애니메이션 스타일 이미지 생성
- **Gemini**: 가사 및 콘티 생성
- **Veo 3**: 이미지→동영상 변환

### 2. API 및 개발 도구
```bash
# 필요한 Python 패키지
pip install anthropic replicate requests aiohttp ffmpeg-python librosa

# Node.js 패키지 (선택사항)
npm install @anthropic-ai/sdk openai replicate
```

### 3. 편집 소프트웨어
- **DaVinci Resolve** (무료) 또는 **Adobe Premiere Pro**
- **FFmpeg** (커맨드라인 영상 처리)

### 4. 프로젝트 폴더 구조
```
music-video-project/
├── 01_theme/              # 주제 및 기획
├── 02_lyrics/             # 생성된 가사
├── 03_music/              # Suno 생성 음악
├── 04_storyboard/         # 콘티 JSON 파일
├── 05_images/             # Nijijourney 이미지
├── 06_videos/             # 개별 영상 클립
├── 07_final/              # 최종 결과물
└── scripts/               # 자동화 스크립트
```

---

## 단계별 제작 워크플로우

## STEP 1: 주제 선정 및 기획

### 1-1. 주제 결정
뮤직비디오의 핵심 메시지와 분위기를 결정합니다.

**예시 주제**:
- "꿈을 향해 날아가는 소녀"
- "사이버펑크 도시의 밤"
- "첫사랑의 추억"

### 1-2. 무드보드 작성
주제에 맞는 시각적 레퍼런스를 수집합니다.

```markdown
# 무드보드 예시
## 색감
- 주조색: 파스텔 핑크, 하늘색
- 보조색: 골드, 화이트

## 분위기
- 따뜻하고 몽환적
- Studio Ghibli 스타일
- 부드러운 빛과 그림자

## 레퍼런스
- 센과 치히로의 행방불명 (배경)
- 너의 이름은 (색감)
```

**💡 TIP**: Pinterest나 ArtStation에서 레퍼런스 이미지를 5-10장 저장하세요.

---

## STEP 2: 가사 생성 (Gemini)

### 2-1. Gemini로 가사 작성

**프롬프트 템플릿**:
```
너는 전문 작사가야. 다음 주제로 뮤직비디오용 가사를 작성해줘.

주제: [당신의 주제]
장르: [팝/발라드/록 등]
분위기: [희망적/슬픈/역동적 등]
길이: 2분 30초 내외 (Verse 2개 + Chorus 2개 + Bridge)

조건:
- 각 섹션을 명확히 구분해줘 ([Verse 1], [Chorus] 등)
- Suno AI에 입력할 수 있는 형식으로
- 감정 전환이 자연스러워야 함
- 시각적 이미지를 떠올릴 수 있는 표현 사용
```

### 2-2. 가사 구조 검증

생성된 가사가 다음 구조를 따르는지 확인:
```
[Intro] (5-10초)
[Verse 1] (20-30초)
[Chorus] (20-30초)
[Verse 2] (20-30초)
[Chorus] (20-30초)
[Bridge] (15-20초)
[Outro] (10-15초)
```

**💡 TIP**: 각 섹션의 예상 시간을 메모해두면 콘티 작성 시 유용합니다.

---

## STEP 3: 음악 생성 (Suno AI)

### 3-1. Suno에서 3-5곡 생성

**Suno 입력 방법**:
1. Suno AI 웹사이트 접속
2. Custom Mode 선택
3. 가사 붙여넣기
4. Style of Music 입력 예시:
   ```
   Anime opening, J-pop, uplifting, female vocals, 
   orchestral elements, 130 BPM
   ```

**생성 전략**:
- 같은 가사로 3-5개 버전 생성
- 보컬 스타일(남성/여성/혼성)을 다르게 시도
- BPM을 조정해가며 테스트 (느린 곡 vs 빠른 곡)

### 3-2. 최적의 곡 선정 기준

| 평가 항목 | 체크 포인트 |
|----------|------------|
| **가사 전달력** | 발음이 명확한가? |
| **감정 표현** | 가사의 감정이 잘 전달되는가? |
| **영상 편집 용이성** | 명확한 비트와 섹션 구분이 있는가? |
| **전체 흐름** | 지루한 구간 없이 몰입되는가? |

### 3-3. 선정곡 분석

선택한 곡의 메타데이터를 추출합니다:

```python
import librosa
import numpy as np

def analyze_song(audio_path):
    """
    노래의 BPM, 비트 타이밍, 섹션을 분석
    """
    # 오디오 로드
    y, sr = librosa.load(audio_path)
    
    # BPM 추출
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    
    # 구조 분석 (Verse, Chorus 추정)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    
    return {
        'bpm': tempo,
        'beat_times': beat_times.tolist(),
        'duration': librosa.get_duration(y=y, sr=sr)
    }

# 사용 예시
song_data = analyze_song('03_music/selected_song.mp3')
print(f"BPM: {song_data['bpm']:.1f}")
print(f"총 길이: {song_data['duration']:.1f}초")
```

**💡 TIP**: BPM이 높을수록 빠른 컷 전환이 필요합니다. BPM 120 이상이면 3-5초 컷, 90 이하면 5-8초 컷 권장.

---

## STEP 4: 콘티 작성 (Gemini)

### 4-1. 구조화된 콘티 스키마 정의

```python
from typing import List, Literal
from pydantic import BaseModel

class Shot(BaseModel):
    """개별 컷(씬) 정의"""
    shot_number: int                                    # 컷 번호
    timestamp_start: float                              # 시작 시간 (초)
    timestamp_end: float                                # 종료 시간 (초)
    lyrics_line: str                                    # 해당 구간 가사
    scene_description: str                              # 씬 설명
    shot_type: Literal["CU", "MS", "LS", "ECU"]        # 샷 타입
    camera_movement: Literal["static", "pan", "zoom", "dolly"]
    character_action: str                               # 캐릭터 동작
    mood: str                                           # 분위기 (bright/dark/dramatic)
    visual_style: str                                   # 시각적 스타일 디테일
    
class Storyboard(BaseModel):
    """전체 콘티"""
    title: str
    total_duration: float
    shots: List[Shot]
```

**용어 설명**:
- **CU (Close-Up)**: 얼굴 클로즈업
- **MS (Medium Shot)**: 상반신
- **LS (Long Shot)**: 전신 또는 넓은 배경
- **ECU (Extreme Close-Up)**: 눈, 손 등 극단적 클로즈업

### 4-2. Gemini로 콘티 생성

**프롬프트**:
```python
prompt = f"""
당신은 애니메이션 뮤직비디오 감독입니다. 
다음 가사와 노래 정보를 바탕으로 상세한 콘티를 작성하세요.

# 노래 정보
- 제목: {song_title}
- BPM: {bpm}
- 총 길이: {duration}초
- 장르: {genre}

# 가사
{lyrics}

# 시각적 스타일
{visual_references}

# 요구사항
1. 30-50개의 컷으로 나눠주세요
2. 각 컷은 3-8초 길이로 (BPM에 따라 조정)
3. 비트가 강한 구간(Chorus)에는 역동적인 샷 배치
4. 가사의 감정 변화에 따라 shot_type과 mood 변경
5. 캐릭터 일관성을 위해 같은 주인공 설정 유지

# 출력 형식
JSON 형식으로 위의 Storyboard 스키마를 따라 출력하세요.
"""

import anthropic

client = anthropic.Anthropic(api_key="YOUR_API_KEY")

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=8000,
    messages=[{
        "role": "user",
        "content": prompt
    }]
)

# JSON 파싱
import json
storyboard_json = json.loads(response.content[0].text)
```

### 4-3. 콘티 검증 및 조정

생성된 콘티를 검토합니다:

```python
def validate_storyboard(storyboard: Storyboard, song_duration: float):
    """
    콘티의 타이밍이 노래 길이와 맞는지 검증
    """
    issues = []
    
    # 1. 총 길이 체크
    last_shot_end = storyboard.shots[-1].timestamp_end
    if abs(last_shot_end - song_duration) > 2.0:
        issues.append(f"콘티 길이({last_shot_end}초)가 노래 길이({song_duration}초)와 {abs(last_shot_end - song_duration):.1f}초 차이남")
    
    # 2. 컷 간 공백 체크
    for i in range(len(storyboard.shots) - 1):
        current_end = storyboard.shots[i].timestamp_end
        next_start = storyboard.shots[i + 1].timestamp_start
        if next_start - current_end > 0.1:
            issues.append(f"컷 {i+1}과 {i+2} 사이 공백 {next_start - current_end:.2f}초")
    
    # 3. 컷 길이 체크 (너무 짧거나 긴 컷)
    for shot in storyboard.shots:
        duration = shot.timestamp_end - shot.timestamp_start
        if duration < 2.0:
            issues.append(f"컷 {shot.shot_number}: 너무 짧음 ({duration:.1f}초)")
        elif duration > 10.0:
            issues.append(f"컷 {shot.shot_number}: 너무 김 ({duration:.1f}초)")
    
    return issues

# 검증 실행
issues = validate_storyboard(storyboard, song_data['duration'])
if issues:
    print("⚠️ 콘티 조정 필요:")
    for issue in issues:
        print(f"  - {issue}")
```

**💡 TIP**: 문제가 발견되면 Gemini에게 피드백을 주고 재생성을 요청하세요.

---

## STEP 5: 이미지 생성 (Nijijourney)

### 5-1. Character Reference 이미지 먼저 생성

일관된 캐릭터를 위해 **첫 번째 이미지가 가장 중요**합니다.

**초기 프롬프트 예시**:
```
A young girl with long flowing brown hair, bright blue eyes, 
wearing a white summer dress, standing in a flower field, 
anime style, Studio Ghibli inspired, soft pastel colors, 
warm lighting, gentle smile, age 16, full body shot
--ar 16:9 --niji 6 --style expressive
```

**생성 절차**:
1. Nijijourney에서 위 프롬프트로 4개 생성
2. 가장 마음에 드는 이미지 선택하여 Upscale
3. 해당 이미지 URL 복사 (이후 모든 이미지에 사용)

### 5-2. 콘티 기반 프롬프트 자동 생성

```python
def generate_niji_prompt(shot: Shot, character_ref_url: str, style_ref_url: str) -> str:
    """
    콘티의 각 샷을 Nijijourney 프롬프트로 변환
    """
    # Shot type별 프롬프트 조정
    shot_descriptions = {
        "CU": "close-up portrait shot, focus on face",
        "MS": "medium shot, waist up",
        "LS": "wide shot, full body with background",
        "ECU": "extreme close-up, eyes or hands detail"
    }
    
    # Camera movement 표현
    camera_descriptions = {
        "static": "static camera",
        "pan": "dynamic pan movement",
        "zoom": "cinematic zoom effect",
        "dolly": "dolly tracking shot"
    }
    
    # 프롬프트 조합
    prompt = f"""
{shot.scene_description}, {shot.character_action},
{shot_descriptions[shot.shot_type]},
{camera_descriptions[shot.camera_movement]},
{shot.visual_style}, {shot.mood} mood,
anime style, Studio Ghibli inspired, soft color palette,
volumetric lighting, detailed background,
--cref {character_ref_url} --cw 100
--sref {style_ref_url} --sw 50
--ar 16:9 --niji 6 --style expressive
""".strip()
    
    return prompt

# 전체 콘티에 대해 프롬프트 생성
character_ref = "https://s.mj.run/YOUR_CHARACTER_IMAGE_ID"
style_ref = "https://s.mj.run/YOUR_STYLE_IMAGE_ID"

prompts = []
for shot in storyboard.shots:
    prompt = generate_niji_prompt(shot, character_ref, style_ref)
    prompts.append({
        'shot_number': shot.shot_number,
        'prompt': prompt,
        'timestamp': shot.timestamp_start
    })

# 프롬프트 저장
with open('04_storyboard/niji_prompts.json', 'w', encoding='utf-8') as f:
    json.dump(prompts, f, indent=2, ensure_ascii=False)
```

### 5-3. Nijijourney 이미지 생성 프로세스

**수동 워크플로우** (Nijijourney는 공식 API 없음):
1. Discord Nijijourney 채널 접속
2. `/imagine` 명령어 사용
3. 각 프롬프트를 순차적으로 입력
4. 생성된 이미지 다운로드 및 이름 정리

**파일명 규칙**:
```
shot_001_CU_girl_smiling.png
shot_002_MS_girl_running.png
shot_003_LS_flower_field.png
...
```

**반자동 워크플로우** (Midjourney API 서비스 이용):
```python
# 비공식 API 사용 예시 (UseAPI, GoAPI 등)
import requests

def generate_niji_image(prompt: str, shot_number: int):
    """
    비공식 API를 통한 Nijijourney 이미지 생성
    """
    response = requests.post(
        "https://api.useapi.net/v2/jobs/imagine",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "prompt": prompt,
            "webhookOverride": "YOUR_WEBHOOK_URL"
        }
    )
    
    job_id = response.json()['jobid']
    
    # 이미지 생성 대기 (약 60초)
    while True:
        status = requests.get(
            f"https://api.useapi.net/v2/jobs/{job_id}",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        
        if status.json()['status'] == 'completed':
            image_url = status.json()['imageURL']
            # 이미지 다운로드
            download_image(image_url, f"05_images/shot_{shot_number:03d}.png")
            break
        
        time.sleep(10)
```

**💡 TIP**: 
- 한 번에 5-10개씩 생성하고 중간 검토
- 캐릭터 일관성이 떨어지는 이미지는 재생성
- `--cw` (character weight) 값을 100으로 최대화

### 5-4. 일관성 체크 및 재생성

```python
def check_character_consistency(image_folder: str):
    """
    생성된 이미지들의 일관성을 시각적으로 체크
    (수동 검토용 HTML 뷰어 생성)
    """
    import glob
    from pathlib import Path
    
    images = sorted(glob.glob(f"{image_folder}/shot_*.png"))
    
    html = """
    <html>
    <head><title>Character Consistency Check</title></head>
    <body>
    <h1>캐릭터 일관성 체크</h1>
    <p>문제가 있는 이미지는 체크하세요</p>
    """
    
    for img in images:
        shot_num = Path(img).stem.split('_')[1]
        html += f"""
        <div style="display:inline-block; margin:10px; border:2px solid #ccc;">
            <img src="{img}" width="400"><br>
            <label><input type="checkbox" name="regenrate" value="{shot_num}">
            Shot {shot_num} 재생성 필요</label>
        </div>
        """
    
    html += "</body></html>"
    
    with open('05_images/consistency_check.html', 'w') as f:
        f.write(html)
    
    print("✅ 05_images/consistency_check.html 파일을 브라우저로 열어서 체크하세요")
```

---

## STEP 6: 동영상 변환

### 6-1. 도구 선택 가이드

| 도구 | 장점 | 단점 | 추천 용도 |
|------|------|------|----------|
| **Veo 3** | 최고 품질, 긴 영상(60초) | API 없음, 수동 작업 | 핵심 씬만 선별 |
| **Replicate API** | 자동화 가능, 다양한 모델 | 품질 편차 | 대량 변환 |
| **ComfyUI** | 세밀한 제어, 로컬 처리 | 복잡한 설정 | 고급 사용자 |

### 6-2. Veo 3 사용 (수동)

**프로세스**:
1. Google AI Studio 접속
2. Veo 3 선택
3. 이미지 업로드
4. 프롬프트 입력:
   ```
   Animate this image with smooth camera movement. 
   The character should [캐릭터 동작], 
   duration: [콘티 duration]초
   ```
5. 생성된 영상 다운로드

**언제 사용하나**:
- 중요한 클라이맥스 씬 (Chorus, Bridge)
- 복잡한 카메라 워크가 필요한 장면
- 총 컷의 20-30%만 Veo 3로 처리하고 나머지는 Replicate 권장

### 6-3. Replicate API 사용 (자동)

```python
import replicate
import time

def image_to_video_replicate(
    image_path: str, 
    output_path: str,
    motion_prompt: str,
    duration_seconds: int = 4
):
    """
    Replicate의 Stable Video Diffusion 또는 Animate Diff 사용
    """
    # 이미지를 base64로 변환
    import base64
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode()
    
    # Replicate API 호출
    output = replicate.run(
        "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
        input={
            "image": f"data:image/png;base64,{image_data}",
            "num_frames": duration_seconds * 24,  # 24fps
            "motion_bucket_id": 127,  # 127 = 중간 모션
            "fps": 24,
            "cond_aug": 0.02
        }
    )
    
    # 결과 동영상 다운로드
    video_url = output  # Replicate는 URL 반환
    download_video(video_url, output_path)
    
    return output_path

# 전체 콘티에 대해 변환
for shot in storyboard.shots:
    shot_num = shot.shot_number
    image_path = f"05_images/shot_{shot_num:03d}.png"
    output_path = f"06_videos/clip_{shot_num:03d}.mp4"
    
    duration = shot.timestamp_end - shot.timestamp_start
    motion_prompt = shot.character_action
    
    print(f"Converting shot {shot_num}...")
    image_to_video_replicate(
        image_path, 
        output_path, 
        motion_prompt,
        int(duration)
    )
    
    # API Rate Limit 고려
    time.sleep(2)
```

### 6-4. ComfyUI 워크플로우 (선택사항)

**필요 조건**:
- NVIDIA GPU (최소 RTX 3060 12GB)
- ComfyUI 설치
- AnimateDiff + ControlNet 모델

**장점**:
- 프레임별 정밀 제어
- 로컬 처리로 비용 절감
- 배치 처리 가능

**워크플로우 JSON 예시**는 ComfyUI 커뮤니티에서 "AnimateDiff workflow" 검색.

---

## STEP 7: 최종 편집

### 7-1. FFmpeg로 클립 결합 (기본 버전)

```python
import subprocess

def create_video_concat_file(storyboard: Storyboard, output_path: str):
    """
    FFmpeg concat을 위한 파일 리스트 생성
    """
    with open(output_path, 'w') as f:
        for shot in storyboard.shots:
            shot_num = shot.shot_number
            duration = shot.timestamp_end - shot.timestamp_start
            f.write(f"file '06_videos/clip_{shot_num:03d}.mp4'\n")
            f.write(f"duration {duration}\n")

# Concat 파일 생성
create_video_concat_file(storyboard, 'concat_list.txt')

# FFmpeg로 결합
subprocess.run([
    'ffmpeg',
    '-f', 'concat',
    '-safe', '0',
    '-i', 'concat_list.txt',
    '-i', '03_music/selected_song.mp3',  # 오디오 추가
    '-c:v', 'libx264',
    '-c:a', 'aac',
    '-shortest',  # 짧은 쪽에 맞춤
    '07_final/music_video_draft.mp4'
])
```

### 7-2. DaVinci Resolve 편집 (권장)

**왜 DaVinci인가**:
- 무료 버전으로 충분
- 정밀한 타이밍 조정
- 색보정 및 이펙트
- 자막 추가 가능

**편집 프로세스**:
1. **프로젝트 생성**
   - 24fps, 1920x1080 (또는 3840x2160)
   
2. **미디어 풀에 Import**
   - `06_videos/` 폴더 전체 import
   - 음악 파일 import

3. **타임라인 배치**
   ```
   Track 1: 오디오 (Suno 음악)
   Track 2: 비디오 클립들
   Track 3: 트랜지션 효과
   Track 4: 자막 (선택)
   ```

4. **클립 길이 조정**
   - 콘티의 `timestamp_start`, `timestamp_end`에 맞춰 정렬
   - Ripple Edit 모드 사용 권장

5. **트랜지션 추가**
   - Chorus 구간: Cross Dissolve (0.5초)
   - Verse 구간: Cut (트랜지션 없음)
   - Bridge: Dip to White (극적 전환)

6. **색보정** (Color 탭)
   - 전체 클립에 통일된 LUT 적용
   - 밝기/대비 조정
   - 색온도 맞춤

7. **Export**
   - Format: MP4
   - Codec: H.264
   - Resolution: 1080p
   - Bitrate: 10 Mbps

### 7-3. 타이밍 미세 조정 스크립트

```python
def adjust_clip_timing(video_path: str, start_time: float, end_time: float, output_path: str):
    """
    개별 클립의 시작/종료 시간을 정밀하게 조정
    """
    duration = end_time - start_time
    
    subprocess.run([
        'ffmpeg',
        '-i', video_path,
        '-ss', str(start_time),
        '-t', str(duration),
        '-c:v', 'libx264',
        '-preset', 'fast',
        output_path
    ])

# 예: 클립이 너무 길어서 트리밍 필요한 경우
adjust_clip_timing(
    '06_videos/clip_015.mp4',
    start_time=0.5,  # 앞 0.5초 제거
    end_time=4.0,    # 4초까지만 사용
    output_path='06_videos/clip_015_trimmed.mp4'
)
```

### 7-4. 품질 향상 옵션

**Upscaling** (1080p → 4K):
```bash
ffmpeg -i music_video_draft.mp4 \
  -vf "scale=3840:2160:flags=lanczos" \
  -c:v libx265 -preset slow -crf 18 \
  music_video_4k.mp4
```

**프레임 보간** (24fps → 60fps):
```bash
# RIFE 모델 사용 (별도 설치 필요)
python inference_video.py \
  --video music_video_draft.mp4 \
  --output music_video_60fps.mp4 \
  --fps 60
```

---

## 자동화 스크립트

### 완전 자동화 파이프라인

```python
import asyncio
import os
from pathlib import Path

class MusicVideoPipeline:
    """
    뮤직비디오 제작 자동화 파이프라인
    """
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.base_dir = Path(f"music-video-project/{project_name}")
        self._create_folders()
        
    def _create_folders(self):
        """프로젝트 폴더 구조 생성"""
        folders = [
            '01_theme', '02_lyrics', '03_music', '04_storyboard',
            '05_images', '06_videos', '07_final', 'scripts'
        ]
        for folder in folders:
            (self.base_dir / folder).mkdir(parents=True, exist_ok=True)
    
    async def step1_generate_lyrics(self, theme: str, genre: str, mood: str):
        """가사 생성"""
        print("📝 STEP 1: 가사 생성 중...")
        
        prompt = f"""
        너는 전문 작사가야. 다음 주제로 뮤직비디오용 가사를 작성해줘.
        
        주제: {theme}
        장르: {genre}
        분위기: {mood}
        길이: 2분 30초 내외
        
        [Verse 1], [Chorus] 등 섹션을 명확히 구분해줘.
        """
        
        # Gemini API 호출
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        lyrics = response.content[0].text
        
        # 저장
        lyrics_path = self.base_dir / '02_lyrics' / 'lyrics.txt'
        with open(lyrics_path, 'w', encoding='utf-8') as f:
            f.write(lyrics)
        
        print(f"✅ 가사 저장: {lyrics_path}")
        return lyrics
    
    def step2_music_generation_guide(self):
        """Suno 음악 생성 가이드 (수동)"""
        print("\n🎵 STEP 2: Suno AI에서 음악 생성")
        print("=" * 50)
        print("1. https://suno.ai 접속")
        print("2. Custom Mode 선택")
        print(f"3. {self.base_dir / '02_lyrics' / 'lyrics.txt'} 파일 내용 붙여넣기")
        print("4. 3-5곡 생성")
        print("5. 최적의 곡 선정 후 다운로드")
        print(f"6. {self.base_dir / '03_music' / 'selected_song.mp3'}로 저장")
        print("=" * 50)
        input("완료 후 Enter를 누르세요...")
    
    async def step3_create_storyboard(self, lyrics: str, song_path: str):
        """콘티 생성"""
        print("\n🎬 STEP 3: 콘티 생성 중...")
        
        # 노래 분석
        song_data = analyze_song(song_path)
        
        prompt = f"""
        당신은 애니메이션 뮤직비디오 감독입니다.
        다음 정보로 상세한 콘티를 JSON 형식으로 작성하세요.
        
        노래 BPM: {song_data['bpm']}
        노래 길이: {song_data['duration']}초
        
        가사:
        {lyrics}
        
        30-50개의 컷으로 나눠주세요. 각 컷마다:
        - shot_number, timestamp_start, timestamp_end
        - lyrics_line, scene_description
        - shot_type (CU/MS/LS), camera_movement
        - character_action, mood, visual_style
        
        JSON 스키마:
        {{
          "title": "string",
          "total_duration": number,
          "shots": [
            {{
              "shot_number": number,
              "timestamp_start": number,
              "timestamp_end": number,
              "lyrics_line": "string",
              "scene_description": "string",
              "shot_type": "CU" | "MS" | "LS",
              "camera_movement": "static" | "pan" | "zoom",
              "character_action": "string",
              "mood": "string",
              "visual_style": "string"
            }}
          ]
        }}
        """
        
        # Gemini 호출
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # JSON 파싱
        import json
        storyboard_text = response.content[0].text
        # ```json 태그 제거
        storyboard_text = storyboard_text.replace('```json', '').replace('```', '').strip()
        storyboard_json = json.loads(storyboard_text)
        
        # 저장
        storyboard_path = self.base_dir / '04_storyboard' / 'storyboard.json'
        with open(storyboard_path, 'w', encoding='utf-8') as f:
            json.dump(storyboard_json, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 콘티 저장: {storyboard_path}")
        return storyboard_json
    
    def step4_generate_niji_prompts(self, storyboard: dict, character_ref: str):
        """Nijijourney 프롬프트 생성"""
        print("\n🎨 STEP 4: Nijijourney 프롬프트 생성 중...")
        
        prompts = []
        for shot in storyboard['shots']:
            prompt = generate_niji_prompt_from_shot(shot, character_ref)
            prompts.append({
                'shot_number': shot['shot_number'],
                'prompt': prompt
            })
        
        # 저장
        prompts_path = self.base_dir / '04_storyboard' / 'niji_prompts.json'
        with open(prompts_path, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 프롬프트 저장: {prompts_path}")
        print("\n🖼️ Nijijourney 이미지 생성을 시작하세요:")
        print("   Discord에서 각 프롬프트를 /imagine으로 입력")
        print(f"   생성된 이미지를 {self.base_dir / '05_images'}에 저장")
        
        return prompts
    
    async def step5_convert_to_videos(self, storyboard: dict):
        """이미지를 동영상으로 변환"""
        print("\n🎞️ STEP 5: 이미지 → 동영상 변환 중...")
        
        tasks = []
        for shot in storyboard['shots']:
            shot_num = shot['shot_number']
            image_path = self.base_dir / '05_images' / f"shot_{shot_num:03d}.png"
            output_path = self.base_dir / '06_videos' / f"clip_{shot_num:03d}.mp4"
            
            if not image_path.exists():
                print(f"⚠️ 이미지 없음: {image_path}")
                continue
            
            duration = shot['timestamp_end'] - shot['timestamp_start']
            task = image_to_video_replicate(
                str(image_path),
                str(output_path),
                shot['character_action'],
                int(duration)
            )
            tasks.append(task)
        
        # 병렬 처리
        await asyncio.gather(*tasks)
        print("✅ 모든 클립 변환 완료")
    
    def step6_final_edit(self, storyboard: dict, music_path: str):
        """최종 편집"""
        print("\n✂️ STEP 6: 최종 편집 중...")
        
        # Concat 파일 생성
        concat_path = self.base_dir / 'concat_list.txt'
        create_video_concat_file_from_dict(storyboard, str(concat_path))
        
        # FFmpeg 결합
        output_path = self.base_dir / '07_final' / 'music_video_final.mp4'
        subprocess.run([
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', str(concat_path),
            '-i', music_path,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            str(output_path)
        ])
        
        print(f"✅ 최종 영상: {output_path}")
        return output_path

# 파이프라인 실행
async def main():
    # 프로젝트 초기화
    pipeline = MusicVideoPipeline("my_first_mv")
    
    # STEP 1: 가사 생성
    lyrics = await pipeline.step1_generate_lyrics(
        theme="꿈을 향해 날아가는 소녀",
        genre="J-pop",
        mood="희망적이고 밝은"
    )
    
    # STEP 2: Suno 음악 생성 (수동)
    pipeline.step2_music_generation_guide()
    
    # STEP 3: 콘티 생성
    storyboard = await pipeline.step3_create_storyboard(
        lyrics,
        "music-video-project/my_first_mv/03_music/selected_song.mp3"
    )
    
    # STEP 4: Nijijourney 프롬프트
    prompts = pipeline.step4_generate_niji_prompts(
        storyboard,
        character_ref="https://s.mj.run/YOUR_CHAR_REF"
    )
    
    print("\n⏸️ Nijijourney에서 이미지 생성 후 계속하려면 Enter")
    input()
    
    # STEP 5: 동영상 변환
    await pipeline.step5_convert_to_videos(storyboard)
    
    # STEP 6: 최종 편집
    final_video = pipeline.step6_final_edit(
        storyboard,
        "music-video-project/my_first_mv/03_music/selected_song.mp3"
    )
    
    print("\n🎉 뮤직비디오 제작 완료!")
    print(f"결과물: {final_video}")

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 품질 체크리스트

### 콘티 단계
- [ ] 모든 가사 구간이 시각화되었는가?
- [ ] 타이밍이 노래 길이와 정확히 일치하는가?
- [ ] 감정 전환이 자연스러운가?
- [ ] 샷 타입이 다양하게 배치되었는가? (CU/MS/LS 균형)

### 이미지 생성 단계
- [ ] 캐릭터 일관성이 유지되는가?
- [ ] 배경 스타일이 통일되어 있는가?
- [ ] 해상도가 충분한가? (최소 1920x1080)
- [ ] 콘티의 scene_description과 일치하는가?

### 동영상 변환 단계
- [ ] 모션이 자연스러운가? (과도한 워핑 없음)
- [ ] 프레임레이트가 일정한가? (24fps)
- [ ] 화질 저하가 없는가?
- [ ] 캐릭터 얼굴/눈이 제대로 보이는가?

### 최종 편집 단계
- [ ] 오디오와 영상 싱크가 정확한가?
- [ ] 트랜지션이 어색하지 않은가?
- [ ] 색보정이 일관되게 적용되었는가?
- [ ] 전체 흐름이 자연스러운가?
- [ ] 렌더링 에러가 없는가?

---

## 문제 해결 가이드

### 문제 1: Nijijourney 캐릭터 일관성 부족

**증상**: 샷마다 캐릭터 얼굴이 다름

**해결**:
```
1. Character Reference 이미지를 더 강하게 적용
   --cref URL --cw 100 (weight 최대)

2. 프롬프트에서 변하지 않을 특징 명시
   "girl with long brown hair and blue eyes" (매 프롬프트)

3. Style Reference도 함께 사용
   --sref URL --sw 50

4. 극단적 각도는 피하기
   CU, MS 위주로 구성하고 LS는 최소화
```

### 문제 2: Image-to-Video 모션이 부자연스러움

**증상**: 캐릭터가 녹아내림, 얼굴 왜곡

**해결**:
```python
# Replicate API의 motion_bucket_id 조정
# 낮을수록 모션 적음 (안정적), 높을수록 역동적 (불안정)

# 정적인 씬 (얼굴 클로즈업)
motion_bucket_id = 50

# 중간 (걷기, 돌아보기)
motion_bucket_id = 100

# 역동적 (뛰기, 춤)
motion_bucket_id = 180
```

**대안**: 
- 중요 씬은 Veo 3 사용 (품질 최우선)
- ComfyUI + ControlNet으로 프레임별 제어

### 문제 3: 노래와 영상 길이 불일치

**증상**: 영상이 노래보다 길거나 짧음

**해결**:
```python
def sync_video_to_audio(video_path: str, audio_path: str, output_path: str):
    """
    영상을 오디오 길이에 정확히 맞춤
    """
    # 오디오 길이 추출
    probe = ffmpeg.probe(audio_path)
    audio_duration = float(probe['format']['duration'])
    
    # 영상 속도 조정
    subprocess.run([
        'ffmpeg', '-i', video_path,
        '-i', audio_path,
        '-filter:v', f"setpts={audio_duration}/duration*PTS",
        '-map', '0:v', '-map', '1:a',
        '-c:v', 'libx264', '-c:a', 'aac',
        output_path
    ])
```

### 문제 4: Replicate API Rate Limit

**증상**: Too many requests 에러

**해결**:
```python
import time
from functools import wraps

def rate_limit(calls_per_minute=10):
    """Rate limiter 데코레이터"""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(calls_per_minute=5)
def safe_replicate_call(image_path, output_path):
    return image_to_video_replicate(image_path, output_path)
```

### 문제 5: 메모리 부족

**증상**: 렌더링 중 프로그램 크래시

**해결**:
```python
# 배치 처리로 메모리 관리
def process_in_batches(shots, batch_size=5):
    """
    한 번에 5개씩만 처리
    """
    for i in range(0, len(shots), batch_size):
        batch = shots[i:i+batch_size]
        for shot in batch:
            process_shot(shot)
        
        # 배치 완료 후 메모리 정리
        import gc
        gc.collect()
        time.sleep(10)
```

---

## 고급 팁

### 1. 자막 추가

```python
def add_subtitles(video_path: str, storyboard: dict, output_path: str):
    """
    가사 자막을 영상에 추가
    """
    # SRT 파일 생성
    srt_content = ""
    for i, shot in enumerate(storyboard['shots'], 1):
        start_time = format_srt_time(shot['timestamp_start'])
        end_time = format_srt_time(shot['timestamp_end'])
        lyrics = shot['lyrics_line']
        
        srt_content += f"{i}\n{start_time} --> {end_time}\n{lyrics}\n\n"
    
    srt_path = 'subtitles.srt'
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    
    # FFmpeg로 자막 번
    subprocess.run([
        'ffmpeg', '-i', video_path,
        '-vf', f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,Outline=2'",
        '-c:a', 'copy',
        output_path
    ])
```

### 2. 인트로/아웃트로 추가

```python
def create_intro_outro(title: str, artist: str):
    """
    타이틀 카드 생성
    """
    from PIL import Image, ImageDraw, ImageFont
    
    # 1920x1080 빈 이미지
    img = Image.new('RGB', (1920, 1080), color='black')
    draw = ImageDraw.Draw(img)
    
    # 폰트 (시스템 폰트 경로)
    font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 72)
    font_artist = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 48)
    
    # 텍스트 중앙 정렬
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((1920 - title_width) / 2, 400), title, fill='white', font=font_title)
    
    artist_bbox = draw.textbbox((0, 0), artist, font=font_artist)
    artist_width = artist_bbox[2] - artist_bbox[0]
    draw.text(((1920 - artist_width) / 2, 550), artist, fill='gray', font=font_artist)
    
    # 저장
    img.save('intro_card.png')
    
    # 5초 정적 영상 생성
    subprocess.run([
        'ffmpeg',
        '-loop', '1',
        '-i', 'intro_card.png',
        '-c:v', 'libx264',
        '-t', '5',
        '-pix_fmt', 'yuv420p',
        'intro.mp4'
    ])
```

### 3. 효과음 추가

```python
def add_sound_effects(video_path: str, sfx_list: list, output_path: str):
    """
    특정 타이밍에 효과음 추가
    
    sfx_list = [
        {'file': 'whoosh.mp3', 'time': 10.5, 'volume': 0.5},
        {'file': 'impact.mp3', 'time': 25.0, 'volume': 0.8}
    ]
    """
    # FFmpeg filter_complex 구성
    filter_parts = []
    for i, sfx in enumerate(sfx_list):
        filter_parts.append(f"[{i+1}:a]adelay={int(sfx['time']*1000)}|{int(sfx['time']*1000)},volume={sfx['volume']}[a{i}]")
    
    # 모든 오디오 믹싱
    amix_inputs = "[0:a]" + "".join([f"[a{i}]" for i in range(len(sfx_list))])
    filter_parts.append(f"{amix_inputs}amix=inputs={len(sfx_list)+1}:duration=longest[aout]")
    
    filter_complex = ";".join(filter_parts)
    
    # FFmpeg 실행
    cmd = ['ffmpeg', '-i', video_path]
    for sfx in sfx_list:
        cmd.extend(['-i', sfx['file']])
    cmd.extend([
        '-filter_complex', filter_complex,
        '-map', '0:v', '-map', '[aout]',
        '-c:v', 'copy', '-c:a', 'aac',
        output_path
    ])
    
    subprocess.run(cmd)
```

---

## 추가 리소스

### 추천 학습 자료
- **Nijijourney 가이드**: https://docs.midjourney.com/docs/niji-model
- **FFmpeg 튜토리얼**: https://ffmpeg.org/documentation.html
- **DaVinci Resolve 무료 강의**: YouTube "DaVinci Resolve Beginners"
- **AnimateDiff 가이드**: GitHub AnimateDiff repository

### 커뮤니티
- **Reddit r/StableDiffusion**: Image-to-Video 기법 공유
- **Discord Midjourney**: Nijijourney 커뮤니티
- **GitHub Awesome AI Video**: AI 영상 도구 모음

### 대안 도구
| 단계 | 원래 도구 | 대안 |
|------|----------|-----|
| 가사 생성 | Gemini | ChatGPT, Claude |
| 음악 생성 | Suno | Udio, MusicGen |
| 이미지 생성 | Nijijourney | Stable Diffusion + LoRA |
| I2V 변환 | Veo 3, Replicate | Runway Gen-3, Pika |
| 편집 | DaVinci Resolve | Premiere Pro, Final Cut |

---

## 최종 체크리스트

제작 시작 전:
- [ ] 모든 AI 서비스 구독 확인
- [ ] API Key 발급 및 환경변수 설정
- [ ] FFmpeg 설치 확인 (`ffmpeg -version`)
- [ ] Python 패키지 설치 완료
- [ ] 프로젝트 폴더 구조 생성

제작 완료 후:
- [ ] 최종 영상 품질 체크 (1080p 이상)
- [ ] 오디오 싱크 확인
- [ ] 색보정 통일성 확인
- [ ] 파일 백업 (원본 이미지, 중간 파일 보관)
- [ ] 포트폴리오용 스크린샷 캡처

---

## 마무리

이 가이드를 따라하면 약 **6-8시간**이면 첫 뮤직비디오를 완성할 수 있습니다.

**핵심 성공 요소**:
1. **콘티를 정교하게** - 전체 품질의 70%가 여기서 결정됨
2. **Character Reference 첫 이미지를 신중히** - 일관성의 기초
3. **타이밍 정확히** - 노래와 영상이 1프레임도 어긋나지 않게
4. **점진적 개선** - 첫 작품은 학습 목적, 두 번째부터 본격화

**개선 로드맵**:
- 1차 제작: 기본 워크플로우 습득
- 2차 제작: 자동화 스크립트 도입 (30% 시간 단축)
- 3차 제작: 고급 이펙트 추가 (색보정, 효과음)
- 4차 제작: ComfyUI 도입으로 품질 극대화

막히는 부분이 있다면 언제든 질문하세요. 파이팅! 🎬✨
