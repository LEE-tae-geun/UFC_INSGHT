# Dockerfile
# 최신 Puppeteer 이미지를 사용하여 Node.js 버전을 올립니다.
FROM ghcr.io/puppeteer/puppeteer:latest

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 기본 사용자를 pptruser로 설정합니다.
USER pptruser

# --- 백엔드 설정 ---
# 1. 백엔드 의존성 파일 복사 및 설치
COPY --chown=pptruser:pptruser backend/package*.json /usr/src/app/backend/
WORKDIR /usr/src/app/backend
RUN npm install

# --- 프론트엔드 설정 ---
# 1. 프론트엔드 의존성 파일 복사 및 설치
COPY --chown=pptruser:pptruser frontend/package*.json /usr/src/app/frontend/
WORKDIR /usr/src/app/frontend
RUN npm install
# 2. 프론트엔드 소스 코드 복사 및 빌드
COPY --chown=pptruser:pptruser frontend/ /usr/src/app/frontend/
RUN npm run build

# --- 최종 설정 ---
# 1. 백엔드 소스 코드 복사
WORKDIR /usr/src/app/backend
COPY --chown=pptruser:pptruser backend/ /usr/src/app/backend/

# 앱 실행
CMD [ "node", "index.js" ]
