import tkinter as tk


def main():
	root = tk.Tk()
	width, height = root.winfo_screenwidth(), root.winfo_screenheight()
	root.geometry(f"{width}x{height}+0+0")
	print(width)
	counter = 0
	padx, pady = 10, 5
 
	for j in range(100): # choose arbitrarily large value
		checkboxes = []
		widths = 0
		for i in range(height//37):
			checkbox = tk.Checkbutton(root, text=f"Check Plus a bunch of blank space and continue {i, j}")
			checkbox.grid(row=i, column=j, pady=pady, padx=padx)
			checkbox.update_idletasks()
			checkboxes.append(checkbox)
			widths = max(widths, checkbox.winfo_width()+padx)
   
		counter+=widths
		if counter>width:
			for box in checkboxes:
				box.destroy()
			break
	root.mainloop()


if __name__ == "__main__":
    main()