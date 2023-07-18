import tkinter as tk
import requests
import tkinter.ttk as ttk
import json

YourAPI = "ENTER_YOUR_API_HERE"

def update_profit():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        if response.status_code == 200 and response.headers.get("content-type") == "application/json":
            data = response.json()
            invested = data["invested"]
            total = data["total"]
            free = data["free"]
            profit = total - invested - free

            if profit > 0:
                profit_label.config(text="+" + "{:.2f}".format(profit) + "€", fg="green")
            else:
                profit_label.config(text="-" + "{:.2f}".format(abs(profit)) + "€", fg="red")
        else:
            print("Invalid JSON response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Request Error:", e)
    except json.decoder.JSONDecodeError as e:
        print("JSON Decode Error:", e)
    
    root.after(60000, update_profit)

def on_drag_start(event):
    root.x = event.x
    root.y = event.y

def on_drag_motion(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"{width}x{height+15}+{x}+{y}")

url = "https://live.trading212.com/api/v0/equity/account/cash"
headers = {"Authorization": YourAPI}

# Create the tkinter root window
root = tk.Tk()

# Make the window background transparent
root.wm_attributes("-transparentcolor", "blue")  # Change "blue" to the desired transparent color

style = ttk.Style()
style.configure("Transparent.TLabel", background="grey", padding=10)

# Hide the title bar and remove decorations
root.overrideredirect(True)

# Set the size of the widget
width = 180
height = 60

# Create a label to display the profit value
label1 = tk.Label(root, font=("Arial", 20), text="", bg="white")
label1.config(text="Trading212")
label1.pack(fill=tk.BOTH, expand=True)

# Create a label to display the profit value
profit_label = tk.Label(root, font=("Arial", 20), text="", bg="white")
profit_label.pack(fill=tk.BOTH, expand=True)

# Bind mouse events for dragging the widget
label1.bind("<ButtonPress-1>", on_drag_start)
label1.bind("<B1-Motion>", on_drag_motion)
profit_label.bind("<ButtonPress-1>", on_drag_start)
profit_label.bind("<B1-Motion>", on_drag_motion)

# Start the initial update
update_profit()

# Start the tkinter main loop
root.mainloop()
