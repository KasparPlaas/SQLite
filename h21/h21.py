import tkinter as tk
from tkinter import ttk
import sqlite3
import subprocess
from tkinter import messagebox


#Funktsioon, mis laadib andmed SQLite andmebaasist ja sisestab need Treeview tabelisse
def load_data_from_db(tree, search_query=""):

    # Puhasta Treeview tabel enne uute andmete lisamist
    for item in tree.get_children():
        tree.delete(item)

    # Loo ühendus SQLite andmebaasiga
    conn = sqlite3.connect('.\kplaas.db')
    cursor = conn.cursor()

    # Tee päring andmebaasist andmete toomiseks
    if search_query:
        cursor.execute("SELECT id, eesnimi, perenimi, email, tel, profiilipilt FROM users WHERE eesnimi LIKE ?", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT id, eesnimi, perenimi, email, tel, profiilipilt FROM users")

    rows = cursor.fetchall()


    # Lisa andmed tabelisse
    for row in rows:
        tree.insert("", "end", values=row[1:], iid=row[0])

    # Sulge ühendus andmebaasiga
    conn.close()



def on_search():
    search_query = search_entry.get()
    load_data_from_db(tree, search_query)



def add_data():
    subprocess.run(["python", ".\h19\h19.py"])

def on_update():
    selected_item = tree.selection()  # Võta valitud rida
    if selected_item:
        record_id = selected_item[0]  # iid (ID)
        open_update_window(record_id)
    else:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")



def open_update_window(record_id):
    # Loo uus aken
    update_window = tk.Toplevel(root)
    update_window.title("Muuda kasutaja andmeid")

    # Loo andmebaasi ühendus ja toomine olemasolevad andmed
    conn = sqlite3.connect('.\kplaas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT eesnimi, perenimi, email, tel, profiilipilt FROM users WHERE id=?", (record_id,))
    record = cursor.fetchone()
    conn.close()

    # Veergude nimed ja vastavad sisestusväljad
    labels = ["eesnimi", "perenimi", "email", "tel", "profiilipilt"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(update_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
        entry = tk.Entry(update_window, width=50)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, record[i])
        entries[label] = entry

    # Salvestamise nupp
    save_button = tk.Button(update_window, text="Salvesta", command=lambda: update_record(record_id, entries, update_window))
    save_button.grid(row=len(labels), column=0, columnspan=2, pady=10)



def update_record(record_id, entries, window):
    eesnimi_kt = entries["eesnimi"].get()
    perenimi_kt = entries["perenimi"].get()
    email_kt = entries["email"].get()
    tel_kt = entries["tel"].get()
    profiilipilt_kt = entries["profiilipilt"].get()

    if not eesnimi_kt:
        messagebox.showerror("Viga", "Eesnimi on kohustuslik!")
        return
    if not perenimi_kt:
        messagebox.showerror("Viga", "Perenimi on kohustuslik!")
        return
    if not email_kt:
        messagebox.showerror("Viga", "Email on kohustuslik!")
        return
    if not tel_kt.isdigit():
        messagebox.showerror("Viga", "Telefoni number peab sisaldama ainult numbreid!")
        return
    if not profiilipilt_kt:
        messagebox.showerror("Viga", "Profiilipilt on kohustuslik!")
        return

    try:
        conn = sqlite3.connect('.\kplaas.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET eesnimi=?, perenimi=?, email=?, tel=?, profiilipilt=?
            WHERE id=?
        """, (eesnimi_kt, perenimi_kt, email_kt, tel_kt, profiilipilt_kt, record_id))
        conn.commit()
        conn.close()
        load_data_from_db(tree)
        window.destroy()
        messagebox.showinfo("Salvestamine", "Andmed on edukalt uuendatud!")
    except sqlite3.Error as error:
        print("Tekkis viga:", error)





root = tk.Tk()
root.title("Kasutaja andmete kuvamine")


search_frame = tk.Frame(root)
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Otsi eesnime järgi:")
search_label.pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=10)

search_button = tk.Button(search_frame, text="Otsi", command=on_search)
search_button.pack(side=tk.LEFT)


# avab h19.py
open_button = tk.Button(root, text="Lisa andmeid", command=add_data)
open_button.pack(pady=20)

# Lisa Uuenda nupp, mis näitab selekteeritud rea ID-d
update_button = tk.Button(root, text="Uuenda", command=on_update)
update_button.pack(pady=10)

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

tree.heading("eesnimi", text="eesnimi")
tree.heading("perenimi", text="perenimi")
tree.heading("email", text="email")
tree.heading("tel", text="tel")
tree.heading("profiilipilt", text="profiilipilt")

tree.column("eesnimi", width=100)
tree.column("perenimi", width=60)
tree.column("email", width=100)
tree.column("tel", width=60)
tree.column("profiilipilt", width=60)


# Lisa andmed tabelisse
load_data_from_db(tree)

root.mainloop()