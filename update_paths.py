import json
import os

# Path to the original rankings.json
input_path = os.path.join("C:", os.sep, "Users", "Lee", "OneDrive", "바탕 화면", "대학", "3-2", "나노랩 심화2 (백우진)", "ufc insight", "rankings.json")
# Path to the new rankings.json in the frontend/src directory
output_path = os.path.join("C:", os.sep, "Users", "Lee", "OneDrive", "바탕 화면", "대학", "3-2", "나노랩 심화2 (백우진)", "ufc insight", "frontend", "src", "rankings.json")

try:
    with open(input_path, 'r', encoding='utf-8') as f:
        rankings = json.load(f)
except FileNotFoundError:
    print(f"Input file not found at {input_path}")
    exit()


for category in rankings:
    image_path = category.get("champion", {}).get("image")
    if image_path:
        filename = os.path.basename(image_path)
        category["champion"]["image"] = f"/images/rankings/{filename}"

try:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(rankings, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated and wrote to {output_path}")
except Exception as e:
    print(f"Error writing to output file: {e}")
