import customtkinter as ctk
import tkinter as tk
from CTkMessagebox import CTkMessagebox


ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.geometry("700x350")

def configure_label():
    if text.get(1.0, tk.END).strip().isnumeric():
        b.configure(text=text.get(1.0, tk.END))
    else:
        print(text.get(1.0, tk.END))
        CTkMessagebox(root, message="Must be a number", icon="cancel")

text = ctk.CTkTextbox(root, width=240, height=45)
text.insert(tk.END, "Type Here")
text.pack()

b = ctk.CTkLabel(root, text="Sample")
b.pack()

l = ctk.CTkButton(root, text="Update", command=configure_label)
l.pack()

root.mainloop()
