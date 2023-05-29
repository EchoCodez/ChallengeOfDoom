import customtkinter as ctk

class Medicine:
    def __init__(self, master):
        self.master = master
        self.labels = {
            0: "Medicine Name",
            1: "Dose",
            2: "Timing",
            3: "Route",
            4: "Before/After Meal"
        }
        
    def run(self):
        for i in range(5):
            label = ctk.CTkLabel(
                self.master,
                text=self.labels[i]
            ).grid(row=0, column=i, padx=20, pady=20)

        self.master.mainloop()


if __name__ == "__main__":
    medicine = Medicine(ctk.CTk())
    medicine.run()