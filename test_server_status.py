import requests

def test_server(url):
    try:
        print(f"Testing {url}...")
        resp = requests.get(f"{url}/api/v1/stats", timeout=5)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text[:100]}")
    except Exception as e:
        print(f"Error: {e}")

test_server("https://inv.tux.pizza")
