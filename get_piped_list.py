import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    response = requests.get("https://piped-instances.kavin.rocks/", verify=False)
    if response.status_code == 200:
        instances = response.json()
        print(f"Found {len(instances)} Piped instances.")
        for inst in instances:
            print(f"- {inst.get('name')} ({inst.get('api_url')})")
    else:
        print("Failed to fetch instance list.")
except Exception as e:
    print(f"Error: {e}")
