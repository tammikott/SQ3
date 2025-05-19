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

def update_record(record_id, entries, window):
    try:
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
    except Exception as e:
        messagebox.showerror("Viga", f"Andmete uuendamine ebaõnnestus: {e}")

def open_update_window(record_id):
    update_window = tk.Toplevel(root)
    update_window.title("Muuda andmeid")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT eesnimi, perenimi, email, tel, profiilipilt FROM users WHERE id=?", (record_id,))
    record = cursor.fetchone()
    conn.close()

    if not record:
        messagebox.showerror("Viga", "Rida ei leitud.")
        return

    labels = ["Eesnimi", "Perenimi", "Email", "Telefon", "Profiilipilt"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(update_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(update_window, width=40)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, record[i])
        entries[label] = entry

    tk.Button(update_window, text="Salvesta", command=lambda: update_record(record_id, entries, update_window)).grid(
        row=len(labels), column=0, columnspan=2, pady=10
    )

def on_update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Valik puudub", "Palun vali rida mida muuta!")
        return
    record_id = selected_item
    open_update_window(record_id)

def on_delete():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Valik puudub", "Palun vali rida kustutamiseks!")
        return

    confirm = messagebox.askyesno("Kustutamise kinnitus", "Kas oled kindel, et soovid selle rea kustutada?")
    if not confirm:
        return

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (selected_item,))
        conn.commit()
        conn.close()

        load_data_from_db(tree)
        messagebox.showinfo("Kustutatud", "Rida kustutati edukalt.")
    except Exception as e:
        messagebox.showerror("Viga", f"Kustutamine ebaõnnestus: {e}")

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
lisa_button.pack(pady=5)

update_button = tk.Button(root, text="Uuenda", command=on_update)
update_button.pack(pady=5)

delete_button = tk.Button(root, text="Kustuta", command=on_delete)
delete_button.pack(pady=5)

load_data_from_db(tree)
root.mainloop()
