import datetime
import time
class Time():
    def __init__(self):
        pass
    @staticmethod
    def nowtime():
        import time
        millis = int(round(time.time() * 1000))
        return str(millis)
    @staticmethod
    def now():
        return datetime.datetime.now()
    @staticmethod
    def nowdate():
        today = datetime.date.today()
        formatted_today = today.strftime('%y%m%d')
        return str(formatted_today)

    @staticmethod
    def todatetime(str):
        time = datetime.datetime.strptime(str, "%Y/%m/%d %H:%M")
        return time
    @staticmethod
    def isVaildDate(date):
        try:
            if ":" in date:
                time.strptime(date, "%Y-%m-%d %H:%M:%S")
            else:
                time.strptime(date, "%Y-%m")
            return True
        except:
            return False