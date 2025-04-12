import tkinter as tk
from tkinter import ttk
import sqlite3

#Funktsioon, mis laadib andmed SQLite andmebaasist ja sisestab need Treeview tabelisse
def load_data_from_db(tree):
    # Loo ühendus SQLite andmebaasiga
    conn = sqlite3.connect('.\kplaas.db')
    cursor = conn.cursor()

    # Tee päring andmebaasist andmete toomiseks
    if search_query:
        cursor.execute("SELECT id, eesnimi, perenimi, email, tel, profiilipilt FROM users WHERE title LIKE ?", ('%' + search_query + '%',))
    else:
cursor.execute("SELECT id, eesnimi, perenimi, email, tel, profiilipilt FROM users")
    rows = cursor.fetchall()


    # Lisa andmed tabelisse
    for row in rows:
        tree.insert("", "end", values=row)

    # Sulge ühendus andmebaasiga
    conn.close()

root = tk.Tk()
root.title("Kasutaja andmete kuvamine")


# Loo raam kerimisribaga
frame = tk.Frame(root)
frame.pack(pady=20, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Loo tabel (Treeview) andmete kuvamiseks
tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, columns=("id","eesnimi", "perenimi", "email", "tel", "profiilipilt"), show="headings")
tree.pack(fill=tk.BOTH, expand=True)

# Seosta kerimisriba tabeliga
scrollbar.config(command=tree.yview)

# Määra veergude pealkirjad ja laius
tree.heading("id", text="id")
tree.heading("eesnimi", text="eesnimi")
tree.heading("perenimi", text="perenimi")
tree.heading("email", text="email")
tree.heading("tel", text="tel")
tree.heading("profiilipilt", text="profiilipilt")

tree.column("id", width=150)
tree.column("eesnimi", width=100)
tree.column("perenimi", width=60)
tree.column("email", width=100)
tree.column("tel", width=60)
tree.column("profiilipilt", width=60)


# Lisa andmed tabelisse
load_data_from_db(tree)

root.mainloop()