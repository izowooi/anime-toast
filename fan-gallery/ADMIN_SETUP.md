# 관리자 페이지 설정 가이드

## 🎯 완료된 작업

관리자 페이지 MVP 버전이 구현되었습니다!

### 구현된 기능
- ✅ Supabase DB 연동
- ✅ Cloudflare R2 이미지 업로드
- ✅ 캐릭터 CRUD (생성, 읽기, 삭제)
- ✅ 테마 CRUD
- ✅ 스토리 패널 CRUD
- ✅ 이미지 업로더 컴포넌트
- ✅ 통합 관리자 대시보드

## 📋 설정 단계

### 1. Supabase 설정

#### 1.1 데이터베이스 테이블 생성

1. Supabase 대시보드 접속: https://supabase.com/dashboard
2. 프로젝트 선택
3. 왼쪽 메뉴에서 **SQL Editor** 클릭
4. **New query** 버튼 클릭
5. `supabase-schema.sql` 파일의 내용을 복사해서 붙여넣기
6. **Run** 버튼 클릭하여 실행

#### 1.2 API 키 확인

1. Supabase 대시보드에서 **Settings** > **API** 이동
2. 다음 정보 복사:
   - **Project URL**
   - **anon / public key**

### 2. Cloudflare R2 설정

#### 2.1 R2 버킷 생성

1. Cloudflare 대시보드 접속
2. **R2** 메뉴 선택
3. **Create bucket** 클릭
4. 버킷 이름 입력 (예: `fan-gallery-images`)
5. 생성 완료

#### 2.2 R2 API 토큰 생성

1. R2 페이지에서 **Manage R2 API Tokens** 클릭
2. **Create API Token** 클릭
3. 권한 설정:
   - Object Read & Write
   - 특정 버킷만 선택 (위에서 만든 버킷)
4. **Create API Token** 클릭
5. 다음 정보 저장:
   - Access Key ID
   - Secret Access Key
   - Account ID

#### 2.3 Public Access 설정

1. 버킷 설정에서 **Settings** 탭
2. **Public Access** 섹션에서 **Allow Access** 활성화
3. Custom Domain 설정 또는 R2.dev 도메인 사용

### 3. 환경 변수 설정

프로젝트 루트에 `.env` 파일 생성:

```bash
# .env.example 파일을 복사하여 .env 생성
cp .env.example .env
```

`.env` 파일 편집:

```env
# Supabase
REACT_APP_SUPABASE_URL=https://your-project.supabase.co
REACT_APP_SUPABASE_ANON_KEY=your-anon-key-here

# Cloudflare R2
REACT_APP_R2_ACCOUNT_ID=your-account-id
REACT_APP_R2_ACCESS_KEY_ID=your-access-key-id
REACT_APP_R2_SECRET_ACCESS_KEY=your-secret-access-key
REACT_APP_R2_BUCKET_NAME=fan-gallery-images
REACT_APP_R2_PUBLIC_URL=https://your-bucket.r2.dev
```

**주의**: `.env` 파일은 절대 Git에 커밋하지 마세요!

### 4. 애플리케이션 실행

```bash
# 개발 서버 시작
npm start
```

브라우저에서 다음 URL 접속:
- 갤러리: http://localhost:3000
- 관리자 페이지: http://localhost:3000/admin

## 🎨 관리자 페이지 사용 방법

### 캐릭터 추가

1. `/admin` 페이지 접속
2. **캐릭터 관리** 섹션에서:
   - 캐릭터 이름 입력
   - 시리즈 이름 입력
   - 이미지 파일 선택 후 업로드 (또는 URL 직접 입력)
   - **캐릭터 추가** 버튼 클릭

### 테마 추가

1. 캐릭터 목록에서 캐릭터 클릭
2. **테마** 섹션이 나타남
3. 테마 정보 입력:
   - 테마 ID (예: `beach`, `school`)
   - 제목
   - 설명
   - 순서 (0부터 시작)
   - 커버 이미지 업로드
4. **테마 추가** 버튼 클릭

### 스토리 패널 추가

1. 테마 목록에서 테마 클릭
2. **스토리 패널** 섹션이 나타남
3. 패널 정보 입력:
   - 이미지 업로드
   - 나레이션 텍스트 입력
   - 순서 (0부터 시작, 스토리 순서대로)
4. **패널 추가** 버튼 클릭

## 🔄 기존 데이터 마이그레이션

`characters.json` 파일의 데이터를 DB로 옮기려면:

### 수동 방법
1. `/admin` 페이지에서 각 캐릭터를 하나씩 입력
2. aura 캐릭터의 경우 5개 테마와 스토리 패널 모두 입력

### 향후 자동화 스크립트
- 추후 마이그레이션 스크립트를 작성하여 자동화 가능

## 🐛 문제 해결

### 이미지 업로드 실패
- R2 API 키가 올바른지 확인
- 버킷 이름이 정확한지 확인
- Public Access가 활성화되어 있는지 확인

### 데이터베이스 연결 실패
- Supabase URL과 API 키가 올바른지 확인
- `.env` 파일이 올바른 위치에 있는지 확인
- 개발 서버를 재시작

### 테이블을 찾을 수 없음
- Supabase SQL Editor에서 `supabase-schema.sql` 스크립트를 실행했는지 확인

## 🚀 다음 단계

MVP 버전이므로 추후 개선 가능:

1. **드래그앤드롭 순서 변경**: 현재는 수동으로 순서 입력
2. **이미지 편집**: 크롭, 리사이즈 기능
3. **배치 업로드**: 여러 이미지 한 번에 업로드
4. **프리뷰**: 실시간으로 결과 미리보기
5. **검색/필터**: 캐릭터/테마 검색
6. **인증**: 구글 로그인 연동
7. **백업/복원**: JSON으로 export/import

## 📝 참고사항

- 현재는 인증 없이 누구나 `/admin` 페이지 접근 가능
- 순서(sort_order)는 0부터 시작하는 정수
- 이미지는 R2에 영구 저장되므로 삭제 시 수동으로 제거 필요
- 테마나 캐릭터 삭제 시 관련 데이터도 자동 삭제 (CASCADE)

## 💡 팁

- 이미지 파일명은 자동으로 타임스탬프 + 랜덤 문자열로 생성
- webp 형식 권장 (용량 절약)
- 나레이션은 간결하게 2-3문장 권장
- 테마 순서는 중요한 테마일수록 낮은 숫자 사용

---

설정 중 문제가 있으면 `.env` 파일과 Supabase 테이블을 먼저 확인하세요!
