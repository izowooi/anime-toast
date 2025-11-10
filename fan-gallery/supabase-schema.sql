-- Fan Gallery Database Schema
-- Supabase SQL Editor에서 실행하세요

-- 1. Characters 테이블
CREATE TABLE IF NOT EXISTS characters (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  series VARCHAR(200) NOT NULL,
  image_url TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Characters 테이블 인덱스
CREATE INDEX IF NOT EXISTS idx_characters_name ON characters(name);

-- 2. Themes 테이블
CREATE TABLE IF NOT EXISTS themes (
  id SERIAL PRIMARY KEY,
  character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  theme_id VARCHAR(50) NOT NULL,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  cover_image_url TEXT NOT NULL,
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Themes 테이블 인덱스
CREATE INDEX IF NOT EXISTS idx_themes_character_id ON themes(character_id);
CREATE INDEX IF NOT EXISTS idx_themes_sort_order ON themes(sort_order);

-- 3. Story Panels 테이블
CREATE TABLE IF NOT EXISTS story_panels (
  id SERIAL PRIMARY KEY,
  theme_id INTEGER NOT NULL REFERENCES themes(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  narration TEXT NOT NULL,
  sort_order INTEGER NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Story Panels 테이블 인덱스
CREATE INDEX IF NOT EXISTS idx_story_panels_theme_id ON story_panels(theme_id);
CREATE INDEX IF NOT EXISTS idx_story_panels_sort_order ON story_panels(sort_order);

-- 4. Admins 테이블 (추후 인증용)
CREATE TABLE IF NOT EXISTS admins (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  google_id VARCHAR(255) UNIQUE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Admins 테이블 인덱스
CREATE INDEX IF NOT EXISTS idx_admins_email ON admins(email);

-- 5. Updated_at 자동 업데이트 함수
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Characters 테이블 트리거
CREATE TRIGGER update_characters_updated_at
  BEFORE UPDATE ON characters
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Themes 테이블 트리거
CREATE TRIGGER update_themes_updated_at
  BEFORE UPDATE ON themes
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Story Panels 테이블 트리거
CREATE TRIGGER update_story_panels_updated_at
  BEFORE UPDATE ON story_panels
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- 6. Row Level Security (RLS) 설정
-- 현재는 비활성화 (누구나 읽기/쓰기 가능)
-- 추후 인증 구현 시 활성화

-- ALTER TABLE characters ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE themes ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE story_panels ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE admins ENABLE ROW LEVEL SECURITY;

-- 읽기는 모두 허용
-- CREATE POLICY "Anyone can read characters" ON characters FOR SELECT USING (true);
-- CREATE POLICY "Anyone can read themes" ON themes FOR SELECT USING (true);
-- CREATE POLICY "Anyone can read story_panels" ON story_panels FOR SELECT USING (true);

-- 쓰기는 관리자만 허용 (추후 구현)
-- CREATE POLICY "Only admins can insert characters" ON characters FOR INSERT WITH CHECK (auth.uid() IN (SELECT id FROM admins));
-- CREATE POLICY "Only admins can update characters" ON characters FOR UPDATE USING (auth.uid() IN (SELECT id FROM admins));
-- CREATE POLICY "Only admins can delete characters" ON characters FOR DELETE USING (auth.uid() IN (SELECT id FROM admins));

-- 7. 샘플 관리자 추가 (선택사항)
-- INSERT INTO admins (email) VALUES ('your-email@example.com');

-- 완료!
-- 이제 React 앱에서 Supabase 클라이언트를 통해 데이터를 읽고 쓸 수 있습니다.
