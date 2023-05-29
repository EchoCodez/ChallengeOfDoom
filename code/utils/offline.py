import time
import os, sys
from plyer import notification
from logging import Logger

class Notifications:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger


    def _give_notifs(self):
        time.sleep(5)
        if os.path.exists("logs/isrunning.log"):
            notification.notify(
                title="Complete your daily checkup!",
                message = "Testing",
                app_icon = None, # or path to a .ico file
                timeout=10
            )
            self.logger.debug("Sent notification to user")
        else:
            self.logger.debug("Terminating as isrunning.log was not found")
            sys.exit(0)

    def start(self):
        while os.path.exists("logs/isrunning.log"):
            self._give_notifs()
        sys.exit(0)
