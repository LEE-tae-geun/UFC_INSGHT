# Dockerfile
# 최신 Puppeteer 이미지를 사용하여 Node.js 버전을 올립니다.
FROM ghcr.io/puppeteer/puppeteer:latest

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 기본 사용자를 pptruser로 설정합니다.
USER pptruser

# 백엔드 종속성 설치
# --chown 플래그를 사용하여 복사된 파일의 소유자를 pptruser로 지정합니다.
COPY --chown=pptruser:pptruser backend/package*.json ./backend/
WORKDIR /usr/src/app/backend
RUN npm install

# 프론트엔드 종속성 설치 및 빌드
COPY --chown=pptruser:pptruser frontend/package*.json ./frontend/
WORKDIR /usr/src/app/frontend
RUN npm install
COPY --chown=pptruser:pptruser frontend/ ./
RUN npm run build

# 다시 백엔드 디렉토리로 이동
WORKDIR /usr/src/app/backend
COPY --chown=pptruser:pptruser backend/ ./

# 앱 실행
CMD [ "node", "index.js" ]
