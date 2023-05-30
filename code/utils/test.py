import customtkinter as ctk
import tkinter as tk

root = ctk.CTk()

ctk.CTkButton(
    root,
    text="End",
    command=exit
).place(relx=.5, rely=.5, anchor=tk.CENTER)
root.bind("<Button-3>", exit)
root.mainloop()
