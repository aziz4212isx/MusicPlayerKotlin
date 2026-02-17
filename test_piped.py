import requests

# The user's playlist ID (Mix)
playlist_id = "RD9KnngSa6vk4"
standard_playlist_id = "PL15B1E77BB5708555"

instances = [
    "https://pipedapi.kavin.rocks",
    "https://api.piped.privacy.com.de",
    "https://pipedapi.drgns.space",
    "https://api-piped.mha.fi"
]

print("Testing Piped API...")

def test_piped(inst, pid, label):
    url = f"{inst}/playlists/{pid}"
    print(f"\nTesting {label} on {inst}")
    print(f"URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            name = data.get('name', 'Unknown')
            videos = data.get('relatedStreams', [])
            print(f"✅ Success! Name: {name}")
            print(f"Video count: {len(videos)}")
        else:
            print(f"❌ Failed. Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error: {e}")

for inst in instances:
    test_piped(inst, playlist_id, "Mix (RD)")
    test_piped(inst, standard_playlist_id, "Standard (PL)")
