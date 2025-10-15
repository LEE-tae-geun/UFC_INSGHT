
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('rankings.json', 'r', encoding='utf-8') as f:
    rankings_data = json.load(f)

for category in rankings_data:
    if category['category'] == '페더급':
        # Update champion
        champion_name = category['champion']['name']
        print(f"Updating image for champion: {champion_name}")
        category['champion']['image'] = "test_image_url"
        break

with open('rankings.json', 'w', encoding='utf-8') as f:
    json.dump(rankings_data, f, indent=2, ensure_ascii=False)

print("Finished updating Featherweight champion image.")
