import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

mix_id = "RDeP3UsuxK30U"
instances = [
    "https://invidious.drgns.space",
    "https://inv.tux.pizza" 
]

print(f"Testing Invidious Mix API (SSL Verify=False) for {mix_id}\n")

for inst in instances:
    url = f"{inst}/api/v1/mixes/{mix_id}"
    try:
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            data = response.json()
            videos = data.get('videos', [])
            print(f"✅ {inst} - OK (Videos: {len(videos)})")
        else:
            print(f"❌ {inst} - Status {response.status_code}")
    except Exception as e:
        print(f"❌ {inst} - Error: {str(e)[:50]}")
