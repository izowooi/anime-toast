# Firebase 설정 가이드

이 문서는 Supabase에서 Firebase Realtime Database로 마이그레이션 후 초기 설정 방법을 안내합니다.

## 📋 목차

1. [데이터 마이그레이션 완료 확인](#1-데이터-마이그레이션-완료-확인)
2. [Firebase Web App 설정](#2-firebase-web-app-설정)
3. [환경 변수 설정](#3-환경-변수-설정)
4. [앱 실행](#4-앱-실행)
5. [Cloudflare R2 설정 (선택 사항)](#5-cloudflare-r2-설정-선택-사항)

---

## 1. 데이터 마이그레이션 완료 확인

이미 `characters.json` 데이터가 Firebase Realtime Database로 마이그레이션되었습니다.

Firebase Console에서 확인:
1. https://console.firebase.google.com 접속
2. "anime-toast" 프로젝트 선택
3. 왼쪽 메뉴에서 "Realtime Database" 선택
4. 다음 데이터가 보이는지 확인:
   - `characters/` (8개 캐릭터)
   - `themes/` (5개 테마)
   - `story_panels/` (18개 패널)

---

## 2. Firebase Web App 설정

Firebase Console에서 Web App 설정 정보 가져오기:

### 단계별 가이드

1. **Firebase Console 접속**
   - https://console.firebase.google.com
   - "anime-toast" 프로젝트 선택

2. **프로젝트 설정 열기**
   - 왼쪽 상단의 톱니바퀴 아이콘 클릭
   - "프로젝트 설정" 선택

3. **웹 앱 찾기**
   - "일반" 탭에서 아래로 스크롤
   - "내 앱" 섹션 찾기
   - 웹 앱 (</> 아이콘) 선택

4. **Firebase SDK 구성 복사**
   - "Firebase SDK 스니펫" 선택
   - "구성" 선택
   - 다음과 같은 형태의 설정이 보임:

```javascript
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "anime-toast.firebaseapp.com",
  databaseURL: "https://anime-toast.asia-southeast1.firebasedatabase.app",
  projectId: "anime-toast",
  storageBucket: "anime-toast.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

5. **필요한 값 복사**
   - `apiKey`
   - `messagingSenderId`
   - `appId`

---

## 3. 환경 변수 설정

`.env` 파일을 열고 Firebase Console에서 복사한 값을 입력하세요:

```bash
# Firebase
REACT_APP_FIREBASE_API_KEY=<여기에 apiKey 붙여넣기>
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=<여기에 messagingSenderId 붙여넣기>
REACT_APP_FIREBASE_APP_ID=<여기에 appId 붙여넣기>

# 아래 값들은 이미 설정되어 있습니다
REACT_APP_FIREBASE_AUTH_DOMAIN=anime-toast.firebaseapp.com
REACT_APP_FIREBASE_DATABASE_URL=https://anime-toast.asia-southeast1.firebasedatabase.app
REACT_APP_FIREBASE_PROJECT_ID=anime-toast
REACT_APP_FIREBASE_STORAGE_BUCKET=anime-toast.appspot.com
```

### 예시

```bash
# 올바른 예시
REACT_APP_FIREBASE_API_KEY=AIzaSyC1234567890abcdefghijklmnopqr
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=123456789012
REACT_APP_FIREBASE_APP_ID=1:123456789012:web:abc123def456

# 잘못된 예시 (따옴표 사용하지 말것!)
REACT_APP_FIREBASE_API_KEY="AIzaSyC1234567890abcdefghijklmnopqr"  # ❌
```

---

## 4. 앱 실행

환경 변수 설정이 완료되면 앱을 실행하세요:

```bash
npm start
```

### 문제 해결

#### 에러: "Firebase 환경 변수가 설정되지 않았습니다"

콘솔에 다음과 같은 메시지가 표시됩니다:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 Firebase 설정 오류
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
다음 환경 변수가 .env 파일에 설정되지 않았습니다:
  ❌ REACT_APP_FIREBASE_API_KEY
  ❌ REACT_APP_FIREBASE_APP_ID
```

**해결 방법:**
1. `.env` 파일을 열어 누락된 값 확인
2. Firebase Console에서 값 복사
3. `.env` 파일에 올바르게 붙여넣기
4. 개발 서버 재시작 (`Ctrl+C` 후 `npm start`)

#### 에러: "Can't determine Firebase Database URL"

이 에러는 환경 변수가 로드되지 않았을 때 발생합니다.

**해결 방법:**
1. `.env` 파일이 프로젝트 루트 디렉토리에 있는지 확인
2. 파일 이름이 정확히 `.env`인지 확인 (`.env.txt` 같은 확장자 없음)
3. 개발 서버 재시작

---

## 5. Cloudflare R2 설정 (선택 사항)

이미지 업로드 기능을 사용하려면 Cloudflare R2 설정이 필요합니다.

### R2 없이 사용하기

R2를 설정하지 않아도 앱은 정상 작동합니다:
- 이미지 업로드 버튼이 비활성화됩니다
- 이미지 URL을 직접 입력할 수 있습니다
- 기존 데이터 조회/수정/삭제는 모두 가능합니다

### R2 설정하기

이미지 업로드 기능을 사용하려면:

1. **Cloudflare 계정 생성**
   - https://cloudflare.com 가입

2. **R2 버킷 생성**
   - Cloudflare Dashboard > R2
   - "Create bucket" 클릭
   - 버킷 이름 입력 (예: anime-toast-images)

3. **API 토큰 생성**
   - R2 > Overview > Manage R2 API Tokens
   - "Create API Token" 클릭
   - 권한: "Admin Read & Write"

4. **`.env` 파일에 추가**

```bash
# Cloudflare R2
REACT_APP_R2_ACCOUNT_ID=your-account-id
REACT_APP_R2_ACCESS_KEY_ID=your-access-key-id
REACT_APP_R2_SECRET_ACCESS_KEY=your-secret-access-key
REACT_APP_R2_BUCKET_NAME=anime-toast-images
REACT_APP_R2_PUBLIC_URL=https://your-bucket.r2.dev
```

5. **개발 서버 재시작**

---

## 📚 추가 정보

### Firebase Realtime Database 규칙

현재 개발 모드로 설정되어 있습니다 (모든 읽기/쓰기 허용):

```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

**프로덕션 환경에서는 반드시 보안 규칙을 강화하세요!**

### 데이터 구조

- **characters**: 캐릭터 정보 (이름, 시리즈, 이미지 URL)
- **themes**: 테마 정보 (캐릭터별 테마, 제목, 설명, 커버 이미지)
- **story_panels**: 스토리 패널 (테마별 패널, 이미지, 나레이션, 순서)

자세한 내용은 `firebase-schema.md` 참조

---

## ❓ 도움이 필요하신가요?

- Firebase 공식 문서: https://firebase.google.com/docs/database
- Cloudflare R2 문서: https://developers.cloudflare.com/r2/

---

## ✅ 설정 완료 체크리스트

- [ ] Firebase Realtime Database에 데이터 마이그레이션 확인
- [ ] Firebase Console에서 Web App 설정 확인
- [ ] `.env` 파일에 Firebase 환경 변수 입력
- [ ] `npm start`로 앱 실행 확인
- [ ] Admin 페이지에서 데이터 조회 테스트
- [ ] (선택) Cloudflare R2 설정 (이미지 업로드용)

모든 체크리스트를 완료하면 앱을 사용할 준비가 완료됩니다! 🎉
