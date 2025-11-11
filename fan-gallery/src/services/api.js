import { ref, get, set, update, remove, push, query, orderByChild, equalTo } from 'firebase/database';
import database from './firebase';

// ============= Characters API =============

/**
 * 모든 캐릭터 조회
 */
export async function getAllCharacters() {
  try {
    const charactersRef = ref(database, 'characters');
    const snapshot = await get(charactersRef);

    if (!snapshot.exists()) {
      return [];
    }

    const data = snapshot.val();
    // Firebase 객체를 배열로 변환하고 id로 정렬
    const characters = Object.keys(data).map(key => ({
      ...data[key],
      id: key
    })).sort((a, b) => {
      // created_at으로 정렬 (없으면 id로)
      const aTime = a.created_at ? new Date(a.created_at).getTime() : 0;
      const bTime = b.created_at ? new Date(b.created_at).getTime() : 0;
      return aTime - bTime;
    });

    return characters;
  } catch (error) {
    console.error('캐릭터 조회 실패:', error);
    throw error;
  }
}

/**
 * 특정 캐릭터 조회 (테마 포함)
 */
export async function getCharacterById(id) {
  try {
    const characterRef = ref(database, `characters/${id}`);
    const snapshot = await get(characterRef);

    if (!snapshot.exists()) {
      throw new Error('캐릭터를 찾을 수 없습니다.');
    }

    const character = { ...snapshot.val(), id };

    // 관련 테마 조회
    const themesRef = ref(database, 'themes');
    const themesQuery = query(themesRef, orderByChild('character_id'), equalTo(id));
    const themesSnapshot = await get(themesQuery);

    if (themesSnapshot.exists()) {
      const themesData = themesSnapshot.val();
      const themes = await Promise.all(
        Object.keys(themesData).map(async (themeKey) => {
          const theme = { ...themesData[themeKey], id: themeKey };

          // 각 테마의 스토리 패널 조회
          const panelsRef = ref(database, 'story_panels');
          const panelsQuery = query(panelsRef, orderByChild('theme_id'), equalTo(themeKey));
          const panelsSnapshot = await get(panelsQuery);

          if (panelsSnapshot.exists()) {
            const panelsData = panelsSnapshot.val();
            theme.story_panels = Object.keys(panelsData)
              .map(panelKey => ({ ...panelsData[panelKey], id: panelKey }))
              .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0));
          } else {
            theme.story_panels = [];
          }

          return theme;
        })
      );

      character.themes = themes.sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0));
    } else {
      character.themes = [];
    }

    return character;
  } catch (error) {
    console.error('캐릭터 상세 조회 실패:', error);
    throw error;
  }
}

/**
 * 캐릭터 생성
 */
export async function createCharacter(character) {
  try {
    const charactersRef = ref(database, 'characters');
    const newCharacterRef = push(charactersRef);

    const characterData = {
      ...character,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    await set(newCharacterRef, characterData);

    return {
      ...characterData,
      id: newCharacterRef.key
    };
  } catch (error) {
    console.error('캐릭터 생성 실패:', error);
    throw error;
  }
}

/**
 * 캐릭터 수정
 */
export async function updateCharacter(id, updates) {
  try {
    const characterRef = ref(database, `characters/${id}`);

    const updateData = {
      ...updates,
      updated_at: new Date().toISOString()
    };

    await update(characterRef, updateData);

    const snapshot = await get(characterRef);
    return {
      ...snapshot.val(),
      id
    };
  } catch (error) {
    console.error('캐릭터 수정 실패:', error);
    throw error;
  }
}

/**
 * 캐릭터 삭제
 */
export async function deleteCharacter(id) {
  try {
    // 캐릭터 삭제
    const characterRef = ref(database, `characters/${id}`);
    await remove(characterRef);

    // 관련 테마 찾기 및 삭제
    const themesRef = ref(database, 'themes');
    const themesQuery = query(themesRef, orderByChild('character_id'), equalTo(id));
    const themesSnapshot = await get(themesQuery);

    if (themesSnapshot.exists()) {
      const themesData = themesSnapshot.val();
      const deletePromises = Object.keys(themesData).map(async (themeKey) => {
        // 각 테마의 스토리 패널 삭제
        const panelsRef = ref(database, 'story_panels');
        const panelsQuery = query(panelsRef, orderByChild('theme_id'), equalTo(themeKey));
        const panelsSnapshot = await get(panelsQuery);

        if (panelsSnapshot.exists()) {
          const panelsData = panelsSnapshot.val();
          await Promise.all(
            Object.keys(panelsData).map(panelKey =>
              remove(ref(database, `story_panels/${panelKey}`))
            )
          );
        }

        // 테마 삭제
        await remove(ref(database, `themes/${themeKey}`));
      });

      await Promise.all(deletePromises);
    }

    return true;
  } catch (error) {
    console.error('캐릭터 삭제 실패:', error);
    throw error;
  }
}

// ============= Themes API =============

/**
 * 특정 캐릭터의 테마 조회
 */
export async function getThemesByCharacterId(characterId) {
  try {
    const themesRef = ref(database, 'themes');
    const themesQuery = query(themesRef, orderByChild('character_id'), equalTo(characterId));
    const snapshot = await get(themesQuery);

    if (!snapshot.exists()) {
      return [];
    }

    const data = snapshot.val();
    const themes = Object.keys(data)
      .map(key => ({ ...data[key], id: key }))
      .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0));

    return themes;
  } catch (error) {
    console.error('테마 조회 실패:', error);
    throw error;
  }
}

/**
 * 특정 테마 조회 (스토리 패널 포함)
 */
export async function getThemeById(id) {
  try {
    const themeRef = ref(database, `themes/${id}`);
    const snapshot = await get(themeRef);

    if (!snapshot.exists()) {
      throw new Error('테마를 찾을 수 없습니다.');
    }

    const theme = { ...snapshot.val(), id };

    // 스토리 패널 조회
    const panelsRef = ref(database, 'story_panels');
    const panelsQuery = query(panelsRef, orderByChild('theme_id'), equalTo(id));
    const panelsSnapshot = await get(panelsQuery);

    if (panelsSnapshot.exists()) {
      const panelsData = panelsSnapshot.val();
      theme.story_panels = Object.keys(panelsData)
        .map(panelKey => ({ ...panelsData[panelKey], id: panelKey }))
        .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0));
    } else {
      theme.story_panels = [];
    }

    return theme;
  } catch (error) {
    console.error('테마 상세 조회 실패:', error);
    throw error;
  }
}

/**
 * 테마 생성
 */
export async function createTheme(theme) {
  try {
    const themesRef = ref(database, 'themes');
    const newThemeRef = push(themesRef);

    const themeData = {
      ...theme,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    await set(newThemeRef, themeData);

    return {
      ...themeData,
      id: newThemeRef.key
    };
  } catch (error) {
    console.error('테마 생성 실패:', error);
    throw error;
  }
}

/**
 * 테마 수정
 */
export async function updateTheme(id, updates) {
  try {
    const themeRef = ref(database, `themes/${id}`);

    const updateData = {
      ...updates,
      updated_at: new Date().toISOString()
    };

    await update(themeRef, updateData);

    const snapshot = await get(themeRef);
    return {
      ...snapshot.val(),
      id
    };
  } catch (error) {
    console.error('테마 수정 실패:', error);
    throw error;
  }
}

/**
 * 테마 삭제
 */
export async function deleteTheme(id) {
  try {
    // 관련 스토리 패널 삭제
    const panelsRef = ref(database, 'story_panels');
    const panelsQuery = query(panelsRef, orderByChild('theme_id'), equalTo(id));
    const panelsSnapshot = await get(panelsQuery);

    if (panelsSnapshot.exists()) {
      const panelsData = panelsSnapshot.val();
      await Promise.all(
        Object.keys(panelsData).map(panelKey =>
          remove(ref(database, `story_panels/${panelKey}`))
        )
      );
    }

    // 테마 삭제
    const themeRef = ref(database, `themes/${id}`);
    await remove(themeRef);

    return true;
  } catch (error) {
    console.error('테마 삭제 실패:', error);
    throw error;
  }
}

/**
 * 테마 순서 업데이트
 */
export async function updateThemesOrder(themes) {
  try {
    const updates = {};

    themes.forEach((theme, index) => {
      updates[`themes/${theme.id}/sort_order`] = index;
      updates[`themes/${theme.id}/updated_at`] = new Date().toISOString();
    });

    await update(ref(database), updates);

    return true;
  } catch (error) {
    console.error('테마 순서 업데이트 실패:', error);
    throw error;
  }
}

// ============= Story Panels API =============

/**
 * 특정 테마의 스토리 패널 조회
 */
export async function getStoryPanelsByThemeId(themeId) {
  try {
    const panelsRef = ref(database, 'story_panels');
    const panelsQuery = query(panelsRef, orderByChild('theme_id'), equalTo(themeId));
    const snapshot = await get(panelsQuery);

    if (!snapshot.exists()) {
      return [];
    }

    const data = snapshot.val();
    const panels = Object.keys(data)
      .map(key => ({ ...data[key], id: key }))
      .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0));

    return panels;
  } catch (error) {
    console.error('스토리 패널 조회 실패:', error);
    throw error;
  }
}

/**
 * 스토리 패널 생성
 */
export async function createStoryPanel(panel) {
  try {
    const panelsRef = ref(database, 'story_panels');
    const newPanelRef = push(panelsRef);

    const panelData = {
      ...panel,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    await set(newPanelRef, panelData);

    return {
      ...panelData,
      id: newPanelRef.key
    };
  } catch (error) {
    console.error('스토리 패널 생성 실패:', error);
    throw error;
  }
}

/**
 * 스토리 패널 수정
 */
export async function updateStoryPanel(id, updates) {
  try {
    const panelRef = ref(database, `story_panels/${id}`);

    const updateData = {
      ...updates,
      updated_at: new Date().toISOString()
    };

    await update(panelRef, updateData);

    const snapshot = await get(panelRef);
    return {
      ...snapshot.val(),
      id
    };
  } catch (error) {
    console.error('스토리 패널 수정 실패:', error);
    throw error;
  }
}

/**
 * 스토리 패널 삭제
 */
export async function deleteStoryPanel(id) {
  try {
    const panelRef = ref(database, `story_panels/${id}`);
    await remove(panelRef);

    return true;
  } catch (error) {
    console.error('스토리 패널 삭제 실패:', error);
    throw error;
  }
}

/**
 * 스토리 패널 순서 업데이트
 */
export async function updateStoryPanelsOrder(panels) {
  try {
    const updates = {};

    panels.forEach((panel, index) => {
      updates[`story_panels/${panel.id}/sort_order`] = index;
      updates[`story_panels/${panel.id}/updated_at`] = new Date().toISOString();
    });

    await update(ref(database), updates);

    return true;
  } catch (error) {
    console.error('스토리 패널 순서 업데이트 실패:', error);
    throw error;
  }
}

// ============= Export =============

export default {
  // Characters
  getAllCharacters,
  getCharacterById,
  createCharacter,
  updateCharacter,
  deleteCharacter,

  // Themes
  getThemesByCharacterId,
  getThemeById,
  createTheme,
  updateTheme,
  deleteTheme,
  updateThemesOrder,

  // Story Panels
  getStoryPanelsByThemeId,
  createStoryPanel,
  updateStoryPanel,
  deleteStoryPanel,
  updateStoryPanelsOrder,
};
