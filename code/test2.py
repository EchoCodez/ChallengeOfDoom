import customtkinter as ctk

# Create the root window
root = ctk.CTk()

# Set the window title
root.title("Dark or Light Mode?")

# Set the appearance mode of the root window to "light"
ctk.set_appearance_mode("light")

# Create a label
label = ctk.CTkLabel(root, text="Please choose your preferred mode:", font=("Arial", 20))

# Create a variable to hold the selected mode
selected_mode = ctk.StringVar(master=root)

# Create a radio button for light mode
light_mode = ctk.CTkRadioButton(root, text="Light Mode", variable=selected_mode, value="light", font=("Arial", 16))

# Create a radio button for dark mode
dark_mode = ctk.CTkRadioButton(root, text="Dark Mode", variable=selected_mode, value="dark", font=("Arial", 16))

# Create a button to submit the selection
submit_button = ctk.CTkButton(root, text="Submit", font=("Arial", 16))

# Add the label and radio buttons to the root window
label.pack(pady=20)
light_mode.pack(pady=10)
dark_mode.pack(pady=10)
submit_button.pack(pady=20)

# Function to handle the user's selection
def handle_selection():
    if selected_mode.get() == "light":
        ctk.set_appearance_mode("light")
    elif selected_mode.get() == "dark":
        ctk.set_appearance_mode("dark")

# Bind the submit button to the handle_selection function
submit_button.bind("<Button-1>", lambda event: handle_selection())

# Start the main event loop
root.mainloop()
