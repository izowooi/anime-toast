(function() {
  const ALLOWED_DOMAIN = 'ac-o.namu.la';
  const REQUIRED_TYPE = 'orig';
  
  console.clear();
  console.log('🔍 Arca.live 이미지 추출 시작...\n');
  
  // 1. 콘텐츠 영역 찾기
  const contentArea = document.querySelector('div.fr-view.article-content');
  if (!contentArea) {
    alert('❌ 게시글 콘텐츠를 찾을 수 없습니다.\n이 북마크릿은 게시글 페이지에서만 작동합니다.');
    console.error('❌ div.fr-view.article-content를 찾을 수 없음');
    return;
  }
  
  console.log('✅ 콘텐츠 영역 발견');
  
  // 2. 이미지 링크 추출
  const imageLinks = contentArea.querySelectorAll('a[href*="' + ALLOWED_DOMAIN + '"]');
  console.log(`📸 발견된 링크 수: ${imageLinks.length}개`);
  
  const urls = new Set();
  
  imageLinks.forEach((link, index) => {
    const href = link.getAttribute('href') || link.href;
    
    if (!href || !href.includes(ALLOWED_DOMAIN)) {
      console.log(`⚠️ [${index + 1}] 건너뜀: 도메인 불일치`);
      return;
    }
    
    try {
      const url = new URL(href);
      
      // type=orig 확인 및 추가
      const currentType = url.searchParams.get('type');
      if (!currentType || currentType !== REQUIRED_TYPE) {
        console.log(`🔧 [${index + 1}] type 파라미터 수정: ${currentType} → ${REQUIRED_TYPE}`);
        url.searchParams.set('type', REQUIRED_TYPE);
      } else {
        console.log(`✅ [${index + 1}] 이미 type=orig`);
      }
      
      const finalUrl = url.toString();
      urls.add(finalUrl);
      console.log(`   ${finalUrl}`);
      
    } catch (e) {
      console.error(`❌ [${index + 1}] URL 파싱 실패:`, href, e);
    }
  });
  
  const urlArray = Array.from(urls);
  
  console.log('\n' + '='.repeat(60));
  console.log(`📊 최종 결과: ${urlArray.length}개의 원본 이미지 URL`);
  console.log('='.repeat(60) + '\n');
  
  if (urlArray.length === 0) {
    alert('❌ 원본 이미지를 찾을 수 없습니다.');
    return;
  }
  
  // 3. 결과 출력 (텍스트 형태)
  const resultText = urlArray.join('\n');
  console.log(resultText);
  
  // 4. 클립보드 복사
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(resultText)
      .then(() => {
        alert(`✅ ${urlArray.length}개의 원본 이미지 URL을 클립보드에 복사했습니다!\n\n개발자 도구 콘솔(F12)에서 상세 내용을 확인하세요.`);
      })
      .catch(err => {
        console.error('❌ 클립보드 복사 실패:', err);
        // 대체: textarea 사용
        fallbackCopy(resultText, urlArray.length);
      });
  } else {
    // 구형 브라우저 대체
    fallbackCopy(resultText, urlArray.length);
  }
  
  // 대체 복사 함수
  function fallbackCopy(text, count) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
      document.execCommand('copy');
      alert(`✅ ${count}개의 원본 이미지 URL을 클립보드에 복사했습니다!\n\n개발자 도구 콘솔(F12)에서 상세 내용을 확인하세요.`);
    } catch (err) {
      alert(`❌ 클립보드 복사 실패\n\n콘솔(F12)에서 URL 목록을 확인하세요.\n\n${text.substring(0, 200)}...`);
    } finally {
      document.body.removeChild(textarea);
    }
  }
  
})();