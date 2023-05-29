import customtkinter as ctk

class Medicine:
    def __init__(self, master: ctk.CTk) -> None:
        self.master = master
        self.labels = {
            0: "Medicine Name",
            1: "Morning", 
            2: "Afternoon", 
            3: "Evening",
            4: "Breakfast Time",
            5: "Lunch Time",
            6: "Dinner Time",
            7: "Before/After Meal",
        }
    
    def submit(self, elements) -> None:
        print([element.get() for element in elements])

    def run(self) -> None:
        elements = []
        for i in range(8):
            ctk.CTkLabel(
                self.master,
                text=self.labels[i]
            ).grid(row=0, column=i, padx=20, pady=20)
        
        entry = ctk.CTkEntry(
            self.master,
            placeholder_text="Enter medicine name"
        )
        entry.grid(row=1, column=0, padx=20, pady=20)
        elements.append(entry)
        
        for i in range(3):
            entry = ctk.CTkEntry(
                self.master,
                placeholder_text="",
                width=30
            )
            entry.grid(row=1, column=i+1, padx=20, pady=20)
            elements.append(entry)
        
        for i in range(3):
            entry = ctk.CTkEntry(
                self.master,
                placeholder_text="hh:mm AM/PM",
            )
            entry.grid(row=1, column=i+4, padx=20, pady=20)
            elements.append(entry)

        menu = ctk.CTkOptionMenu(
            self.master,
            values=["Before", "After"]
        )
        menu.grid(row=1, column=7, padx=20, pady=20)
        elements.append(menu)

        
        ctk.CTkButton(
            self.master, 
            text="Submit",
            command=lambda: self.submit(elements)
        ).grid(row=2, column=4, padx=20, pady=20)

        
        self.master.mainloop()


if __name__ == "__main__":
    medicine = Medicine(ctk.CTk())
    medicine.run()