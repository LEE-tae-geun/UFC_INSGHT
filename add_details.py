import json
import os

# Path to the rankings.json file
json_path = os.path.join("C:", os.sep, "Users", "Lee", "OneDrive", "바탕 화면", "대학", "3-2", "나노랩 심화2 (백우진)", "ufc insight", "frontend", "src", "rankings.json")

# Detailed info for the fighters
fighters_details = {
    "Sean O'Malley": { "record": "18-3-0", "age": "30", "height": "71.00", "weight": "135.00", "reach": "72.00", "leg_reach": "40.00" },
    "Umar Nurmagomedov": { "record": "18-1-0", "height": "68.00", "weight": "135.00" },
    "Petr Yan": { "record": "19-5-0", "age": "32", "height": "67.50", "weight": "136.00", "reach": "67.00", "leg_reach": "38.00", "octagon_debut": "Jun 23, 2018" },
    "Cory Sandhagen": { "record": "18-6-0", "age": "33", "height": "71.00", "weight": "134.50", "reach": "70.00", "leg_reach": "40.00", "octagon_debut": "Jan 28, 2018" },
    "Song Yadong": { "record": "22-8-1", "age": "27", "height": "68.00", "weight": "136.00", "reach": "67.00", "leg_reach": "38.00" },
    "Deiveson Figueiredo": { "record": "25-5-1", "age": "37", "height": "65.00", "weight": "136.00", "reach": "68.00", "leg_reach": "38.00" },
    "Marlon Vera": { "record": "23-10-1", "age": "32", "height": "68.00", "weight": "136.00", "reach": "70.50", "leg_reach": "40.50" },
    "Mario Bautista": { "record": "16-2-0", "age": "32", "height": "69.00", "weight": "135.00", "reach": "72.00", "leg_reach": "39.00" },
    "Aiemann Zahabi": { "record": "13-2-0", "height": "68.00", "weight": "142.00" },
    "Henry Cejudo": { "record": "16-5-0", "age": "38", "height": "64.00", "weight": "135.00", "reach": "64.00", "leg_reach": "37.00", "octagon_debut": "Dec 13, 2014" },
    "David Martinez": { "record": "13-1-0", "age": "27", "height": "65.00", "weight": "135.50", "reach": "67.50", "leg_reach": "37.50", "octagon_debut": "Mar 29, 2025" },
    "Vinicius Oliveira": { "record": "23-3-0", "height": "69.00", "weight": "136.00" },
    "Rob Font": { "record": "22-9-0", "age": "38", "height": "68.00", "weight": "135.00", "reach": "71.50", "leg_reach": "38.50", "octagon_debut": "Jul 05, 2014" },
    "Kyler Phillips": { "record": "12-4-0", "age": "30", "height": "68.00", "weight": "135.00", "reach": "72.00", "leg_reach": "38.00", "octagon_debut": "Aug 01, 2017" },
    "Montel Jackson": { "record": "15-3-0", "age": "33", "height": "70.00", "weight": "136.00", "reach": "75.50", "leg_reach": "41.00", "octagon_debut": "Aug 04, 2018" }
}

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        rankings = json.load(f)
except FileNotFoundError:
    print(f"File not found at {json_path}")
    exit()

# Find and update fighters' data
for category in rankings:
    if category["category"] == "밴텀급":
        for fighter in category["fighters"]:
            if fighter["name"] in fighters_details:
                fighter["details"] = fighters_details[fighter["name"]]

try:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rankings, f, indent=2, ensure_ascii=False)
    print(f"Successfully updated {json_path} with details for Bantamweight fighters.")
except Exception as e:
    print(f"Error writing to file: {e}")
