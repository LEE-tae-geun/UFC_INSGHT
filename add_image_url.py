import json
import os

# Path to the rankings.json file
json_path = os.path.join("C:", os.sep, "Users", "Lee", "OneDrive", "바탕 화면", "대학", "3-2", "나노랩 심화2 (백우진)", "ufc insight", "frontend", "src", "rankings.json")

# Data provided by the user
fighter_name = "Shavkat Rakhmonov"
image_url = "https://ufc.com/images/styles/event_results_athlete_headshot/s3/2025-01/5/RAKHMONOV_SHAVKAT_12-07.png?itok=eurNu6bu"

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        rankings = json.load(f)
except FileNotFoundError:
    print(f"File not found at {json_path}")
    exit()

# Find and update the fighter's image
updated = False
for category in rankings:
    if category.get("champion", {}).get("name") == fighter_name:
        category["champion"]["image"] = image_url
        updated = True
    
    for fighter in category.get("fighters", []):
        if fighter.get("name") == fighter_name:
            fighter["image"] = image_url
            updated = True

if updated:
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(rankings, f, indent=2, ensure_ascii=False)
        print(f"Successfully updated {json_path} with {fighter_name}'s image URL.")
    except Exception as e:
        print(f"Error writing to file: {e}")
else:
    print(f"Fighter {fighter_name} not found in rankings.")