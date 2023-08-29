from __future__ import annotations

import customtkinter as ctk
import utils.parse_json as jsonUtils
import utils.constants as constants
from logging import Logger
from datetime import date, datetime

__all__ = (
    "UseLogger",
    "ceil",
    "set_theme",
    "FileHandler",
    "HomepageSection"
)

def ceil(n: float) -> int:
    '''Return ceil(n)'''
    return int(n) if isinstance(n, int) or n.is_integer() else int(n)+1

def set_theme() -> bool:
    '''Check if theme preference in file already.
    
    Returns:
    --------
        bool: whether or not appearance theme was found
    '''
    
    with open("json/preferences.json") as f:
        return jsonUtils.get(f, "appearance_theme", func = ctk.set_appearance_mode)

class UseLogger:
    '''Defines empty logger init method and print method'''
    def __init__(self) -> None:
        self.logger = constants.LOGGER
    
    def print(self, __s: str, /, level: str | int = "info", **kwargs):
        if isinstance(level, str):
            getattr(self.logger, level.lower())(__s)
        elif self.logger.isEnabledFor(level):
            self.logger._log(level, __s)

class FileHandler(UseLogger):       
    def delete_logs(self):
        '''Delete logs'''
        
        self.logger.info("Deleting all health logs")
        for log in constants.HEALTH_LOGS.iterdir():
            log.unlink()
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
                getattr(logger, level.lower())(txt, **kwargs)
        
        if isinstance(_date, (str, Path)):
            path = Path(_date)
        elif isinstance(_date, date):
            path = constants.HEALTH_LOGS / Path(_date.strftime('%d_%m_%y')).with_suffix(".json")
        else:
            raise TypeError("Date for get_log must be a properly formatted path or datetime/date object")
        
        print(f"Attempting to access {path}")
        
        try:
            return jsonUtils.read(path)
        except FileNotFoundError as e:
            print(e, level="exception")
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
        
    @staticmethod
    def today_file_path() -> Path:
        return 
class HomepageSection(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        placement = kwargs.pop("placement")
        super().__init__(*args, **kwargs)
        self.place(**placement)
    