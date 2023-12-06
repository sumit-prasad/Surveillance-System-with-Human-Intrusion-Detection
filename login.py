import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from mysql_db import initialize_connection, login
from home import Homepage
from forgot_password import ForgotPasswordWindow

conn, cursor = initialize_connection()

class LoginWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Surveillance System with Human Intrusion Detection")
        self.master.geometry("1400x720")
        self.master.withdraw()  # Hide the window initially

        # Use ThemedStyle for a dark theme
        style = ThemedStyle(self.master)
        style.set_theme("arc")

        self.configure(bg="#232831")  # Set background color for the main window

        # Create a custom frame with the same appearance as in customtkinter
        frame = tk.Frame(self, width=380, height=450, bg="#2E3B4E", bd=2, relief="solid", borderwidth=5)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame, text="Log into your Account", font=('Century Gothic', 20), bg="#2E3B4E", fg="white").place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.entry1 = ttk.Entry(frame, font=("Helvetica", 12), width=28)
        self.entry1.place(relx=0.5, rely=0.38, anchor=tk.CENTER, height=35, bordermode="inside")
        self.add_placeholder(self.entry1, "Username")

        self.entry2 = ttk.Entry(frame, show="*", font=("Helvetica", 12), width=28)
        self.entry2.place(relx=0.5, rely=0.55, anchor=tk.CENTER, height=35, bordermode="inside")
        self.add_placeholder(self.entry2, "Password")

        # Show password button
        show_password_button = ttk.Checkbutton(frame, text="Show Password", command=self.toggle_password_visibility)
        show_password_button.place(relx=0.70, rely=0.64, anchor=tk.CENTER)
        # "Forgot Password" label
        forgot_password_label = tk.Label(frame, text="Forgot Password?", font=('Century Gothic', 12), bg="#2E3B4E", fg="white", cursor="hand2")
        forgot_password_label.place(relx=0.66, rely=0.71, anchor=tk.CENTER)
        forgot_password_label.bind("<Button-1>", lambda event: self.forgot_password())

        # Error message label
        self.error_label = tk.Label(frame, text="", font=('Helvetica', 12), fg="red", bg="#2E3B4E")
        self.error_label.place(relx=0.5, rely=0.86, anchor=tk.CENTER)

        # Use a regular tk.Button with a custom style
        login_button = tk.Button(frame, text="Login", command=self.submit, font=('Helvetica', 12), width=22, foreground="#2E3B4E", background="#4CAF50")
        login_button.place(relx=0.5, rely=0.80, height=38, anchor=tk.CENTER)

        # Schedule the show_window method to run after a delay
        self.after(50, self.show_window)

        self.pack(fill=tk.BOTH, expand=True)  # Pack to fill the entire window

    def show_window(self):
        # Show the window
        self.master.deiconify()
        # Force geometry update
        self.master.update_idletasks()
        # Make the window resizable
        self.master.resizable(True, True)

    def add_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, entry, placeholder))
        entry.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, entry, placeholder))

    def on_entry_focus_in(self, event, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(show="*" if placeholder == "Password" else "")
            entry["style"] = "TEntry"  # Apply the default style

    def on_entry_focus_out(self, event, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(show="" if placeholder == "Password" else "*")
            entry["style"] = "Placeholder.TEntry"  # Apply the placeholder style

    def toggle_password_visibility(self):
        current_state = self.entry2.cget("show")
        self.entry2["show"] = "" if current_state == "*" else "*"

    def submit(self):
        data = {}
        data["email"] = self.entry1.get()
        data["password"] = self.entry2.get()

        if login(cursor, data):
            print("Successful Login")
            self.show_homepage()
        else:
            self.error_label.config(text="Invalid username/password")

    def show_homepage(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Update the geometry after destroying widgets
        self.master.geometry("1400x720+0+0")
        Homepage(self.master)

    def forgot_password(self):
        self.master.withdraw()
        ForgotPasswordWindow(self.master, self)

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()