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

`scrape_active_players.py`

Scrapes all active and inactive NBA players from Basketball-Reference and syncs them into the local SQLite database.

`update_active_player_game_logs.py`

 iterates through each active player and updates their game logs according to the last time you ran an update