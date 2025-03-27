import tkinter as tk
from tkinter import messagebox
import requests

SERVER_URL = "http://127.0.0.1:5000/signup"  # Your Flask server URL


def signup():
    email = email_entry.get()
    password = password_entry.get()
    nickname = nickname_entry.get()

    if not email or not password or not nickname:
        messagebox.showerror("Error", "All fields are required!")
        return

    data = {"email": email, "password": password, "nickname": nickname}

    try:
        response = requests.post(SERVER_URL, json=data)
        result = response.json()
        messagebox.showinfo("Signup", result.get("message", "Unknown response"))

        if response.status_code == 200:
            root.destroy()  # Close the window if signup is successful

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request failed: {e}")


# Create Tkinter window
root = tk.Tk()
root.title("Sign Up")

# Email input
tk.Label(root, text="Email:").pack()
email_entry = tk.Entry(root)
email_entry.pack()

# Password input
tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Nickname input
tk.Label(root, text="Nickname:").pack()
nickname_entry = tk.Entry(root)
nickname_entry.pack()

# Signup button
signup_button = tk.Button(root, text="Sign Up", command=signup)
signup_button.pack()

# Run Tkinter
root.mainloop()
