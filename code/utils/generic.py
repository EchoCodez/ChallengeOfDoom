from __future__ import annotations

import customtkinter as ctk
import utils.parse_json as jsonUtils
from logging import Logger
from datetime import date, datetime

# aliases
DATE = date | datetime | str
DATES = date | datetime

__all__ = (
    "UseLogger",
    "set_theme",
    "FileHandler",
    "HomepageSection"
)

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
        logs = jsonUtils.read("json/logs.json")["logs_list"] if logs is None else logs
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
            return jsonUtils.read(path)
        except FileNotFoundError as e:
            print(
                txt=e,
                level="exception"
            )
            return f"Diagnosis Results for {path} not found"
    
    @staticmethod
    def get_entry(
        master: ctk.CTk | ctk.CTkScrollableFrame,
        placement_kwargs: dict = dict,
        **kwargs
        ) -> ctk.CTkEntry:
        
        """
        Creates an entry textbox on the scene

        Parameters:
        -----------
            master (CTk, CTkScrollableFrame): entrybox and label master
            
            placement_kwargs (dict, optional): kwargs for placing the label
            
            text (str): Title text
            
            placeholder (str): placeholder for `CTkEntry`
            
            width (int): width of entry widget
            
            height (int): height of entry widget
            
            entry_kwargs (dict, optional): kwargs for creating the `CTkEntry` widget
            
            kwargs (dict, optional): kwargs to be passed in when packing `CTkEntry`

        Raises:
        --------
            TypeError: Unexpected Kwarg

        Returns:
        --------
            CTkEntry
        """        
        
        default_label_kwargs = {"pady": 100}
        label_kwargs = default_label_kwargs | (placement_kwargs() if placement_kwargs is dict else placement_kwargs)
        
        
        text = kwargs.pop("text", "")
        placeholder = kwargs.pop("placeholder", "")
        
        if kwargs:
            raise TypeError(f"Unexpected kwarg(s) {kwargs.keys()}")
        
        ctk.CTkLabel(
            master,
            text=text
        ).pack(**label_kwargs)
        
        result = ctk.CTkEntry(
            master,
            placeholder_text=placeholder,
            width=kwargs.pop("width", 280),
            height=kwargs.pop("height", 56),
            **kwargs.pop("entry_kwargs", {})
        )
        result.pack(**({"pady": 20} | kwargs.pop("kwargs", {})))
        
        master.mainloop()
        
        return result
        
    
    @staticmethod
    def reset_username(master: ctk.CTk | ctk.CTkScrollableFrame, **kwargs):
        username = FileHandler.get_entry(master, **kwargs)
        jsonUtils.add({"api_username": username.get()})
        
    @staticmethod
    def reset_password(master: ctk.CTk | ctk.CTkScrollableFrame, **kwargs):
        username = FileHandler.get_entry(master, **kwargs)
        jsonUtils.add({"api_username": username.get()})
        
class HomepageSection(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        placement = kwargs.pop("placement")
        super().__init__(*args, **kwargs)
        self.place(**placement)
    