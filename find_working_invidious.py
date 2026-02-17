import requests
import json
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("Fetching Invidious Instances List...")

try:
    resp = requests.get("https://api.invidious.io/instances.json?sort_by=health", timeout=10)
    data = resp.json()
    print(f"Got data type: {type(data)}")
    if isinstance(data, list) and len(data) > 0:
        print(f"First item: {data[0]}")
except Exception as e:
    print(f"Failed to fetch list: {e}")
    data = []

candidates = []

# Handle both list of lists and list of dicts if structure changed
if isinstance(data, list):
    for item in data:
        if isinstance(item, list) and len(item) >= 2:
            domain = item[0]
            info = item[1]
        elif isinstance(item, dict):
            info = item
            domain = info.get('uri', '').replace('https://', '').replace('http://', '')
        else:
            continue

        if info.get('type') == 'https':
            uri = info.get('uri')
            # Check monitor status if available
            monitor = info.get('monitor', {})
            if monitor and monitor.get('statusClass') == 'success':
                if uri:
                    candidates.append(uri)
            # Or just try anyway if monitor info missing
            elif uri and 'monitor' not in info:
                 candidates.append(uri)

print(f"Found {len(candidates)} candidate instances. Testing...\n")

# Fallback manual list if API returns few results
manual_list = [
    "https://inv.nadeko.net",
    "https://invidious.projectsegfau.lt",
    "https://invidious.nerdvpn.de",
    "https://yewtu.be",
    "https://iv.ggtyler.dev",
    "https://vid.puffyan.us",
    "https://invidious.drgns.space",
    "https://invidious.privacydev.net",
    "https://invidious.protokolla.fi",
    "https://invidious.flokinet.to",
    "https://invidious.lunar.icu",
    "https://invidious.private.coffee"
]

for url in manual_list:
    if url not in candidates:
        candidates.append(url)

video_id = "jNQXAC9IVRw" # Me at the zoo
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

working_instances = []

# Limit candidates to avoid too long run
if len(candidates) > 30:
    candidates = candidates[:30]

for inst in candidates:
    # Skip onion/i2p
    if ".onion" in inst or ".i2p" in inst:
        continue
        
    print(f"Checking {inst}...")
    url = f"{inst}/api/v1/videos/{video_id}"
    
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=5, verify=False)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            try:
                vid_data = response.json()
                if "formatStreams" in vid_data and len(vid_data["formatStreams"]) > 0:
                    print(f"  ✅ SUCCESS! ({duration:.2f}s)")
                    working_instances.append((inst, duration))
                elif "adaptiveFormats" in vid_data and len(vid_data["adaptiveFormats"]) > 0:
                    print(f"  ✅ SUCCESS (Adaptive)! ({duration:.2f}s)")
                    working_instances.append((inst, duration))
                else:
                    print(f"  ⚠️ JSON OK but no streams.")
            except:
                print(f"  ❌ JSON Parse Error")
        else:
            print(f"  ❌ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Exception: {str(e)[:50]}")

print("\n=== WORKING INVIDIOUS INSTANCES ===")
working_instances.sort(key=lambda x: x[1])
for url, time in working_instances:
    print(f'"{url}", // {time:.2f}s')
