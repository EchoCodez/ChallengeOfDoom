import tkinter as tk

def main():
    root = tk.Tk()
    root.geometry("400x600")
    button = tk.Button(root, text="next", command=root.quit)
    button.pack()
    root.mainloop()
    root.geometry("600x400")
    root.mainloop()


if __name__ == "__main__":
    main()