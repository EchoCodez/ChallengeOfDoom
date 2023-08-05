from __future__ import annotations

from utils import jsonUtils, InformationSheet, UseLogger, CustomQuestion, SettingsAttr
import customtkinter as ctk
import tkinter as tk
from logging import Logger

INFORMATION_PAGES = list[InformationSheet | CustomQuestion]

class Settings(ctk.CTkScrollableFrame):
    def __init__(self, master: ctk.CTk | ctk.CTkScrollableFrame, logger: Logger, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.logger = logger
        self.logger.debug("Settings Clicked")
        self.row = 0
        self.show_settings()
        self.logger.debug("Done")
    
    def clean(self):
        for w in (i for i in self.master.winfo_children() if i is not self):
            w.destroy()
    
    def show_settings(self, mainloop=False, font=("", 50)) -> dict | None:
        from utils import FileHandler
        self.master.quit()
        self.clean()
        self.setting_vars = {}
        
        def swap_mode():
            ctk.set_appearance_mode("dark" if ctk.get_appearance_mode().lower()=="light" else "light")
            jsonUtils.write(
                {"appearance_theme": ctk.get_appearance_mode().lower()},
                file="json/preferences.json"
                )
            self.logger.debug(f"Appearance Mode: \"{ctk.get_appearance_mode().lower()}\" written to file")
        
        switch_settings = (
            SettingsAttr("Toggle Appearance Mode", swap_mode),
        )
        
        # TODO: create bar for button colors
        files = FileHandler(self.logger)
        button_settings: tuple[SettingsAttr] = (
            SettingsAttr(
                "Reset API Username",
                lambda: None
            ),
            SettingsAttr(
                "Delete Diagnosis Logs",
                lambda: files.delete_logs()
            ),
            SettingsAttr(
                "Delete Health Logs",
                lambda: files.delete_logs([])
            ), # TODO
            SettingsAttr(
                "Delete Medicine Logs",
                lambda: files.delete_logs([])
            ), # TODO
            SettingsAttr(
                "Delete all data",
                lambda: jsonUtils.clearfiles(clearlogs=True)
            )
        )
        
        for setting in switch_settings:
            self.setting_vars[setting.name] = self._create_switch_setting(
                    setting.name,
                    command=setting.command,
                    font=font,
                    **setting.kwargs
                )
        
        for setting in button_settings:
            self._create_button_setting(
                    setting.name,
                    font=font,
                    command=setting.command,
                    **setting.kwargs
                )
        
        if mainloop:
            self.pack()
            self.mainloop()
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
        font = kwargs.pop("font", None)
        
        var = kwargs.pop("var", tk.StringVar)()
        
        switch_kwargs = {
            "column":5,
            "row":self.row,
            "sticky": tk.E,
            "pady": 50,
            } | kwargs.pop("switch_place_kwargs", {})
        
        label_kwargs = {
            "column":0,
            "row":self.row,
            "sticky": tk.E,
            "pady": 50,
            "padx": 50,
            "columnspan": 2
            } | kwargs.pop("label_place_kwargs", {})
        
        on, off = kwargs.pop("on_off", ("on", "off"))
        command = kwargs.pop("command", None)
        switch_creation_kwargs, label_creation_kwargs = kwargs.pop("switch_kwargs", {}), kwargs.pop("label_kwargs", {})
        self.row+=1
        
        if kwargs:
            raise TypeError("Invalid kwargs {0}".format(kwargs))
        
        l = ctk.CTkLabel(
            self,
            text=name,
            font=font,
            **label_creation_kwargs
        )
        
        self._create_invisible_buttons(
            label_kwargs["column"]+label_kwargs["columnspan"]+1,
            switch_kwargs["column"],
            switch_kwargs.copy(),
            width,
            height
            )
        
        ctk.CTkSwitch(
            self,
            onvalue=on,
            offvalue=off,
            variable=var,
            command=command,
            switch_width=width,
            switch_height=height,
            text="",
            **switch_creation_kwargs
        ).grid(**switch_kwargs)
        l.grid(**label_kwargs)
        return var

    def _create_button_setting(self, name: str, **kwargs) -> None:
        '''
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
        font = kwargs.pop("font", None)
        
        button_kwargs = {
            "column":5,
            "row":self.row,
            "pady": 50,
            "sticky": tk.E
            } | kwargs.pop("button_place_kwargs", {})
        
        label_kwargs = {
            "column":0,
            "row":self.row,
            "pady": 30,
            "padx": 50,
            "sticky": tk.W,
            "columnspan": 2
            } | kwargs.pop("label_place_kwargs", {})
        command = kwargs.pop("command", None)
        label_creation_kwargs = kwargs.pop("label_kwargs", {})
        button_creation_kwargs = kwargs.pop("button_kwargs", {})
        
        self.row+=1
        
        if kwargs:
            raise TypeError(f"Invalid kwargs {kwargs}")
        
        
        ctk.CTkLabel(
            self,
            text=name,
            font=font,
            **label_creation_kwargs
        ).grid(**label_kwargs)
        
        temp_placements = button_kwargs.copy()
        
        self._create_invisible_buttons(
            label_kwargs["column"]+label_kwargs["columnspan"]+1,
            button_kwargs["column"],
            temp_placements,
            width,
            height
            )
        
        ctk.CTkButton(
            self,
            command=command,
            width=width,
            height=height,
            text="Click here",
            **button_creation_kwargs
        ).grid_configure(**button_kwargs)

    def _create_invisible_buttons(
            self,
            start: int,
            end: int,
            temp_placements: dict,
            width: int,
            height:int
        ) -> None:
        
        TRANSPARENT = self.master.cget("bg")
        
        for col in range(start, end):
            temp_placements["column"] = col
            
            ctk.CTkButton(
                self,
                width=width,
                height=height,
                text="",
                fg_color=TRANSPARENT,
                hover_color=TRANSPARENT,
                border_color=TRANSPARENT,
                text_color=TRANSPARENT,
            ).grid(**temp_placements)

class InformationPages(UseLogger):
    _pages: INFORMATION_PAGES = []
    
    @property
    def pages(self) -> INFORMATION_PAGES:
        return self._pages
    
    @pages.setter
    def pages(self, pages: INFORMATION_PAGES) -> InformationPages:
        if not all(isinstance(page, (InformationSheet, CustomQuestion)) for page in pages):
            raise TypeError("Pages must be an list of pages")
        self._pages = pages
        return self
    
    def add_pages(self, *pages: InformationSheet) -> InformationPages:
        self.pages = self.pages+pages
        return self
    
    def create_pages(self, master: ctk.CTk, **content_kwargs) -> list:
        def create_page(page: InformationSheet):
            def _quit():
                master.quit()
                self.logger.debug("Next information page")
                
            ctk.CTkButton(
                master,
                text="Next Page",
                command=_quit
            ).place(relx=0.8, rely=0.8, anchor="center")
            
            if self._current_page_number != 0:
                ctk.CTkButton(
                    master,
                    text="Back",
                    command=back
                ).place(relx=0.2, rely=0.8, anchor='center')
            
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
            t.configure(state=state)
            t.pack(pady=50)
            
            for action_button in page.buttons:
                ctk.CTkButton(
                    master,
                    text=action_button.text,
                    command=action_button.command,
                    **action_button.kwargs
                ).pack(**{"pady": 20} | page.button_pack_kwargs)
        
        def back():
            master.quit()
            for w in master.winfo_children():
                w.destroy()
            self.logger.debug("Going back a page")
            self._current_page_number-=2
        
        # Driver code
        self._current_page_number = 0
        results = []
        state = content_kwargs.pop("state", "normal")
        
        while self._current_page_number < len(self):
            for w in master.winfo_children():
                w.destroy()
            
            page: InformationSheet | CustomQuestion = self[self._current_page_number]
            if isinstance(page, InformationSheet):
                create_page(page)
            else:
                results+=[page.question(*page.args, **page.kwargs)]
                
                ctk.CTkButton(
                    master,
                    text="Next",
                    command=master.quit
                ).place(relx=0.8, rely=0.8, anchor=tk.CENTER)
                
                ctk.CTkButton(
                    master,
                    text="Back",
                    command=back,
                ).place(relx=0.2, rely=0.8, anchor=tk.CENTER)
                
            master.mainloop()    
            self._current_page_number+=1

        self.logger.debug(results)
        return results
    
    def copy(self) -> InformationPages:
        return self.__copy__()
    
    def __copy__(self) -> InformationPages:
        return InformationPages(*self.logger).add_pages(*self.pages)
            
    def __iadd__(self, __o: InformationSheet, /) -> InformationSheet:
        self.pages += [ __o ]
        return self
        
    def __repr__(self) -> str:
        pages = '\n'.join(self.pages)
        return f"{type(self).__name__}({pages=})"
            
    def __len__(self) -> int:
        return self.pages.__len__()
            
    def __getitem__(self, arg: int | slice) -> InformationSheet:
        return self.pages.__getitem__(arg)
            
    def __iter__(self) -> list:
        return self.pages.__iter__()
