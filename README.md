# 🛰️ Issue Radar

> Never miss a beginner-friendly GitHub issue again.

Issue Radar automatically scans GitHub for open contribution opportunities across hundreds of repositories — and notifies you the moment new ones drop.

---

## 🚀 What It Does

Finding good open source issues to contribute to is harder than it should be. Labels like `good first issue` exist, but there's no way to get notified when new ones appear across repos you don't already follow.

Issue Radar solves that by:
- Continuously fetching issues tagged with beginner-friendly labels across all of GitHub
- Displaying them in a clean, searchable dashboard
- Sending you a browser notification the moment new issues are found

---

## ✨ Features

- 🔍 **Multi-label scanning** — tracks `good first issue`, `help wanted`, `beginner friendly`, `easy`, `first-timers-only`, `up-for-grabs`, `hacktoberfest`, and more
- 🔔 **Browser push notifications** — get alerted when new issues drop, no app or email needed
- 🔎 **Search & filter** — filter by label or search by repo/issue title
- 🟢 **NEW badge** — freshly fetched issues are highlighted so you spot them instantly
- ♻️ **Auto-refresh** — dashboard updates every 60 seconds automatically
- 🐳 **Fully Dockerized** — runs anywhere with one command

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Fetcher | Python 3.10, Requests, Schedule |
| Frontend | HTML, CSS, Vanilla JS |
| Server | Nginx (Alpine) |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| API | GitHub REST API v3 |

---

## 📁 Project Structure

```
issue-radar/
├── fetcher/
│   ├── main.py          # GitHub API polling logic
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   └── index.html       # Dashboard UI
├── data/                # Fetched issues (auto-generated)
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── deploy.yml   # CI/CD pipeline
└── .env                 # Your GitHub token (never committed)
```

---

## ⚡ Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- A [GitHub Personal Access Token](https://github.com/settings/tokens) with `public_repo` scope

### 1. Clone the repo
```bash
git clone https://github.com/m21ahima/issue-radar.git
cd issue-radar
```

### 2. Add your token
Create a `.env` file in the root:
```
GITHUB_TOKEN=ghp_your_token_here
```

### 3. Run
```bash
docker compose up --build
```

### 4. Open the dashboard
Go to [http://localhost:8080](http://localhost:8080)

Click **Enable Notifications** to get browser alerts when new issues drop!

---

## 🔄 CI/CD Pipeline

Every push to `main` automatically:
1. Sets up Python and installs dependencies
2. Checks for syntax errors in the fetcher
3. Builds the Docker image

Powered by GitHub Actions — see `.github/workflows/deploy.yml`.

---

## 🗺️ Roadmap

- [ ] Filter by programming language
- [ ] User accounts — save favourite repos and labels
- [ ] Telegram / Discord notification support
- [ ] Staleness detection — hide issues with no activity in 30+ days
- [ ] Deploy to cloud (Railway / Render)

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">Built to make open source more accessible 🌍</p>
