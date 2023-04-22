import tkinter as tk
import customtkinter as ctk
from parse_json import jsonUtils

conditions_list = "conditions.json"
 
class Test:
	def __init__(self) -> None:
		ctk.set_appearance_mode("dark")
		self.__root = ctk.CTk()
		self.__root.geometry(f"{self.__root.winfo_screenwidth()}x{self.__root.winfo_screenheight()}+0+0")


	def main(self):
		self.__root.geometry(f"{self.__root.winfo_screenwidth()}x{self.__root.winfo_screenheight()}+0+0")
		title = ctk.CTkLabel(
			self.__root,
			text="What previous medical conditions do you have?",
			font=("Default", 25)
			)
		next_button = ctk.CTkButton(
			self.__root,
			text="Continue",
			command=lambda: print({key: value.get() for key, value in self.conditions.items()})
			)
		title.grid(column=0, columnspan=5, padx=5, pady=5)
		self.conditions = {}
		row, col = 0, 0
		for name in (d["disease"] for d in jsonUtils.open(conditions_list)):
			self.conditions[name]=tk.BooleanVar(value=False)
			checkbox = ctk.CTkCheckBox(
				self.__root, text=name,
				variable=self.conditions[name],
				onvalue=True,
				offvalue=False
				)
			checkbox.grid(pady=5, sticky=tk.W, padx=10) # goes off screen because only 29 diseases are allowed
		next_button.grid(pady=5)
			
		self.__root.mainloop()

Test().main()