# import customtkinter as ctk
# import tkinter as tk

# ctk.set_appearance_mode("dark")
# r = ctk.CTk()
# r.geometry("400x400")
# ctk.CTkFrame(r, fg_color="#00FF00", corner_radius=40).place(relx=0.5, rely=0.5, anchor=tk.CENTER) #  rounded frame
# r.mainloop()
import requests

url = "https://priaid-symptom-checker-v1.p.rapidapi.com/body/locations/15"

querystring = {"language":"en-gb"}

headers = {
	"X-RapidAPI-Key": "43a51db6fdmsh6723745eb2e12c3p190edcjsnc405e75fdbbb",
	"X-RapidAPI-Host": "priaid-symptom-checker-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())

