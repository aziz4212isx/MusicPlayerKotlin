import requests
import json

playlist_id = "RDeP3UsuxK30U"
instance = "https://api.piped.projectsegfau.lt"
url = f"{instance}/playlists/{playlist_id}"

print(f"Testing URL: {url}")

try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("JSON Keys:", data.keys())
            if "relatedStreams" in data:
                print(f"Found 'relatedStreams' with {len(data['relatedStreams'])} items")
            elif "videos" in data:
                 print(f"Found 'videos' with {len(data['videos'])} items")
            else:
                print("Unknown structure. First 500 chars of JSON:")
                print(json.dumps(data)[:500])
        except Exception as e:
            print("Failed to parse JSON")
            print("Response text prefix:", response.text[:500])
    else:
        print("Response text prefix:", response.text[:500])

except Exception as e:
    print(f"Request failed: {e}")
