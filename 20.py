import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess

def load_data_from_db(tree, search_query=""):
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    if search_query:
        cursor.execute(
            "SELECT id, eesnimi, perenimi, email, tel, profiilipilt FROM users WHERE eesnimi LIKE ?",
            ("%" + search_query + "%",),
        )
    else:
        cursor.execute("SELECT id, eesnimi, perenimi, email, tel, profiilipilt FROM users")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row[1:], iid=row[0])
    conn.close()

def on_search():
    search_query = search_entry.get()
    load_data_from_db(tree, search_query)

def lisa_andmeid():
    subprocess.Popen(["python", "19.py"], shell=True)

root = tk.Tk()
root.title("Kasutajad")

frame = tk.Frame(root)
frame.pack(pady=20, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree = ttk.Treeview(
    frame,
    yscrollcommand=scrollbar.set,
    columns=("eesnimi", "perenimi", "email", "tel", "profiilipilt"),
    show="headings",
)
tree.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=tree.yview)

tree.heading("eesnimi", text="Eesnimi")
tree.heading("perenimi", text="Perenimi")
tree.heading("email", text="Email")
tree.heading("tel", text="Telefon")
tree.heading("profiilipilt", text="Pilt")

tree.column("eesnimi", width=150)
tree.column("perenimi", width=100)
tree.column("email", width=150)
tree.column("tel", width=100)
tree.column("profiilipilt", width=100)

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Otsi eesnime järgi:")
search_label.pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=10)

search_button = tk.Button(search_frame, text="Otsi", command=on_search)
search_button.pack(side=tk.LEFT)

lisa_button = tk.Button(root, text="Lisa andmeid", command=lisa_andmeid)
lisa_button.pack(pady=10)

load_data_from_db(tree)
root.mainloop()
