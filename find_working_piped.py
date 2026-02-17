import requests
import time

instances = [
    "https://pipedapi.kavin.rocks",
    "https://api.piped.private.coffee",
    "https://pipedapi.leptons.xyz",
    "https://pipedapi.nosebs.ru",
    "https://pipedapi-libre.kavin.rocks",
    "https://api-piped.mha.fi",
    "https://pipedapi.smnz.de",
    "https://pipedapi.adminforge.de",
    "https://pipedapi.drgns.space",
    "https://pipedapi.ducks.party",
    "https://piped-api.lunar.icu",
    "https://pipedapi.r4fo.com",
    "https://api.piped.projectsegfau.lt",
    "https://pipedapi.us-free.kavin.rocks",
    "https://pa.il.ax",
    "https://p.lu.lgbt",
    "https://api.piped.yt",
    "https://piped-api.garudalinux.org"
]

video_id = "eP3UsuxK30U" # The video ID from the log

print(f"Testing {len(instances)} Piped instances for video {video_id}...\n")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

working_instances = []

for url in instances:
    try:
        start = time.time()
        api_url = f"{url}/streams/{video_id}"
        print(f"Checking {url} ...", end=" ", flush=True)
        
        response = requests.get(api_url, headers=headers, timeout=10)
        duration = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            if "audioStreams" in data and len(data["audioStreams"]) > 0:
                print(f"✅ OK ({duration:.2f}s)")
                working_instances.append(url)
            else:
                print(f"❌ 200 OK but no audioStreams")
        else:
            print(f"❌ HTTP {response.status_code}")
            if response.status_code == 500:
                try:
                    err_json = response.json()
                    print(f"   -> {err_json.get('message', 'Unknown Error')}")
                except:
                    pass
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print("\n=== SUMMARY ===")
if working_instances:
    print("Working Instances:")
    for i in working_instances:
        print(f"- {i}")
else:
    print("No working instances found.")
