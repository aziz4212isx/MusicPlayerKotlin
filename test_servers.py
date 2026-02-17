import requests
import time

instances = [
    "https://inv.tux.pizza",
    "https://invidious.jing.rocks",
    "https://vid.puffyan.us",
    "https://inv.nadeko.net",
    "https://invidious.nerdvpn.de",
    "https://invidious.lunar.icu",
    "https://yewtu.be",
    "https://invidious.drgns.space",
    "https://invidious.projectsegfau.lt",
    "https://invidious.slipfox.xyz",
    "https://invidious.privacydev.net",
    "https://iv.ggtyler.dev"
]

print(f"Testing {len(instances)} instances...\n")

working_instances = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for url in instances:
    try:
        start = time.time()
        # Test with a simple stats endpoint or just the root API
        response = requests.get(f"{url}/api/v1/stats", headers=headers, timeout=5)
        duration = time.time() - start
        
        if response.status_code == 200:
            print(f"✅ {url} - {duration:.2f}s")
            working_instances.append((url, duration))
        else:
            print(f"❌ {url} - Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ {url} - Error: {str(e)}")

print("\n--- Summary ---")
working_instances.sort(key=lambda x: x[1]) # Sort by fastest
for url, duration in working_instances:
    print(f'"{url}", // {duration:.2f}s')
