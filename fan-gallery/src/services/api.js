import supabase from './supabase';

// ============= Characters API =============

/**
 * 모든 캐릭터 조회
 */
export async function getAllCharacters() {
  const { data, error } = await supabase
    .from('characters')
    .select('*')
    .order('id', { ascending: true });

  if (error) {
    console.error('캐릭터 조회 실패:', error);
    throw error;
  }

  return data;
}

/**
 * 특정 캐릭터 조회 (테마 포함)
 */
export async function getCharacterById(id) {
  const { data, error } = await supabase
    .from('characters')
    .select(`
      *,
      themes (
        *,
        story_panels (*)
      )
    `)
    .eq('id', id)
    .single();

  if (error) {
    console.error('캐릭터 상세 조회 실패:', error);
    throw error;
  }

  // 테마와 스토리 패널 정렬
  if (data && data.themes) {
    data.themes = data.themes.sort((a, b) => a.sort_order - b.sort_order);
    data.themes.forEach(theme => {
      if (theme.story_panels) {
        theme.story_panels = theme.story_panels.sort((a, b) => a.sort_order - b.sort_order);
      }
    });
  }

  return data;
}

/**
 * 캐릭터 생성
 */
export async function createCharacter(character) {
  const { data, error } = await supabase
    .from('characters')
    .insert([character])
    .select()
    .single();

  if (error) {
    console.error('캐릭터 생성 실패:', error);
    throw error;
  }

  return data;
}

/**
 * 캐릭터 수정
 */
export async function updateCharacter(id, updates) {
  const { data, error } = await supabase
    .from('characters')
    .update(updates)
    .eq('id', id)
    .select()
    .single();

  if (error) {
    console.error('캐릭터 수정 실패:', error);
    throw error;
  }

  return data;
}

/**
 * 캐릭터 삭제
 */
export async function deleteCharacter(id) {
  const { error } = await supabase
    .from('characters')
    .delete()
    .eq('id', id);

  if (error) {
    console.error('캐릭터 삭제 실패:', error);
    throw error;
  }

  return true;
}

// ============= Themes API =============

/**
 * 특정 캐릭터의 테마 조회
 */
export async function getThemesByCharacterId(characterId) {
  const { data, error } = await supabase
    .from('themes')
    .select('*')
    .eq('character_id', characterId)
    .order('sort_order', { ascending: true });

  if (error) {
    console.error('테마 조회 실패:', error);
    throw error;
  }

  return data;
}

/**
 * 특정 테마 조회 (스토리 패널 포함)
 */
export async function getThemeById(id) {
  const { data, error } = await supabase
    .from('themes')
    .select(`
      *,
      story_panels (*)
    `)
    .eq('id', id)
    .single();

  if (error) {
    console.error('테마 상세 조회 실패:', error);
    throw error;
  }

  // 스토리 패널 정렬
  if (data && data.story_panels) {
    data.story_panels = data.story_panels.sort((a, b) => a.sort_order - b.sort_order);
  }

  return data;
}

/**
 * 테마 생성
 */
export async function createTheme(theme) {
  const { data, error } = await supabase
    .from('themes')
    .insert([theme])
    .select()
    .single();

  if (error) {
    console.error('테마 생성 실패:', error);
    throw error;
  }

  return data;
}

/**
 * 테마 수정
 */
export async function updateTheme(id, updates) {
  const { data, error } = await supabase
    .from('themes')
    .update(updates)
    .eq('id', id)
    .select()
    .single();

  if (error) {
    console.error('테마 수정 실패:', error);
    throw error;
  }

  return data;
}

/**
 * 테마 삭제
 */
export async function deleteTheme(id) {
  const { error } = await supabase
    .from('themes')
    .delete()
    .eq('id', id);

  if (error) {
    console.error('테마 삭제 실패:', error);
    throw error;
  }

  return true;
}

/**
 * 테마 순서 업데이트
 */
export async function updateThemesOrder(themes) {
  const updates = themes.map((theme, index) => ({
    id: theme.id,
    sort_order: index,
  }));

  const promises = updates.map(update =>
    supabase
      .from('themes')
      .update({ sort_order: update.sort_order })
      .eq('id', update.id)
  );

  const results = await Promise.all(promises);
  const errors = results.filter(r => r.error);

  if (errors.length > 0) {
    console.error('테마 순서 업데이트 실패:', errors);
    throw errors[0].error;
  }

  return true;
}

// ============= Story Panels API =============

/**
 * 특정 테마의 스토리 패널 조회
 */
export async function getStoryPanelsByThemeId(themeId) {
  const { data, error } = await supabase
    .from('story_panels')
    .select('*')
    .eq('theme_id', themeId)
    .order('sort_order', { ascending: true });

  if (error) {
    console.error('스토리 패널 조회 실패:', error);
    throw error;
  }

  return data;
}

/**
 * 스토리 패널 생성
 */
export async function createStoryPanel(panel) {
  const { data, error } = await supabase
    .from('story_panels')
    .insert([panel])
    .select()
    .single();

  if (error) {
    console.error('스토리 패널 생성 실패:', error);
    throw error;
  }

  return data;
}

/**
 * 스토리 패널 수정
 */
export async function updateStoryPanel(id, updates) {
  const { data, error } = await supabase
    .from('story_panels')
    .update(updates)
    .eq('id', id)
    .select()
    .single();

  if (error) {
    console.error('스토리 패널 수정 실패:', error);
    throw error;
  }

  return data;
}

/**
 * 스토리 패널 삭제
 */
export async function deleteStoryPanel(id) {
  const { error } = await supabase
    .from('story_panels')
    .delete()
    .eq('id', id);

  if (error) {
    console.error('스토리 패널 삭제 실패:', error);
    throw error;
  }

  return true;
}

/**
 * 스토리 패널 순서 업데이트
 */
export async function updateStoryPanelsOrder(panels) {
  const updates = panels.map((panel, index) => ({
    id: panel.id,
    sort_order: index,
  }));

  const promises = updates.map(update =>
    supabase
      .from('story_panels')
      .update({ sort_order: update.sort_order })
      .eq('id', update.id)
  );

  const results = await Promise.all(promises);
  const errors = results.filter(r => r.error);

  if (errors.length > 0) {
    console.error('스토리 패널 순서 업데이트 실패:', errors);
    throw errors[0].error;
  }

  return true;
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
