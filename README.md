# nba-predictor

**Work in Progress**

NBA web application and API for predicting future NBA player stats for fantasy use.

## Contributors
- Mousa Najjar
- Ameel Aziz
- Jonathan Liu

## Running the Project Locally

### Frontend
From the `frontend/` directory:

```bash
npm run dev
```

### Backend
*uvicorn backend.app.main:app --reload* runs the API locally from nba-predictor

### Data & Scraping Scripts

All scripts live under `backend/app/scripts/`.

| Script | Location | Purpose |
|--------|----------|---------|
| `scrape_active_players.py` | `one_time/` | Scrapes all active/inactive NBA players from Basketball-Reference and syncs them into the local SQLite database |
| `scrape_player_season.py` | `one_time/` | Scrapes game logs for a specific player and season |
| `update_active_player_game_logs.py` | `one_time/` | Iterates through each active player and backfills their full game log history |
| `update_players_logs_by_season.py` | `daily/` | Syncs the active player list and updates game logs for the current season only |

## Daily Data Updates (GitHub Actions)

A GitHub Actions workflow (`.github/workflows/daily-update.yml`) runs the daily update script automatically on a cron schedule.

### How it works

The SQLite database (`backend/app/nba.db`) is checked into git — there is no external database server. The workflow cycle is:

1. **Checkout** — GitHub Actions clones the repo onto a temporary Ubuntu VM, which includes `nba.db`
2. **Run script** — The daily script scrapes Basketball-Reference and inserts new rows into the local `nba.db` file
3. **Commit & push** — The workflow commits the modified `nba.db` back to `main` (only if there are changes)

The cron runs at **10:00 UTC (5:00 AM ET)** daily, after NBA games have finished. It can also be triggered manually from the **Actions** tab in GitHub.

### Limitations

- **Repo size growth** — Each daily commit stores a new version of the binary `.db` file. Git can't efficiently diff binaries, so the repo will grow over time.
- **Merge conflicts** — If someone pushes changes to `nba.db` while the workflow is running, the push will fail.
- **No concurrent access** — Only the GitHub Actions runner reads/writes the DB at a time.

As the project scales, migrating to a hosted database (e.g. PostgreSQL) would address these limitations. The existing SQLAlchemy setup makes that switch straightforward — only the `DATABASE_URL` in `database.py` needs to change.