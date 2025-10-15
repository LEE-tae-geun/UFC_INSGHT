const express = require("express");
const cors = require("cors");
const axios = require("axios");
const cheerio = require("cheerio");
const puppeteer = require("puppeteer");

const path = require("path"); // path 모듈 추가
const app = express();
const port = 5000; // 프론트엔드 프록시 설정과 일치시킵니다.

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const UFC_NEWS_URL = "https://www.ufc.com/news";
const NEWS_ITEM_SELECTOR = ".c-card--grid-card-trending"; // article 태그가 div로 변경됨
const NEWS_LIMIT = 6;
const RANK_ITEM_SELECTOR = ".view-grouping-content";
const UFC_RANKINGS_URL = "https://www.ufc.com/rankings";
const EVENTS_ITEM_SELECTOR = ".c-card-event--result"; // 예정된 이벤트 카드 선택자
const UFC_EVENTS_URL = "https://www.ufc.com/events";

// HTML을 가져와 cheerio 객체로 파싱하는 헬퍼 함수
const fetchAndParseHTML = async (url) => {
  // Puppeteer를 사용하여 실제 브라우저 환경에서 페이지를 엽니다.
  const browser = await puppeteer.launch({ headless: "new" }); // 'new' headless mode
  const page = await browser.newPage();

  // 실제 브라우저처럼 보이도록 User-Agent 설정
  await page.setUserAgent(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
  );

  await page.goto(url, { waitUntil: "networkidle2" }); // 페이지 로딩 및 네트워크 안정화 대기
  const content = await page.content(); // 렌더링된 페이지의 HTML 가져오기
  await browser.close();

  return cheerio.load(content);
};

// UFC 뉴스 스크래핑 API 엔드포인트
app.get("/api/news", async (req, res) => {
  try {
    const $ = await fetchAndParseHTML(UFC_NEWS_URL);

    const news = $(NEWS_ITEM_SELECTOR)
      .slice(0, NEWS_LIMIT)
      .map((i, el) => {
        const title = $(el)
          .find(".c-card--grid-card-trending__headline")
          .text()
          .trim();
        const href = $(el).find("a").attr("href");
        const link = href ? new URL(href, UFC_NEWS_URL).href : "";
        const image = $(el).find("img").attr("src");
        const summary = $(el).find(".c-card__summary").text().trim();
        const date = $(el)
          .find(".c-card--grid-card-trending__info-suffix")
          .text()
          .trim(); // 날짜 선택자 변경
        return { title, summary, image, date, link };
      })
      .get();

    res.json(news);
  } catch (error) {
    if (process.env.NODE_ENV !== "test") {
      console.error("Error scraping news:", error);
    }
    res.status(500).json({ error: "뉴스를 가져오는 데 실패했습니다." });
  }
});

// UFC 랭킹 스크래핑 API 엔드포인트
app.get("/api/rankings", async (req, res) => {
  try {
    const $ = await fetchAndParseHTML(UFC_RANKINGS_URL);
    const rankings = [];

    // Pound-for-Pound 랭킹 스크래핑
    const p4pGroup = $("#block-mainpagecontent .view-grouping").first();
    if (p4pGroup.length) {
      const p4pCategory = p4pGroup.find(".view-grouping-header").text().trim();
      const p4pFighters = [];
      p4pGroup.find("tbody tr").each((j, row) => {
        const rank = $(row).find(".views-field-rank").text().trim(); // P4P 랭크 선택자
        const name = $(row).find(".views-field-title a").text().trim();
        const href = $(row).find(".views-field-title a").attr("href");
        const link = href ? new URL(href, UFC_RANKINGS_URL).href : "";

        if (name) {
          p4pFighters.push({
            rank: rank || "N/A", // P4P에는 챔피언이 없으므로 그대로 표시
            name,
            link,
          });
        }
      });
      if (p4pCategory && p4pFighters.length > 0) {
        rankings.push({ category: p4pCategory, fighters: p4pFighters });
      }
    }

    $(".view-grouping").each((i, group) => {
      const category = $(group).find(".view-grouping-header").text().trim();
      const fighters = [];

      $(group)
        .find("tbody tr")
        .each((j, row) => {
          const rank = $(row)
            .find(".views-field-weight-class-rank")
            .text()
            .trim();
          const name = $(row).find(".views-field-title a").text().trim();
          const href = $(row).find(".views-field-title a").attr("href");
          const link = href ? new URL(href, UFC_RANKINGS_URL).href : "";

          if (name) {
            fighters.push({
              rank: rank === "C" || !rank ? "Champion" : rank,
              name,
              link,
            });
          }
        });

      // 이미 추가된 P4P 랭킹은 건너뜁니다.
      if (
        category &&
        !category.toLowerCase().includes("pound-for-pound") &&
        fighters.length > 0
      ) {
        rankings.push({ category, fighters });
      }
    });
    res.json(rankings);
  } catch (error) {
    if (process.env.NODE_ENV !== "test") {
      console.error("Error scraping rankings:", error);
    }
    res.status(500).json({ error: "랭킹 정보를 가져오는 데 실패했습니다." });
  }
});

// UFC 경기 일정 스크래핑 API 엔드포인트
app.get("/api/events", async (req, res) => {
  try {
    const $ = await fetchAndParseHTML(UFC_EVENTS_URL);
    const scrapedEvents = $(EVENTS_ITEM_SELECTOR);
    const events = [];

    // 예정된 이벤트 카드만 선택
    scrapedEvents.each((i, el) => {
      const href = $(el).find(".c-card-event--result__headline a").attr("href");
      const link = href ? new URL(href, UFC_EVENTS_URL).href : "";
      const title = $(el).find(".c-card-event--result__headline").text().trim();
      const dateElement = $(el).find(".c-card-event--result__date");
      const date =
        dateElement.attr("data-prelims-card") ||
        dateElement.attr("data-main-card") ||
        "";
      const mainCardTime = dateElement.attr("data-main-card") || "";
      const location = $(el).find(".country").text().trim();
      // 티켓 구매 링크를 가져옵니다. "Buy Tickets" 텍스트를 포함하는 링크를 찾습니다.
      const ticketLinkHref = $(el).find(".e-button--white").attr("href");
      const ticketLink = ticketLinkHref
        ? new URL(ticketLinkHref, UFC_EVENTS_URL).href
        : "";

      const fighters = [];
      $(el)
        .find(".c-card-event--result__headline")
        .each((i, fighterEl) => {
          fighters.push($(fighterEl).text().trim());
        });

      const mainEvent =
        fighters.length === 2 ? `${fighters[0]} vs ${fighters[1]}` : "TBD";

      if (title) {
        events.push({
          title,
          date,
          mainCardTime,
          location,
          mainEvent,
          link,
          ticketLink,
        });
      }
    });

    res.json(events);
  } catch (error) {
    if (process.env.NODE_ENV !== "test") {
      console.error("Error scraping events:", error);
    }
    res.status(500).json({ error: "경기 일정을 가져오는 데 실패했습니다." });
  }
});

// ########### 배포를 위한 설정 ###########
// React 앱의 빌드된 정적 파일들을 제공합니다.
app.use(express.static(path.join(__dirname, "../frontend/build")));

// 모든 경로에 대한 요청을 React 앱으로 전달하여 클라이언트 사이드 라우팅이 동작하게 합니다.
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "../frontend/build", "index.html"));
});
// ######################################

// `node index.js`로 직접 실행될 때만 서버를 시작합니다.
// 테스트 환경에서는 서버가 자동으로 시작되지 않습니다.
if (require.main === module) {
  app.listen(port, () => {
    console.log(`서버가 http://localhost:${port} 에서 실행 중입니다.`);
  });
}

module.exports = app; // 테스트를 위해 app을 export 합니다.
