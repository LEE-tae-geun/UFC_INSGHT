# Dockerfile
# Node.js 18 버전을 기반으로 하고, Puppeteer에 필요한 종속성을 포함한 이미지를 사용합니다.
FROM ghcr.io/puppeteer/puppeteer:22.10.0

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 프로젝트 전체 파일 복사
COPY . .

# 백엔드 종속성 설치
WORKDIR /usr/src/app/backend
RUN npm install

# 프론트엔드 종속성 설치 및 빌드
WORKDIR /usr/src/app/frontend
RUN npm install
RUN npm run build

# 다시 백엔드 디렉토리로 이동
WORKDIR /usr/src/app/backend

# 앱 실행
CMD [ "node", "index.js" ]

