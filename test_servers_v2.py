import requests
import time

instances = [
    "https://inv.tux.pizza",
    "https://invidious.jing.rocks",
    "https://vid.puffyan.us",
    "https://inv.nadeko.net",
    "https://invidious.nerdvpn.de",
    "https://invidious.lunar.icu",
    "https://yewtu.be",
    "https://invidious.drgns.space",
    "https://invidious.projectsegfau.lt",
    "https://invidious.slipfox.xyz",
    "https://invidious.privacydev.net",
    "https://iv.ggtyler.dev",
    "https://invidious.fdn.fr",
    "https://invidious.perennialteks.com",
    "https://yt.artemislena.eu"
]

playlist_id = "PL15B1E77BB5708555" # Standard playlist for testing

print(f"Testing Playlist API on {len(instances)} instances...\n")

working_instances = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for url in instances:
    try:
        start = time.time()
        api_url = f"{url}/api/v1/playlists/{playlist_id}"
        response = requests.get(api_url, headers=headers, timeout=5)
        duration = time.time() - start
        
        if response.status_code == 200:
            ct = response.headers.get('Content-Type', '')
            if 'json' in ct:
                data = response.json()
                if 'videos' in data:
                    print(f"✅ {url} - {duration:.2f}s (JSON OK)")
                    working_instances.append((url, duration))
                else:
                    print(f"⚠️ {url} - JSON OK but no 'videos' key")
            else:
                 print(f"⚠️ {url} - Status 200 but Content-Type: {ct}")
        else:
            print(f"❌ {url} - Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ {url} - Error: {str(e)}")

print("\n--- Working Servers ---")
working_instances.sort(key=lambda x: x[1])
for url, duration in working_instances:
    print(f'"{url}",')
