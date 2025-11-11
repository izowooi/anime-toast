#!/usr/bin/env node

/**
 * Firebase Realtime Database 데이터 마이그레이션 스크립트
 *
 * characters.json의 데이터를 Firebase Realtime Database로 마이그레이션합니다.
 *
 * 사용법:
 *   node migrate-to-firebase.js
 */

const admin = require('firebase-admin');
const fs = require('fs');
const path = require('path');

// Firebase Admin SDK 초기화
const serviceAccount = require('./anime-toast-firebase-adminsdk-fbsvc-25ac8b5ae6.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://anime-toast-default-rtdb.asia-southeast1.firebasedatabase.app'
});

const db = admin.database();

// characters.json 파일 읽기
const charactersPath = path.join(__dirname, 'src', 'data', 'characters.json');
const charactersData = JSON.parse(fs.readFileSync(charactersPath, 'utf8'));

console.log('🚀 Firebase 데이터 마이그레이션 시작...\n');

async function migrateData() {
  try {
    let totalCharacters = 0;
    let totalThemes = 0;
    let totalPanels = 0;

    for (const character of charactersData) {
      console.log(`📝 캐릭터 추가: ${character.name} (${character.series})`);

      // 캐릭터 데이터 저장
      const characterRef = db.ref('characters').push();
      const characterId = characterRef.key;

      await characterRef.set({
        name: character.name,
        series: character.series,
        image_url: character.image,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      });

      totalCharacters++;

      // 테마가 있는 경우 처리
      if (character.themes && character.themes.length > 0) {
        for (let themeIndex = 0; themeIndex < character.themes.length; themeIndex++) {
          const theme = character.themes[themeIndex];

          console.log(`  ↳ 테마 추가: ${theme.title}`);

          // 테마 데이터 저장
          const themeRef = db.ref('themes').push();
          const themeId = themeRef.key;

          await themeRef.set({
            character_id: characterId,
            theme_id: theme.id,
            title: theme.title,
            description: theme.description || '',
            cover_image_url: theme.coverImage,
            sort_order: themeIndex,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString()
          });

          totalThemes++;

          // 스토리 패널이 있는 경우 처리
          if (theme.story && theme.story.length > 0) {
            for (let panelIndex = 0; panelIndex < theme.story.length; panelIndex++) {
              const panel = theme.story[panelIndex];

              // 스토리 패널 데이터 저장
              const panelRef = db.ref('story_panels').push();

              await panelRef.set({
                theme_id: themeId,
                image_url: panel.image,
                narration: panel.narration,
                sort_order: panelIndex,
                created_at: new Date().toISOString(),
                updated_at: new Date().toISOString()
              });

              totalPanels++;
            }

            console.log(`    ↳ 스토리 패널 ${theme.story.length}개 추가`);
          }
        }
      }

      console.log('');
    }

    console.log('✅ 마이그레이션 완료!\n');
    console.log('📊 통계:');
    console.log(`  - 캐릭터: ${totalCharacters}개`);
    console.log(`  - 테마: ${totalThemes}개`);
    console.log(`  - 스토리 패널: ${totalPanels}개`);
    console.log('');

  } catch (error) {
    console.error('❌ 마이그레이션 실패:', error);
    throw error;
  }
}

// 기존 데이터 삭제 확인
async function confirmAndMigrate() {
  // 기존 데이터 확인
  const charactersSnapshot = await db.ref('characters').once('value');
  const existingData = charactersSnapshot.exists();

  if (existingData) {
    console.log('⚠️  경고: Firebase에 이미 데이터가 있습니다!');
    console.log('계속하면 새로운 데이터가 추가됩니다. (기존 데이터는 유지됨)\n');

    // 5초 대기 후 자동 실행
    console.log('5초 후 자동으로 시작됩니다... (Ctrl+C로 취소 가능)');
    await new Promise(resolve => setTimeout(resolve, 5000));
  }

  await migrateData();

  console.log('🎉 모든 작업이 완료되었습니다!');
  process.exit(0);
}

// 실행
confirmAndMigrate().catch(error => {
  console.error('오류 발생:', error);
  process.exit(1);
});
