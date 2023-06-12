from __future__ import annotations

from logging import Logger
from utils import jsonUtils
from utils.data_classes import InformationSheet
from logging import Logger
import customtkinter as ctk
from datetime import date, datetime

DATE = date | datetime | str
DATES = date | datetime
INFORMATION_PAGES = list[InformationSheet]

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
        
        def print(txt: str, level="info"):
            if logger is not None:
                exec(f"logger.{level}(\"{txt}\")")
        
        if isinstance(_date, str):
            path = _date
        elif isinstance(_date, DATES):
            path = str(_date.strftime("%d_%m_%Y"))
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
        
class InformationPages(UseLogger):
    _pages: INFORMATION_PAGES = []
    
    @property
    def pages(self) -> INFORMATION_PAGES:
        return self._pages
    
    @pages.setter
    def pages(self, pages: INFORMATION_PAGES) -> InformationPages:
        if not all(isinstance(page, InformationSheet) for page in pages):
            raise TypeError("Pages must be an list of pages")
        self._pages = pages
        return self
    
    def add_pages(self, *pages: InformationSheet) -> InformationPages:
        self.pages+=pages
        return self
    
    def create_pages(self, master: ctk.CTk, **content_kwargs) -> None:
        def create_page(page: InformationSheet):
            ctk.CTkButton(
                master,
                text="Next Page",
                command=master.quit
            ).place(relx=0.8, rely=0.8, anchor="center")
            
            ctk.CTkLabel(
                master,
                text=page.title
            ).pack(pady=50)
            
            t = ctk.CTkTextbox(
                master,
                width=960,
                height=540,
                **content_kwargs
            )
            t.insert('insert', page.content)
            t.pack(pady=50)
            
            for action_button in page.buttons:
                ctk.CTkButton(
                    master,
                    text=action_button.text,
                    command=action_button.command,
                    **action_button.kwargs
                ).pack(**{"pady": 20} | page.button_pack_kwargs)
        
        for page in self:
            for w in master.winfo_children():
                w.destroy()
                
            create_page(page)
            master.mainloop()
            
    
    def copy(self) -> InformationPages:
        return self.__copy__()
    
    def __copy__(self) -> InformationPages:
        return InformationPages(*self._pages)
            
    def __iadd__(self, __o: InformationSheet, /) -> None:
        self.pages += [ __o ]
        return self
        
    def __repr__(self) -> str:
        pages = '\n'.join(self._pages)
        return f"{type(self).__name__}(pages={pages})"
            
    def __iter__(self) -> list.__iter__:
        return self._pages.__iter__()
    