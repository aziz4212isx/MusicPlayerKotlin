import requests
import json

video_id = "eP3UsuxK30U"
instance = "https://inv.nadeko.net" # One of the working Invidious instances
url = f"{instance}/api/v1/videos/{video_id}"

print(f"Testing Video ID: {video_id} on {instance}")

try:
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Title: {data.get('title')}")
        print(f"Author: {data.get('author')}")
        
        if "recommendedVideos" in data:
            print(f"Found {len(data['recommendedVideos'])} recommended videos.")
            print("First 3 recommendations:")
            for v in data['recommendedVideos'][:3]:
                print(f"- {v.get('title')} ({v.get('videoId')})")
        else:
            print("No recommended videos found.")
    else:
        print("Video not found or error.")
        print(response.text[:200])

except Exception as e:
    print(f"Error: {e}")
