
import requests
from bs4 import BeautifulSoup
import json
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base_url = "https://www.ufc.com"

fighter_name = "Alexander Volkanovski"
search_url = f"{base_url}/search?query={fighter_name.replace(' ', '%20')}"
print(f"Search URL: {search_url}")
try:
    resp = requests.get(search_url)
    with open('search_results.html', 'w', encoding='utf-8') as f:
        f.write(resp.text)
    print("Saved search results to search_results.html")
except Exception as e:
    print(f"Error getting search results: {e}")
