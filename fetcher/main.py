import requests
import schedule
import time
import json
import os
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
    "beginner",
    "newcomer",
    "starter",
    "low-hanging-fruit",
]

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
} if GITHUB_TOKEN else {}

SEEN_FILE = "data/seen_issues.json"
ISSUES_FILE = "data/new_issues.json"
MAX_ISSUES = 500


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


def load_existing_issues():
    if os.path.exists(ISSUES_FILE):
        with open(ISSUES_FILE, "r") as f:
            return json.load(f)
    return []


def fetch_issues():
    print("Fetching new issues...")
    seen = load_seen()
    existing_issues = load_existing_issues()
    new_issues = []

    for label in LABELS:
        for page in range(1, 6):
            query = f'label:"{label}" state:open is:issue no:assignee'
            url = (
                f"https://api.github.com/search/issues"
                f"?q={requests.utils.quote(query)}"
                f"&sort=created&order=desc&per_page=100&page={page}"
            )

            try:
                response = requests.get(url, headers=HEADERS)

                if response.status_code == 403:
                    print(f"Rate limited on label '{label}', skipping...")
                    time.sleep(10)
                    break

                if response.status_code != 200:
                    print(f"Error on label '{label}' page {page}: {response.status_code}")
                    break

                items = response.json().get("items", [])
                if not items:
                    break

                for issue in items:
                    issue_id = str(issue["id"])
                    if issue_id not in seen:
                        seen.add(issue_id)
                        new_issues.append({
                            "id": issue_id,
                            "title": issue["title"],
                            "url": issue["html_url"],
                            "repo": issue["repository_url"].replace(
                                "https://api.github.com/repos/", ""
                            ),
                            "label": label,
                            "created_at": issue["created_at"],
                            "comments": issue["comments"],
                            "body_length": len(issue.get("body") or ""),
                        })

                time.sleep(2)

            except Exception as e:
                print(f"Exception on label '{label}': {e}")
                break

        time.sleep(3)

    save_seen(seen)

    if new_issues:
        print(f"Found {len(new_issues)} new issues!")
        all_issues = new_issues + existing_issues
        all_issues = all_issues[:MAX_ISSUES]
        with open(ISSUES_FILE, "w") as f:
            json.dump(all_issues, f, indent=2)

        with open("data/latest_batch.json", "w") as f:
            json.dump(new_issues[:20], f, indent=2)

        print(f"Total stored: {len(all_issues)} issues")
    else:
        print("No new issues found.")


fetch_issues()
schedule.every(30).minutes.do(fetch_issues)

while True:
    schedule.run_pending()
    time.sleep(60)