import React, { useState } from 'react';
import { uploadImageToR2, isR2Configured } from '../../services/cloudflareR2';
import './ImageUploader.css';

function ImageUploader({ onUploadSuccess, folder = 'images', currentImageUrl = null }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(currentImageUrl);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const r2Configured = isR2Configured();

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // 이미지 파일 검증
    if (!file.type.startsWith('image/')) {
      setError('이미지 파일만 업로드 가능합니다.');
      return;
    }

    setSelectedFile(file);
    setError(null);

    // 프리뷰 생성
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreviewUrl(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('파일을 선택해주세요.');
      return;
    }

    try {
      setUploading(true);
      setError(null);

      const imageUrl = await uploadImageToR2(selectedFile, folder);

      // 업로드 성공 콜백
      if (onUploadSuccess) {
        onUploadSuccess(imageUrl);
      }

      setSelectedFile(null);
    } catch (err) {
      console.error('업로드 에러:', err);
      setError(err.message || '업로드에 실패했습니다.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="image-uploader">
      {!r2Configured && (
        <div className="warning-message" style={{
          backgroundColor: '#fff3cd',
          border: '1px solid #ffc107',
          borderRadius: '4px',
          padding: '12px',
          marginBottom: '12px',
          color: '#856404'
        }}>
          <strong>⚠️ Cloudflare R2 미설정</strong>
          <p style={{ margin: '8px 0 0 0', fontSize: '14px' }}>
            이미지 업로드 기능을 사용하려면 .env 파일에 R2 설정을 추가하세요.
            <br />
            또는 이미지 URL을 직접 입력할 수 있습니다.
          </p>
        </div>
      )}

      <div className="upload-area">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          disabled={uploading || !r2Configured}
          className="file-input"
        />

        {previewUrl && (
          <div className="preview-container">
            <img src={previewUrl} alt="Preview" className="preview-image" />
          </div>
        )}

        {selectedFile && !uploading && r2Configured && (
          <button onClick={handleUpload} className="upload-button">
            업로드
          </button>
        )}

        {uploading && <div className="uploading-indicator">업로드 중...</div>}

        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
}

export default ImageUploader;
