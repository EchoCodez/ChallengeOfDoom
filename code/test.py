import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")
r = ctk.CTk()
r.geometry("400x400")
ctk.CTkFrame(r, fg_color="#00FF00", corner_radius=40).place(relx=0.5, rely=0.5, anchor=tk.CENTER) #  rounded frame
r.mainloop()

