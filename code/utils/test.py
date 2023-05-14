from typing import Tuple, Union, Callable
import customtkinter as ctk
import tkinter as tk
from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.widgets.core_rendering import DrawEngine


class CTkCalender(ctk.CTkBaseClass):
    def __init__(
        self,
        master: ctk.CTk,
        width: int = 560,
        height: int = 204,
        fg_color = None,
        bg_color: str | Tuple[str, str] = "transparent",
        command = lambda: None,
        text="",
        textvariable = None,
        anchor="center",
        **kwargs
        ):
        super().__init__(
            master=master,
            width=width,
            height=height,
            bg_color=bg_color,
            **kwargs
            )
        
        # color
        self._fg_color: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"]["fg_color"] if fg_color is None else self._check_color_type(fg_color, transparency=True)
        # self._hover_color: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"]["hover_color"] if hover_color is None else self._check_color_type(hover_color)
        # self._border_color: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"]["border_color"] if border_color is None else self._check_color_type(border_color)
        # self._text_color: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"]["text_color"] if text_color is None else self._check_color_type(text_color)
        # self._text_color_disabled: Union[str, Tuple[str, str]] = ThemeManager.theme["CTkButton"]["text_color_disabled"] if text_color_disabled is None else self._check_color_type(text_color_disabled)

        # text, font
        # self._text = text
        self._text_label: Union[tk.Label, None] = None
        self._textvariable: tk.Variable = textvariable
        # self._font: Union[tuple, ctk.CTkFont] = ctk.CTkFont() if font is None else self._check_font_type(font)
        if isinstance(self._font, ctk.CTkFont):
            self._font.add_size_configure_callback(self._update_font)

        # other
        # self._state: str = state
        # self._hover: bool = hover
        self._command: Callable = command
        # self._compound: str = compound
        self._anchor: str = anchor
        self._click_animation_running: bool = False

        # canvas and draw engine
        self._canvas = ctk.CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._desired_width),
                                 height=self._apply_widget_scaling(self._desired_height))
        self._canvas.grid(row=0, column=0, rowspan=5, columnspan=5, sticky="nsew")
        self._draw_engine = DrawEngine(self._canvas)
        self._draw_engine.set_round_to_even_numbers(self._round_width_to_even_numbers, self._round_height_to_even_numbers)  # rendering options

        # configure cursor and initial draw
        self._create_bindings()
        self._set_cursor()
        self._draw()
        
        self._create_bindings() # TODO?
        self._set_cursor() # TODO?
        self._draw()
    
    def _set_cursor(self):
        pass
    def _create_bindings(self):
        pass

class App(ctk.CTk):
    def __init__(self, fg_color = None):
        super().__init__(fg_color=fg_color)
        self.run()
    
    def run(self):
        CTkCalender(self).pack()
        self.mainloop()

        

if __name__ == "__main__":
    app = App()
    app.mainloop()
