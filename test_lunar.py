import requests
import json

instance = "https://pipedapi.lunar.icu"
playlist_id = "RDeP3UsuxK30U"
url = f"{instance}/playlists/{playlist_id}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"Testing {instance} for Playlist {playlist_id}")

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("JSON Keys:", data.keys())
            if "relatedStreams" in data:
                print(f"Found 'relatedStreams': {len(data['relatedStreams'])}")
            elif "videos" in data:
                print(f"Found 'videos': {len(data['videos'])}")
            else:
                print("Unknown structure. Dump:")
                print(json.dumps(data)[:500])
        except:
            print("Not valid JSON. First 500 chars:")
            print(response.text[:500])
    else:
        print("Response text:", response.text[:500])

except Exception as e:
    print(f"Error: {e}")
