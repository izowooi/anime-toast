# Firebase Realtime Database Schema

이 문서는 Firebase Realtime Database의 데이터 구조를 설명합니다.

## 데이터 구조

Firebase Realtime Database는 NoSQL JSON 트리 구조를 사용합니다.

```json
{
  "characters": {
    "<character_id>": {
      "name": "캐릭터 이름",
      "series": "시리즈 이름",
      "image_url": "이미지 URL",
      "created_at": "2024-01-01T00:00:00.000Z",
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  },
  "themes": {
    "<theme_id>": {
      "character_id": "<character_id>",
      "theme_id": "beach",
      "title": "테마 제목",
      "description": "테마 설명",
      "cover_image_url": "커버 이미지 URL",
      "sort_order": 0,
      "created_at": "2024-01-01T00:00:00.000Z",
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  },
  "story_panels": {
    "<panel_id>": {
      "theme_id": "<theme_id>",
      "image_url": "패널 이미지 URL",
      "narration": "나레이션 텍스트",
      "sort_order": 0,
      "created_at": "2024-01-01T00:00:00.000Z",
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  }
}
```

## 테이블 설명

### characters (캐릭터)
- **id**: Firebase에서 자동 생성된 고유 키
- **name**: 캐릭터 이름 (필수)
- **series**: 소속 시리즈 (필수)
- **image_url**: 캐릭터 대표 이미지 URL (필수)
- **created_at**: 생성 시각 (ISO 8601 형식)
- **updated_at**: 수정 시각 (ISO 8601 형식)

### themes (테마)
- **id**: Firebase에서 자동 생성된 고유 키
- **character_id**: 연결된 캐릭터 ID (필수)
- **theme_id**: 테마 식별자 (예: 'beach', 'school')
- **title**: 테마 제목 (필수)
- **description**: 테마 설명
- **cover_image_url**: 테마 커버 이미지 URL (필수)
- **sort_order**: 정렬 순서 (기본값: 0)
- **created_at**: 생성 시각 (ISO 8601 형식)
- **updated_at**: 수정 시각 (ISO 8601 형식)

### story_panels (스토리 패널)
- **id**: Firebase에서 자동 생성된 고유 키
- **theme_id**: 연결된 테마 ID (필수)
- **image_url**: 패널 이미지 URL (필수)
- **narration**: 나레이션 텍스트 (필수)
- **sort_order**: 스토리 순서 (필수)
- **created_at**: 생성 시각 (ISO 8601 형식)
- **updated_at**: 수정 시각 (ISO 8601 형식)

## 관계

- **characters → themes**: 1:N 관계 (한 캐릭터는 여러 테마를 가질 수 있음)
- **themes → story_panels**: 1:N 관계 (한 테마는 여러 스토리 패널을 가질 수 있음)

## 데이터 삭제 시 주의사항

Firebase Realtime Database는 Supabase의 CASCADE 삭제를 자동으로 지원하지 않으므로,
애플리케이션 코드에서 수동으로 처리합니다:

- 캐릭터 삭제 시 → 관련된 모든 테마와 스토리 패널도 함께 삭제
- 테마 삭제 시 → 관련된 모든 스토리 패널도 함께 삭제

## 보안 규칙 (Firebase Console에서 설정)

현재는 개발 단계이므로 모든 읽기/쓰기를 허용합니다:

```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

**프로덕션 환경에서는 반드시 보안 규칙을 설정해야 합니다:**

```json
{
  "rules": {
    ".read": true,
    ".write": "auth != null"
  }
}
```

## 인덱스 설정 (Firebase Console에서 설정)

성능 최적화를 위해 다음 인덱스를 설정하세요:

### themes 인덱스
```json
{
  "rules": {
    "themes": {
      ".indexOn": ["character_id", "sort_order"]
    }
  }
}
```

### story_panels 인덱스
```json
{
  "rules": {
    "story_panels": {
      ".indexOn": ["theme_id", "sort_order"]
    }
  }
}
```

## 초기 설정

1. Firebase Console에서 새 프로젝트 생성
2. Realtime Database 활성화
3. 보안 규칙 설정 (개발 단계에서는 읽기/쓰기 모두 허용)
4. 인덱스 설정
5. `.env` 파일에 Firebase 설정 추가

## 환경 변수

`.env.example` 파일을 `.env`로 복사하고 Firebase 설정을 입력하세요:

```env
REACT_APP_FIREBASE_API_KEY=your-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
REACT_APP_FIREBASE_DATABASE_URL=https://your-project-default-rtdb.firebaseio.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
REACT_APP_FIREBASE_APP_ID=your-app-id
```

Firebase Console의 프로젝트 설정에서 이 값들을 확인할 수 있습니다.
