"""
TrendPulse - Task 1: Data Collection

This script fetches trending stories from HackerNews API,
categorises them using keywords, and saves them into a JSON file.

Output file: data/trends_YYYYMMDD.json
"""

import requests
import json
import time
import os
from datetime import datetime


# Configuration
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

ID_FETCH_LIMIT = 500
MAX_PER_CATEGORY = 25
SLEEP_TIME = 2


# Categories and keywords (case-insensitive matching)
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}


def assign_category(title):
    """
    Check title and return category based on keyword match.
    I used simple substring matching because it's easy and works well here.
    """
    if not title:
        return None

    title = title.lower()

    for category, keywords in CATEGORIES.items():
        for word in keywords:
            if word in title:
                return category

    return None


def fetch_top_story_ids():
    """Fetch top story IDs from HackerNews"""
    print("Fetching top stories...")

    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        ids = response.json()[:ID_FETCH_LIMIT]
        print(f"Fetched {len(ids)} story IDs")
        return ids
    except requests.exceptions.RequestException as e:
        print("Error fetching top stories:", e)
        return []


def fetch_story(story_id):
    """Fetch individual story details"""
    try:
        response = requests.get(ITEM_URL.format(id=story_id), headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        print(f"Skipping story {story_id} due to error")
        return None


def collect_stories(story_ids):
    """Collect and categorize stories"""
    collected = {cat: [] for cat in CATEGORIES}

    print("Processing stories...")

    for story_id in story_ids:

        # Stop early if all categories are filled
        if all(len(v) >= MAX_PER_CATEGORY for v in collected.values()):
            break

        story = fetch_story(story_id)

        if not story or "title" not in story:
            continue

        title = story.get("title")
        category = assign_category(title)

        if not category:
            continue

        # Skip if category already has enough stories
        if len(collected[category]) >= MAX_PER_CATEGORY:
            continue

        # Extract required fields
        record = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected[category].append(record)

        # Sleep once when a category reaches limit (as per instructions)
        if len(collected[category]) == MAX_PER_CATEGORY:
            print(f"{category} completed. Waiting {SLEEP_TIME}s...")
            time.sleep(SLEEP_TIME)

    # Combine all categories into one list
    all_stories = []
    for stories in collected.values():
        all_stories.extend(stories)

    return all_stories


def save_to_json(stories):
    """Save stories to JSON file"""
    os.makedirs("data", exist_ok=True)

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stories, f, indent=4)

    print(f"Collected {len(stories)} stories. Saved to {filename}")


def main():
    print("Starting TrendPulse data collection...")

    story_ids = fetch_top_story_ids()

    if not story_ids:
        print("No data fetched. Exiting.")
        return

    stories = collect_stories(story_ids)

    if stories:
        save_to_json(stories)
    else:
        print("No stories collected.")


if __name__ == "__main__":
    main()