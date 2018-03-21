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
    ellapsed = ''

    years = int(seconds / YEARS)
    seconds -= (years * YEARS)
    if years:
        if years > 1:
            ellapsed += str(years) + 'yrs '
        else:
            ellapsed += str(years) + 'yr '

    months = int(seconds / MONTHS)
    seconds -= (months * MONTHS)
    if months:
        if months > 1:
            ellapsed += str(months) + ' months '
        else:
            ellapsed += str(months) + ' month '
        return ellapsed

    weeks = int(seconds / WEEKS)
    seconds -= (weeks * WEEKS)
    if weeks:
        ellapsed += str(weeks) + 'w '
        return ellapsed

    days = int(seconds / DAYS)
    seconds -= (days * DAYS)
    if days:
        ellapsed += str(days) + 'd '
        return ellapsed

    hours = int(seconds / HOURS)
    seconds -= (hours * HOURS)
    if hours:
        ellapsed += str(hours) + 'h '

    minutes = int(seconds / MINUTES)
    seconds -= int(minutes * MINUTES)
    if minutes:
        ellapsed += str(minutes) + 'm '

    return ellapsed


def get_total_seconds(date_str: str):
    present = datetime.now()
    post_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    delta = present - post_date
    seconds = delta.total_seconds()
    return seconds