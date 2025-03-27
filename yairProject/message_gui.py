import tkinter as tk
from tkinter import messagebox
import requests

# Function to load messages from the server
def load_messages():
    url = 'http://127.0.0.1:5000/messages'  # Flask server URL
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        messages_box.delete(1.0, tk.END)  # Clear previous messages

        # Display messages
        for msg in data:
            messages_box.insert(tk.END, f"{msg['sender']}: {msg['text']}\n")
    else:
        messagebox.showerror("Error", "Failed to load messages")

# Function to send a message
def send_message():
    recipient_id = entry_recipient_id.get()
    text = entry_message.get()

    if recipient_id and text:
        url = 'http://127.0.0.1:5000/send_message'  # Flask server URL
        payload = {'recipient_id': recipient_id, 'text': text}
        response = requests.post(url, json=payload)

        data = response.json()
        if response.status_code == 200:
            messagebox.showinfo("Success", data['message'])
            load_messages()  # Refresh messages after sending
        else:
            messagebox.showerror("Error", data['message'])
    else:
        messagebox.showerror("Error", "Please fill in all fields")

# Tkinter setup
root = tk.Tk()
root.title("Messages")
root.geometry("400x400")

# Messages Box (Text widget to display messages)
messages_box = tk.Text(root, height=15, width=40, state=tk.DISABLED, bg="#f9f9f9")
messages_box.pack(padx=10, pady=10)

# Recipient ID input
label_recipient = tk.Label(root, text="Recipient ID")
label_recipient.pack(padx=10)
entry_recipient_id = tk.Entry(root, width=40)
entry_recipient_id.pack(padx=10)

# Message input
label_message = tk.Label(root, text="Message")
label_message.pack(padx=10)
entry_message = tk.Entry(root, width=40)
entry_message.pack(padx=10)

# Send button
btn_send_message = tk.Button(root, text="Send Message", command=send_message)
btn_send_message.pack(pady=10)

# Load messages when the application starts
load_messages()

# Start the Tkinter loop
root.mainloop()
