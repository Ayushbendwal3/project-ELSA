import datetime

DAYS = ["monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"]
MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_date(text):
    text.lower()
    today = datetime.date.today()

    if text.count("what day is it") > 0 or text.count("what date is it"):
        return today
    if text.count("tomorrow") > 0:
        tomorrow = today + datetime.timedelta(days=1)
        return tomorrow
    if text.count("today") > 0:
        return today
    if text.count("yesterday") > 0:
        yesterday = today + datetime.timedelta(days=-1)
        return yesterday

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year + 1

    if day < today.day and month == -1 and day != -1:
        month = month + 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)
