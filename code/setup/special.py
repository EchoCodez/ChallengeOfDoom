from __future__ import annotations

from utils import jsonUtils, InformationSheet, UseLogger
import customtkinter as ctk
import tkinter as tk
from logging import Logger

INFORMATION_PAGES = list[InformationSheet]

class Settings:
    def __init__(self, master: ctk.CTk, logger: Logger) -> None:
        self.master = master
        self.logger = logger
        self.logger.debug("Settings Clicked")
        self.y_place = 0.3
        self.show_settings()
    
    def show_settings(self, mainloop=True, font=("", 50)) -> dict | None:
        from utils import FileHandler
        self.master.clean()
        self.setting_vars = {}
        
        def swap_mode():
            ctk.set_appearance_mode("dark" if ctk.get_appearance_mode().lower()=="light" else "light")
            jsonUtils.write(
                {"appearance_theme": ctk.get_appearance_mode().lower()},
                file="json/preferences.json"
                )
            self.logger.debug(f"Appearance Mode: \"{ctk.get_appearance_mode().lower()}\" written to file")
        
        switch_settings = (
            ("Toggle Appearance Mode", swap_mode, {}),
        )
        
        # TODO: create bar for button colors
        
        button_settings = (
            ("Delete Diagnosis Logs", FileHandler(self.logger).delete_logs, {}),
            ("Delete Health Logs", lambda: FileHandler(self.logger).delete_logs([]), {}),
            ("Delete Medicine Logs", lambda: FileHandler(self.logger).delete_logs([]), {})
        )
        
        for name, command, kwargs in switch_settings:
            self.setting_vars[name] = self._create_switch_setting(
                name, command=command, font=font, **kwargs
                )
        
        for name, command, kwargs in button_settings:
            self.setting_vars[name] = self._create_button_setting(
                name, font=font, command=command, **kwargs
                )
        
        if mainloop:
            self.master.mainloop()
        else:
            return self.setting_vars
    
    def _create_switch_setting(self, name: str, **kwargs) -> tk.Variable:
        """Create a setting button controlled by a switch

        Parameters:
        -----------
            name (str): Setting name
            
            ACCEPTABLE KWARGS: width, height, font, switch_font, var, switch_place_kwargs, label_place_kwargs, on_off,
            command, switch_kwargs, label_kwargs

        Raises:
        -------
            TypeError: Unknown kwarg passed in

        Returns:
        --------
            tk.Variable: The variable after being attached to the button
        """
        
        width, height = kwargs.pop("width", 300), kwargs.pop("height", 72)
        font, switch_font = kwargs.pop("font", None), kwargs.pop("switch_font", None)
        var = kwargs.pop("var", tk.StringVar)()
        switch_kwargs = kwargs.pop("switch_place_kwargs", {"relx":0.7, "rely":self.y_place, "anchor":tk.CENTER})
        label_kwargs = kwargs.pop("label_place_kwargs", {"relx":0.2, "rely":self.y_place, "anchor":tk.CENTER})
        on, off = kwargs.pop("on_off", ("on", "off"))
        command = kwargs.pop("command", None)
        switch_creation_kwargs, label_creation_kwargs = kwargs.pop("switch_kwargs", {}), kwargs.pop("label_kwargs", {})
        self.y_place+=.1
        
        if kwargs:
            raise TypeError("Invalid kwargs {0}".format(kwargs))
        
        l = ctk.CTkLabel(
            self.master,
            text=name,
            font=font,
            **label_creation_kwargs
        )
        ctk.CTkSwitch(
            self.master,
            onvalue=on,
            offvalue=off,
            variable=var,
            command=command,
            switch_width=width,
            switch_height=height,
            font=switch_font,
            text="",
            **switch_creation_kwargs
        ).place(**switch_kwargs)
        l.place(**label_kwargs)
        return var

    def _create_button_setting(self, name: str, **kwargs) -> None:
        '''
        WORK IN PROGRESS!!!!!!!!!!
        
        Create a setting button controlled by a switch

        Parameters:
        -----------
            name (str): Setting's name
            
            ACCEPTABLE KWARGS: width, height, font, button_font, button_place_kwargs, label_place_kwargs,
            command, button_kwargs, label_kwargs

        Raises:
        -------
            TypeError: Unknown kwarg passed in

        Returns:
        --------
            tk.Variable: The variable after being attached to the button
        '''
        
        width, height = kwargs.pop("width", 300), kwargs.pop("height", 72)
        font, button_font = kwargs.pop("font", None), kwargs.pop("button_font", None)
        
        button_kwargs = {
            "column":4,
            "row":int(self.y_place*10),
            "pady": 50,
            "sticky": tk.E
            } | kwargs.pop("button_place_kwargs", {})
        
        label_kwargs = {
            "column":0,
            "row":int(self.y_place*10),
            "pady": 30,
            "padx": 50,
            "sticky": tk.W,
            "columnspan": 2
            } | kwargs.pop("label_place_kwargs", {})
        command = kwargs.pop("command", None)
        label_creation_kwargs = kwargs.pop("label_kwargs", {})
        button_creation_kwargs = kwargs.pop("button_kwargs", {})
        
        self.y_place+=.1
        
        if kwargs:
            raise TypeError("Invalid kwargs {0}".format(kwargs))
        
        
        ctk.CTkLabel(
            self.master,
            text=name,
            font=font,
            **label_creation_kwargs
        ).grid(**label_kwargs)
        
        ctk.CTkButton(
            self.master,
            command=command,
            width=width,
            height=height,
            font=button_font,
            text="",
            **button_creation_kwargs
        ).grid_configure(**button_kwargs)

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
