from datetime import datetime

class Util:
    @classmethod
    def today(self):
        return datetime.today().strftime("%Y-%m-%d")
