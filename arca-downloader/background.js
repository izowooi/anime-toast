// 다운로드 처리
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'downloadSingleImage') {
    downloadSingleImage(request.dataUrl, request.filename)
      .then(() => sendResponse({ success: true }))
      .catch((error) => sendResponse({ success: false, error: error.message }));
    return true; // 비동기 응답을 위해 필요
  }
});

// 단일 이미지 다운로드
function downloadSingleImage(dataUrl, filename) {
  return new Promise((resolve, reject) => {
    chrome.downloads.download({
      url: dataUrl,
      filename: filename,
      saveAs: false,
      conflictAction: 'uniquify'
    }, (downloadId) => {
      if (chrome.runtime.lastError) {
        console.error('❌ 다운로드 시작 실패:', chrome.runtime.lastError);
        reject(chrome.runtime.lastError);
        return;
      }

      console.log(`📥 다운로드 시작: ${filename} (ID: ${downloadId})`);

      // 다운로드 상태 감시
      function onChanged(delta) {
        if (delta.id !== downloadId) return;

        if (delta.state) {
          if (delta.state.current === 'complete') {
            chrome.downloads.onChanged.removeListener(onChanged);
            console.log(`✅ 다운로드 완료: ${filename}`);
            resolve(downloadId);
          } else if (delta.state.current === 'interrupted') {
            chrome.downloads.onChanged.removeListener(onChanged);
            console.error(`❌ 다운로드 중단: ${filename}`);
            reject(new Error('다운로드 중단됨'));
          }
        }
      }

      chrome.downloads.onChanged.addListener(onChanged);
    });
  });
}
