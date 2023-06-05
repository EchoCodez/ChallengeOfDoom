from plyer import notification

class Notification:
    def __init__(self, title: str, message: str, time: str, increment: int =1440):
        self.title = title
        self.message = message
        if len(time) != 8:
            self.time = "0" + time
        else:
            self.time = time
        if self.time[-2] == "P":
            self.time = str(int(self.time[0:2])+12)+self.time[2:5]+":00"
        else:
            self.time = self.time[0:5]+":00"
        self.increment = increment

    def send(self):
        notification.notify(
            title = self.title,
            message = self.message,
        )
    
    def __repr__(self) -> str:
        return "{0}(title={1}, message={2}, time={3})".format(self.__class__.__name__, self.title, self.message, self.time)