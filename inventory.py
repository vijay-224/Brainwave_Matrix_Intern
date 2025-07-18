import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ---------- AUTHENTICATION ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result is not None

# ---------- PRODUCT MANAGEMENT ----------
def add_product(name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)",
              (name, quantity, price))
    conn.commit()
    conn.close()

def update_product(product_id, name, quantity, price):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor() 
    c.execute("UPDATE products SET name=?, quantity=?, price=? WHERE id=?",
              (name, quantity, price, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

def get_all_products():
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return products

def get_low_stock(threshold=5):
    conn = sqlite3.connect("inventory.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE quantity <= ?", (threshold,))
    products = c.fetchall()
    conn.close()
    return products

# ---------- GUI COMPONENTS ----------
def login_screen():
    def try_login():
        if login_user(username_entry.get(), password_entry.get()):
            messagebox.showinfo("Login", "Login Successful")
            root.destroy()
            main_screen()
        else:
            messagebox.showerror("Login", "Invalid credentials")

    def go_register():
        register_screen()

    root = tk.Tk()
    root.title("Login")
    root.geometry("300x200")

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    tk.Button(root, text="Login", command=try_login).pack(pady=5)
    tk.Button(root, text="Register", command=go_register).pack()

    root.mainloop()

def register_screen():
    def try_register():
        if register_user(username_entry.get(), password_entry.get()):
            messagebox.showinfo("Register", "Registration Successful")
            reg.destroy()
        else:
            messagebox.showerror("Register", "Username already exists")

    reg = tk.Tk()
    reg.title("Register")
    reg.geometry("300x200")

    tk.Label(reg, text="Username").pack()
    username_entry = tk.Entry(reg)
    username_entry.pack()

    tk.Label(reg, text="Password").pack()
    password_entry = tk.Entry(reg, show="*")
    password_entry.pack()

    tk.Button(reg, text="Register", command=try_register).pack(pady=10)

    reg.mainloop()

def main_screen():
    win = tk.Tk()
    win.title("Inventory Management System")
    win.geometry("600x400")

    def refresh_list():
        for row in product_list.get_children():
            product_list.delete(row)
        for prod in get_all_products():
            product_list.insert("", "end", values=prod)

    def add_item():
        name = simpledialog.askstring("Add Product", "Enter Product Name:")
        quantity = simpledialog.askinteger("Add Product", "Enter Quantity:")
        price = simpledialog.askfloat("Add Product", "Enter Price:")
        if name and quantity is not None and price is not None:
            add_product(name, quantity, price)
            refresh_list()

    def delete_item():
        selected = product_list.selection()
        if selected:
            prod_id = product_list.item(selected)["values"][0]
            delete_product(prod_id)
            refresh_list()

    def edit_item():
        selected = product_list.selection()
        if selected:
            item = product_list.item(selected)["values"]
            new_name = simpledialog.askstring("Edit", "Name:", initialvalue=item[1])
            new_quantity = simpledialog.askinteger("Edit", "Quantity:", initialvalue=item[2])
            new_price = simpledialog.askfloat("Edit", "Price:", initialvalue=item[3])
            if new_name and new_quantity is not None and new_price is not None:
                update_product(item[0], new_name, new_quantity, new_price)
                refresh_list()

    def show_low_stock():
        lows = get_low_stock()
        message = "\n".join([f"{row[1]}: {row[2]} in stock" for row in lows])
        if message:
            messagebox.showinfo("Low Stock", message)
        else:
            messagebox.showinfo("Low Stock", "All stocks are sufficient.")

    product_list = ttk.Treeview(win, columns=("ID", "Name", "Qty", "Price"), show="headings")
    for col in ("ID", "Name", "Qty", "Price"):
        product_list.heading(col, text=col)
    product_list.pack(expand=True, fill="both", pady=10)

    tk.Button(win, text="Add Product", command=add_item).pack(side="left", padx=5)
    tk.Button(win, text="Edit Product", command=edit_item).pack(side="left", padx=5)
    tk.Button(win, text="Delete Product", command=delete_item).pack(side="left", padx=5)
    tk.Button(win, text="Low Stock Alert", command=show_low_stock).pack(side="left", padx=5)
    tk.Button(win, text="Refresh", command=refresh_list).pack(side="left", padx=5)

    refresh_list()
    win.mainloop()

# ---------- RUN PROGRAM ----------
if __name__ == "__main__":
    init_db()
    login_screen()
    
