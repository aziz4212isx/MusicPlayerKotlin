import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

instance = "https://api.piped.private.coffee"
mix_id = "RDeP3UsuxK30U"
url = f"{instance}/playlists/{mix_id}"

print(f"Testing {instance} for Mix {mix_id}")

try:
    response = requests.get(url, verify=False, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if "relatedStreams" in data:
            print(f"✅ Success! Found {len(data['relatedStreams'])} streams.")
        else:
            print("Keys:", data.keys())
    else:
        print("Failed:", response.text[:200])
except Exception as e:
    print(f"Error: {e}")
