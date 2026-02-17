import requests

# The user's playlist ID (Mix)
playlist_id = "RD9KnngSa6vk4"

instance = "https://invidious.projectsegfau.lt" 
# Let's try another one too just in case
instance2 = "https://inv.nadeko.net"

def test_id(inst, pid):
    url = f"{inst}/api/v1/playlists/{pid}"
    print(f"\nTesting on {inst}")
    print(f"URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"First 500 chars: {response.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

test_id(instance, playlist_id)
test_id(instance2, playlist_id)
