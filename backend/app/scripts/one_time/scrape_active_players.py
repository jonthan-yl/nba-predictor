import time
import requests
from bs4 import BeautifulSoup

from app.db.database import SessionLocal
from app.db.models import Player
from datetime import datetime

BASE_URL = "https://www.basketball-reference.com"
INDEX_URL = f"{BASE_URL}/players/"

HEADERS = {
    "User-Agent": "nba-predictor/1.0 (educational project)"
}


def fetch_html(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.text


def get_letter_links(html: str):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("div#content a")
    letters = []

    for a in links:
        href = a.get("href", "")
        if href.startswith("/players/") and len(href) == len("/players/a/"):
            letters.append(BASE_URL + href)

    return sorted(set(letters))


def parse_active_players(html: str):
    soup = BeautifulSoup(html, "html.parser")
    players = []

    for row in soup.select("table tbody tr"):
        th = row.find("th")
        if not th:
            continue

        link = th.find("a")
        if not link:
            continue

        # Active players are bolded
        if not th.find("strong"):
            continue

        href = link["href"]
        player_id = href.split("/")[-1].replace(".html", "")
        full_name = link.text.strip()

        pos_td = row.find("td", {"data-stat": "pos"})
        height_td = row.find("td", {"data-stat": "height"})
        weight_td = row.find("td", {"data-stat": "weight"})
        birth_date_td = row.find("td", {"data-stat": "birth_date"})

        position = pos_td.text.strip() if pos_td else None
        height = height_td.text.strip() if height_td else None
        weight = weight_td.text.strip() if weight_td else None
        birthdate = birth_date_td.text.strip() if birth_date_td else None

        players.append({
            "id": player_id,
            "full_name": full_name,
            "position": position,
            "height": get_height(height),
            "weight": int(weight),
            "birthdate": get_date_from_string(birthdate)
        })

    return players


def upsert_players(db, players):
    inserted = 0
    updated = 0

    for p in players:
        existing = db.query(Player).filter(Player.id == p["id"]).first()

        if existing:
            if not existing.is_active:
                existing.is_active = True
                updated += 1
        else:
            db.add(Player(
                id=p["id"],
                full_name=p["full_name"],
                position=p["position"],
                height=p["height"],
                weight=p["weight"],
                birthdate=p["birthdate"],
                is_active=True
            ))
            inserted += 1

    db.commit()
    return inserted, updated


def deactivate_missing_players(db, active_ids):
    updated = 0

    for player in db.query(Player).filter(Player.is_active == True).all():
        if player.id not in active_ids:
            player.is_active = False
            updated += 1

    db.commit()
    return updated

def get_height(height_str: str) -> int:
    if not height_str:
        return None
    parts = height_str.split("-")
    if len(parts) != 2:
        return None
    feet = int(parts[0])
    inches = int(parts[1])
    return feet * 12 + inches

def get_date_from_string(date_str: str):
    try:
        return datetime.strptime(date_str, "%B %d, %Y").date()
    except Exception:
        print(f"Failed to parse date: {date_str}")
        return None


def main():
    print("Fetching player index...")
    index_html = fetch_html(INDEX_URL)

    letter_links = get_letter_links(index_html)
    print(f"Found {len(letter_links)} letter pages")

    all_active_players = []

    for url in letter_links:
        print(f"Scraping {url}")
        html = fetch_html(url)
        players = parse_active_players(html)
        all_active_players.extend(players)
        time.sleep(2)

    print(f"Found {len(all_active_players)} active players")

    db = SessionLocal()
    try:
        inserted, updated = upsert_players(db, all_active_players)
        active_ids = {p["id"] for p in all_active_players}
        deactivated = deactivate_missing_players(db, active_ids)
    finally:
        db.close()

    print(f"Inserted: {inserted}")
    print(f"Reactivated: {updated}")
    print(f"Deactivated: {deactivated}")

if __name__ == "__main__":
    main()
