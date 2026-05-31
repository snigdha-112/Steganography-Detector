import requests
import os
import time

# --- YOUR KEY HERE ---
ACCESS_KEY = "2RkALZNUwg3c08uXLDYsGL2gYamnhaBW59TgeWgW3B0"

# --- SETTINGS ---
SAVE_FOLDER = "D:/stegoproject/dataset/clean"
TOTAL_IMAGES = 300        # how many you want
IMAGES_PER_PAGE = 10      # max allowed by Unsplash free tier
SEARCH_TOPICS = ["nature", "city", "people", "architecture", "animals", "food", "travel"]

os.makedirs(SAVE_FOLDER, exist_ok=True)

downloaded = 0
topic_index = 0

print("Starting download...")

while downloaded < TOTAL_IMAGES:
    topic = SEARCH_TOPICS[topic_index % len(SEARCH_TOPICS)]
    page = (downloaded // IMAGES_PER_PAGE) + 1

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": topic,
        "per_page": IMAGES_PER_PAGE,
        "page": page,
        "client_id": ACCESS_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"API error: {response.status_code} — check your key")
        break

    results = response.json().get("results", [])

    if not results:
        topic_index += 1  # move to next topic if no results
        continue

    for photo in results:
        if downloaded >= TOTAL_IMAGES:
            break

        img_url = photo["urls"]["regular"]  # good quality, not huge
        img_response = requests.get(img_url)

        if img_response.status_code == 200:
            filename = f"img_{downloaded+1:04d}.jpg"
            filepath = os.path.join(SAVE_FOLDER, filename)

            with open(filepath, "wb") as f:
                f.write(img_response.content)

            downloaded += 1
            print(f"Downloaded {downloaded}/{TOTAL_IMAGES} — {filename} [{topic}]")

    topic_index += 1
    time.sleep(1)  # be polite to the API

print(f"\nDone! {downloaded} images saved to {SAVE_FOLDER}")
