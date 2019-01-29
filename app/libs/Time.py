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
    def nowdate():
        today = datetime.date.today()
        formatted_today = today.strftime('%y%m%d')
        return str(formatted_today)