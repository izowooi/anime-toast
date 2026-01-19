// 페이지에 플로팅 다운로드 버튼 추가
(function() {
  console.log('🔌 Arca Image Downloader 로드됨');

  // 플로팅 버튼 생성
  const btn = document.createElement('button');
  btn.id = 'arca-download-btn';
  btn.innerHTML = '📥 이미지 다운로드';
  btn.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 99999;
    padding: 15px 25px;
    font-size: 16px;
    font-weight: bold;
    color: white;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 50px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    transition: all 0.3s ease;
  `;

  btn.onmouseenter = () => {
    btn.style.transform = 'scale(1.05)';
    btn.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
  };
  btn.onmouseleave = () => {
    btn.style.transform = 'scale(1)';
    btn.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
  };

  btn.onclick = async function() {
    console.log('🖱️ 다운로드 버튼 클릭됨');

    const postId = window.location.pathname.split('/').pop();
    console.log('📝 게시글 ID:', postId);

    const content = document.querySelector('div.fr-view.article-content');

    if (!content) {
      console.error('❌ 게시글 콘텐츠를 찾을 수 없습니다.');
      alert('❌ 게시글 콘텐츠를 찾을 수 없습니다.');
      return;
    }

    const links = content.querySelectorAll('a[href*="ac-o.namu.la"]');
    console.log('🔍 찾은 링크 수:', links.length);

    const urls = [];

    links.forEach(link => {
      const href = link.getAttribute('href');
      if (href && href.includes('ac-o.namu.la')) {
        try {
          const url = new URL(href);
          url.searchParams.set('type', 'orig');
          urls.push(url.toString());
        } catch (e) {
          console.error('URL 파싱 오류:', e);
        }
      }
    });

    console.log('📷 다운로드할 이미지 수:', urls.length);

    if (urls.length === 0) {
      alert('❌ 이미지를 찾을 수 없습니다.');
      return;
    }

    btn.innerHTML = `⏳ 다운로드 중... (0/${urls.length})`;
    btn.style.pointerEvents = 'none';
    btn.style.opacity = '0.7';

    // 순차적으로 다운로드
    for (let i = 0; i < urls.length; i++) {
      const url = urls[i];
      const filename = `nai_images/${postId}/${String(i + 1).padStart(3, '0')}.png`;

      try {
        console.log(`⏳ [${i + 1}/${urls.length}] fetch 시작: ${url}`);

        // fetch로 이미지 가져오기
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const blob = await response.blob();

        // blob을 data URL로 변환
        const dataUrl = await new Promise((resolve) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result);
          reader.readAsDataURL(blob);
        });

        console.log(`📤 [${i + 1}/${urls.length}] background로 전송`);

        // background script로 전송
        await new Promise((resolve, reject) => {
          chrome.runtime.sendMessage({
            action: 'downloadSingleImage',
            dataUrl: dataUrl,
            filename: filename
          }, (response) => {
            if (response && response.success) {
              resolve();
            } else {
              reject(new Error(response?.error || '다운로드 실패'));
            }
          });
        });

        console.log(`✅ [${i + 1}/${urls.length}] 완료: ${filename}`);
        btn.innerHTML = `⏳ 다운로드 중... (${i + 1}/${urls.length})`;

      } catch (error) {
        console.error(`❌ [${i + 1}/${urls.length}] 실패:`, error);
      }
    }

    btn.innerHTML = '✅ 완료!';
    setTimeout(() => {
      btn.innerHTML = '📥 이미지 다운로드';
      btn.style.pointerEvents = 'auto';
      btn.style.opacity = '1';
    }, 2000);

    console.log(`\n✅ 모든 다운로드 완료!\n📁 위치: Downloads/nai_images/${postId}/`);
  };

  document.body.appendChild(btn);
  console.log('✅ 다운로드 버튼 추가 완료 (우측 하단)');
})();
