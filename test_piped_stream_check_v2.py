import requests
import json
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

instances = [
    "https://api.piped.private.coffee",
    "https://pipedapi.kavin.rocks",
    "https://pipedapi-libre.kavin.rocks",
    "https://api.piped.projectsegfau.lt",
    "https://pipedapi.moomoo.me",
    "https://pipedapi.smnz.de",
    "https://pipedapi.adminforge.de",
    "https://api.piped.privacy.com.de",
    "https://api.piped.forcadell.xyz",
    "https://pipedapi.ducks.party",
    "https://pipedapi.r4fo.com",
    "https://api.piped.chalvantzis.com",
    "https://api.piped.076.ne.jp",
    "https://pipedapi.leptons.xyz",
    "https://pipedapi.nosebs.ru",
    "https://pipedapi.drivet.xyz",
    "https://piped-api.lunar.icu",
    "https://pipedapi.tokhmi.xyz",
    "https://api.piped.yt",
    "https://pipedapi.drgns.space",
    "https://api-piped.mha.fi"
]

video_ids = ["jNQXAC9IVRw"] # Me at the zoo (Short, simple)

print(f"Testing Stream Fetch for {len(instances)} Instances...\n")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

working_instances = []

for inst in instances:
    print(f"--- Checking {inst} ---")
    works = True
    
    for vid in video_ids:
        url = f"{inst}/streams/{vid}"
        try:
            start_time = time.time()
            response = requests.get(url, headers=headers, timeout=8, verify=False)
            duration = time.time() - start_time
            
            if response.status_code != 200:
                print(f"  ❌ HTTP {response.status_code}")
                works = False
                break

            if response.text.strip().startswith("<"):
                print(f"  ❌ HTML Response")
                works = False
                break

            try:
                data = response.json()
                stream_found = False
                
                if "audioStreams" in data and len(data["audioStreams"]) > 0:
                    stream_found = True
                elif "hls" in data and data["hls"]:
                    stream_found = True
                elif "dash" in data and data["dash"]:
                    stream_found = True
                
                if not stream_found:
                     print(f"  ⚠️ JSON OK but NO streams")
                     works = False
                     break
                else:
                     print(f"  ✅ OK ({duration:.2f}s)")

            except json.JSONDecodeError:
                print(f"  ❌ JSON Parse Error")
                works = False
                break

        except Exception as e:
            print(f"  ❌ Exception: {str(e)[:50]}")
            works = False
            break
    
    if works:
        print(f"🎉 {inst} IS WORKING!")
        working_instances.append((inst, duration))

print("\n=== SUMMARY OF WORKING INSTANCES ===")
working_instances.sort(key=lambda x: x[1])
for url, time in working_instances:
    print(f'"{url}", // {time:.2f}s')
