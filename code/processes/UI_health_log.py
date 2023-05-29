from datetime import datetime, timedelta
import customtkinter as ctk

def get_previous_month(master: ctk.CTk) -> tuple[tuple[ctk.CTkButton, datetime]]:
    for i in range(1, 31):
        date = (datetime.today()-timedelta(days=i)).strftime("%m/%d/%y")
        yield (ctk.CTkButton(
            master,
            text=date
            ), datetime.strptime(date, "%m/%d/%y"))
