import requests
import json
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

instances = [
    "https://inv.nadeko.net",
    "https://invidious.projectsegfau.lt",
    "https://invidious.nerdvpn.de",
    "https://yewtu.be",
    "https://iv.ggtyler.dev",
    "https://vid.puffyan.us",
    "https://invidious.drgns.space",
    "https://invidious.privacydev.net"
]

video_id = "jNQXAC9IVRw" # Me at the zoo

print(f"Testing Invidious Video Fetch for Video ID: {video_id}\n")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

working_instances = []

for inst in instances:
    print(f"--- Checking {inst} ---")
    url = f"{inst}/api/v1/videos/{video_id}"
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        duration = time.time() - start_time
        
        if response.status_code != 200:
            print(f"  ❌ HTTP {response.status_code}")
            continue

        try:
            data = response.json()
            if "formatStreams" in data and len(data["formatStreams"]) > 0:
                print(f"  ✅ OK - Found formatStreams ({duration:.2f}s)")
                working_instances.append((inst, duration))
            elif "adaptiveFormats" in data and len(data["adaptiveFormats"]) > 0:
                print(f"  ✅ OK - Found adaptiveFormats ({duration:.2f}s)")
                working_instances.append((inst, duration))
            else:
                print(f"  ⚠️ JSON OK but NO streams found")

        except json.JSONDecodeError:
            print(f"  ❌ JSON Parse Error")

    except Exception as e:
        print(f"  ❌ Exception: {str(e)[:50]}")

print("\n=== WORKING INVIDIOUS INSTANCES ===")
working_instances.sort(key=lambda x: x[1])
for url, time in working_instances:
    print(f'"{url}", // {time:.2f}s')
