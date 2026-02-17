import requests
import json
import time

instances = [
    "https://api.piped.private.coffee",
    "https://pipedapi-libre.kavin.rocks",
    "https://pipedapi.kavin.rocks",
    "https://pipedapi.leptons.xyz",
    "https://pipedapi.nosebs.ru"
]

video_id = "dQw4w9WgXcQ" # Never Gonna Give You Up (Reliable test video)

print(f"Testing Stream Fetch for Video ID: {video_id}\n")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for inst in instances:
    url = f"{inst}/streams/{video_id}"
    print(f"Checking {inst}...")
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        duration = time.time() - start_time
        
        if response.status_code != 200:
            print(f"❌ {inst} - HTTP {response.status_code}")
            try:
                if response.status_code == 403:
                    print(f"   Reason: Forbidden (Cloudflare/Rate Limit)")
                else:
                    print(f"   Body: {response.text[:100]}")
            except:
                pass
            continue

        if response.text.strip().startswith("<"):
            print(f"❌ {inst} - HTML Response (Blocked/Error)")
            continue

        try:
            data = response.json()
            stream_found = False
            
            # Check for audioStreams
            if "audioStreams" in data and len(data["audioStreams"]) > 0:
                print(f"✅ {inst} - Found {len(data['audioStreams'])} audio streams ({duration:.2f}s)")
                stream_found = True
            elif "hls" in data and data["hls"]:
                print(f"✅ {inst} - Found HLS stream ({duration:.2f}s)")
                stream_found = True
            elif "dash" in data and data["dash"]:
                print(f"✅ {inst} - Found DASH stream ({duration:.2f}s)")
                stream_found = True
            
            if not stream_found:
                 print(f"⚠️ {inst} - JSON OK but NO streams found")

        except json.JSONDecodeError:
            print(f"❌ {inst} - JSON Parse Error")
            print(f"   Body: {response.text[:100]}")

    except Exception as e:
        print(f"❌ {inst} - Exception: {str(e)}")
