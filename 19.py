import sqlite3
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("andmete sisestamine")


def validate_data():
    enimi = entries["eesnimi"].get()
    pnimi = entries["perenimi"].get()
    email = entries["email"].get()
    tel = entries["telefon"].get()
    pilt = entries["profiilipilt"].get()

    if not enimi or not pnimi or not email or not tel or not pilt:
        tk.messagebox.showerror("Viga", "Väljad on kohustuslikud!")
        return
    
    return True

def insert_data():
    if validate_data():
        try:
            connection = sqlite3.connect("users.db")
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO users3 (eesnimi, perenimi, email, tel, profiilipilt)
                VALUES (?, ?, ?, ?, ?)
            """, (
                entries["eesnimi"].get(),
                entries["perenimi"].get(),
                entries["email"].get(),
                entries["telefon"].get(),  
                entries["profiilipilt"].get(),
            ))

            connection.commit()
            messagebox.showinfo("Edu", "Andmed sisestati edukalt!")
        except sqlite3.Error as e:
            messagebox.showerror("Viga", f"Andmete sisestamine ebaõnnestus: {e}")
        finally:
            connection.close()


labels = ["eesnimi", "perenimi", "email", "telefon", "profiilipilt"]  
entries = {}

for i, label in enumerate(labels):
    tk.Label(root, text=label.capitalize()).grid(row=i, column=0, padx=10, pady=5)
    entry = tk.Entry(root, width=40)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[label] = entry


submit_button = tk.Button(root, text="Sisesta kasutaja", command=insert_data)
submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)


root.mainloop()
