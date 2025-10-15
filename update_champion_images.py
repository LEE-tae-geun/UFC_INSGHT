import json
import os

# Path to the rankings.json file
json_path = os.path.join("C:", os.sep, "Users", "Lee", "OneDrive", "바탕 화면", "대학", "3-2", "나노랩 심화2 (백우진)", "ufc insight", "frontend", "src", "rankings.json")

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        rankings = json.load(f)
except FileNotFoundError:
    print(f"File not found at {json_path}")
    exit()

# First, create a map of champion names to their image URLs
champion_images = {}
for category in rankings:
    champion_name = category.get("champion", {}).get("name")
    champion_image = category.get("champion", {}).get("image")
    if champion_name and champion_image:
        champion_images[champion_name] = champion_image

# Now, iterate through the whole structure and add the image URL to any fighter who is a champion
for category in rankings:
    # Update champion's own entry first (though it should already be correct)
    champion_name = category.get("champion", {}).get("name")
    if champion_name in champion_images:
        category["champion"]["image"] = champion_images[champion_name]

    # Update the fighters list
    for fighter in category.get("fighters", []):
        if fighter["name"] in champion_images:
            fighter["image"] = champion_images[fighter["name"]]

try:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rankings, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {json_path} to ensure all champions have images.")
except Exception as e:
    print(f"Error writing to file: {e}")
