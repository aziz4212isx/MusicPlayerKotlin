import requests

# The user's playlist ID (Mix)
playlist_id = "RD9KnngSa6vk4"
# A standard playlist ID for comparison
standard_playlist_id = "PL15B1E77BB5708555" 

instance = "https://invidious.projectsegfau.lt" # The fastest one from previous test

print(f"Testing Playlist API on {instance}")

def test_id(pid, type_label):
    url = f"{instance}/api/v1/playlists/{pid}"
    print(f"\nTesting {type_label} ID: {pid}")
    print(f"URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Title: {data.get('title')}")
            print(f"Video count: {len(data.get('videos', []))}")
        else:
            print(f"Failed. Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

test_id(playlist_id, "Mix (RD)")
test_id(standard_playlist_id, "Standard (PL)")
