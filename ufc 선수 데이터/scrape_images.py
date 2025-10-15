
import requests
from bs4 import BeautifulSoup

base_url = "https://www.ufc.com"
rankings_url = f"{base_url}/rankings"

resp = requests.get(rankings_url)
soup = BeautifulSoup(resp.text, "html.parser")

links = [base_url + a["href"] for a in soup.select("a[href^='/athlete/']")]

image_urls = []
for link in links[:10]:  # 예시로 상위 10명만
    page = requests.get(link)
    s = BeautifulSoup(page.text, "html.parser")
    img = s.select_one(".hero-profile__image")
    if img and img.get("src"):
        image_urls.append(img["src"])

print(image_urls)
