import requests
import schedule
import time
import json
import os
import sys
sys.stdout.flush()
from dotenv import load_dotenv

load_dotenv()

LABELS = [
    "good first issue",
    "help wanted",
    "beginner friendly",
    "easy",
    "first-timers-only",
    "up-for-grabs",
    "hacktoberfest",
]

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
SEEN_FILE = "data/seen_issues.json"


def load_seen():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    os.makedirs("data", exist_ok=True)
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def fetch_issues():
    print("Fetching new issues...")
    seen = load_seen()
    new_issues = []

    for label in LABELS:
        query = f'label:"{label}" state:open is:issue no:assignee'
        url = f"https://api.github.com/search/issues?q={requests.utils.quote(query)}&sort=created&order=desc&per_page=20"

        try:
            response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                print(f"Error fetching label '{label}': {response.status_code}")
                continue

            items = response.json().get("items", [])
            for issue in items:
                issue_id = str(issue["id"])
                if issue_id not in seen:
                    seen.add(issue_id)
                    new_issues.append({
                        "id": issue_id,
                        "title": issue["title"],
                        "url": issue["html_url"],
                        "repo": issue["repository_url"].replace("https://api.github.com/repos/", ""),
                        "label": label,
                    })
        except Exception as e:
            print(f"Exception: {e}")

    save_seen(seen)

    if new_issues:
        print(f"Found {len(new_issues)} new issues!")
        with open("data/new_issues.json", "w") as f:
            json.dump(new_issues, f, indent=2)
    else:
        print("No new issues found.")


fetch_issues()
schedule.every(30).minutes.do(fetch_issues)

while True:
    schedule.run_pending()
    time.sleep(60)