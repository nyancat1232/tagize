from datetime import datetime,timezone

def assume_year(date_given):
    now_date = datetime.now(tz=timezone.utc)
    year = now_date.year
    comp_date = datetime(year,date_given.month,date_given.day)
    if comp_date > now_date:
        year -= 1
    return datetime(year,date_given.month,date_given.day).date()