# **니지저니 7 기반의 캐릭터 일관성 유지 및 뮤직 비디오 제작을 위한 전문 워크플로우 분석 보고서**

2026년 1월 9일 출시된 니지저니 7(Nijijourney 7, 이하 Niji 7)은 생성형 인공지능이 애니메이션 미학을 해석하는 방식에 있어 기념비적인 전환점을 시사한다.1 지난 1년 반 동안의 연구 개발 끝에 공개된 이 모델은 단순한 화질 개선을 넘어, 미학적 정교함과 구조적 일관성이라는 두 가지 핵심 과제를 해결하는 데 집중하였다.1 특히 뮤직 비디오 제작과 같이 고도의 시각적 연속성이 요구되는 프로젝트에서 Niji 7은 캐릭터의 정체성을 유지하면서도 정밀한 연출을 가능케 하는 강력한 도구들을 제공한다. 본 보고서는 니지저니의 기초부터 캐릭터 일관성 유지 기법, 그리고 이를 활용한 전문적인 뮤직 비디오 제작 워크플로우에 이르기까지 모든 핵심 기능을 기술적 심도와 함께 상세히 분석한다.

## **니지저니 7의 기술적 기원과 미학적 패러다임의 변화**

니지저니는 미드저니(Midjourney)와 스펠브러시(Spellbrush)의 협력으로 탄생한 모델로, 동양적인 애니메이션 및 일러스트레이션 스타일을 해석하는 데 최적화되어 있다.3 Niji 7은 이전 버전들과 달리 '선의 미학(The Beauty of Line)'과 '공간의 단순성(Combining Line and Space)'이라는 철학적 기초 위에 설계되었다.1 이는 인공지능이 단순히 이미지를 픽셀 단위로 생성하는 것을 넘어, 애니메이션 제작자가 형태와 질감, 조명을 선을 통해 표현하는 방식인 '선 언어'를 깊이 있게 이해하고 있음을 의미한다.1

과거의 생성 모델들이 화려한 광원 효과나 복잡한 디테일로 구조적 결함을 가리려 했다면, Niji 7은 정교한 선과 여백의 활용을 통해 애니메이션 본연의 미학을 극대화한다.1 특히 선은 단순히 사물의 경계를 표시하는 역할을 넘어 형태의 입체감과 질감을 전달하는 정교한 스타일화의 도구로 사용된다.1 이러한 기술적 토대는 뮤직 비디오의 스토리보드를 제작할 때 캐릭터의 선화가 일관되게 유지되어야 하는 전문적인 요구를 충족시킨다.5

| 기능 범주 | 이전 버전(Niji 6)의 특징 | 니지저니 7(Niji 7)의 발전 사항 |
| :---- | :---- | :---- |
| **선 표현력(Linework)** | 경계선 위주의 지시적 표현 | 형태, 질감, 조명을 전달하는 표현적 선 1 |
| **프롬프트 해석** | 추상적이고 분위기 중심의 해석 | 구체적이고 문자 그대로의 정밀한 해석 6 |
| **이미지 선명도** | 표준 해상도의 일반적 디테일 | 눈의 반사광, 꽃잎의 세부 묘사 등 HD 업그레이드 1 |
| **공간 일관성** | 좌우 배치 등 복잡한 명령에 취약 | "왼쪽의 빨간 큐브"와 같은 공간 지시 완벽 수행 1 |
| **배경 및 여백** | 빈 공간을 임의의 디테일로 채우는 경향 | 의도적인 단순함과 평면적 렌더링 지원 1 |

## **니지저니 7 기초: 핵심 인터페이스 및 활성화 메커니즘**

Niji 7을 사용하기 위한 첫 번째 단계는 해당 모델을 명시적으로 활성화하는 것이다. 사용자는 디스코드(Discord) 환경에서 프롬프트 끝에 \--niji 7 파라미터를 추가하거나, 웹 인터페이스의 설정 메뉴에서 'Version' 드롭다운을 통해 Niji 7을 선택할 수 있다.1 Niji 7은 이전 버전들과 비교하여 훨씬 더 '문자 그대로(Literal)' 프롬프트를 해석하는 경향이 있으며, 이는 제작자가 의도한 바를 정확히 이미지에 반영할 수 있게 한다.1

이러한 문자 그대로의 해석 방식은 양날의 검과 같다. "Remote Spring"이라는 프롬프트를 입력했을 때, 이전 모델은 '한적한 샘터'를 연상하며 이미지를 생성했을 수 있으나, Niji 7은 이를 문자 그대로 받아들여 '봄날의 리모컨'을 생성할 수도 있다는 점을 유의해야 한다.1 따라서 Niji 7을 사용할 때는 비유적 표현보다는 구체적인 사물과 환경에 대한 묘사가 우선시되어야 한다.7

### **시각적 코히어런시(Coherency)의 진보**

Niji 7의 가장 두드러진 특징 중 하나는 비약적으로 향상된 코히어런시이다.1 이는 특히 캐릭터의 눈동자 내부에 비치는 미세한 반사광이나, 몽환적인 배경 속에 흩날리는 개별 꽃잎 하나하나를 HD 급의 선명도로 묘사할 수 있게 한다.1 뮤직 비디오와 같이 캐릭터의 감정선이 중요한 영상 매체에서 이러한 눈동자의 디테일과 표현력은 관객과의 정서적 교감을 강화하는 핵심 요소로 작용한다.1

또한, Niji 7은 복잡한 공간적 배치를 요구하는 프롬프트를 이전보다 훨씬 잘 소화한다. 예를 들어 "네 개의 팔을 가진 소녀가 각 손에 아이스크림을 들고 있는 모습"과 같이 논리적으로 복잡한 신체 구조도 해부학적 붕괴 없이 구현해낼 수 있다.1 이는 콘티 작업 시 특정 캐릭터의 특수한 설정을 유지하는 데 있어 큰 이점을 제공한다.

## **정밀 프롬프팅(Precision Prompting) 체계 분석**

Niji 7은 "흥미로운 프롬프트가 흥미로운 이미지를 만든다"는 원칙을 고수한다.6 이전 모델들이 단순한 키워드만으로도 인공지능이 알아서 배경과 조명을 '추측'하여 화려하게 그려냈다면, Niji 7은 사용자가 요청하지 않은 요소는 과감히 생략한다.6 따라서 뮤직 비디오 제작을 위한 풍부한 화면을 얻기 위해서는 정밀한 프롬프트 구조화가 필수적이다.

### **구조적 프롬프트의 설계 원칙**

전문가들은 Niji 7에서 최상의 결과를 얻기 위해 '주체(Subject) → 특징(Traits) → 행동(Action) → 환경(Environment)' 순의 구조적 접근을 권장한다.7 분위기 중심의 단어(예: dreamy, emotional)는 구조가 확립된 후에 추가하는 것이 바람직하다.

1. **주체 및 세부 특징**: "라임 그린색 짧은 머리의 소녀, 푸른 눈, 송곳니, 한 개로 묶은 번 헤어 스타일".6  
2. **행동**: "시장 바닥의 조약돌 위에 앉아 차를 따르고 있는 모습".6  
3. **환경**: "야외 시장, 배경에 붉은 스포츠카가 주차된 차고".6  
4. **스타일 제어**: "애니메이션 스크린샷(Anime screenshot), 골든 아워 조명, 심도 효과(Depth of field)".1

### **핵심 파워 키워드 활용 전략**

Niji 7의 고유한 기능을 끌어내기 위해 반드시 익혀야 할 핵심 키워드들이 존재한다.1

* **"Anime Screenshot"**: 이 키워드는 Niji 7의 진보된 선 표현력과 애니메이션 특유의 평면적 채색법을 활성화한다. 실제 애니메이션의 한 장면 같은 구도와 스타일을 얻기 위해 필수적인 도구이다.1  
* **"Minimalist Graphic Logo"**: Niji 7의 뛰어난 여백 활용 능력을 테스트하고 싶을 때 사용한다. 이는 간결한 디자인과 깨끗한 선이 요구되는 아이콘이나 그래픽 소스 제작에 최적이다.1  
* **신발 종류 지정(예: "wearing boots")**: Niji 7에서 캐릭터의 전신 샷(Full-body)을 유도하기 위한 가장 효과적인 방법은 캐릭터가 신고 있는 신발의 종류를 구체적으로 명시하는 것이다. 인공지능은 신발을 그리기 위해 논리적으로 발끝까지의 전신을 렌더링하게 된다.6

## **캐릭터 일관성 유지의 핵심: 옴니-레퍼런스(Omni-Reference)**

뮤직 비디오 제작에서 가장 큰 난제는 서로 다른 장면에서도 주인공 캐릭터가 동일 인물로 보여야 한다는 점이다. Niji 7은 이전의 캐릭터 레퍼런스(--cref) 기능을 넘어선 **옴니-레퍼런스(Omni-Reference, \--oref)** 시스템을 도입하였다.8 이는 캐릭터뿐만 아니라 사물, 차량, 비인간 생명체까지도 하나의 레퍼런스 이미지로 고정하여 반복적으로 생성할 수 있게 한다.

### **옴니-레퍼런스의 작동 메커니즘**

현재 Niji 7에서는 기존의 \--cref 파라미터가 지원되지 않으며, 제작팀은 이를 대체할 더욱 강력한 시스템으로 옴니-레퍼런스를 제시하였다.1 이 기능은 사용자가 제공한 단일 이미지의 형태, 색상, 해부학적 구조를 분석하여 새로운 장면에 완벽하게 이식한다.8

* **디스코드 사용법**: 프롬프트 끝에 \--oref을 추가한다.  
* **웹 사용법**: 이미지 아이콘을 클릭하여 이미지를 업로드한 후, 'Omni-Reference' 섹션으로 드래그하여 고정한다.8

### **옴니-웨이트(Omni-Weight, \--ow)를 통한 정밀 제어**

옴니-레퍼런스의 영향력을 조절하는 \--ow 파라미터는 1에서 1,000 사이의 값을 가지며, 기본값은 100이다.8 이 값은 프로젝트의 성격에 따라 전략적으로 조정되어야 한다.

| 웨이트 값 범위 | 영향력 수준 | 권장 사용 사례 |
| :---- | :---- | :---- |
| **25 – 50** | 낮음(Low) | 스타일 전이 최적화. 사진 소스를 애니메이션 스타일로 변환할 때 유용.8 |
| **100 – 300** | 중간(Moderate) | 균형 잡힌 일관성. 캐릭터의 정체성을 유지하면서 새로운 포즈와 행동을 유도할 때 적합.8 |
| **400 – 1000** | 높음(High) | 극한의 일관성. 캐릭터의 얼굴, 복장, 복잡한 로고 등을 원본과 거의 똑같이 복제해야 할 때 사용.8 |

옴니-웨이트를 400 이상으로 설정할 경우 인공지능의 창의성이 제한되어 예측 불가능한 아티팩트가 발생할 수 있으므로, 높은 스타일라이즈(--stylize) 값과 함께 사용하는 것이 권장된다.9

## **스타일 레퍼런스(--sref)와 프로젝트 전체의 시각적 통일성**

캐릭터의 일관성만큼 중요한 것이 뮤직 비디오 전체의 시각적 톤앤매너이다. 이를 위해 니지저니는 **스타일 레퍼런스(Style Reference, \--sref)** 기능을 제공한다.15 이는 특정 이미지의 화풍, 색조, 질감만을 추출하여 생성물에 적용하는 기능이다.

### **스타일 레퍼런스 랜덤(--sref random)과 고유 ID 시스템**

뮤직 비디오 제작 과정에서 자신만의 독특한 스타일을 구축하고 싶다면 \--sref random 기능을 활용할 수 있다.17 이 명령어를 실행하면 시스템은 'random'이라는 단어를 특정 숫자 ID(예: \--sref 3403639244)로 변환한다. 이 숫자는 해당 스타일의 고유 번호이며, 이를 기록해 두었다가 다른 프롬프트에 동일하게 적용하면 영상의 모든 컷이 같은 화풍을 공유하게 된다.5

### **캐릭터와 스타일의 복합 적용 워크플로우**

가장 전문적인 워크플로우는 옴니-레퍼런스와 스타일 레퍼런스를 동시에 사용하는 것이다. \[장면 묘사 프롬프트\] \--oref \[캐릭터 이미지\] \--ow 200 \--sref \[스타일 이미지\] \--sw 250 \--niji 7 이러한 조합을 통해 캐릭터는 특정 인물로 고정되면서, 화면의 전체적인 미학은 지정된 스타일을 따르게 되어 고도로 통제된 연출이 가능해진다.9

## **뮤직 비디오 콘티 및 스토리보드 제작 기법**

뮤직 비디오는 시간의 흐름에 따른 시각적 서사를 담고 있으므로, 효율적인 콘티 작업이 필수적이다. Niji 7은 다중 패널 레이아웃과 정밀한 화면 구성을 지원하여 이 과정을 가속화한다.

### **다중 패널 스토리보드 프롬프팅**

하나의 이미지 안에 여러 개의 내러티브 컷을 포함하고 싶을 때 다중 패널 프롬프트를 사용할 수 있다.19

* **프롬프트 예시**: "A storyboard with 4 panels, anime screenshot,, Panel 1: walking in rain, Panel 2: close-up of a smile, Panel 3: reflection in a window, Panel 4: looking at the camera \--ar 16:9 \--niji 7".20  
* **주의사항**: Niji 7이 아무리 정밀하더라도 단일 프롬프트에서 모든 패널의 내용을 완벽하게 통제하기는 어려울 수 있다. 이 경우 각 컷을 개별적으로 생성한 후 나중에 결합하거나, 웹 에디터의 'Vary Region' 기능을 사용하여 특정 패널의 내용만 수정하는 방식이 더 효율적이다.19

### **멀티 프롬프트(::)와 가중치 제어**

화면 내 요소들 간의 중요도를 조절하기 위해 이중 콜론(::)을 사용하는 멀티 프롬프트 기법이 활용된다.22

* **메커니즘**: \[아이디어 1\]::\[가중치\]\[아이디어 2\]::\[가중치\] 형식을 사용한다.  
* **적용**: 예를 들어 "우주선 내부의 사이버펑크 도시 배경"을 생성할 때, 배경보다 우주선의 디테일이 더 중요하다면 space ship::2 cyberpunk city::1과 같이 입력하여 인공지능이 우주선 묘사에 더 많은 계산 자원을 할당하도록 유도할 수 있다.22

## **웹 인터페이스 에디터와 고급 편집 워크플로우**

니지저니 웹사이트의 'Edit' 탭은 단순한 생성을 넘어, 생성된 이미지를 수정하고 확장하는 전문적인 스튜디오 환경을 제공한다.23

### **영역 수정(Vary Region) 및 인페인팅**

'Vary Region' 도구는 이미지의 특정 부분만 선택하여 다시 생성하는 기능이다.21

1. **선택(Select)**: 라쏘 툴이나 사각형 선택 툴로 수정하고 싶은 영역(예: 어색한 손가락, 배경의 불필요한 사물)을 지정한다.21  
2. **리믹스 모드(Remix Mode)**: 설정에서 리믹스 모드를 활성화하면, 선택 영역을 위한 별도의 프롬프트 수정창이 나타난다.24  
3. **프롬프트 단순화**: 수정 영역에 대한 프롬프트를 입력할 때는 전체 이미지 묘사가 아닌, 해당 영역에 들어갈 대상만 간결하게 입력하는 것이 가장 정확한 결과를 얻는 비결이다. 예를 들어 칼을 꽃으로 바꾸고 싶다면, 수정창에는 "flower"라고만 입력한다.21

### **캔버스 확장: 팬(Pan)과 줌(Zoom)**

뮤직 비디오 연출 중 구도가 너무 답답하거나 배경의 정보량이 더 필요할 때 사용한다.25

* **팬(Pan)**: 이미지를 상, 하, 좌, 우 네 방향 중 하나로 확장한다. 확장된 영역은 기존 이미지의 맥락과 프롬프트의 지시를 따라 자연스럽게 채워진다.25  
* **줌 아웃(Zoom Out)**: 카메라를 뒤로 빼는 효과를 주어 원래 이미지 주위에 더 많은 배경을 생성한다. 1.5배, 2배 혹은 사용자 지정 값(1.0\~2.0)으로 설정 가능하다.26

### **업스케일링(Upscaling) 전략**

Niji 7은 두 가지 네이티브 업스케일러를 제공하여 이미지의 해상도를 2048x2048 이상으로 높인다.4

* **Subtle 업스케일**: 원본의 구도와 디테일을 최대한 유지하면서 픽셀 밀도만 높인다.28  
* **Creative 업스케일**: 해상도를 높이는 과정에서 인공지능이 새로운 디테일을 추가한다. 이는 때때로 저해상도에서 발생한 미세한 노이즈나 어색한 선을 수정해주는 부수적인 효과를 준다.28  
* **외부 도구 활용**: 4K 이상의 초고해상도 영상 제작을 위해서는 Aiarty나 Topaz와 같은 전문 업스케일러를 병행하여 사용하는 것이 업계의 표준이다.5

## **AI 뮤직 비디오 제작 파이프라인: 정지 영상에서 영상으로**

Niji 7을 통해 완성된 콘티 이미지는 영상 제작의 '키프레임(Keyframe)' 역할을 한다.5 2026년 현재의 영상 제작 트렌드는 텍스트만으로 영상을 만드는 것이 아니라, 이미지를 기반으로 움직임을 부여하는 **Image-to-Video (I2V)** 워크플로우를 중심으로 형성되어 있다.31

### **영상 제작 5단계 워크플로우**

1. **참조 이미지 생성**: Niji 7에서 주인공 캐릭터와 배경 스타일을 확립한다.31  
2. **스토리보드 키프레임 추출**: 노래의 가사와 비트에 맞춰 필요한 모든 장면을 Niji 7로 생성한다. 이때 일관성을 위해 \--oref와 \--sref를 적극 활용한다.5  
3. **애니메이션 플랫폼 선택**: 프로젝트의 요구 사양에 따라 최적의 영상 생성 AI를 선택한다.31  
4. **모션 프롬프팅**: 영상 도구에 이미지를 업로드하고, 움직임의 방식(예: "바람에 머리카락이 찰랑거림", "천천히 줌인하며 미소 지음")을 지시한다.5  
5. **포스트 프로덕션**: 생성된 5\~10초 단위의 클립들을 프리미어(Premiere)나 다빈치 리졸브(DaVinci Resolve) 같은 편집 툴로 가져와 음악과 싱크를 맞추고 최종 색보정을 진행한다.5

### **2026년 주요 AI 영상 생성 도구 비교**

뮤직 비디오의 품질을 결정짓는 것은 Niji 7의 정교한 이미지를 얼마나 잘 유지하면서 움직임을 부여하느냐에 달려 있다.5

| 플랫폼 명칭 | 주요 특징 및 장점 | 뮤직 비디오 제작 시의 한계점 |
| :---- | :---- | :---- |
| **Kling 2.6** | 현재 최고의 화질과 물리 엔진 보유. 고해상도 사운드와 대사 싱크 지원.31 | 물리적 법칙이 가끔 붕괴됨(사물을 뚫고 지나가는 등).31 |
| **DomoAI** | 애니메이션 스타일에 특화됨. 다중 키프레임 interpolation 기능으로 캐릭터 일관성 극대화.5 | 실사 영화 같은 웅장한 모션보다는 정적인 애니메이션 연출에 적합.6 |
| **Sora 2** | 소셜 미디어용 숏폼 콘텐츠에 최적화된 화려하고 역동적인 연출 가능.31 | 엄격한 검열 시스템과 긴 대기 시간이 제작 효율을 저하시킬 수 있음.31 |
| **Luma Ray 3** | 시작 프레임과 끝 프레임을 지정하여 움직임의 궤적을 제어할 수 있는 기능 제공.36 | 영상의 길이가 길어질수록 화질의 저하나 지터링(떨림) 현상이 발생할 수 있음.31 |

### **영상 프롬프팅의 3대 원칙**

영상을 생성할 때는 정지 이미지를 설명하던 방식과는 다른 접근이 필요하다.33

1. **시각적으로 관찰 가능한 행동만 묘사**: 캐릭터의 내면 심리가 아닌, 겉으로 드러나는 움직임(예: "고개를 돌림", "사과를 집어 올림")을 명시한다.33  
2. **주요 동작과 부수 동작의 구분**: 주인공의 움직임뿐만 아니라 옷자락의 흔들림, 배경의 흐름 같은 부수적인 움직임을 추가하면 영상의 생동감이 살아난다.33  
3. **해결되지 않은 행동(Unresolved Action)에서 시작**: 동작이 이미 끝난 이미지보다는 동작이 시작되려는 찰나의 이미지를 첫 프레임으로 사용하는 것이 더 자연스러운 물리 법칙을 만들어낸다.33

## **전략적 제언 및 결론**

니지저니 7은 단순한 이미지 생성기를 넘어, 전문적인 애니메이션 제작 공정의 파트너로서 그 입지를 굳히고 있다.2 특히 이번 업데이트에서 보여준 선의 정교함과 옴니-레퍼런스를 통한 극한의 일관성은 독립 창작자가 고품질의 뮤직 비디오를 제작할 수 있는 기술적 장벽을 획기적으로 낮추어 주었다.1

제작자는 Niji 7의 '문자 그대로의 해석'이라는 특성을 이해하고, 추상적인 분위기보다는 구조적이고 정밀한 프롬프트를 작성하는 습관을 들여야 한다.6 또한 캐릭터 고정을 위한 \--oref와 스타일 유지를 위한 \--sref를 결합한 복합 워크플로우를 내재화하는 것이 가장 중요하다.9 다가오는 2026년 하반기에는 더욱 진화된 개인화 시스템과 무드보드 기능이 추가될 예정이므로, 지속적인 평가 작업(Rating Task) 참여를 통해 자신만의 고유한 니지 스타일을 구축해 나갈 것을 권장한다.1

본 보고서에서 다룬 기술적 분석과 워크플로우를 충실히 따른다면, 니지저니 7의 잠재력을 풀 가동하여 상업적 수준의 시각적 완성도를 갖춘 뮤직 비디오를 성공적으로 제작할 수 있을 것이다. 인공지능이 제공하는 정밀한 통제력을 창작자의 감각과 결합하는 것, 그것이 미래 애니메이션 제작의 핵심 경쟁력이다.2

#### **참고 자료**

1. Welcome to Niji V7\! \- niji・journey, 2월 13, 2026에 액세스, [https://nijijourney.com/blog/niji-7](https://nijijourney.com/blog/niji-7)  
2. Midjourney Anime Masterpiece Evolves Again\! Niji 7 Released: Exquisite Eye Highlights, Enhanced Prompt Understanding \+ Sref Style Transfer Upgrade \- Why AIBase?, 2월 13, 2026에 액세스, [https://news.aibase.com/news/24495](https://news.aibase.com/news/24495)  
3. Midjourney v7 Niji Is Here: My Honest Review for Creative Pros | Chase Jarvis, 2월 13, 2026에 액세스, [https://chasejarvis.com/blog/midjourney-v7-niji-is-here-my-honest-review-for-creative-pros/](https://chasejarvis.com/blog/midjourney-v7-niji-is-here-my-honest-review-for-creative-pros/)  
4. Version \- Midjourney, 2월 13, 2026에 액세스, [https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)  
5. Niji 7 Launched: What's New and How to Animate Your AI Anime \- DomoAI, 2월 13, 2026에 액세스, [https://domoai.app/blog/niji-7-guide-animate-ai-anime](https://domoai.app/blog/niji-7-guide-animate-ai-anime)  
6. Niji 7 Prompting Guide, 2월 13, 2026에 액세스, [https://nijijourney.com/blog/niji-7-prompting](https://nijijourney.com/blog/niji-7-prompting)  
7. Midjourney Niji 7 Is Here: 5 Ways Prompting Has Changed (and What to Do Instead), 2월 13, 2026에 액세스, [https://generativeai.pub/midjourney-niji-7-is-here-how-to-actually-prompt-it-and-why-your-old-prompts-might-fail-4d52a576d24f](https://generativeai.pub/midjourney-niji-7-is-here-how-to-actually-prompt-it-and-why-your-old-prompts-might-fail-4d52a576d24f)  
8. How to Use Omni-Reference in Midjourney V7: Beginner's Guide \- Medium, 2월 13, 2026에 액세스, [https://medium.com/@AIEntrepreneurs/how-to-use-omni-reference-in-midjourney-v7-beginners-guide-f3b686ff06df](https://medium.com/@AIEntrepreneurs/how-to-use-omni-reference-in-midjourney-v7-beginners-guide-f3b686ff06df)  
9. Omni Reference \- Midjourney, 2월 13, 2026에 액세스, [https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)  
10. How to Use Omni-Reference in Midjourney V7? Usage Guide \- CometAPI, 2월 13, 2026에 액세스, [https://www.cometapi.com/how-to-use-omni-reference-in-midjourney-v7/](https://www.cometapi.com/how-to-use-omni-reference-in-midjourney-v7/)  
11. Character Reference \- Midjourney, 2월 13, 2026에 액세스, [https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference](https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference)  
12. Simple Steps for Consistent Characters in Midjourney V7 Using Omni-Reference \- Titan XT, 2월 13, 2026에 액세스, [https://www.titanxt.io/post/simple-steps-for-consistent-characters-in-midjourney-v7-using-omnireference](https://www.titanxt.io/post/simple-steps-for-consistent-characters-in-midjourney-v7-using-omnireference)  
13. Omni-Reference \--oref \- Midjourney, 2월 13, 2026에 액세스, [https://updates.midjourney.com/omni-reference-oref/](https://updates.midjourney.com/omni-reference-oref/)  
14. Easily Use Omni Reference in Midjourney V7: A Simple Guide \- Titan XT, 2월 13, 2026에 액세스, [https://www.titanxt.io/post/easily-use-omni-reference-in-midjourney-v7-a-simple-guide](https://www.titanxt.io/post/easily-use-omni-reference-in-midjourney-v7-a-simple-guide)  
15. Sref: Style References\! \- niji・journey, 2월 13, 2026에 액세스, [https://nijijourney.com/blog/niji-features-sref-style-references](https://nijijourney.com/blog/niji-features-sref-style-references)  
16. Consistent A.I. Characters in MidJourney \- Apex Authors, 2월 13, 2026에 액세스, [https://apexauthors.com/consistent-a-i-characters-in-midjourney/](https://apexauthors.com/consistent-a-i-characters-in-midjourney/)  
17. How to use sref random \- niji・journey, 2월 13, 2026에 액세스, [https://nijijourney.com/blog/niji-guides-how-to-use-sref-random](https://nijijourney.com/blog/niji-guides-how-to-use-sref-random)  
18. How to properly use Omni Reference : r/midjourney \- Reddit, 2월 13, 2026에 액세스, [https://www.reddit.com/r/midjourney/comments/1knhw8l/how\_to\_properly\_use\_omni\_reference/](https://www.reddit.com/r/midjourney/comments/1knhw8l/how_to_properly_use_omni_reference/)  
19. Making multi-panel comic pages more coherent : r/midjourney \- Reddit, 2월 13, 2026에 액세스, [https://www.reddit.com/r/midjourney/comments/19ess7j/making\_multipanel\_comic\_pages\_more\_coherent/](https://www.reddit.com/r/midjourney/comments/19ess7j/making_multipanel_comic_pages_more_coherent/)  
20. Midjourney Prompt Generator \- A Storyboard With 7 \- PromptFolder, 2월 13, 2026에 액세스, [https://promptfolder.com/midjourney-prompt-update/exom5snx/](https://promptfolder.com/midjourney-prompt-update/exom5snx/)  
21. Advanced Vary (Region) Techniques \- niji・journey, 2월 13, 2026에 액세스, [https://nijijourney.com/blog/niji-features-advanced-vary-region-techniques](https://nijijourney.com/blog/niji-features-advanced-vary-region-techniques)  
22. Multi-Prompts & Weights \- Midjourney, 2월 13, 2026에 액세스, [https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights](https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights)  
23. Editor \- Midjourney, 2월 13, 2026에 액세스, [https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor](https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor)  
24. Vary Region \- Midjourney, 2월 13, 2026에 액세스, [https://docs.midjourney.com/hc/en-us/articles/32794723105549-Vary-Region](https://docs.midjourney.com/hc/en-us/articles/32794723105549-Vary-Region)  
25. Pan \- Midjourney, 2월 13, 2026에 액세스, [https://docs.midjourney.com/hc/en-us/articles/32570788043405-Pan](https://docs.midjourney.com/hc/en-us/articles/32570788043405-Pan)  
26. How to Pan, Zoom, and Edit Specific Areas in Midjourney V6, 2월 13, 2026에 액세스, [https://www.titanxt.io/post/how-to-pan-zoom-and-edit-specific-areas-in-midjourney-v6](https://www.titanxt.io/post/how-to-pan-zoom-and-edit-specific-areas-in-midjourney-v6)  
27. Midjourney v6 Prompting, How to use Pan, Zoom, Vary Region, New features Midjourney v6 \- YouTube, 2월 13, 2026에 액세스, [https://www.youtube.com/watch?v=2swFQXj02nA](https://www.youtube.com/watch?v=2swFQXj02nA)  
28. Upscalers \- Midjourney, 2월 13, 2026에 액세스, [https://docs.midjourney.com/hc/en-us/articles/32804058614669-Upscalers](https://docs.midjourney.com/hc/en-us/articles/32804058614669-Upscalers)  
29. Midjourney Upscale Guide 2026: How to Upscale AI Images to 4K, 8K, and Print Quality, 2월 13, 2026에 액세스, [https://www.aiarty.com/ai-upscale-image/midjourney-upscale.htm](https://www.aiarty.com/ai-upscale-image/midjourney-upscale.htm)  
30. Best AI Image Upscalers in 2026: Enhance Image Resolution with AI | WaveSpeedAI Blog, 2월 13, 2026에 액세스, [https://wavespeed.ai/blog/posts/best-ai-image-upscalers-2026](https://wavespeed.ai/blog/posts/best-ai-image-upscalers-2026)  
31. AI Video Creation: Best Generators of 2026 Ranked & Reviewed \- AI Fire, 2월 13, 2026에 액세스, [https://www.aifire.co/p/ai-video-creation-best-generators-of-2026-ranked-reviewed](https://www.aifire.co/p/ai-video-creation-best-generators-of-2026-ranked-reviewed)  
32. AI Video Generators Ranked: Who Does Anime BEST in 2026? (Grok, Sora 2, Kling, VEO 3, Midjourney) \- YouTube, 2월 13, 2026에 액세스, [https://www.youtube.com/watch?v=ctNvfJRiLHE](https://www.youtube.com/watch?v=ctNvfJRiLHE)  
33. How to make videos with niji・journey, 2월 13, 2026에 액세스, [https://nijijourney.com/blog/niji-video](https://nijijourney.com/blog/niji-video)  
34. How to Storyboard a Music Video (The Complete 2025 Guide) \- Shai Creative, 2월 13, 2026에 액세스, [https://shaicreative.ai/how-to-storyboard-a-music-video-the-complete-2025-guide/](https://shaicreative.ai/how-to-storyboard-a-music-video-the-complete-2025-guide/)  
35. How to Generate Consistent Characters Using Image-to-Video in Kling 2.5 \- Peerlist, 2월 13, 2026에 액세스, [https://peerlist.io/aristides/articles/how-to-generate-consistent-characters-using-imagetovideo-in-](https://peerlist.io/aristides/articles/how-to-generate-consistent-characters-using-imagetovideo-in-)  
36. The Great Gen AI Video Tool Shootout: Runway, Kling, Luma, Pika and MiniMax, 2월 13, 2026에 액세스, [https://hotelemarketer.com/2024/10/12/the-great-gen-ai-video-tool-shootout-runway-kling-luma-pika-and-minimax/](https://hotelemarketer.com/2024/10/12/the-great-gen-ai-video-tool-shootout-runway-kling-luma-pika-and-minimax/)  
37. Tool Comparison: Runway vs Kling vs Luma (More Info In Comments, Including Price Breakdown) : r/aivideo \- Reddit, 2월 13, 2026에 액세스, [https://www.reddit.com/r/aivideo/comments/1etttl9/tool\_comparison\_runway\_vs\_kling\_vs\_luma\_more\_info/](https://www.reddit.com/r/aivideo/comments/1etttl9/tool_comparison_runway_vs_kling_vs_luma_more_info/)