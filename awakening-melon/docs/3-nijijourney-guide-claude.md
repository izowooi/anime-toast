# Nijijourney 7로 애니메이션 뮤직비디오 만들기

Nijijourney 7(2026년 1월 9일 출시)은 현존하는 **최고의 애니메이션 특화 AI 이미지 생성 모델**이다. 선명한 선화, 정교한 디테일, 리터럴한 프롬프트 해석력으로 뮤직비디오용 이미지 30~50컷을 한 사람이 제작할 수 있는 시대를 열었다. 다만 **--cref(캐릭터 레퍼런스)가 Niji V7에서는 사용 불가**하므로, 캐릭터 일관성을 위해 상세한 텍스트 설명 + --sref 코드 + --seed 조합이라는 대체 워크플로우가 필수다. 이 가이드는 완전 초보자가 Discord 가입부터 최종 컷 생성까지 따라할 수 있도록 설계했다.

---

## Nijijourney 7은 무엇이고 어떻게 시작하나

Nijijourney(니지저니)는 **Midjourney와 Spellbrush(MIT 수학자 팀)의 합작** 애니메이션 특화 AI 모델이다. "Niji"는 일본어로 무지개를 의미한다. 일반 Midjourney가 사진 같은 사실적 이미지에 강하다면, Niji는 **애니메이션 선화, 셀 셰이딩, 큰 눈, 단순화된 코** 등 동양 일러스트 미학에 최적화되어 있다. 하나의 구독으로 Midjourney와 Niji를 모두 사용할 수 있다.

**시작 3단계:**

1. **Discord 계정 생성** → Discord 앱 또는 웹에서 무료 가입
2. **구독 선택** → midjourney.com에서 결제 (Basic $10/월부터)
3. **이미지 생성 시작** → Nijijourney Discord 서버 접속 또는 nijijourney.com 웹 UI에서 바로 시작

| 플랜 | 월 요금 | Fast GPU 시간 | Relax 모드 | 추천 대상 |
|------|---------|--------------|-----------|----------|
| **Basic** | $10 | 3.3시간 | ❌ | 테스트/입문 |
| **Standard** | $30 | 15시간 | ✅ 무제한 | **MV 프로젝트 추천** |
| **Pro** | $60 | 30시간 | ✅ 무제한 | 대량 작업 |
| **Mega** | $120 | 60시간 | ✅ 무제한 | 상업 대규모 |

30~50컷 뮤직비디오 프로젝트에는 **Standard 플랜($30/월)**이 적합하다. Relax 모드로 탐색하고, Fast 모드로 최종본만 뽑으면 충분하다. 연간 결제 시 **20% 할인**을 받을 수 있다.

**첫 이미지 생성법:**
Discord #image-generation 채널에서 다음을 입력한다:

```
/imagine prompt: anime girl with pastel green hair, standing in a village --niji 7 --ar 16:9
```

약 30~60초 후 **4장의 이미지가 2×2 그리드**로 생성된다.

---

## 반드시 알아야 할 핵심 명령어와 파라미터

### 기본 명령어 6가지

| 명령어 | 기능 | 사용 시점 |
|--------|------|----------|
| `/imagine` | 이미지 생성 (핵심 명령어) | 매번 |
| `/settings` | 기본 모델·모드 설정 변경 | 프로젝트 시작 시 |
| `/info` | 잔여 GPU 시간·사용량 확인 | 수시 체크 |
| `/describe` | 이미지 업로드 → 프롬프트 역추출 | 레퍼런스 분석 시 |
| `/blend` | 2~5장 이미지 블렌딩 | 스타일 합성 시 |
| `/remix` | 리믹스 모드 토글 | 변형 작업 시 |

### 핵심 파라미터 완전 정리

**`--niji 7`** — Niji V7 모델 활성화. Midjourney 봇에서 사용 시 필수 추가.

**`--ar` (종횡비)** — 뮤직비디오는 반드시 `--ar 16:9` 사용. 기본값은 1:1(정사각형)이므로 매번 명시해야 한다.

**`--s` (스타일라이즈, 0~1000)** — 기본값 100. 값이 높을수록 AI의 미적 해석이 강해진다. 애니메이션 제작에는 **150~250** 권장. 너무 높으면 프롬프트를 무시하고 너무 낮으면 밋밋해진다.

**`--chaos` (다양성, 0~100)** — 기본값 0. 4장의 그리드 이미지 간 차이를 조절한다. 초기 탐색 시 **20~40**, 최종 생성 시 **0~10** 권장.

**`--no` (네거티브 프롬프트)** — 제외할 요소 지정. 예: `--no text, watermark, chibi, deformed`. 한 번만 사용 가능하며 쉼표로 구분한다.

**`--seed` (시드, 0~4,294,967,295)** — 동일 시드 + 동일 프롬프트 = 유사한 결과. 캐릭터 일관성의 보조 수단. `--seed 42`처럼 사용.

**`--sref` (스타일 레퍼런스)** — **Niji V7에서 가장 중요한 파라미터**. 이미지 URL 또는 숫자 코드로 시각 스타일을 고정한다. `--sref 2213253170` 또는 `--sref [이미지URL]` 형태.

**`--sw` (스타일 웨이트, 0~1000)** — --sref의 영향력 조절. 기본값 100. 프로젝트 전체에 동일한 sref + sw 값을 써야 스타일 일관성이 유지된다.

**`--style raw`** — AI의 미적 해석을 줄이고 프롬프트에 충실한 결과를 낸다. 너무 "예쁘게" 나올 때 사용.

**`--q` (품질, 1/2/4)** — 기본값 1. 값이 높으면 디테일 증가하지만 GPU 시간도 비례 증가. 탐색 시 1, 최종본에 2 사용.

---

## V6에서 V7으로 — 무엇이 달라졌나

Niji V7은 V6 대비 **전면적인 품질 도약**을 이루었다. 약 1.5년 만의 메이저 업데이트(V6: 2024년 6월 → V7: 2026년 1월)로, 가장 눈에 띄는 변화는 다음과 같다.

**눈, 손, 디테일의 극적 개선.** V6에서 빈번했던 손가락 오류, 흐릿한 배경, 의미 없는 얼룩이 V7에서는 대폭 줄었다. 눈동자 반사, 머리카락 결, 꽃잎 하나하나가 선명하게 렌더링된다.

**더 리터럴한 프롬프트 해석.** V7은 작성한 내용을 **그대로** 그린다. V6처럼 자동으로 배경과 조명을 추가해주지 않으므로, "outdoors", "indoors" 같은 배경 키워드를 직접 명시해야 한다. 짧고 모호한 프롬프트보다 **구체적이고 상세한 프롬프트**가 훨씬 좋은 결과를 낸다.

**선화(Linework)의 비약적 발전.** 애니메이션 특유의 자신감 있고 표현력 넘치는 선화가 V7의 가장 큰 강점이다. `anime screenshot` 키워드와 함께 사용하면 정통 애니메이션 프레임 느낌을 얻을 수 있다.

**의도적으로 평면적인 미학.** V6의 약간 3D적인 렌더링 대신, V7은 **셀 애니메이션에 가까운 플랫한 룩**을 기본으로 채택했다.

**Draft 모드 신설.** 10배 빠른 속도에 50% 비용으로 이미지를 생성한다. 아이디어 탐색 단계에서 필수적이다.

⚠️ **중요 변경사항: --cref 사용 불가.** Niji V7에서는 캐릭터 레퍼런스(--cref)가 지원되지 않는다. 개발팀은 "사용자가 더 좋아할 대체 기능"을 준비 중이라고 밝혔다. 현재는 --sref + 상세 텍스트 + --seed 조합으로 대체해야 한다.

---

## 캐릭터 일관성 유지 — Niji V7 실전 전략

캐릭터 일관성은 뮤직비디오 제작의 **최대 난제**다. Niji V7에서 --cref가 없는 상황에서의 실전 워크플로우를 단계별로 정리한다.

### 1단계: 캐릭터 마스터 설명문 작성

프로젝트에 사용할 캐릭터의 모든 외형 디테일을 **한 문장으로 고정**한다. 이 문장을 모든 프롬프트에 동일하게 복사·붙여넣기한다.

```
a young girl with long wavy pastel green hair reaching her waist, bright emerald eyes, 
fair skin, wearing a simple white blouse with short sleeves and a brown knee-length skirt, 
brown leather boots
```

변신 후 모습도 별도로 정의한다:

```
a young girl with long wavy pastel green hair reaching her waist, bright emerald eyes, 
fair skin, wearing ornate silver fantasy armor with emerald accents, wielding a glowing 
silver sword, magical green aura
```

### 2단계: 스타일 레퍼런스(--sref) 코드 확정

프로젝트 전체에 **하나의 --sref 코드**를 사용하는 것이 일관성의 핵심이다.

```
/imagine prompt: anime girl with pastel green hair, simple portrait, white background 
--niji 7 --sref random --ar 1:1
```

`--sref random`으로 여러 스타일을 생성한 뒤, 마음에 드는 결과물의 숫자 코드를 기록해둔다. 이 코드를 이후 **모든 프롬프트에 동일하게** 적용한다. nijijourney.com 웹 UI에서 Style Creator를 통해 커스텀 코드를 만들 수도 있다.

### 3단계: 캐릭터 시트 생성

일관성의 기준이 될 캐릭터 시트를 먼저 만든다:

```
/imagine prompt: anime character sheet, front view and 3/4 view, a young girl with long 
wavy pastel green hair reaching her waist, bright emerald eyes, white blouse, brown skirt, 
brown boots, Slayers anime style, Production I.G quality, clean white background, neutral 
lighting --ar 16:9 --niji 7 --sref [확정코드] --s 150 --seed 73
```

### 4단계: 씬별 프롬프트에서 핵심 규칙 준수

- **캐릭터 설명문**을 매 프롬프트에 동일하게 복붙
- **동일한 --sref 코드**를 매번 사용
- **동일한 --seed 값** 사용 (완전 동일 결과는 아니지만 구조적 유사성 유지)
- **한 번에 하나만 변경** — 포즈 바꿀 때는 배경 고정, 배경 바꿀 때는 포즈 고정

### --sref와 --cref 비교 (참고용)

| 기능 | --sref (스타일 레퍼런스) | --cref (캐릭터 레퍼런스) |
|------|----------------------|----------------------|
| **역할** | 시각 스타일·색감·분위기 통일 | 캐릭터 외형(얼굴·의상) 통일 |
| **Niji V7 지원** | ✅ 사용 가능 | ❌ 사용 불가 |
| **Midjourney V7** | ✅ 사용 가능 | --oref로 대체됨 |
| **웨이트** | --sw 0~1000 | --cw 0~100 |
| **복수 사용** | ✅ 여러 URL/코드 가능 | URL 여러 개 가능 |

### Midjourney V7에서 --oref 활용 (대안)

만약 Niji V7 대신 **Midjourney V7**으로 작업한다면, `--oref`(Omni Reference)를 사용할 수 있다. --cref의 진화판으로 캐릭터뿐 아니라 물체, 탈것까지 레퍼런스로 활용 가능하다. 단, Midjourney V7은 애니메이션 특화가 아니므로 Niji만큼의 애니메이션 퀄리티는 기대하기 어렵다. `--oref [이미지URL] --ow 100~400`으로 사용하며, GPU 시간이 **2배** 소모된다.

### 일관성 유지 DO / DON'T

- ✅ 캐릭터 설명문을 문서에 저장하고 매번 동일하게 복붙할 것
- ✅ 프로젝트 전체에 하나의 --sref 코드를 사용할 것
- ✅ 의상은 단색·심플하게 디자인할 것 (복잡한 패턴은 일관성 파괴)
- ✅ 한 번에 하나의 변수만 변경할 것
- ✅ 여러 장 생성 후 가장 일관된 것을 선별(cherry-pick)할 것
- ❌ --cref를 Niji V7에서 사용하려 시도하지 말 것
- ❌ 매번 다른 --sref 코드를 쓰지 말 것
- ❌ 포즈 + 의상 + 배경을 동시에 바꾸지 말 것
- ❌ 시드 값에만 의존하지 말 것 (보조 수단일 뿐)
- ❌ 지나치게 긴 프롬프트를 쓰지 말 것 (핵심만 간결하게)

---

## 뮤직비디오 제작 워크플로우 — 컨셉에서 최종 컷까지

### Phase 1: 사전 기획 (프롬프트 작성 전)

**컷 분배 계획** (1분 10초, 약 35~45컷 기준):

| 구간 | 시간 | 컷 수 | 컷당 길이 | 분위기 |
|------|------|-------|----------|--------|
| 인트로 (일상) | 0~15초 | 5~7컷 | 2~3초 | 따뜻하고 평화로움 |
| 전개 (변신) | 15~30초 | 6~8컷 | 2~3초 | 신비롭고 긴장감 |
| 클라이맥스 (전투) | 30~55초 | 12~16컷 | 1.5~2초 | 격렬하고 다이내믹 |
| 엔딩 (귀환) | 55~70초 | 4~6컷 | 3~4초 | 감성적, 노스탤직 |

### Phase 2: 스타일 확정 (5~10장 테스트)

Draft 모드로 다양한 sref 코드를 빠르게 테스트한다:

```
/imagine prompt: anime screenshot, girl with pastel green hair in a village 
--niji 7 --sref random --ar 16:9
```

마음에 드는 스타일을 발견하면 해당 sref 코드를 기록하고, 이후 모든 작업에 고정한다.

### Phase 3: 마스터 프롬프트 템플릿

```
[샷 타입], [캐릭터 설명문], [행동/포즈], [배경/장소], [조명/시간대], [분위기], 
anime screenshot --ar 16:9 --sref [코드] --niji 7 --s [값] --seed [값]
```

### Phase 4: 씬별 배치 생성

동일 장소의 컷을 묶어서 생성하면 배경 일관성이 높아진다. "마을 아침 씬" 5컷 → "거울 씬" 3컷 → "전투 씬" 10컷 → "귀환 씬" 4컷 순서로 작업한다.

### Phase 5: 선별 → 보정 → 업스케일

4장 그리드 중 최고를 선택(U 버튼) → Vary Region으로 부분 수정 → **Upscale Subtle**로 최종 해상도 확보.

---

## 샷 타입과 카메라 앵글 프롬프트 사전

뮤직비디오의 시각적 다양성을 위해 샷 타입과 카메라 앵글 키워드를 정확히 알아야 한다.

**샷 타입 키워드:**

| 샷 타입 | 프롬프트 키워드 | 활용 |
|---------|---------------|------|
| 익스트림 클로즈업 | `extreme close-up of eyes` | 눈빛, 감정 극대화 |
| 클로즈업 | `close-up shot`, `close-up portrait` | 표정, 대사 |
| 미디엄 샷 | `medium shot`, `waist-up` | 캐릭터 + 일부 배경 |
| 풀 바디 샷 | `full body shot` | 캐릭터 전신, 의상 |
| 와이드 샷 | `wide shot`, `long shot` | 환경 속 캐릭터 |
| 이스타블리싱 샷 | `extreme wide shot`, `establishing shot` | 장소 소개, 세계관 |

**카메라 앵글 키워드:**

| 앵글 | 키워드 | 효과 |
|------|--------|------|
| 눈높이 | `eye-level shot` | 중립적, 기본 |
| 로우 앵글 | `low angle shot`, `from below` | 영웅적, 파워풀 |
| 하이 앵글 | `high angle shot`, `from above` | 취약함, 작아 보임 |
| 버즈아이 뷰 | `bird's eye view`, `overhead shot` | 스케일, 전경 |
| 더치 앵글 | `dutch angle`, `tilted shot` | 긴장감, 불안 |
| 뒷모습 | `back view`, `backshot` | 미스터리, 여정 |

**시네마틱 키워드 보너스:** `cinematic composition`, `dramatic lighting`, `shallow depth of field`, `speed lines` (액션), `dynamic angle`, `silhouette` (역광)

---

## 씬별 실전 프롬프트 — 바로 복사해서 쓰기

아래 프롬프트에서 `[SREF코드]`를 본인이 확정한 스타일 코드로, `[SEED]`를 고정 시드값으로 교체한다.

### 일상 씬: 시골 마을을 걷는 소녀

**Cut 01 — 이스타블리싱 (마을 전경):**
```
/imagine prompt: extreme wide shot, medieval fantasy village nestled in rolling green 
hills, stone cottages with thatched roofs, wildflower meadows, cobblestone paths, warm 
golden morning light, peaceful atmosphere, anime screenshot --ar 16:9 --niji 7 
--sref [SREF코드] --s 200 --seed [SEED]
```

**Cut 03 — 미디엄 샷 (소녀 등장):**
```
/imagine prompt: medium shot, a young girl with long wavy pastel green hair reaching 
her waist, bright emerald eyes, wearing a simple white blouse and brown skirt, walking 
on a cobblestone path through a sun-drenched rural village, carrying a basket, warm 
afternoon light, gentle breeze, Slayers anime style, Production I.G animation quality, 
anime screenshot --ar 16:9 --niji 7 --sref [SREF코드] --s 200 --seed [SEED]
```

**Cut 05 — 클로즈업 (하늘을 올려다보는 얼굴):**
```
/imagine prompt: close-up shot, a young girl with long wavy pastel green hair, bright 
emerald eyes, looking up at the sky with a gentle smile, sunlight filtering through 
leaves, dappled light on face, soft pastel tones, anime screenshot --ar 16:9 --niji 7 
--sref [SREF코드] --s 180 --seed [SEED]
```

### 변신 씬: 거울 앞 각성의 순간

**Cut 12 — 미디엄 샷 (거울 발견):**
```
/imagine prompt: medium shot, a young girl with long wavy pastel green hair standing 
before an ornate ancient full-length mirror in a dimly lit stone room, curious expression, 
mysterious atmosphere, soft dust particles in air, anime screenshot --ar 16:9 --niji 7 
--sref [SREF코드] --s 180 --seed [SEED]
```

**Cut 14 — 클로즈업 (마법 각성):**
```
/imagine prompt: close-up shot, a young girl with pastel green hair, eyes widening with 
shock, her reflection in an ornate mirror glowing with arcane golden light, Slayers-style 
magic circles appearing around her hands, dramatic contrast between dark room and magical 
glow, Production I.G quality, anime screenshot --ar 16:9 --niji 7 --sref [SREF코드] 
--s 200 --seed [SEED] --no chibi, deformed
```

**Cut 16 — 풀 바디 (변신 완료):**
```
/imagine prompt: full body shot, dynamic angle, a young girl with long wavy pastel green 
hair, bright emerald eyes, now wearing ornate silver fantasy armor with emerald accents, 
holding a glowing silver sword, magical green aura swirling around her, determined 
expression, dramatic lighting, Slayers anime style, anime screenshot --ar 16:9 --niji 7 
--sref [SREF코드] --s 220 --seed [SEED]
```

### 전투 씬: 검과 마법으로 괴수와 싸우는 장면

**Cut 22 — 로우 앵글 액션:**
```
/imagine prompt: dynamic low angle shot, a young girl with flowing pastel green hair in 
silver fantasy armor, swinging a glowing silver sword leaving a magical fire trail, 
speed lines, sparks flying, intense determined expression, dark stormy sky, Slayers-style 
explosive magic, Production I.G action quality, anime screenshot --ar 16:9 --niji 7 
--sref [SREF코드] --s 220 --seed [SEED] --no blurry, watermark
```

**Cut 25 — 와이드 샷 (마법 폭발):**
```
/imagine prompt: wide shot, a young girl with pastel green hair in silver armor casting 
a massive Slayers-style fireball spell at dark fantasy monsters in a forest clearing, 
magical energy explosion, dramatic rim lighting, battle dust, vivid colors, cinematic 
composition, anime screenshot --ar 16:9 --niji 7 --sref [SREF코드] --s 250 
--seed [SEED]
```

**전투 씬 Permutation (4가지 변형 동시 생성):**
```
/imagine prompt: anime screenshot, dynamic action, pastel green-haired girl in silver 
armor, {slashing dark wolf monster with sword, casting fire spell at shadow creatures, 
deflecting magical attack with glowing shield, leaping through the air sword raised}, 
forest clearing, Slayers fantasy, Production I.G quality, speed lines --ar 16:9 --niji 7 
--sref [SREF코드] --s 200
```

### 엔딩 씬: 평화로운 마을 귀환

**Cut 38 — 와이드 샷 (귀환):**
```
/imagine prompt: wide shot, a young girl with long pastel green hair walking toward a 
rural fantasy village at golden hour sunset, seen from behind, gentle wind blowing her 
hair, sword strapped to her back, warm orange and pink sky, silhouettes of thatched-roof 
cottages, birds flying overhead, peaceful melancholic atmosphere, Production I.G painterly 
background, anime screenshot --ar 16:9 --niji 7 --sref [SREF코드] --s 250 
--seed [SEED] --no text, watermark
```

**Cut 40 — 클로즈업 (미소):**
```
/imagine prompt: close-up shot, a young girl with long wavy pastel green hair, bright 
emerald eyes, gentle peaceful smile, sunset light casting warm glow on face, a single 
tear on cheek, nostalgic mood, soft focus background of village, anime screenshot 
--ar 16:9 --niji 7 --sref [SREF코드] --s 200 --seed [SEED]
```

---

## 고급 기법으로 품질 끌어올리기

### Vary Region — 부분만 고쳐 완성도 높이기

이미지의 **특정 영역만 수정**할 수 있는 강력한 기능이다. 업스케일한 이미지에서 "Vary (Region)" 버튼 → 직사각형 또는 올가미 도구로 수정 영역 선택 → Remix 프롬프트로 교체 내용 입력 → 4장의 새 버전 생성. 이미지의 **20~50%** 영역을 선택할 때 가장 잘 작동한다. 손가락 오류, 배경 잡티, 의상 디테일 수정에 핵심적이다.

### Permutation Prompts — 변형 대량 생성

중괄호 `{}`로 옵션을 나열하면 각각 별도의 이미지 생성 작업이 자동으로 실행된다. `a girl {walking, running, sitting, casting spell}`은 4개의 프롬프트를 한 번에 실행한다. 파라미터에도 적용 가능하여 `--s {100, 200, 300}`으로 스타일라이즈 값을 비교 테스트할 수 있다. **Fast 모드에서만 작동**하며, Standard 플랜은 최대 10개 동시 생성이 가능하다.

### Multi-Prompt(::) — 개념 가중치 조절

`sword::2 magic::3 background::1`처럼 더블콜론으로 개념을 분리하고 숫자로 가중치를 부여한다. 전투 씬에서 마법 이펙트를 강조하고 싶을 때 `magic effects::3 character::2 forest background::1`로 비중을 조절할 수 있다. 네거티브 웨이트도 가능해서 `forest::1 people::-0.5`로 사람을 줄일 수 있다.

### Pan과 Zoom — 구도 확장

**Zoom Out:** 업스케일 후 1.5x 또는 2x로 캔버스를 확장한다. 클로즈업을 먼저 생성한 뒤 Zoom Out으로 전신을 드러내는 이스타블리싱 샷 제작에 유용하다. **Pan:** 상하좌우로 캔버스를 확장하며, Remix 모드와 결합하면 방향에 따라 다른 요소를 추가할 수 있다. 파노라마 배경 제작에 활용 가능하다.

---

## 애니메이션 스타일 구현 — 슬레이어즈와 Production I.G 재현

### 슬레이어즈 스타일 재현 키워드

핵심 키워드 조합: `90s anime aesthetic, cel-shaded, bold outlines, vibrant colors, high-energy, Slayers anime style, fantasy anime, dramatic magical effects`

레퍼런스 아티스트로 **아라이즈미 루이**(Rui Araizumi, 슬레이어즈 캐릭터 디자이너)를 언급하면 해당 미학에 더 가까워진다. **90년대 애니메이션** 특유의 약간 따뜻한 톤, 굵은 외곽선, 대담한 원색이 특징이다.

### Production I.G 작화 퀄리티 재현

키워드: `anime key visual, high detail, cinematic composition, professional anime production quality, rich color depth, detailed shading, atmospheric lighting, Production I.G animation quality`

I.G 스타일은 **사실적 배경 위의 디테일한 캐릭터**, 풍부한 색감 깊이, 시네마틱 구도가 핵심이다.

### 파스텔 색감 구현

`pastel color palette, soft pastel tones, muted colors, gentle color harmony, soft shading, light and airy tones`를 프롬프트에 추가한다. --sref 코드 중 파스텔 톤에 특화된 코드를 찾아 고정하는 것이 가장 효과적이다.

### 마법 이펙트 표현 사전

`glowing runes`, `magical particles`, `energy burst`, `spell circle`, `glowing aura`, `light trails`, `sparkle effects`, `swirling energy`, `floating light orbs`, `magical fire`, `beam of light`

---

## 품질 최적화와 비용 관리

### 업스케일 선택 가이드

**Upscale Subtle** — 원본을 최대한 보존하면서 해상도만 2배 증가. 뮤직비디오 최종 컷에 **기본 추천**. 원본 이미지가 만족스러울 때 사용한다.

**Upscale Creative** — 해상도 2배 증가 + AI가 디테일을 추가·보정. 손가락, 눈, 작은 결함을 자동 수정하는 효과가 있다. 원본에 소소한 문제가 있을 때 사용한다.

Niji V7의 기본 출력 해상도는 16:9 기준 약 **1456×816px**이다. Upscale 후 약 **2912×1632px**로, HD 뮤직비디오에 충분하다. 4K가 필요하면 **Topaz Gigapixel AI** 같은 외부 업스케일러를 추가 사용한다.

### 비용 최적화 전략

30~50컷 프로젝트의 예상 GPU 소모: 컷당 평균 3~5회 생성(리롤+보정 포함) + 업스케일 = **약 150~300분(2.5~5시간)**의 Fast GPU 시간. Standard 플랜(15시간)이면 여유 있다.

- **탐색 단계:** Relax 모드(무제한, 1~10분 대기)로 스타일·구도 실험
- **Draft 모드:** 아이디어 테스트 시 10배 빠르고 50% 비용으로 빠른 반복
- **최종 렌더링만 Fast 모드:** 확정된 프롬프트만 Fast로 생성
- **Permutation으로 효율화:** 한 명령에 여러 변형 동시 테스트
- **불필요한 업스케일 자제:** 최종 선택분만 업스케일

---

## 문제가 생겼을 때 — 트러블슈팅

**"캐릭터가 컷마다 달라 보여요"**
→ 캐릭터 설명문이 매번 동일한지 확인. --sref 코드가 모든 프롬프트에 같은지 체크. 의상을 단순화(단색). 한 번에 하나의 변수만 변경. 여러 장 생성 후 가장 일관된 것 선별.

**"원하는 스타일이 안 나와요"**
→ `--sref` 코드를 변경하거나 `--sref random`으로 새 스타일 탐색. `--s` 값 조정(낮추면 프롬프트에 충실). `--style raw` 추가 시도. `--no 3d, realistic, photograph`로 원치 않는 스타일 배제.

**"배경이 없이 캐릭터만 나와요"**
→ V7의 특성. 반드시 `outdoors`, `indoors`, 또는 구체적 배경 묘사를 추가. 예: `in a medieval fantasy village`, `forest clearing`.

**"손가락이 이상해요"**
→ V7에서 대폭 개선되었지만 여전히 발생 가능. Vary Region으로 손 부분만 재생성. Creative Upscale이 자동 수정하기도 함. "five fingers, correct hand anatomy" 명시.

**"텍스트/워터마크가 생겨요"**
→ `--no text, words, writing, letters, watermark, signature, logo` 추가. V7은 텍스트 이해력이 높아서 오히려 텍스트를 잘 생성하므로, 원치 않으면 반드시 네거티브로 제외.

**"프롬프트를 무시하는 것 같아요"**
→ 가장 중요한 키워드를 프롬프트 **앞쪽에** 배치. `::` 멀티프롬프트로 가중치 부여. `--s` 값 낮추기. 모순되는 키워드 제거. 프롬프트를 짧고 명확하게 다듬기.

**"GPU 시간이 부족해요"**
→ `/info`로 잔여 시간 확인. Relax 모드로 전환. Draft 모드 활용. 연간 결제로 전환하면 20% 절약. 추가 Fast GPU 시간은 $4/시간에 구매 가능.

---

## 전체 제작 체크리스트

프로젝트 시작부터 완료까지의 순서를 정리한다.

1. **Midjourney/Niji 구독 결제** (Standard $30/월 추천)
2. **Discord 서버 접속** 또는 nijijourney.com 웹 UI 접속
3. **`/settings`에서 Niji 7 기본 설정** + Remix Mode 활성화
4. **캐릭터 마스터 설명문 작성** (일상 버전 + 변신 버전)
5. **--sref 코드 탐색 및 확정** (Draft 모드로 5~10개 테스트)
6. **캐릭터 시트 생성** (앞모습, 3/4 뷰)
7. **컷 리스트 작성** (씬별 샷 타입·내용·분위기 정리)
8. **씬별 배치 생성** (일상 → 변신 → 전투 → 귀환 순)
9. **선별 + Vary Region 보정**
10. **최종 Upscale** (Subtle 기본, 필요시 Creative)
11. **폴더 정리** (`01_village/`, `02_mirror/`, `03_battle/`, `04_ending/`)
12. **영상 편집 소프트웨어에서 시퀀싱** (Premiere, DaVinci, Canva 등)

---

## 결론: 핵심 원칙 3가지

Niji V7으로 뮤직비디오를 만드는 전체 과정은 결국 세 가지 원칙으로 수렴한다. **첫째, 일관성은 시스템으로 만든다.** --cref 없이도 동일한 텍스트 설명 + 동일한 --sref 코드 + 동일한 --seed를 모든 프롬프트에 적용하면 놀라운 수준의 캐릭터 일관성을 달성할 수 있다. **둘째, V7은 구체성을 보상한다.** "anime girl" 대신 "a young girl with long wavy pastel green hair reaching her waist, bright emerald eyes"라고 쓰면 결과가 극적으로 달라진다. V7의 리터럴한 해석력은 상세한 프롬프트를 정확히 반영한다. **셋째, 효율은 워크플로우에서 나온다.** Draft 모드로 빠르게 탐색하고, Relax 모드로 비용을 아끼고, Permutation으로 변형을 동시에 테스트하고, Vary Region으로 부분만 수정하는 이 파이프라인이 30~50컷을 현실적인 시간과 비용 안에서 완성하게 해준다.