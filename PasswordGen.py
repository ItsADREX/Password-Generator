import tkinter as tk
from tkinter import ttk
import random
import string

class PasswordGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")
        master.geometry("400x450")
        master.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.create_widgets()
        self.generate_password()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Password Generator", font=('Helvetica', 16, 'bold')).grid(column=0, row=0, columnspan=2, pady=10)

        ttk.Label(main_frame, text="Password Length:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.length_var = tk.IntVar(value=12)
        length_scale = ttk.Scale(main_frame, from_=6, to=30, orient="horizontal", variable=self.length_var, 
                                 command=self.update_password, style="Custom.Horizontal.TScale")
        length_scale.grid(column=0, row=2, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.length_label = ttk.Label(main_frame, text="12")
        self.length_label.grid(column=1, row=1, sticky=tk.E)

        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, width=40, font=('Courier', 10))
        password_entry.grid(column=0, row=3, columnspan=2, pady=10)

        self.show_password = tk.BooleanVar(value=False)
        show_password_check = ttk.Checkbutton(main_frame, text="Show Password", variable=self.show_password, command=self.toggle_password_visibility)
        show_password_check.grid(column=0, row=4, columnspan=2, sticky=tk.W, pady=5)

        generate_button = ttk.Button(main_frame, text="Generate Password", command=self.generate_password, style="Accent.TButton")
        generate_button.grid(column=0, row=5, sticky=tk.W, pady=10)

        copy_button = ttk.Button(main_frame, text="Copy Password", command=self.copy_password)
        copy_button.grid(column=1, row=5, sticky=tk.E, pady=10)

        self.strength_var = tk.StringVar(value="Weak")
        strength_label = ttk.Label(main_frame, text="Password Strength:")
        strength_label.grid(column=0, row=6, sticky=tk.W, pady=5)
        strength_indicator = ttk.Label(main_frame, textvariable=self.strength_var, font=('Helvetica', 10, 'bold'))
        strength_indicator.grid(column=1, row=6, sticky=tk.E, pady=5)

        self.create_custom_styles()

    def create_custom_styles(self):
        self.style.configure("TLabel", font=('Helvetica', 10))
        self.style.configure("TButton", font=('Helvetica', 10))
        self.style.configure("TCheckbutton", font=('Helvetica', 10))
        self.style.configure("Custom.Horizontal.TScale", resolution=1)

        self.style.configure("Accent.TButton", background="#4CAF50", foreground="white")
        self.style.map("Accent.TButton",
                       background=[('active', '#45a049'), ('pressed', '#3e8e41')])

    def generate_password(self):
        length = self.length_var.get()
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_var.set(password)
        self.update_password_strength(password)

    def update_password(self, *args):
        self.length_label.config(text=f"{int(self.length_var.get())}")
        self.generate_password()

    def copy_password(self):
        password = self.password_var.get()
        self.master.clipboard_clear()
        self.master.clipboard_append(password)
        self.master.update()

    def toggle_password_visibility(self):
        password_entry = self.master.nametowidget(".!frame.!entry")
        if self.show_password.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    def update_password_strength(self, password):
        length = len(password)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)

        strength = sum([has_lower, has_upper, has_digit, has_special])

        if length < 8 or strength < 3:
            self.strength_var.set("Weak")
        elif length < 12 or strength < 4:
            self.strength_var.set("Moderate")
        else:
            self.strength_var.set("Strong")

root = tk.Tk()
app = PasswordGenerator(root)
root.mainloop()