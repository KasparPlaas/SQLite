# Jätkame ülesanne 17 ja 18 kasutatud andmebaasiga.
# Kursuste andmebaas
# Spordiklubi andmebaas
# Raamatukogu andmebaas
# Majutuse andmebaas
# Loo oma andmebaasile graafiline liides andmete lisamiseks.
# Muuda välja kohustuslikuks ja loo vastav teade
# Loo teatekast, mis teavitab edukast või ebaõnnestunud lisamisest

import sqlite3
import tkinter as tk
from tkinter import messagebox


def validate_data():
    eesnimi_kt = entries["eesnimi"].get()
    perenimi_kt = entries["perenimi"].get()
    email_kt = entries["email"].get()
    tel_kt = entries["tel"].get()
    profiilipilt_kt = entries["profiilipilt"].get()

    if not eesnimi_kt:
        messagebox.showerror("Viga", "Eesnimi on kohustuslik!")
        return False
    if not perenimi_kt:
        messagebox.showerror("Viga", "Perenimi on kohustuslik!")
        return False
    if not email_kt:
        messagebox.showerror("Viga", "Email on kohustuslik!")
        return False
    if not tel_kt.isdigit():
        messagebox.showerror("Viga", "Telefoni number on kohustuslik ja sisaldama ainult numbreid!")
        return False
    if not profiilipilt_kt:
        messagebox.showerror("Viga", "Profiilipilt on kohustuslik!")
        return False

    return True



def insert_data():
    if validate_data():
        try:


            connection = sqlite3.connect(".\kplaas.db")
            cursor = connection.cursor()
            print("Andmebaasiga ühendus loodud")

            cursor.execute("""
                INSERT INTO users (eesnimi, perenimi, email, tel, profiilipilt)
                VALUES (?, ?, ?, ?, ?)
            """, (
                entries["eesnimi"].get(),
                entries["perenimi"].get(),
                entries["email"].get(),
                entries["tel"].get(),
                entries["profiilipilt"].get()
            ))


        except sqlite3.Error as error:
            print("Tekkis viga andmebaasiga ühendamisel või päringu teostamisel:", error)


        finally:
            if connection:
                connection.commit()
                connection.close()
                clear_entries()
                print("Ühendus suleti")
                messagebox.showinfo("Edu", "Andmed sisestati edukalt!")



def clear_entries():
    for entry in entries.values():
        entry.delete(0, tk.END)



root = tk.Tk()
root.title("Kasutaja andmete sisestamine")

# Loo sildid ja sisestusväljad
labels = ["eesnimi", "perenimi", "email", "tel", "profiilipilt"]
entries = {}

for i, label in enumerate(labels):
    tk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5)
    entry = tk.Entry(root, width=40)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[label] = entry

# Loo nupp andmete sisestamiseks
submit_button = tk.Button(root, text="Sisesta andmed", command=insert_data)
submit_button.grid(row=len(labels), column=0, columnspan=2, pady=20)

# Näita Tkinteri akent
root.mainloop()