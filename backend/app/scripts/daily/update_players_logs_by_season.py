from app.db.models import Player
from app.db.database import SessionLocal
from app.utils.season import current_nba_season
from app.scripts.one_time import scrape_active_players, scrape_player_season

def main(season: int = -1):
    if season == -1:
        season = current_nba_season()

    db = SessionLocal()
    scrape_active_players.main()
    players = db.query(Player).filter(Player.is_active == True).all()
    for player in players:
        print(f"Scraping game logs for {player.full_name} ({player.id})")
        rowsInserted = scrape_player_season.main(player.id, season)

    db.close()

if __name__ == "__main__":
    main()