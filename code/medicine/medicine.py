import customtkinter as ctk

class Medicine:
    def __init__(self, master):
        self.master = master
        self.labels = {
            0: "Medicine Name",
            1: "Morning", 
            2: "Afternoon", 
            3: "Evening",
            4: "Before/After Meal",
        }
        
    def run(self):
        for i in range(5):
            ctk.CTkLabel(
                self.master,
                text=self.labels[i]
            ).grid(row=0, column=i, padx=20, pady=20)
        
        ctk.CTkEntry(
            self.master,
            placeholder_text="Enter medicine name"
        ).grid(row=1, column=0, padx=20, pady=20)
        '''ctk.CTkOptionMenu(
            self.master,
            values=["1 tablet", "2 tablets"]
        ).grid(row=1, column=1, padx=20, pady=20)'''
        for i in range(3):
            ctk.CTkEntry(
                self.master,
                placeholder_text="",
                width=30
            ).grid(row=1, column=i+1, padx=20, pady=20)

        self.master.mainloop()


if __name__ == "__main__":
    medicine = Medicine(ctk.CTk())
    medicine.run()