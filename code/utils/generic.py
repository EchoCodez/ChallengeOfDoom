from logging import Logger
from utils import jsonUtils
from logging import Logger
import customtkinter as ctk

class UseLogger:
    '''Defines empty logger init method'''
    def __init__(self, logger: Logger) -> None:
        self._logger = logger
        
    @property
    def logger(self):
        return self._logger
    
    def print(self, __s: str, /, *, level: str = "info"):
        exec(f"self.logger.{level.lower()}(\"{__s}\")")

def set_theme() -> bool:
    '''Check if theme preference in file already.
    
    Returns:
    --------
        bool: whether or not appearance theme was found
    '''
    
    with open("json/preferences.json") as f:
        if jsonUtils.get(f, "appearance_theme", func = ctk.set_appearance_mode):
            return True
    return False

class FileHandler(UseLogger):
    def create_new_application(self):
        with open("logs/isrunning.log", "w"): # create the file
            pass
        self.logger.debug("Successfully created logs/isrunning.log")

    def clear_old_application(self):
        import os
        try:
            os.remove("logs/isrunning.log")
            self.logger.debug("Deleted logs/isrunning.log")
        except FileNotFoundError:
            self.logger.debug("Attempted to delete logs/isrunning.log, but it did not exist")
            
    def delete_logs(self, logs: list[str] = None):
        '''Delete info
        
        Parameters:
        -----------
            logs (`list[str]`, optional): logs to delete. Defaults to those in `json/logs.json`
        '''
        import os
        logs = jsonUtils.open("json/logs.json")["logs_list"] if logs is None else logs
        self.logger.info("Deleting {0}".format(logs))
        for log in logs:
            try:
                os.remove(path=log)
            except FileNotFoundError:
                continue
        self.logger.debug("Finished")
        