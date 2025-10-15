const request = require("supertest");
const app = require("./index"); // 테스트할 Express 앱
const puppeteer = require("puppeteer");

// puppeteer 모듈을 모킹합니다.
jest.mock("puppeteer", () => ({
  launch: jest.fn(),
}));

// puppeteer의 mock 함수들을 담을 변수를 선언합니다.
let mockPage;
let mockBrowser;

describe("Scraping API Endpoints", () => {
  // 각 테스트 전에 mock 객체들을 초기화하고 launch 함수가 mockBrowser를 반환하도록 설정합니다.
  beforeEach(() => {
    mockPage = {
      setUserAgent: jest.fn(),
      goto: jest.fn(),
      content: jest.fn(),
      close: jest.fn(),
    };
    mockBrowser = {
      newPage: jest.fn().mockResolvedValue(mockPage),
      close: jest.fn(),
    };
    puppeteer.launch.mockResolvedValue(mockBrowser);
    jest.clearAllMocks();
  });

  describe("GET /api/news", () => {
    it("should return scraped news data successfully", async () => {
      // 모킹할 가짜 HTML 데이터
      const mockHtml = `
        <html>
          <body>
            <article class="c-card--news">
              <a href="/news/mock-news-1">
                <img src="image1.jpg" />
                <div class="c-card__title"><a>Mock News Title 1</a></div>
                <div class="c-card__summary">Mock Summary 1</div>
                <div class="c-card__date">Jan 01, 2024</div>
              </a>
            </article>
            <article class="c-card--news">
              <a href="/news/mock-news-2">
                <img src="image2.jpg" />
                <div class="c-card__title"><a>Mock News Title 2</a></div>
                <div class="c-card__summary">Mock Summary 2</div>
                <div class="c-card__date">Jan 02, 2024</div>
              </a>
            </article>
          </body>
        </html>
      `;

      // puppeteer의 content() 함수가 가짜 HTML을 반환하도록 설정
      mockPage.content.mockResolvedValue(mockHtml);

      const response = await request(app).get("/api/news");

      expect(response.status).toBe(200);
      expect(response.body).toBeInstanceOf(Array);
      expect(response.body.length).toBe(2);
      expect(response.body[0].title).toBe("Mock News Title 1");
      expect(response.body[1].summary).toBe("Mock Summary 2");
      expect(response.body[0].link).toContain("/news/mock-news-1");
    });

    it("should return 500 if scraping fails", async () => {
      // puppeteer.launch가 에러를 발생시키도록 설정
      puppeteer.launch.mockRejectedValueOnce(new Error("Scraping failed"));

      const response = await request(app).get("/api/news");

      expect(response.status).toBe(500);
      expect(response.body).toEqual({
        error: "뉴스를 가져오는 데 실패했습니다.",
      });
    });
  });

  describe("GET /api/rankings", () => {
    it("should return scraped rankings data successfully", async () => {
      const mockHtml = `
        <html>
          <body>
            <div class="view-grouping">
              <div class="view-grouping-header">Flyweight</div>
              <table>
                <tbody>
                  <tr>
                    <td class="views-field-weight-class-rank">C</td>
                    <td class="views-field-title"><a href="/athlete/fighter-1">Fighter One</a></td>
                  </tr>
                  <tr>
                    <td class="views-field-weight-class-rank">1</td>
                    <td class="views-field-title"><a href="/athlete/fighter-2">Fighter Two</a></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </body>
        </html>
      `;

      mockPage.content.mockResolvedValue(mockHtml);

      const response = await request(app).get("/api/rankings");

      expect(response.status).toBe(200);
      expect(response.body).toBeInstanceOf(Array);
      expect(response.body.length).toBe(1);
      expect(response.body[0].category).toBe("Flyweight");
      expect(response.body[0].fighters.length).toBe(2);
      expect(response.body[0].fighters[0].name).toBe("Fighter One");
      expect(response.body[0].fighters[0].rank).toBe("Champion");
      expect(response.body[0].fighters[1].name).toBe("Fighter Two");
      expect(response.body[0].fighters[1].rank).toBe("1");
    });

    it("should return 500 if scraping fails", async () => {
      puppeteer.launch.mockRejectedValueOnce(new Error("Scraping failed"));

      const response = await request(app).get("/api/rankings");

      expect(response.status).toBe(500);
      expect(response.body).toEqual({
        error: "랭킹 정보를 가져오는 데 실패했습니다.",
      });
    });
  });

  describe("GET /api/events", () => {
    it("should return scraped events data successfully", async () => {
      const mockHtml = `
        <html>
          <body>
            <div class="c-card-event">
              <div class="c-card-event__title">UFC 300: Pereira vs Hill</div>
              <div class="c-card-event__date">Sat, Apr 13 / 7:00 PM PDT</div>
              <div class="c-card-event__main-card-time">Main Card: 10:00 PM</div>
              <div class="c-card-event__location-text">Las Vegas, Nevada</div>
              <div class="c-card-event__fighter-name">Alex Pereira</div>
              <div class="c-card-event__fighter-name">Jamahal Hill</div>
            </div>
            <div class="c-card-event">
              <div class="c-card-event__title">UFC 301: Pantoja vs Erceg</div>
              <div class="c-card-event__date">Sat, May 4 / 8:00 PM PDT</div>
              <div class="c-card-event__main-card-time">Main Card: 11:00 PM</div>
              <div class="c-card-event__location-text">Rio de Janeiro, Brazil</div>
              <div class="c-card-event__fighter-name">Alexandre Pantoja</div>
              <div class="c-card-event__fighter-name">Steve Erceg</div>
            </div>
          </body>
        </html>
      `;

      mockPage.content.mockResolvedValue(mockHtml);

      const response = await request(app).get("/api/events");

      expect(response.status).toBe(200);
      expect(response.body).toBeInstanceOf(Array);
      expect(response.body.length).toBe(2);
      expect(response.body[0].title).toBe("UFC 300: Pereira vs Hill");
      expect(response.body[0].mainEvent).toBe("Alex Pereira vs Jamahal Hill");
      expect(response.body[1].location).toBe("Rio de Janeiro, Brazil");
    });

    it("should return 500 if scraping fails", async () => {
      puppeteer.launch.mockRejectedValueOnce(new Error("Scraping failed"));

      const response = await request(app).get("/api/events");

      expect(response.status).toBe(500);
      expect(response.body).toEqual({
        error: "경기 일정을 가져오는 데 실패했습니다.",
      });
    });
  });
});
