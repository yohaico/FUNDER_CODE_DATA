from datetime import datetime


def print_msg(msg):
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    print(date_time + "   " + msg)
