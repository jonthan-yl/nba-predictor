import argparse
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

from app.db.database import SessionLocal
from app.db.models import PlayerGameLog

HEADERS = {
    "User-Agent": "nba-predictor/1.0 (educational project)"
}


def fetch_html(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.text


def parse_game_logs(html: str, player_id: str):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="player_game_log_reg")
    if not table:
        print("Game log table not found")
        return []
    
    logs = []

    for row in table.tbody.find_all("tr"):
        # Skip header rows inside tbody
        if row.get("class") == ["thead"]:
            continue

        date_cell = row.find("td", {"data-stat": "date"})
        if not date_cell:
            continue

        game_date = date_cell.text.strip()
        if not game_date:
            continue

        def stat(name):
            cell = row.find("td", {"data-stat": name})
            return cell.text.strip() if cell else ""
        
        def minutes_played():
            mp = stat("mp")
            if not mp:
                return 0.0
            parts = mp.split(":")
            if len(parts) == 2:
                return int(parts[0]) + round(int(parts[1]) / 60.0, 3)
            return float(mp)

        logs.append({
            "player_id": player_id,
            "game_date": datetime.strptime(game_date, "%Y-%m-%d").date(),
            "minutes": float(minutes_played()) if stat("mp") else 0.0,
            "points": int(stat("pts")) if stat("pts") else 0,
            "rebounds": int(stat("trb")) if stat("trb") else 0,
            "assists": int(stat("ast")) if stat("ast") else 0,
            "steals": int(stat("stl")) if stat("stl") else 0,
            "blocks": int(stat("blk")) if stat("blk") else 0,
            "turnovers": int(stat("tov")) if stat("tov") else 0,
            "field_goals_made": int(stat("fg")) if stat("fg") else 0,
            "field_goals_attempted": int(stat("fga")) if stat("fga") else 0,
            "three_points_made": int(stat("fg3")) if stat("fg3") else 0,
            "three_points_attempted": int(stat("fg3a")) if stat("fg3a") else 0,
            "free_throws_made": int(stat("ft")) if stat("ft") else 0,
            "free_throws_attempted": int(stat("fta")) if stat("fta") else 0,
            "personal_fouls": int(stat("pf")) if stat("pf") else 0, 
        })

    return logs


def insert_logs(db, logs):
    inserted = 0

    for log in logs:
        exists = db.query(PlayerGameLog).filter(
            PlayerGameLog.player_id == log["player_id"],
            PlayerGameLog.game_date == log["game_date"]
        ).first()

        if exists:
            continue

        db.add(PlayerGameLog(**log))
        inserted += 1

    db.commit()
    return inserted

def build_game_log_url(player_id: str, season: int) -> str:
    first_letter = player_id[0]
    return f"https://www.basketball-reference.com/players/{first_letter}/{player_id}/gamelog/{season}"

def main(player_id: str = None, season: int = None):
    db = None
    inserted = 0
    try:
        url = build_game_log_url(player_id, season)
        html = fetch_html(url)
        logs = parse_game_logs(html, player_id)
        
        db = SessionLocal()
        inserted = insert_logs(db, logs)
        print(f"Inserted {inserted} new rows")
        
    except Exception as e:
        print(f"Error processing {player_id} for season {season}: {e}")
        
    finally:
        if db:
            db.close()

    time.sleep(2)  # Be polite to the server
    return inserted

if __name__ == "__main__":
    main()
