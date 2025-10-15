# Dockerfile
# 최신 Puppeteer 이미지를 사용하여 Node.js 버전을 올립니다.
# 이 이미지는 pptruser 사용자와 /home/pptruser 작업 디렉토리를 기본으로 사용합니다.
FROM ghcr.io/puppeteer/puppeteer:latest

# --- 1. 백엔드 설정 ---
# package.json 파일을 먼저 복사하여 의존성을 설치합니다. (Docker 캐시 활용)
WORKDIR /home/pptruser/app/backend
COPY --chown=pptruser:pptruser backend/package*.json ./
RUN npm install

# --- 2. 프론트엔드 설정 ---
# package.json 파일을 먼저 복사하여 의존성을 설치합니다. (Docker 캐시 활용)
WORKDIR /home/pptruser/app/frontend
COPY --chown=pptruser:pptruser frontend/package*.json ./
RUN npm install

# --- 3. 소스 코드 복사 ---
# 의존성 설치 후 나머지 소스 코드를 복사합니다.
WORKDIR /home/pptruser/app
COPY --chown=pptruser:pptruser backend/ ./backend/
COPY --chown=pptruser:pptruser frontend/ ./frontend/

# --- 4. 프론트엔드 빌드 ---
WORKDIR /home/pptruser/app/frontend
RUN npm run build

# --- 5. 앱 실행 ---
# 다시 백엔드 디렉토리로 이동하여 서버를 시작합니다.
WORKDIR /home/pptruser/app/backend

# 앱 실행
CMD [ "node", "index.js" ]
