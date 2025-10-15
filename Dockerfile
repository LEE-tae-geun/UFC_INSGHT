# Dockerfile
# 최신 Puppeteer 이미지를 사용하여 Node.js 버전을 올립니다.
# 이 이미지는 pptruser 사용자와 /home/pptruser 작업 디렉토리를 기본으로 사용합니다.
FROM ghcr.io/puppeteer/puppeteer:latest

# --- 1. 의존성 설치 (백엔드 & 프론트엔드) ---
# 작업 디렉토리를 설정합니다.
WORKDIR /home/pptruser/app

# backend의 package.json 파일을 먼저 복사하고 의존성을 설치합니다.
# 이렇게 하면 소스 코드가 변경되어도 매번 의존성을 새로 설치하지 않아 빌드 속도가 빨라집니다.
COPY --chown=pptruser:pptruser backend/package*.json ./backend/
RUN cd backend && npm install

# frontend의 package.json 파일을 먼저 복사하고 의존성을 설치합니다.
COPY --chown=pptruser:pptruser frontend/package*.json ./frontend/
RUN cd frontend && npm install

# --- 2. 소스 코드 복사 ---
# 의존성 설치 후 나머지 모든 소스 코드를 복사합니다.
COPY --chown=pptruser:pptruser . .

# --- 3. 프론트엔드 빌드 ---
# frontend 디렉토리로 이동하여 React 앱을 빌드합니다.
WORKDIR /home/pptruser/app/frontend
RUN npm run build

# --- 4. 앱 실행 ---
# backend 디렉토리로 이동하여 서버를 시작합니다.
WORKDIR /home/pptruser/app/backend

# 앱 실행
CMD [ "node", "index.js" ]
