import requests
import json

video_id = "eP3UsuxK30U"
instances = [
    "https://yewtu.be",
    "https://invidious.nerdvpn.de",
    "https://vid.puffyan.us",
    "https://inv.tux.pizza",
    "https://invidious.drgns.space"
]

print(f"Testing Mix Fallback (Video ID: {video_id}) on Invidious instances...\n")

for instance in instances:
    url = f"{instance}/api/v1/videos/{video_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            title = data.get('title')
            recs = data.get('recommendedVideos', [])
            
            print(f"✅ {instance} - OK")
            print(f"   Title: {title}")
            print(f"   Recommendations: {len(recs)}")
            if len(recs) > 0:
                print(f"   First Rec: {recs[0].get('title')} ({recs[0].get('videoId')})")
                break # Found a working one
        else:
            print(f"❌ {instance} - Status {response.status_code}")
    except Exception as e:
        print(f"❌ {instance} - Error: {e}")
