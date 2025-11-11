#!/usr/bin/env node

/**
 * Firebase Admin SDK를 사용하여 Web App 설정 정보 가져오기
 *
 * 사용법:
 *   node get-firebase-config.js
 */

const admin = require('firebase-admin');

// Firebase Admin SDK 초기화
const serviceAccount = require('./anime-toast-firebase-adminsdk-fbsvc-25ac8b5ae6.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://anime-toast.asia-southeast1.firebasedatabase.app'
});

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('🔥 Firebase Web App 설정 정보');
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

console.log('Admin SDK 파일에서 추출한 정보:');
console.log('');
console.log(`REACT_APP_FIREBASE_PROJECT_ID=${serviceAccount.project_id}`);
console.log(`REACT_APP_FIREBASE_AUTH_DOMAIN=${serviceAccount.project_id}.firebaseapp.com`);
console.log(`REACT_APP_FIREBASE_DATABASE_URL=https://anime-toast.asia-southeast1.firebasedatabase.app`);
console.log(`REACT_APP_FIREBASE_STORAGE_BUCKET=${serviceAccount.project_id}.appspot.com`);

console.log('\n⚠️  다음 값들은 Firebase Console에서 직접 확인해야 합니다:\n');
console.log('Firebase Console 접속 방법:');
console.log('1. https://console.firebase.google.com 접속');
console.log('2. "anime-toast" 프로젝트 선택');
console.log('3. 왼쪽 메뉴에서 "프로젝트 설정" (톱니바퀴 아이콘) 클릭');
console.log('4. "일반" 탭에서 "내 앱" 섹션으로 스크롤');
console.log('5. 웹 앱 선택 (</> 아이콘)');
console.log('6. "Firebase SDK 스니펫" > "구성" 선택');
console.log('');
console.log('다음 값들을 복사하여 .env 파일에 입력하세요:');
console.log('');
console.log('REACT_APP_FIREBASE_API_KEY=<firebaseConfig.apiKey>');
console.log('REACT_APP_FIREBASE_MESSAGING_SENDER_ID=<firebaseConfig.messagingSenderId>');
console.log('REACT_APP_FIREBASE_APP_ID=<firebaseConfig.appId>');

console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log('\n✅ 완료 후 "npm start"로 앱을 실행하세요!\n');

process.exit(0);
