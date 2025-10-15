
import requests
from bs4 import BeautifulSoup
import json

base_url = "https://www.ufc.com"
rankings_url = f"{base_url}/rankings"

resp = requests.get(rankings_url)
soup = BeautifulSoup(resp.text, "html.parser")

links = []
for a in soup.select("a[href^='/athlete/']"):
    link = base_url + a["href"]
    if link not in links:
        links.append(link)

image_urls = []
fighter_names = []
for link in links[:15]:  # p4p 15명
    page = requests.get(link)
    s = BeautifulSoup(page.text, "html.parser")
    
    # Get fighter name
    name_element = s.select_one(".hero-profile__name")
    name = name_element.text.strip() if name_element else "Unknown"
    fighter_names.append(name)

    # Get image URL
    img = s.select_one(".hero-profile__image")
    if img and img.get("src"):
        image_urls.append(img["src"])
    else:
        image_urls.append(None)

# Now I have a list of names and a list of image_urls
# I will create a dictionary to map names to image_urls
fighter_images = dict(zip(fighter_names, image_urls))

# Read the rankings.json file
with open('rankings.json', 'r', encoding='utf-8') as f:
    rankings_data = json.load(f)

# Update the image URLs
for category in rankings_data:
    if category['category'] == "Men's Pound-for-Pound Top Rank":
        # Update champion image
        champion_name = category['champion']['name']
        if champion_name in fighter_images:
            category['champion']['image'] = fighter_images[champion_name]

        # Update fighters' images
        for fighter in category['fighters']:
            fighter_name = fighter['name']
            if fighter_name in fighter_images:
                fighter['image'] = fighter_images[fighter_name]

# Write the updated data back to the file
with open('rankings.json', 'w', encoding='utf-8') as f:
    json.dump(rankings_data, f, indent=2, ensure_ascii=False)

print("rankings.json has been updated with image URLs.")
