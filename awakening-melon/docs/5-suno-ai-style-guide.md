# Suno AI 완벽 프롬프트 작성 가이드 (2025~2026)

Suno AI에서 고품질 음악을 생성하려면 **Style of Music 프롬프트와 Lyrics 포맷팅을 별도로 최적화**해야 한다. 이 가이드는 Custom Mode 기반으로 가사 구조화, 스타일 프롬프트 설계, 고급 옵션 활용, 그리고 YOASOBI 스타일 J-pop 생성까지 단계별로 다룬다. 최신 V5 모델(2025년 9월 출시)은 **8분 길이 생성, 10배 빠른 처리, 스튜디오급 44.1kHz 오디오**를 지원하며 이전 버전과 프롬프트 작성법이 일부 달라졌다.

---

## 1. Lyrics 입력: 섹션 태그와 가사 구조화

Suno의 Custom Mode에서 가사는 **대괄호 섹션 태그**로 곡의 뼈대를 잡는다. 태그는 명령이 아닌 "제안"이므로 AI가 무시할 수도 있지만, 올바르게 사용하면 곡 구조가 극적으로 개선된다.

### 핵심 섹션 태그 일람

| 태그 | 용도 | 비고 |
|------|------|------|
| `[Intro]` | 도입부 | 단독 사용 시 불안정. `[Instrumental Intro]`가 더 안정적 |
| `[Verse]` / `[Verse 1]` | 절(벌스) | 4줄 권장, 줄당 음절 수 일정하게 |
| `[Pre-Chorus]` | 코러스 전 빌드업 | 1~2줄 짧게 |
| `[Chorus]` | 후렴 | 2~4줄, 짧고 반복 가능한 훅 |
| `[Bridge]` | 브릿지 | 1~3줄, 분위기 전환 |
| `[Instrumental]` / `[Instrumental Break]` | 기악 구간 | 보컬 없는 간주 |
| `[Outro]` | 아웃트로 | `[End]` 또는 `[Fade Out]`과 함께 사용 가능 |
| `[Build-Up]` | 점진적 에너지 상승 | 코러스 직전에 배치 |
| `[Breakdown]` | 에너지를 줄인 구간 | 브릿지와 결합 효과적 |
| `[Drop]` / `[Bass Drop]` | EDM 드롭 | 에너지 폭발 지점 |

### 섹션 태그 작성 규칙

**반드시 지켜야 할 것:**
- 대괄호 `[ ]` 사용 (소괄호, 중괄호 불가)
- 태그는 **자체 줄**에 단독 배치, 가사 위에 위치
- 섹션 사이에 **빈 줄** 삽입
- 태그는 **3단어 이내**로 짧게 (긴 문장은 가사로 불려버림)

**피해야 할 것:**
- `[call and response between percussion and bass]` ← 너무 길면 가사처럼 노래됨
- 한 섹션에 성능 큐를 여러 개 겹쳐 쌓기 (혼란 유발)
- 가사 없이 태그만 나열 (AI가 임의로 가사 생성)

### 보컬·퍼포먼스 메타태그

가사 필드 안에서 보컬 스타일을 지정할 수 있다:

```
[Female Vocal]    — 여성 보컬
[Male Vocal]      — 남성 보컬
[Whisper]         — 속삭임
[Rap]             — 랩 딜리버리
[Spoken Word]     — 나레이션/말하기
[Duet]            — 듀엣
[Falsetto]        — 팔세토
[Belting]         — 파워 보컬
```

듀엣 예시:
```
[Verse 2]
[Male Vocal] I walked through fire
[Female Vocal] And I held the line
[Both] We rise together, every time
```

에너지·무드 메타태그(섹션 시작에 배치):
```
[Mood: Calm]
[Energy: High]
[Instrument: Keys, Soft Drums]
```

### 일본어 가사 입력 시 핵심 주의사항

일본어 가사를 Suno에 입력할 때 **가장 중요한 원칙은 히라가나 중심으로 작성하는 것**이다. 한자(漢字)는 여러 읽기(음독/훈독)가 있어 AI가 오독할 수 있고, 로마자(romaji)는 영어로 인식되어 발음이 망가진다.

- **히라가나/카타카나 직접 입력** 권장. 예: `覚悟` → `かくご`로 변환
- 외래어는 카타카나로: `AI` → `エーアイ`
- **로마자(romaji) 사용 금지** — 영어 악센트로 발음됨
- 섹션 태그는 **영어** 그대로 사용: `[Verse]`, `[Chorus]` 등
- **한 섹션 내에서 언어 혼합 최소화** — "언어 드리프트" 방지
- Style Prompt에 `"All lyrics in Japanese"` 또는 `"J-pop"` 명시
- 일본어는 영어보다 줄당 모라(mora) 수가 적으므로 **한 줄을 짧게** 유지
- 이중 언어 곡의 경우 언어별로 **섹션을 분리**

---

## 2. Style of Music 프롬프트 설계법

Style of Music 필드는 **120자 제한**이며, 곡의 음향적 청사진을 정의한다. Suno는 **앞쪽 단어에 더 높은 가중치**를 부여하므로 핵심 장르를 맨 앞에 배치해야 한다.

### 황금 공식

```
[장르] + [BPM] + [무드] + [악기] + [보컬 스타일] + [시대/분위기]
```

**4~7개 디스크립터**가 최적이다. 너무 적으면 제네릭한 결과, 너무 많으면 AI가 혼란을 일으킨다. 악기는 **2~3개**, 장르는 **1~2개**가 적당하다.

### J-pop / 애니메이션 스타일 프롬프트 예시

| 용도 | Style Prompt |
|------|-------------|
| 애니 오프닝 (범용) | `J-Rock, Anime Opening, high tempo 170 BPM, soaring female vocals, electric guitar, emotional chorus, optimistic` |
| 애니 엔딩 (발라드) | `J-pop, Anime OST, slow tempo, emotional female vocals, piano, soft strings, melancholic, bittersweet` |
| 소년 만화 액션 OP | `J-Rock, anime opening, fast-paced 180 BPM, intense male vocals, driving electric guitar, powerful drums, heroic` |
| 아이돌/카와이 OP | `J-pop, Idol Pop, upbeat, kawaii vocals, bright synths, catchy hook, energetic, cute` |
| 시티팝 | `City Pop, 1980s Japan, funk bassline, shimmering synths, urban night vibe, smooth vocals` |

### YOASOBI 스타일 재현을 위한 프롬프트

YOASOBI의 시그니처 사운드는 **일렉트로닉 팝 프로덕션 + 빠른 리듬(130~170 BPM) + 에너지 넘치는 여성 보컬 + 밝은 멜로디 + 감성적 강렬함**으로 요약된다. 아티스트명은 저작권 문제로 차단되므로 음악적 특성을 묘사해야 한다.

**추천 프롬프트 (120자 이내):**

```
J-pop, electropop, 150 BPM, energetic female vocals, bright synths, emotional, fast-paced, catchy
```
(82자 — 여유 있음)

```
anime pop, synth-driven electronic J-pop, fast 145 BPM, bright female vocals, pulsing synths, emotional melody, upbeat
```
(116자 — 거의 한계)

**곡별 스타일 변형:**

- **「夜に駆ける」 스타일:** `J-pop, synth-driven electronic pop, 140 BPM, energetic female vocals, bright arps, emotional melody, fast-paced`
- **「アイドル」 스타일:** `J-pop, anime pop, energetic, bright synths, dynamic drums, soaring female vocals, upbeat, catchy chorus`
- **「群青」 스타일:** `J-pop, electronic pop, 130 BPM, emotional female vocals, piano + synth layers, bittersweet, driving rhythm`
- **고에너지 댄스:** `J-pop, electropop, dance-pop, 155 BPM, bright female vocals, pulsing synths, euphoric, fast-paced`

### YOASOBI 스타일 핵심 키워드 조합표

| 요소 | 효과적인 키워드 |
|------|----------------|
| 장르 | `J-pop`, `anime pop`, `electropop`, `synth-pop`, `dance-pop` |
| 템포 | `fast-paced`, `140 BPM`, `150 BPM`, `energetic tempo` |
| 보컬 | `energetic female vocals`, `bright female vocals`, `soaring female vocals` |
| 악기 | `bright synths`, `pulsing synths`, `bright arps`, `electronic drums`, `piano` |
| 무드 | `upbeat`, `emotional`, `bright`, `bittersweet`, `euphoric`, `dynamic` |

---

## 3. YOASOBI 스타일 일본어 곡 — 완전한 입력 예시

아래는 실제 Suno Custom Mode에 붙여넣을 수 있는 **완전한 예시**다.

### Title 필드
```
夜を超えて
```

### Style of Music 필드
```
J-pop, electropop, 148 BPM, energetic female vocals, bright synths, piano, emotional, fast-paced, catchy
```

### Lyrics 필드
```
[Instrumental Intro]

[Verse 1]
[Female Vocal]
よるのまちを かけぬけて
きえそうな こえを たどる
だれも しらない みちのさき
ひかりが まっている きがした

[Pre-Chorus]
[Build-Up]
とまらないで このままで
いまなら まだ まにあうから

[Chorus]
[Energy: High]
よるをこえて きみのもとへ
つよくなれる きがしたんだ
なみだも いたみも ぜんぶ つれて
あしたへ はしりだす

[Verse 2]
[Female Vocal]
わすれかけた やくそくが
むねのおくで ふるえてる
ことばに できない おもいだけ
このうたに のせて とどけたい

[Pre-Chorus]
[Build-Up]
こわくないよ ひとりじゃない
きみが いるから だいじょうぶ

[Chorus]
[Energy: High]
よるをこえて きみのもとへ
つよくなれる きがしたんだ
なみだも いたみも ぜんぶ つれて
あしたへ はしりだす

[Bridge]
[Breakdown]
しずかな よるに ひびく メロディー
それだけで じゅうぶんだった

[Final Chorus]
[Energy: High]
よるをこえて きみのもとへ
もうにどと はなさないよ
なみだも いたみも ぜんぶ つれて
ひかりへ はしりだす

[Outro]
[Fade Out]
```

**이 예시의 설계 포인트:**
- 전체 가사를 **히라가나**로 작성해 AI 발음 오류 최소화
- 외래어 `メロディー`만 카타카나 사용
- Verse **4줄**, Chorus **4줄**, Pre-Chorus **2줄**로 일관된 구조
- `[Build-Up]`으로 코러스 전 에너지 상승 유도
- `[Energy: High]`로 코러스 에너지 레벨 명시
- `[Breakdown]`으로 브릿지에서 잠시 숨 쉬는 공간 확보
- `[Fade Out]`으로 자연스러운 종결

---

## 4. Advanced Options와 모드별 차이점

### Custom Mode vs Simple Mode

**Simple Mode**는 하나의 텍스트 설명만 입력하면 AI가 가사·멜로디·구조를 모두 자동 생성한다. 빠른 실험에 유용하지만 정밀한 제어가 불가능하다. **Custom Mode**는 Title, Lyrics, Style of Music를 각각 분리해 입력할 수 있으며, 섹션 태그·메타태그·퍼소나 선택이 가능하다. 고품질 결과물을 원한다면 **항상 Custom Mode를 사용**해야 한다.

### Instrumental 토글

Custom Mode에서 **Instrumental 토글을 켜면** 보컬 없이 기악곡만 생성된다. 배경음악, 팟캐스트 BGM, 게임/영상 음악 제작에 적합하다. Simple Mode에서도 프롬프트에 "instrumental"을 명시하면 비슷한 효과를 얻을 수 있다.

### Personas (V4 이후, Pro/Premier 전용)

특정 곡의 보컬·스타일·분위기의 "에센스"를 저장해 **재사용 가능한 크리에이티브 자산**으로 만드는 기능이다. 곡의 점 세 개 메뉴에서 "Make Persona"를 선택하면 생성되며, 이후 Custom Mode에서 가사 필드 위에서 퍼소나를 선택하면 해당 음색과 스타일이 적용된다. 일관된 아티스트 사운드를 유지하는 데 핵심적이다.

### ReMi 가사 모델 (V4 이후)

기본 Classic 가사 생성기 외에 **ReMi 모델**을 선택하면 더 창의적이고 "엣지 있는" 가사를 생성한다. Lyrics 입력 모달에서 "Write with Suno" → 모델 드롭다운에서 ReMi 선택으로 접근한다.

### Song Editor (Pro/Premier)

생성된 곡의 **특정 섹션만 교체(Replace Section)**, 크롭(Crop), 확장(Extend)이 가능하다. 최대 **12개 스템 분리**도 지원하며, 이를 외부 DAW에서 믹싱할 수 있다.

---

## 5. 버전별 특성과 2024-2025 최신 업데이트

Suno는 2023년 가을 V2 출시 이후 급격하게 진화해왔으며, **2025년 9월 출시된 V5가 현재 최신 모델**이다.

### 버전 타임라인

| 버전 | 출시 시기 | 최대 생성 길이 | 핵심 변화 |
|------|----------|--------------|----------|
| V3 | 2024년 봄 | 2분 | 웹 앱 전환 |
| V3.5 | 2024년 여름 | 4분 | 곡 구조 개선 |
| **V4** | **2024년 11월** | 4분 | Covers, Personas, ReMi, Remaster 추가 |
| **V4.5** | **2025년 5월** | **8분** | 프롬프트 준수도 향상, 44.1kHz 스튜디오 품질, 속도 2배 |
| V4.5+ | 2025년 7월 | 8분 | Add Vocals, Add Instrumentals, Inspire 기능 |
| **V5** | **2025년 9월** | **8분** | 처리속도 10배, 지능형 작곡 아키텍처, 보이스/악기 메모리, 프로페셔널 컨트롤 |

### 2025년 주요 업데이트

**Suno Studio 출시 (2025년 9월, Premier 전용):** 브라우저 기반 제너러티브 오디오 워크스테이션(DAW)이다. 멀티트랙 타임라인 편집, BPM/볼륨/피치 조절, 무제한 스템 변형 생성, 오디오+MIDI 내보내기를 지원한다. WavTool 인수 기술 기반이다.

**Warner Music Group 합의 (2025년 11월):** Suno가 WMG 카탈로그를 학습에 사용하는 대가로 **5억 달러** 규모의 합의가 이루어졌다. 이후 유료 계정에서만 다운로드가 가능하며 월간 다운로드 캡이 도입되었다.

**현재 모델 접근성:** 무료 플랜은 V4.5-All, Pro/Premier 플랜은 V5를 사용한다.

---

## 6. 테스트 변수 실험 가이드와 품질 향상 전략

### BPM 테스트 매트릭스

장르에 따라 최적 BPM이 크게 다르다. Style Prompt에 `"140 BPM"`처럼 직접 숫자를 넣으면 **리듬 안정성이 극적으로 향상**된다.

| BPM | 적합 장르 | YOASOBI 적용도 |
|-----|----------|---------------|
| 120~128 | 팝, 하우스, EDM | 느린 YOASOBI 곡 (「たぶん」 류) |
| 130~140 | 일렉트로팝, K-pop, 트랩 | 중간 템포 감성곡 (「群青」 류) |
| **140~155** | **J-pop, 댄스팝, 애니 OP** | **YOASOBI 핵심 BPM 구간** |
| 160~180 | J-Rock, 수학록, 펑크 | 고에너지 애니 OP |

### 보컬 스타일 A/B 테스트 전략

동일 가사·구조에서 보컬 키워드만 바꿔 비교하라:

```
테스트 A: "energetic female vocals" (밝고 파워풀)
테스트 B: "soft female vocals" (부드럽고 섬세)  
테스트 C: "breathy female vocals" (브레시, 감성적)
```

한 번에 **하나의 변수만 변경**하고 나머지는 고정해야 어떤 키워드가 결과에 영향을 주는지 파악할 수 있다. Suno는 매번 **2개 버전을 생성**하므로 자연스럽게 비교가 가능하다.

### 악기 조합 실험

YOASOBI 스타일 기준으로 아래 조합을 순차 테스트:

- **전자 중심:** `bright synths, electronic drums, pulsing bass` → 「夜に駆ける」
- **피아노 + 신스:** `piano, synth layers, electronic drums` → 「群青」
- **오케스트라 믹스:** `strings, synths, piano, dramatic drums` → 영화적 감성
- **어쿠스틱 블렌드:** `acoustic guitar, light synths, soft drums` → 발라드 변형

### 무드 키워드 효과 맵

| 키워드 | 생성 결과 경향 |
|--------|--------------|
| `uplifting` | 밝은 코드 진행, 상승감 있는 멜로디 |
| `emotional` | 감성적 보컬 딜리버리, 다이내믹 변화 |
| `energetic` | 빠른 리듬, 강한 드럼, 높은 에너지 |
| `bittersweet` | 장조와 단조 혼합, 노스탤직한 느낌 |
| `euphoric` | 코러스에서 폭발적 상승, EDM적 빌드업 |
| `melancholic` | 단조 중심, 느린 템포 경향, 어두운 톤 |

---

## 실전 워크플로우: 고품질 곡 생성 7단계

**Step 1 — 비전 정의:** 장르, BPM, 무드, 보컬 타입을 먼저 결정한다. 레퍼런스 곡 2~3곡을 선정해 목표 사운드를 명확히 한다.

**Step 2 — 외부에서 가사 작성:** ChatGPT나 Claude에서 가사를 작성한다. 일본어의 경우 모라(mora) 수를 맞추고 히라가나 중심으로 변환한다. 음절 수를 Verse 8~10, Chorus 10~12로 맞추면 싱크가 좋다.

**Step 3 — Style Prompt 제작:** 황금 공식(장르+BPM+무드+악기+보컬)에 맞춰 120자 이내로 작성한다. 핵심 장르를 **맨 앞에** 배치한다.

**Step 4 — 초기 2테이크 생성:** Custom Mode에서 가사+스타일 입력 후 생성. 2개 결과 중 좋은 것을 기반으로 선택한다.

**Step 5 — 수술적 편집:** Replace Section으로 약한 부분만 교체한다. **한 번에 하나의 문제만** 수정한다(가사 OR 멜로디 OR 에너지). Extend는 **30초 단위**로 짧게 해서 스타일 드리프트를 방지한다.

**Step 6 — Extend 시 Style Prompt 재입력:** 확장 시 원래의 스타일 프롬프트를 반드시 다시 포함한다. 커뮤니티 조사에 따르면 **확장 트랙의 62%가 원래 프롬프트에서 벗어난다.**

**Step 7 — 최종 품질 검수:** 훅의 캐치함, 보컬 클리어리티, 편곡 흐름(Intro→Verse→Chorus→Bridge→Outro)을 점검한다. Pro/Premier라면 12트랙 스템을 추출해 외부 DAW에서 미세 조정할 수 있다.

---

## 피해야 할 8가지 치명적 실수

1. **모호한 프롬프트** — "슬픈 록 노래"는 크레딧 낭비. BPM, 키, 보컬 타입까지 명시하라
2. **모순되는 지시** — "calm aggressive" 같은 상충 키워드는 AI를 혼란시킨다
3. **디스크립터 과적재** — 10개 이상의 키워드 나열은 역효과. **4~7개**가 최적
4. **BPM 미지정** — 템포를 숫자로 지정하면 리듬 안정성이 극적으로 향상된다
5. **원샷 기대** — 첫 생성에서 완벽한 결과를 기대하지 마라. 프로 크리에이터도 반복 생성→평가→수정 과정을 거친다
6. **아티스트명 직접 입력** — "YOASOBI style"은 차단될 수 있다. **음악적 특성을 묘사**하라
7. **Extend 시 Style Prompt 누락** — 확장할 때 원래 스타일을 다시 넣지 않으면 곡이 변질된다
8. **가사-장르 에너지 불일치** — 펑크 스타일에 느긋한 시적 가사, 발라드에 짧고 공격적인 가사는 싱크가 무너진다

---

## 결론: YOASOBI 스타일 최적 세팅 요약

YOASOBI 사운드를 Suno에서 재현하기 위한 최종 권장 세팅은 다음과 같다. Style Prompt에는 `J-pop, electropop, 145-150 BPM, energetic female vocals, bright synths, piano, emotional, fast-paced`를 넣고, 가사는 히라가나 중심의 4줄 Verse / 4줄 Chorus 구조로 작성하며, `[Build-Up]`과 `[Energy: High]`를 코러스 전후에 배치한다. V5 또는 V4.5 모델에서 Custom Mode를 사용하되, 매 생성마다 **한 변수만 조정하며 반복 실험**하는 것이 핵심이다. 프롬프트는 "명령"이 아니라 "제안"이므로, 같은 설정으로 5~10회 생성해 최적의 테이크를 선별하는 접근이 가장 현실적이고 효과적인 전략이다.