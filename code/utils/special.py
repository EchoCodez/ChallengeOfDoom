from utils import jsonUtils
import customtkinter as ctk
import tkinter as tk
from logging import Logger

class Settings:
    def __init__(self, master: ctk.CTk, logger: Logger) -> None:
        self.master = master
        self.logger = logger
        self.logger.debug("Settings Clicked")
        self.show_settings()
    
    def show_settings(self, mainloop=True, font=("", 50)):
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
            ("Toggle Appearance Mode", swap_mode),
            
        )
        # TODO: create bar for button colors
        for name, command in switch_settings:
            self.setting_vars[name] = self.create_switch_setting(name, command=command, font=font),
        
        if mainloop:
            self.master.mainloop()
    
    def create_switch_setting(self, name: str, **kwargs) -> tk.Variable:
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
        font, switch_font = kwargs.pop("font"), kwargs.pop("switch_font", None)
        var = kwargs.pop("var", tk.StringVar())
        switch_kwargs = kwargs.pop("switch_place_kwargs", {"relx":0.7, "rely":0.1, "anchor":tk.CENTER})
        label_kwargs = kwargs.pop("label_place_kwargs", {"relx":0.2, "rely":0.1, "anchor":tk.CENTER})
        on, off = kwargs.pop("on_off", ("on", "off"))
        command = kwargs.pop("command")
        switch_creation_kwargs, label_creation_kwargs = kwargs.pop("switch_kwargs", {}), kwargs.pop("label_kwargs", {})
        
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

