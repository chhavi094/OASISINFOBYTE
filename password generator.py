import random
import string
import tkinter as tk
from tkinter import ttk, messagebox

def generate_password(length, use_uppercase, use_digits, use_special):
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    if not characters:
        return "Error: No character types selected."

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def on_generate():
    try:
        length = int(length_entry.get())
        if length <= 0:
            messagebox.showerror("Input Error", "Please enter a positive integer for the length.")
            return
        
        use_uppercase = uppercase_var.get()
        use_digits = digits_var.get()
        use_special = special_var.get()

        password = generate_password(length, use_uppercase, use_digits, use_special)
        result_var.set(password)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid integer for the length.")

# Set up the main application window
root = tk.Tk()
root.title("Password Generator")
root.geometry("500x350")  # Window size
root.resizable(False, False)

# Style configuration
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 14), padding=10)  # Increased font size
style.configure('TEntry', padding=10, font=('Helvetica', 14))  # Increased font size
style.configure('TButton', font=('Helvetica', 14), padding=10)  # Increased font size
style.configure('TCheckbutton', font=('Helvetica', 14), padding=5)  # Increased font size

# Main frame
frame = ttk.Frame(root, padding="20 20 20 20")
frame.pack(fill='both', expand=True)

# Length input
ttk.Label(frame, text="Enter the desired length of the password:").grid(column=0, row=0, columnspan=2, sticky='W')
length_entry = ttk.Entry(frame, width=25)  # Adjusted width
length_entry.grid(column=1, row=1, sticky='W')

# Character type options
uppercase_var = tk.BooleanVar()
digits_var = tk.BooleanVar()
special_var = tk.BooleanVar()

ttk.Checkbutton(frame, text="Include uppercase letters", variable=uppercase_var).grid(column=0, row=2, columnspan=2, sticky='W')
ttk.Checkbutton(frame, text="Include digits", variable=digits_var).grid(column=0, row=3, columnspan=2, sticky='W')
ttk.Checkbutton(frame, text="Include special characters", variable=special_var).grid(column=0, row=4, columnspan=2, sticky='W')

# Generate button
generate_button = ttk.Button(frame, text="Generate Password", command=on_generate)
generate_button.grid(column=0, row=5, columnspan=2, pady=10)

# Result display
result_var = tk.StringVar()
ttk.Entry(frame, textvariable=result_var, state='readonly', width=50).grid(column=0, row=6, columnspan=2, pady=5)  # Adjusted width

# Set padding for all child widgets of the main frame
for child in frame.winfo_children():
    child.grid_configure(padx=10, pady=5)

# Run the application
root.mainloop()
