
import requests
from bs4 import BeautifulSoup
import json
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_url = "https://www.ufc.com"

def get_image_url(fighter_name):
    search_url = f"{base_url}/search?query={fighter_name.replace(' ', '%20')}"
    try:
        resp = requests.get(search_url, allow_redirects=True)
        if "/athlete/" in resp.url:
            soup = BeautifulSoup(resp.text, "html.parser")
            img = soup.select_one(".hero-profile__image")
            if img and img.get("src"):
                return img["src"]
    except Exception as e:
        print(f"Error getting image for {fighter_name}: {e}")
    return None

with open('rankings.json', 'r', encoding='utf-8') as f:
    rankings_data = json.load(f)

for category in rankings_data:
    if category['category'] == '페더급':
        # Update champion
        champion_name = category['champion']['name']
        print(f"Getting image for champion: {champion_name}")
        image_url = get_image_url(champion_name)
        if image_url:
            category['champion']['image'] = image_url
        time.sleep(1)

        # Update fighters
        if 'fighters' in category:
            for fighter in category['fighters']:
                fighter_name = fighter['name']
                print(f"Getting image for fighter: {fighter_name}")
                image_url = get_image_url(fighter_name)
                if image_url:
                    fighter['image'] = image_url
                time.sleep(1)
        break # Exit after processing featherweight category

with open('rankings.json', 'w', encoding='utf-8') as f:
    json.dump(rankings_data, f, indent=2, ensure_ascii=False)

print("Finished updating Featherweight images.")
