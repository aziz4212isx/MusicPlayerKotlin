import requests
import time
import json

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

video_id = "eP3UsuxK30U"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"Testing Piped API for Video Streams (Mix Fallback): {video_id}\n")

working_instances = []

for inst in instances:
    url = f"{inst}/streams/{video_id}"
    try:
        start = time.time()
        response = requests.get(url, headers=headers, timeout=5)
        duration = time.time() - start
        
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                try:
                    data = response.json()
                    if "relatedStreams" in data and len(data["relatedStreams"]) > 0:
                        print(f"✅ {inst} - {duration:.2f}s (Streams + Related OK)")
                        working_instances.append(inst)
                    else:
                        print(f"⚠️ {inst} - JSON OK but missing 'relatedStreams'")
                except:
                    print(f"❌ {inst} - Invalid JSON")
            else:
                print(f"❌ {inst} - Not JSON (Type: {content_type})")
        else:
            print(f"❌ {inst} - Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ {inst} - Error: {str(e)[:50]}")

print("\n--- Working Instances for Streams ---")
for w in working_instances:
    print(w)
