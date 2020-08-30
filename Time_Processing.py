import datetime


def format_time(time_str):
    time_str = time_str.replace(' +0800', '')
    time_format = datetime.datetime.strptime(time_str, '%a %b %d %H:%M:%S %Y')
    date = time_format.date()
    time = time_format.time()
    return date, time
