import requests
import json

mix_id = "RDeP3UsuxK30U"
instances = [
    "https://inv.nadeko.net",
    "https://yewtu.be",
    "https://invidious.nerdvpn.de",
    "https://vid.puffyan.us",
    "https://inv.tux.pizza",
    "https://invidious.drgns.space",
    "https://invidious.fdn.fr",
    "https://invidious.perennialteks.com"
]

print(f"Testing Invidious Mix API (/api/v1/mixes/) for {mix_id}\n")

working_instances = []

for inst in instances:
    url = f"{inst}/api/v1/mixes/{mix_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            title = data.get('title')
            videos = data.get('videos', [])
            
            if len(videos) > 0:
                print(f"✅ {inst} - OK")
                print(f"   Title: {title}")
                print(f"   Videos: {len(videos)}")
                print(f"   First Video: {videos[0].get('title')} ({videos[0].get('videoId')})")
                working_instances.append(inst)
            else:
                print(f"⚠️ {inst} - JSON OK but no videos")
        else:
            print(f"❌ {inst} - Status {response.status_code}")
    except Exception as e:
        print(f"❌ {inst} - Error: {str(e)[:50]}")

print("\n--- Working Instances for Mixes ---")
for w in working_instances:
    print(w)
