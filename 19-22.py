# Muudetud failinimi: users.db

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
        cursor.execute(
            "SELECT id, eesnimi, perenimi, email, tel, profiilipilt FROM users"
        )
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row[1:], iid=row[0])
    conn.close()

def on_search():
    search_query = search_entry.get()
    load_data_from_db(tree, search_query)

def lisa_andmeid():
    subprocess.Popen(["python", "01.py"], shell=True)

def update_record(record_id, entries, window):
    eesnimi = entries["Eesnimi"].get()
    perenimi = entries["Perenimi"].get()
    email = entries["Email"].get()
    tel = entries["Telefon"].get()
    profiilipilt = entries["Profiilipilt"].get()
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET eesnimi=?, perenimi=?, email=?, tel=?, profiilipilt=? WHERE id=?",
        (eesnimi, perenimi, email, tel, profiilipilt, record_id),
    )
    conn.commit()
    conn.close()
    load_data_from_db(tree)
    window.destroy()
    messagebox.showinfo("Salvestamine", "Andmed on edukalt uuendatud!")

def open_update_window(record_id):
    update_window = tk.Toplevel(root)
    update_window.title("Muuda kasutaja andmeid")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT eesnimi, perenimi, email, tel, profiilipilt FROM users WHERE id=?",
        (record_id,),
    )
    record = cursor.fetchone()
    conn.close()
    if record is None:
        messagebox.showerror("Viga", "Valitud rida ei leitud andmebaasist!")
        return
    labels = ["Eesnimi", "Perenimi", "Email", "Telefon", "Profiilipilt"]
    entries = {}
    for i, label in enumerate(labels):
        tk.Label(update_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(update_window, width=50)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, record[i])
        entries[label] = entry
    save_button = tk.Button(
        update_window,
        text="Salvesta",
        command=lambda: update_record(record_id, entries, update_window),
    )
    save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

def on_update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")
        return
    record_id = selected_item
    open_update_window(record_id)

def on_delete():
    selected_item = tree.selection()
    if selected_item:
        record_id = selected_item[0]
        confirm = messagebox.askyesno("Kinnita kustutamine", "Kas oled kindel, et soovid selle rea kustutada?")
        if confirm:
            try:
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id=?", (record_id,))
                conn.commit()
                conn.close()
                load_data_from_db(tree)
                messagebox.showinfo("Edukalt kustutatud", "Rida on edukalt kustutatud!")
            except sqlite3.Error as e:
                messagebox.showerror("Viga", f"Andmebaasi viga: {e}")
    else:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")

root = tk.Tk()
root.title("Kasutajad")

frame = tk.Frame(root)
frame.pack(pady=20, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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
update_button = tk.Button(root, text="Uuenda", command=on_update)
update_button.pack(pady=10)
kustuta_button = tk.Button(root, text="Kustuta", command=on_delete)
kustuta_button.pack(pady=10)

tree = ttk.Treeview(
    frame,
    yscrollcommand=scrollbar.set,
    columns=("id", "eesnimi", "perenimi", "email", "tel", "profiilipilt"),
    show="headings",
)
tree.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=tree.yview)

tree.heading("id", text="eesnimi")
tree.heading("eesnimi", text="eesnimi")
tree.heading("perenimi", text="perenimi")
tree.heading("email", text="gmail")
tree.heading("tel", text="telefoni number")
tree.heading("profiilipilt", text="pilt")

tree.column("id", width=50)
tree.column("eesnimi", width=150)
tree.column("perenimi", width=100)
tree.column("email", width=150)
tree.column("tel", width=100)
tree.column("profiilipilt", width=100)

load_data_from_db(tree)

root.mainloop()
