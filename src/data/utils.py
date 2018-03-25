from datetime import datetime

YEARS = 31557600
MONTHS = 2629800
WEEKS = 604800
DAYS = 86400
HOURS = 3600
MINUTES = 60


def get_elapsed_time(date_str: str):
    present = datetime.now()
    post_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    delta = present - post_date
    seconds = delta.total_seconds()
    elapsed = ''

    years = int(seconds / YEARS)
    seconds -= (years * YEARS)
    if years:
        if years > 1:
            elapsed += str(years) + 'yrs '
        else:
            elapsed += str(years) + 'yr '

    months = int(seconds / MONTHS)
    seconds -= (months * MONTHS)
    if months:
        if months > 1:
            elapsed += str(months) + ' months '
        else:
            elapsed += str(months) + ' month '
        return elapsed

    weeks = int(seconds / WEEKS)
    seconds -= (weeks * WEEKS)
    if weeks:
        elapsed += str(weeks) + 'w '
        return elapsed

    days = int(seconds / DAYS)
    seconds -= (days * DAYS)
    if days:
        elapsed += str(days) + 'd '
        return elapsed

    hours = int(seconds / HOURS)
    seconds -= (hours * HOURS)
    if hours:
        elapsed += str(hours) + 'h '

    minutes = int(seconds / MINUTES)
    seconds -= int(minutes * MINUTES)
    if minutes:
        elapsed += str(minutes) + 'm '
    else:
        elapsed = 'a few seconds'

    return elapsed
