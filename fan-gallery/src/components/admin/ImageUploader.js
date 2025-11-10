import React, { useState } from 'react';
import { uploadImageToR2 } from '../../services/cloudflareR2';
import './ImageUploader.css';

function ImageUploader({ onUploadSuccess, folder = 'images', currentImageUrl = null }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(currentImageUrl);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

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
      <div className="upload-area">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          disabled={uploading}
          className="file-input"
        />

        {previewUrl && (
          <div className="preview-container">
            <img src={previewUrl} alt="Preview" className="preview-image" />
          </div>
        )}

        {selectedFile && !uploading && (
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
