import requests
import time

instances = [
    "https://pipedapi.kavin.rocks",
    "https://api.piped.privacy.com.de",
    "https://pipedapi.drgns.space",
    "https://api-piped.mha.fi",
    "https://pipedapi.tokhmi.xyz",
    "https://pipedapi.moomoo.me",
    "https://api.piped.projectsegfau.lt",
    "https://pipedapi.leptons.xyz",
    "https://api.piped.yt",
    "https://pipedapi.adminforge.de",
    "https://pipedapi.smnz.de",
    "https://api.piped.forcadell.xyz",
    "https://pipedapi.ducks.party",
    "https://pipedapi.r4fo.com",
    "https://api.piped.chalvantzis.com",
    "https://pipedapi.nosebs.ru",
    "https://api.piped.076.ne.jp"
]

playlist_id = "RD9KnngSa6vk4"
standard_playlist_id = "PL15B1E77BB5708555"

print("Testing Piped API Instances...\n")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

working_instances = []

def test_piped_instance(inst):
    url = f"{inst}/playlists/{playlist_id}"
    try:
        start = time.time()
        response = requests.get(url, headers=headers, timeout=5)
        duration = time.time() - start
        
        if response.status_code == 200:
            print(f"✅ {inst} - {duration:.2f}s (Mix Supported)")
            return True, duration
        elif response.status_code == 404:
            # Try standard playlist
            url_std = f"{inst}/playlists/{standard_playlist_id}"
            resp_std = requests.get(url_std, headers=headers, timeout=5)
            if resp_std.status_code == 200:
                 print(f"⚠️ {inst} - Standard OK, Mix Failed (404)")
            else:
                 print(f"❌ {inst} - Failed (Status {resp_std.status_code})")
        else:
            print(f"❌ {inst} - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ {inst} - Error: {str(e)[:50]}")
    return False, 0

for inst in instances:
    success, duration = test_piped_instance(inst)
    if success:
        working_instances.append((inst, duration))

print("\n--- Working Piped Instances for Mix ---")
working_instances.sort(key=lambda x: x[1])
for url, duration in working_instances:
    print(f'"{url}", // {duration:.2f}s')
