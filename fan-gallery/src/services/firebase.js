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

// 환경 변수 검증
if (!firebaseConfig.apiKey || !firebaseConfig.databaseURL) {
  console.error('Firebase 환경 변수가 설정되지 않았습니다.');
  console.error('REACT_APP_FIREBASE_API_KEY:', firebaseConfig.apiKey ? '설정됨' : '없음');
  console.error('REACT_APP_FIREBASE_DATABASE_URL:', firebaseConfig.databaseURL || '없음');
}

// Firebase 초기화
const app = initializeApp(firebaseConfig);
export const database = getDatabase(app);

export default database;
