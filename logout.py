import tkinter as tk
from tkinter import ttk, messagebox
from database import get_db_connection, init_db
import sqlite3

class UserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Authentication")
        self.root.geometry("880x540")
        self.root.configure(bg="#e9edf0")
        self.root.resizable(False, False)

        # Initialize database
        init_db()

        # Theme Colors & Fonts
        self.primary_color = "#003366"
        self.accent_color = "#007acc"
        self.success_color = "#28a745"
        self.hover_success = "#218838"
        self.font = ("Segoe UI", 11)

        style = ttk.Style()
        style.configure("TEntry", padding=8, font=self.font)

        self.show_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_panel(self, bg_color, title, subtitle):
        panel = tk.Frame(self.root, width=300, bg=bg_color)
        panel.pack(side="left", fill="y")

        tk.Label(panel, text=title, font=("Segoe UI", 22, "bold"), bg=bg_color, fg="white").pack(pady=(100, 10))
        tk.Label(panel, text=subtitle, font=("Segoe UI", 11), bg=bg_color, fg="white", wraplength=240, justify="center").pack(pady=10)
        return panel

    def create_form_frame(self):
        shadow = tk.Frame(self.root, bg="#cbd2d9")
        shadow.place(x=310, y=60, width=530, height=420)

        frame = tk.Frame(self.root, bg="white", bd=0)
        frame.place(x=300, y=50, width=530, height=420)

        return frame

    def styled_button(self, parent, text, bg, hover_bg, command):
        btn = tk.Button(parent, text=text, font=self.font, bg=bg, fg="white", width=25, relief="flat",
                        activebackground=hover_bg, activeforeground="white", command=command, cursor="hand2", bd=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def show_login(self):
        self.clear_window()
        self.create_panel(self.primary_color, "Welcome Back!", "Log in to manage your account")
        frame = self.create_form_frame()

        tk.Label(frame, text="Sign In", font=("Segoe UI", 20, "bold"), fg=self.primary_color, bg="white").pack(pady=(20, 30))

        self.login_email = ttk.Entry(frame, width=40)
        self.set_placeholder(self.login_email, "Email Address")
        self.login_email.pack(pady=10)

        self.login_password = ttk.Entry(frame, width=40)
        self.set_password_placeholder(self.login_password, "Password")
        self.login_password.pack(pady=10)

        login_btn = self.styled_button(frame, "Login", self.primary_color, self.accent_color, self.validate_login)
        login_btn.pack(pady=25)

        tk.Button(frame, text="Create an account", font=("Segoe UI", 10, "underline"), fg=self.accent_color,
                  bg="white", bd=0, cursor="hand2", command=self.show_register).pack()

    def show_register(self):
        self.clear_window()
        self.create_panel(self.accent_color, "New Here?", "Create an account to get started")
        frame = self.create_form_frame()

        tk.Label(frame, text="Register", font=("Segoe UI", 20, "bold"), fg=self.accent_color, bg="white").pack(pady=(20, 20))

        self.reg_name = ttk.Entry(frame, width=40)
        self.set_placeholder(self.reg_name, "Full Name")
        self.reg_name.pack(pady=8)

        self.reg_email = ttk.Entry(frame, width=40)
        self.set_placeholder(self.reg_email, "Email")
        self.reg_email.pack(pady=8)

        self.reg_password = ttk.Entry(frame, width=40)
        self.set_password_placeholder(self.reg_password, "Password")
        self.reg_password.pack(pady=8)

        self.reg_confirm = ttk.Entry(frame, width=40)
        self.set_password_placeholder(self.reg_confirm, "Confirm Password")
        self.reg_confirm.pack(pady=8)

        self.terms_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="I agree to the Terms & Conditions", variable=self.terms_var, bg="white", font=("Segoe UI", 9)).pack(pady=10)

        reg_btn = self.styled_button(frame, "Register", self.success_color, self.hover_success, self.validate_register)
        reg_btn.pack(pady=15)

        tk.Button(frame, text="Back to Login", font=("Segoe UI", 10, "underline"), fg=self.accent_color,
                  bg="white", bd=0, cursor="hand2", command=self.show_login).pack()

    def validate_login(self):
        email = self.login_email.get()
        password = self.login_password.get()

        if email == "Email Address" or password == "Password":
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                messagebox.showinfo("Login", "Logged in successfully!")
                self.root.destroy()
                # Lazy import to avoid circular dependency
                from main import StudentResultSystem
                # Launch the main app
                root = tk.Tk()
                app = StudentResultSystem(root)
                root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid email or password!")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")

    def validate_register(self):
        name = self.reg_name.get()
        email = self.reg_email.get()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()

        if not self.terms_var.get():
            messagebox.showwarning("Terms", "You must accept the terms.")
            return
        if name == "Full Name" or email == "Email" or password == "Password" or confirm == "Confirm Password":
            messagebox.showerror("Error", "All fields are required.")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        try:
            conn = get_db_connection()
            if conn is None:
                messagebox.showerror("Error", "Failed to connect to the database!")
                return
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists!")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def set_placeholder(self, entry, text):
        entry.insert(0, text)
        entry.configure(foreground="grey")
        entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, entry, text))
        entry.bind("<FocusOut>", lambda e: self.add_placeholder(e, entry, text))

    def set_password_placeholder(self, entry, text):
        entry.insert(0, text)
        entry.configure(foreground="grey")
        entry.bind("<FocusIn>", lambda e: self.clear_password(e, entry, text))
        entry.bind("<FocusOut>", lambda e: self.add_password(e, entry, text))

    def clear_placeholder(self, event, entry, text):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.configure(foreground="black")

    def add_placeholder(self, event, entry, text):
        if not entry.get():
            entry.insert(0, text)
            entry.configure(foreground="grey")

    def clear_password(self, event, entry, text):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.configure(show="*", foreground="black")

    def add_password(self, event, entry, text):
        if not entry.get():
            entry.insert(0, text)
            entry.configure(show="", foreground="grey")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserApp(root)
    root.mainloop()