from datetime import datetime


def current_nba_season(today: datetime | None = None) -> int:
    if today is None:
        today = datetime.utcnow()

    year = today.year
    month = today.month

    return year + 1 if month >= 10 else year
