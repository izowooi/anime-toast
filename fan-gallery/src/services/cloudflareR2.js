import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

// Cloudflare R2 클라이언트 초기화
const r2Client = new S3Client({
  region: 'auto',
  endpoint: `https://${process.env.REACT_APP_R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: process.env.REACT_APP_R2_ACCESS_KEY_ID || '',
    secretAccessKey: process.env.REACT_APP_R2_SECRET_ACCESS_KEY || '',
  },
});

const bucketName = process.env.REACT_APP_R2_BUCKET_NAME || '';
const publicUrl = process.env.REACT_APP_R2_PUBLIC_URL || '';

/**
 * R2에 이미지 업로드
 * @param {File} file - 업로드할 파일
 * @param {string} folder - 저장할 폴더 (예: 'characters/aura')
 * @returns {Promise<string>} - 업로드된 이미지의 공개 URL
 */
export async function uploadImageToR2(file, folder = 'images') {
  // R2 설정 확인
  if (!isR2Configured()) {
    const missingVars = [];
    if (!process.env.REACT_APP_R2_ACCOUNT_ID) missingVars.push('REACT_APP_R2_ACCOUNT_ID');
    if (!process.env.REACT_APP_R2_ACCESS_KEY_ID) missingVars.push('REACT_APP_R2_ACCESS_KEY_ID');
    if (!process.env.REACT_APP_R2_SECRET_ACCESS_KEY) missingVars.push('REACT_APP_R2_SECRET_ACCESS_KEY');
    if (!process.env.REACT_APP_R2_BUCKET_NAME) missingVars.push('REACT_APP_R2_BUCKET_NAME');
    if (!process.env.REACT_APP_R2_PUBLIC_URL) missingVars.push('REACT_APP_R2_PUBLIC_URL');

    throw new Error(
      `Cloudflare R2가 설정되지 않았습니다.\n\n` +
      `다음 환경 변수를 .env 파일에 추가하세요:\n` +
      missingVars.map(v => `  - ${v}`).join('\n') +
      `\n\n이미지 업로드 기능을 사용하지 않으려면 URL을 직접 입력하세요.`
    );
  }

  try {
    // 파일 이름 생성 (타임스탬프 + 랜덤 문자열)
    const timestamp = Date.now();
    const randomString = Math.random().toString(36).substring(2, 8);
    const ext = file.name.split('.').pop();
    const fileName = `${timestamp}-${randomString}.${ext}`;
    const key = `${folder}/${fileName}`;

    // S3 업로드 커맨드
    const command = new PutObjectCommand({
      Bucket: bucketName,
      Key: key,
      Body: file,
      ContentType: file.type,
    });

    // 업로드 실행
    await r2Client.send(command);

    // 공개 URL 반환
    const imageUrl = `${publicUrl}/${key}`;
    return imageUrl;
  } catch (error) {
    console.error('R2 업로드 실패:', error);
    throw new Error(`이미지 업로드 실패: ${error.message}`);
  }
}

/**
 * 여러 이미지를 한 번에 업로드
 * @param {File[]} files - 업로드할 파일 배열
 * @param {string} folder - 저장할 폴더
 * @returns {Promise<string[]>} - 업로드된 이미지 URL 배열
 */
export async function uploadMultipleImagesToR2(files, folder = 'images') {
  try {
    const uploadPromises = files.map((file) => uploadImageToR2(file, folder));
    const urls = await Promise.all(uploadPromises);
    return urls;
  } catch (error) {
    console.error('다중 이미지 업로드 실패:', error);
    throw error;
  }
}

/**
 * R2 설정 확인
 * @returns {boolean} - 설정이 올바른지 여부
 */
export function isR2Configured() {
  return !!(
    process.env.REACT_APP_R2_ACCOUNT_ID &&
    process.env.REACT_APP_R2_ACCESS_KEY_ID &&
    process.env.REACT_APP_R2_SECRET_ACCESS_KEY &&
    process.env.REACT_APP_R2_BUCKET_NAME &&
    process.env.REACT_APP_R2_PUBLIC_URL
  );
}

const r2Service = {
  uploadImageToR2,
  uploadMultipleImagesToR2,
  isR2Configured,
};

export default r2Service;
