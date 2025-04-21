from tkinter import Tk, Frame, Label, Button, PhotoImage
from tkinter.ttk import Notebook, Entry
from main import knapSack
from PIL import ImageTk, Image
import sqlite3

# --- Database Setup ---
conn = sqlite3.connect('backpack_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS backpack_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_items INTEGER,
    capacity INTEGER,
    weights TEXT,
    item_values TEXT
)
''')
conn.commit()

# --- Save Function ---
def save_to_database(num_items, capacity, weights, values):
    weights_str = ','.join(map(str, weights))
    values_str = ','.join(map(str, values))
    cursor.execute('''
        INSERT INTO backpack_data (num_items, capacity, weights, item_values)
        VALUES (?, ?, ?, ?)
    ''', (num_items, capacity, weights_str, values_str))
    conn.commit()

# --- GUI Constants ---
_BACKGROUNDCOLOR = "#ECD3CB"
_BACKGROUNDCOLOR_VARIANT = "#a5938e"

# --- Main Window Setup ---
window = Tk()
window.title("Backpack Optimizer")
window.geometry("1280x720")
window["bg"] = _BACKGROUNDCOLOR

title = Label(window, text="Backpack Optimizer", font=('Arial', 27), bg=_BACKGROUNDCOLOR)
title.pack(padx=20, pady=20)

img = ImageTk.PhotoImage(Image.open("logo.png"))
logo = Label(window, image=img, bg=_BACKGROUNDCOLOR)
logo.pack(fill="both")

image_container = Frame(window, bg=_BACKGROUNDCOLOR)
sack_image = ImageTk.PhotoImage(Image.open("sackR.png"))
sack = Label(image_container, image=sack_image, bg=_BACKGROUNDCOLOR)
sack.pack(side='left', padx=180)

element_image = ImageTk.PhotoImage(Image.open("elementR.png"))
element = Label(image_container, image=element_image, bg=_BACKGROUNDCOLOR)
element.pack(side='right', padx=70)

image_container.pack(fill="both")

container = Frame(window, borderwidth=1, bg=_BACKGROUNDCOLOR)
nomber_of_element_entry = Entry(container)
nomber_of_element_entry.pack(side="right", padx=20, pady=10)
nomber_of_element_label = Label(container, text="Number of Items: ", bg=_BACKGROUNDCOLOR)
nomber_of_element_label.pack(side="right", padx=10, pady=10)

box_wight_label = Label(container, text="My Capacity ", bg=_BACKGROUNDCOLOR)
box_wight_label.pack(side="left", padx=5, pady=5)
box_wight_entry = Entry(container)
box_wight_entry.pack(side="left", padx=5, pady=5)
container.pack(fill="both")

# --- Functions ---
def get_values():
    wt = list()
    val = list()
    n = int(nomber_of_element_entry.get())
    wight = int(box_wight_entry.get())

    for i in range(n):
        wt.append(int(tab1.grid_slaves(1, i + 1)[0].get()))
        val.append(int(tab1.grid_slaves(2, i + 1)[0].get()))

    # Save to DB
    save_to_database(n, wight, wt, val)

    # Get result from knapsack
    max_val, elem = knapSack(wight, wt, val)
    result = f"Maximum Capacity: {max_val}\nThe sequence of elements is: {elem}"
    lab = Label(frame2, text=result, font=('Arial', 22), bg=_BACKGROUNDCOLOR)
    lab.pack(padx=20, pady=20)

def reset_table():
    for widget in frame2.winfo_children():
        widget.destroy()
    frame2.pack_forget()

def print_table():
    global tab1, frame2
    n = int(nomber_of_element_entry.get())

    frame2 = Frame(window, bg=_BACKGROUNDCOLOR)
    frame2.pack(fill="both")

    tablayout = Notebook(frame2)
    tab1 = Frame(tablayout, bg=_BACKGROUNDCOLOR)
    tab1.pack(fill="both")

    for row in range(3):
        for column in range(n + 1):
            if column == 0:
                if row == 1:
                    label = Label(tab1, text="Weight", font=('Arial', 14), bg=_BACKGROUNDCOLOR_VARIANT)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                elif row == 2:
                    label = Label(tab1, text="Value", font=('Arial', 14), bg=_BACKGROUNDCOLOR_VARIANT)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
            else:
                if row == 0:
                    label = Label(tab1, text="Object: " + str(column), font=('Arial', 14), bg=_BACKGROUNDCOLOR_VARIANT)
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                else:
                    entry = Entry(tab1)
                    entry.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)

    tablayout.pack(fill="both")

    calc = Button(frame2, text="Calculate", command=get_values)
    calc.pack(padx=20, pady=20)

    reset = Button(frame2, text="Reset", command=reset_table)
    reset.pack(padx=5, pady=5)

# --- Buttons ---
button = Button(window, text="Add the elements", command=print_table)
button.pack()

# --- Main Loop ---
window.mainloop()
