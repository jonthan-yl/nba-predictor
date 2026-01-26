from app.db.models import Player, PlayerGameLog
from app.db.database import SessionLocal
from app.scripts import scrape_player_season

def main():
    db = SessionLocal()
    players = db.query(Player).filter(Player.is_active == True).all()
    for player in players:
        print(f"Scraping game logs for {player.full_name} ({player.id})")
        skippedCount = 0
        for year in range(2026, 1980, -1):
            rowsInserted = scrape_player_season.main(player.id, year)
            skippedCount += rowsInserted == 0
            if skippedCount >= 4:
                break
    db.close()

if __name__ == "__main__":
    main()