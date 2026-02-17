import requests
import time

instances = [
    "https://pipedapi.aeong.one",
    "https://pipedapi.lunar.icu",
    "https://pipedapi.nwpss.ru",
    "https://pipedapi.rivo.lol",
    "https://pipedapi.beincrypto.com", 
    "https://api.piped.privacy.com.de", # Retrying
    "https://pipedapi.adminforge.de" # Retrying
]

playlist_id = "RD9KnngSa6vk4"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Testing NEW Piped Instances...\n")

for inst in instances:
    url = f"{inst}/playlists/{playlist_id}"
    try:
        start = time.time()
        response = requests.get(url, headers=headers, timeout=5)
        duration = time.time() - start
        
        if response.status_code == 200:
            print(f"✅ {inst} - {duration:.2f}s")
        else:
            print(f"❌ {inst} - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ {inst} - Error: {str(e)[:50]}")
