import { charactersBySeriesMap } from '../data/tags';

/**
 * 검색어로 캐릭터를 필터링 (영문 및 한국어 검색 지원)
 * @param {string} query - 검색어
 * @param {string} series - 특정 작품 필터 (선택사항)
 * @returns {Array} 필터링된 캐릭터 배열
 */
export const searchCharacters = (query, series = null) => {
  const lowerQuery = query.toLowerCase().trim();
  const allCharacters = [];

  // 모든 캐릭터를 평탄화
  Object.entries(charactersBySeriesMap).forEach(([key, characters]) => {
    if (series === null || key === series) {
      allCharacters.push(...characters);
    }
  });

  // 검색어가 없으면 모두 반환
  if (!lowerQuery) {
    return allCharacters;
  }

  // 캐릭터명(영문, 한글) 또는 작품명(영문, 한글)으로 검색
  return allCharacters.filter(char => {
    const nameMatch = char.name ? char.name.toLowerCase().includes(lowerQuery) : false;
    const nameKoMatch = char.name_ko ? char.name_ko.includes(query) : false; // 한글은 대소문자 구분 없음
    const seriesMatch = char.series ? char.series.toLowerCase().includes(lowerQuery) : false;
    const seriesKoMatch = char.series_ko ? char.series_ko.includes(query) : false;

    return nameMatch || nameKoMatch || seriesMatch || seriesKoMatch;
  });
};

/**
 * 작품별로 캐릭터를 그룹화
 * @param {Array} characters - 캐릭터 배열
 * @returns {Object} 작품별로 그룹화된 객체
 */
export const groupCharactersBySeriesName = (characters) => {
  return characters.reduce((acc, char) => {
    if (!acc[char.series]) {
      acc[char.series] = [];
    }
    acc[char.series].push(char);
    return acc;
  }, {});
};

/**
 * 모든 캐릭터 반환
 * @returns {Array} 모든 캐릭터 배열
 */
export const getAllCharacters = () => {
  const allCharacters = [];
  Object.values(charactersBySeriesMap).forEach(characters => {
    allCharacters.push(...characters);
  });
  return allCharacters;
};
