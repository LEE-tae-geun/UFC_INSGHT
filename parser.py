from bs4 import BeautifulSoup
import json
import os

# Correctly construct the path to the HTML file
html_path = os.path.join("C:", os.sep, "Users", "Lee", "OneDrive", "바탕 화면", "대학", "3-2", "나노랩 심화2 (백우진)", "ufc insight", "ufc 랭커 데이터", "UFC 랭킹 _ KR.UFC.com.html")
base_path = os.path.join("C:", os.sep, "Users", "Lee", "OneDrive", "바탕 화면", "대학", "3-2", "나노랩 심화2 (백우진)", "ufc insight", "ufc 랭커 데이터")
output_path = os.path.join("C:", os.sep, "Users", "Lee", "OneDrive", "바탕 화면", "대학", "3-2", "나노랩 심화2 (백우진)", "ufc insight", "rankings.json")


try:
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
except FileNotFoundError:
    print(f"Error: HTML file not found at {html_path}")
    exit()


soup = BeautifulSoup(html_content, 'html.parser')

rankings = []

for grouping in soup.find_all('div', class_='view-grouping'):
    category_name_tag = grouping.find('div', class_='view-grouping-header')
    if not category_name_tag:
        continue
    category_name = category_name_tag.text.strip()
    
    champion_div = grouping.find('div', class_='rankings--athlete--champion')
    if not champion_div:
        continue

    champion_name_tag = champion_div.find('h5')
    champion_name = champion_name_tag.text.strip() if champion_name_tag else "N/A"
    
    champion_img_tag = champion_div.find('img')
    champion_img_src = champion_img_tag['src'] if champion_img_tag else ""
    
    image_abs_path = ""
    if champion_img_src:
        image_rel_path = champion_img_src.lstrip('./')
        image_abs_path = os.path.join(base_path, image_rel_path).replace('\\', '/')
    
    category_data = {
        "category": category_name,
        "champion": {
            "name": champion_name,
            "image": image_abs_path
        },
        "fighters": []
    }
    
    table_body = grouping.find('tbody')
    if table_body:
        for row in table_body.find_all('tr'):
            rank_td = row.find('td', class_='views-field-weight-class-rank')
            name_td = row.find('td', class_='views-field-title')
            
            if rank_td and name_td:
                rank = rank_td.text.strip()
                name = name_td.text.strip()
                
                category_data["fighters"].append({
                    "rank": rank,
                    "name": name
                })
    
    rankings.append(category_data)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(rankings, f, indent=2, ensure_ascii=False)
