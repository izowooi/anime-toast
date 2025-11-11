import { initializeApp } from 'firebase/app';
import { getDatabase } from 'firebase/database';

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  databaseURL: process.env.REACT_APP_FIREBASE_DATABASE_URL,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID
};

// 환경 변수 검증 (필수 값들)
const requiredFields = {
  'REACT_APP_FIREBASE_API_KEY': firebaseConfig.apiKey,
  'REACT_APP_FIREBASE_DATABASE_URL': firebaseConfig.databaseURL,
  'REACT_APP_FIREBASE_PROJECT_ID': firebaseConfig.projectId,
  'REACT_APP_FIREBASE_APP_ID': firebaseConfig.appId
};

const missingFields = Object.entries(requiredFields)
  .filter(([, value]) => !value)
  .map(([key]) => key);

if (missingFields.length > 0) {
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.error('🚨 Firebase 설정 오류');
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.error('다음 환경 변수가 .env 파일에 설정되지 않았습니다:');
  missingFields.forEach(field => console.error(`  ❌ ${field}`));
  console.error('\n해결 방법:');
  console.error('1. Firebase Console (https://console.firebase.google.com) 접속');
  console.error('2. 프로젝트 설정 > 일반 탭 > 내 앱 > 웹 앱 선택');
  console.error('3. Firebase SDK 구성 복사');
  console.error('4. .env 파일에 값 입력');
  console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  throw new Error('Firebase 환경 변수가 설정되지 않았습니다. 콘솔을 확인하세요.');
}

// Firebase 초기화
const app = initializeApp(firebaseConfig);
export const database = getDatabase(app);

export default database;
