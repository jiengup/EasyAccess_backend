import datetime


def classify_pub_time(pub_time):
    now = datetime.datetime.now()
    if now.year == pub_time.year and now.month == pub_time.month and now.day == pub_time.day:
        return str(pub_time)[11:16]
    else:
        return str(pub_time)[0:10]