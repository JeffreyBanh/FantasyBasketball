# Fantasy Basketball Daily Top 10

## Overview

This project automatically collects daily NBA data from **Basketball Monster** and posts (or displays) the top 10 players in 9 fantasy basketball categories. The script can generate either the **best** or **worst** performers for the day.

The workflow is automated via **GitHub Actions**, which runs the script every day after all NBA games are finished, ensuring that the statistics are final.

---

## Features

- Fetches daily NBA data from Basketball Monster
- Generates **top 10 rankings** for 9 key fantasy basketball categories
- Supports three output modes:
  - `best`: Displays the top 10 best performers
  - `worst`: Displays the top 10 worst performers
  - `both`: Can combine best and worst outputs (future extension)
- Can either **print results** for review (dry run) or **post to Reddit** automatically
- Automated scheduling via GitHub Actions ensures daily execution without manual intervention

---

## Repository Structure

```
FantasyBasketball/
├── .github/
│   └── workflows/
│       └── run-daily.yml      # GitHub Actions workflow
├── src/
│   └── reddit_api.py          # Main script
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## Setup & Installation

1. **Clone the repository:**

```bash
git clone https://github.com/<your-username>/FantasyBasketball.git
cd FantasyBasketball
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Configure Reddit credentials (if posting to Reddit):**

   - Create a Reddit app [here](https://www.reddit.com/prefs/apps)
   - In your GitHub repository, go to **Settings → Secrets → Actions → New repository secret** and add:
     - `REDDIT_CLIENT_ID`
     - `REDDIT_CLIENT_SECRET`
     - `REDDIT_USER_AGENT`

---

## Usage

### Dry Run (Print Output)

```bash
python src/reddit_api.py -dr 1 -ot worst
```

### Post to Reddit

```bash
python src/reddit_api.py -dr 0 -ot best
```

### Parameters

- `-dr` → Dry run flag (0 = post, 1 = print only)
- `-ot` → Output type (best, worst, both)

---

## Automation with GitHub Actions

The project is set up to run daily at **11:30 PM Pacific Time** automatically via GitHub Actions.

**Workflow location:**
```
.github/workflows/run-daily.yml
```

The workflow:
- Installs all dependencies
- Loads Reddit credentials from repository secrets
- Runs `reddit_api.py` with the desired flags

---

## Dependencies

- Python 3.11+
- beautifulsoup4
- requests
- pandas
- praw
- ipython
- python-dotenv

---

## Notes

- Ensure that your Reddit credentials are correctly set in GitHub Secrets for automatic posting
- The script relies on Basketball Monster data being available for the day's games
- Scheduling is configured to run after NBA games are typically finished, ensuring data completeness

---

## License

This project is for personal or educational use. Please do not repost data publicly without permission from Basketball Monster.