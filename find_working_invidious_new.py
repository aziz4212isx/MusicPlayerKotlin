import requests
import time

instances = [
    "https://inv.nadeko.net",
    "https://invidious.projectsegfau.lt",
    "https://invidious.nerdvpn.de",
    "https://yewtu.be",
    "https://iv.ggtyler.dev",
    "https://vid.puffyan.us",
    "https://invidious.drgns.space",
    "https://invidious.lunar.icu"
]

video_id = "eP3UsuxK30U" 

print(f"Testing {len(instances)} Invidious instances for video {video_id}...\n")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

working_instances = []

for url in instances:
    try:
        start = time.time()
        api_url = f"{url}/api/v1/videos/{video_id}"
        print(f"Checking {url} ...", end=" ", flush=True)
        
        response = requests.get(api_url, headers=headers, timeout=10)
        duration = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            if "formatStreams" in data and len(data["formatStreams"]) > 0:
                print(f"✅ OK ({duration:.2f}s)")
                working_instances.append(url)
            elif "adaptiveFormats" in data and len(data["adaptiveFormats"]) > 0:
                 print(f"✅ OK (Adaptive) ({duration:.2f}s)")
                 working_instances.append(url)
            else:
                print(f"❌ 200 OK but no streams")
        else:
            print(f"❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print("\n=== SUMMARY ===")
if working_instances:
    print("Working Invidious Instances:")
    for i in working_instances:
        print(f"- {i}")
else:
    print("No working instances found.")
