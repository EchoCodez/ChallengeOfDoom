from __future__ import annotations

from logging import Logger
from utils.parse_json import jsonUtils
from logging import Logger
import customtkinter as ctk
from datetime import date, datetime

# aliases
DATE = date | datetime | str
DATES = date | datetime

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
        return jsonUtils.get(f, "appearance_theme", func = ctk.set_appearance_mode)

class FileHandler(UseLogger):       
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
    
    @staticmethod
    def get_log(_date: DATE, /, logger: Logger = None) -> list[dict[str, dict[str, str|int]]]:
        """Get the diagnosis results for a specific date

        Parameters:
        -----------
            _date (str | date | datetime): The date of diagnosis results. Positional only argument

        Raises:
        -------
            TypeError: Date argument was not a string, date, or datetime object

        Returns:
        --------
            `list[dict[str, dict[str, str|int]]]`: The diagnosis results for that day\n
            `str`: Diagnosis Results for <day> not found
        """        
        
        def print(txt: str, level="info",  **kwargs):
            if logger is not None:
                exec(f"logger.{level}(\"{txt}\")", **kwargs)
        
        if isinstance(_date, str):
            path = _date
        elif isinstance(_date, DATES):
            path = str(_date.strftime("%d_%m_%y"))
        else:
            raise TypeError("Date for get_log must be a properly formatted string or datetime/date object")
        
        print(f"Attempted to access json/health/{path}.json")
        
        try:
            return jsonUtils.open(path)
        except FileNotFoundError as e:
            print(
                txt=e,
                level="exception"
            )
            return f"Diagnosis Results for {path} not found"
        
class HomepageSection(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        placement = kwargs.pop("placement")
        super().__init__(*args, **kwargs)
        self.place(**placement)
    