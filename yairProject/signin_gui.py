import tkinter as tk
from tkinter import messagebox
import requests

def sign_in():
    email = entry_email.get()
    password = entry_password.get()

    if email and password:
        url = 'http://127.0.0.1:5000/signin'  # Flask server URL
        payload = {'email': email, 'password': password}
        response = requests.post(url, json=payload)

        data = response.json()
        if response.status_code == 200:
            messagebox.showinfo("Success", data['message'])
            root.quit()  # Close the sign-in window
        else:
            messagebox.showerror("Error", data['message'])
    else:
        messagebox.showerror("Error", "Please fill all fields")

# Tkinter setup
root = tk.Tk()
root.title("Sign In")
root.geometry("300x300")

label_email = tk.Label(root, text="Email")
label_email.pack()
entry_email = tk.Entry(root)
entry_email.pack()

label_password = tk.Label(root, text="Password")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

btn_signin = tk.Button(root, text="Sign In", command=sign_in)
btn_signin.pack()

root.mainloop()
