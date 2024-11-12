import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import PhotoImage



# Database Setup
conn = sqlite3.connect('electricity_bills.db')
cursor = conn.cursor()

# Create required tables if they do not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    contact TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS bills (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    usage INTEGER,
    bill_amount REAL,
    status TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
)
''')
conn.commit()

# Initialize Admin and some default data
cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
conn.commit()

# Tkinter App
class ElectricityBillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Electricity Bill Management System")
        self.root.geometry("1000x1000")
        self.root.configure(bg='#ADD8E6')  # Light blue background

        # Background Image
        self.bg_image = PhotoImage(file="c.png")  # Change this path as per your image location
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        self.frame = tk.Frame(self.root, bg='#ADD8E6')
        self.frame.pack(pady=20)
    
        self.login_screen()

    def login_screen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Login", font=("Arial", 20, 'bold'), bg='#ADD8E6', fg="white").grid(row=0, column=0, columnspan=2)
        
        tk.Label(self.frame, text="Username:", bg='#ADD8E6', font=("Arial", 14)).grid(row=1, column=0, pady=10)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.username_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Password:", bg='#ADD8E6', font=("Arial", 14)).grid(row=2, column=0)
        self.password_entry = tk.Entry(self.frame, show="*", font=("Arial", 14))
        self.password_entry.grid(row=2, column=1)

        login_btn = tk.Button(self.frame, text="Login", font=("Arial", 14), command=self.login, bg="#4CAF50", fg="white")
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)

        signup_btn = tk.Button(self.frame, text="Sign Up", font=("Arial", 14), command=self.signup_screen, bg="#FF5722", fg="white")
        signup_btn.grid(row=4, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            role = user[3]
            if role == "admin":
                self.admin_dashboard()
            else:
                self.customer_dashboard(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signup_screen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Sign Up", font=("Arial", 20, 'bold'), bg='#ADD8E6', fg="white").grid(row=0, column=0, columnspan=2)
        
        tk.Label(self.frame, text="Username:", bg='#ADD8E6', font=("Arial", 14)).grid(row=1, column=0, pady=10)
        self.new_username_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.new_username_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Password:", bg='#ADD8E6', font=("Arial", 14)).grid(row=2, column=0)
        self.new_password_entry = tk.Entry(self.frame, show="*", font=("Arial", 14))
        self.new_password_entry.grid(row=2, column=1)

        role_label = tk.Label(self.frame, text="Role (admin/customer):", bg='#ADD8E6', font=("Arial", 14))
        role_label.grid(row=3, column=0)
        self.role_var = tk.StringVar(value="customer")
        role_option = tk.OptionMenu(self.frame, self.role_var, "admin", "customer")
        role_option.grid(row=3, column=1)

        signup_btn = tk.Button(self.frame, text="Sign Up", font=("Arial", 14), command=self.create_user, bg="#4CAF50", fg="white")
        signup_btn.grid(row=4, column=0, columnspan=2, pady=20)

    def create_user(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        role = self.role_var.get()

        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully")
            self.login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def admin_dashboard(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Admin Dashboard", font=("Arial", 20, 'bold'), bg='#ADD8E6', fg="white").grid(row=0, column=0, columnspan=2)

        # Admin functionalities buttons
        add_bill_btn = tk.Button(self.frame, text="Add Bill", font=("Arial", 14), command=self.add_bill_screen, bg="#2196F3", fg="white")
        add_bill_btn.grid(row=1, column=0, pady=10)

        update_bill_btn = tk.Button(self.frame, text="Update Bill", font=("Arial", 14), command=self.update_bill_screen, bg="#FF9800", fg="white")
        update_bill_btn.grid(row=2, column=0, pady=10)

        delete_bill_btn = tk.Button(self.frame, text="Delete Bill", font=("Arial", 14), command=self.delete_bill_screen, bg="#F44336", fg="white")
        delete_bill_btn.grid(row=3, column=0, pady=10)

        logout_btn = tk.Button(self.frame, text="Logout", font=("Arial", 14), command=self.login_screen, bg="#FF5722", fg="white")
        logout_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def add_bill_screen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Add Bill", font=("Arial", 20, 'bold'), bg='#ADD8E6', fg="white").grid(row=0, column=0, columnspan=2)

        tk.Label(self.frame, text="Customer ID:", bg='#ADD8E6', font=("Arial", 14)).grid(row=1, column=0)
        customer_id_entry = tk.Entry(self.frame, font=("Arial", 14))
        customer_id_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Usage (units):", bg='#ADD8E6', font=("Arial", 14)).grid(row=2, column=0)
        usage_entry = tk.Entry(self.frame, font=("Arial", 14))
        usage_entry.grid(row=2, column=1)

        tk.Label(self.frame, text="Bill Amount:", bg='#ADD8E6', font=("Arial", 14)).grid(row=3, column=0)
        bill_amount_entry = tk.Entry(self.frame, font=("Arial", 14))
        bill_amount_entry.grid(row=3, column=1)

        tk.Label(self.frame, text="Status (paid/unpaid):", bg='#ADD8E6', font=("Arial", 14)).grid(row=4, column=0)
        status_entry = tk.Entry(self.frame, font=("Arial", 14))
        status_entry.grid(row=4, column=1)

        add_btn = tk.Button(self.frame, text="Add Bill", font=("Arial", 14), command=lambda: self.add_bill(customer_id_entry, usage_entry, bill_amount_entry, status_entry), bg="#4CAF50", fg="white")
        add_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def add_bill(self, customer_id_entry, usage_entry, bill_amount_entry, status_entry):
        customer_id = customer_id_entry.get()
        usage = usage_entry.get()
        bill_amount = bill_amount_entry.get()
        status = status_entry.get()

        cursor.execute("INSERT INTO bills (customer_id, usage, bill_amount, status) VALUES (?, ?, ?, ?)", (customer_id, usage, bill_amount, status))
        conn.commit()
        messagebox.showinfo("Success", "Bill added successfully")
        self.admin_dashboard()

    def update_bill_screen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Update Bill", font=("Arial", 20, 'bold'), bg='#ADD8E6', fg="white").grid(row=0, column=0, columnspan=2)

        tk.Label(self.frame, text="Bill ID:", bg='#ADD8E6', font=("Arial", 14)).grid(row=1, column=0)
        self.bill_id_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.bill_id_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Customer ID:", bg='#ADD8E6', font=("Arial", 14)).grid(row=2, column=0)
        self.customer_id_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.customer_id_entry.grid(row=2, column=1)

        tk.Label(self.frame, text="Usage (units):", bg='#ADD8E6', font=("Arial", 14)).grid(row=3, column=0)
        self.usage_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.usage_entry.grid(row=3, column=1)

        tk.Label(self.frame, text="Bill Amount:", bg='#ADD8E6', font=("Arial", 14)).grid(row=4, column=0)
        self.bill_amount_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.bill_amount_entry.grid(row=4, column=1)

        tk.Label(self.frame, text="Status (paid/unpaid):", bg='#ADD8E6', font=("Arial", 14)).grid(row=5, column=0)
        self.status_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.status_entry.grid(row=5, column=1)

        update_btn = tk.Button(self.frame, text="Update Bill", font=("Arial", 14), command=self.update_bill, bg="#FF9800", fg="white")
        update_btn.grid(row=6, column=0, columnspan=2, pady=10)

    def update_bill(self):
        bill_id = self.bill_id_entry.get()
        customer_id = self.customer_id_entry.get()
        usage = self.usage_entry.get()
        bill_amount = self.bill_amount_entry.get()
        status = self.status_entry.get()

        cursor.execute("""
        UPDATE bills SET usage=?, bill_amount=?, status=? WHERE bill_id=? AND customer_id=?
        """, (usage, bill_amount, status, bill_id, customer_id))

        conn.commit()
        messagebox.showinfo("Success", "Bill updated successfully")
        self.admin_dashboard()

    def delete_bill_screen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Delete Bill", font=("Arial", 20, 'bold'), bg='#ADD8E6', fg="white").grid(row=0, column=0, columnspan=2)

        tk.Label(self.frame, text="Bill ID:", bg='#ADD8E6', font=("Arial", 14)).grid(row=1, column=0)
        self.delete_bill_id_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.delete_bill_id_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Customer ID:", bg='#ADD8E6', font=("Arial", 14)).grid(row=2, column=0)
        self.delete_customer_id_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.delete_customer_id_entry.grid(row=2, column=1)

        delete_btn = tk.Button(self.frame, text="Delete Bill", font=("Arial", 14), command=self.delete_bill, bg="#F44336", fg="white")
        delete_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def delete_bill(self):
        bill_id = self.delete_bill_id_entry.get()
        customer_id = self.delete_customer_id_entry.get()

        cursor.execute("DELETE FROM bills WHERE bill_id=? AND customer_id=?", (bill_id, customer_id))
        conn.commit()
        messagebox.showinfo("Success", "Bill deleted successfully")
        self.admin_dashboard()

    def customer_dashboard(self, username):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Customer Dashboard", font=("Arial", 20, 'bold'), bg='#ADD8E6', fg="white").grid(row=0, column=0, columnspan=2)

        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            customer_id = user[0]
            cursor.execute("SELECT * FROM bills WHERE customer_id=?", (customer_id,))
            bills = cursor.fetchall()

            if bills:
                row = 1
                for bill in bills:
                    bill_id, usage, bill_amount, status = bill[0], bill[2], bill[3], bill[4]
                    tk.Label(self.frame, text=f"Bill ID: {bill_id}, Usage: {usage} units, Amount: ${bill_amount}, Status: {status}",
                             bg='#ADD8E6', font=("Arial", 14)).grid(row=row, column=0, columnspan=2, pady=5)
                    row += 1
            else:
                tk.Label(self.frame, text="No bills found.", bg='#ADD8E6', font=("Arial", 14)).grid(row=1, column=0, columnspan=2)

        logout_btn = tk.Button(self.frame, text="Logout", font=("Arial", 14), command=self.login_screen, bg="#FF5722", fg="white")
        logout_btn.grid(row=row+1, column=0, columnspan=2, pady=10)

root = tk.Tk()
app = ElectricityBillApp(root)
root.mainloop()
