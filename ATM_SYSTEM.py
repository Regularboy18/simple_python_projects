import sqlite3
import tkinter as tk
from tkinter import simpledialog, messagebox

def initialize_database():
    conn = sqlite3.connect('atm.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        balance REAL,
        pin TEXT
    )''')
    conn.commit()
    conn.close()

class ATM:
    def __init__(self, user_id):
        self.user_id = user_id
        self.conn = sqlite3.connect('atm.db')
        self.cursor = self.conn.cursor()
        self.balance = self.get_balance()
        self.pin = self.get_pin()

    def get_balance(self):
        self.cursor.execute('SELECT balance FROM users WHERE id=?', (self.user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0.0

    def get_pin(self):
        self.cursor.execute('SELECT pin FROM users WHERE id=?', (self.user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def check_balance(self):
        return f"Your current balance is: ${self.balance:.2f}"

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.cursor.execute('UPDATE users SET balance=? WHERE id=?', (self.balance, self.user_id))
            self.conn.commit()
            return f"${amount:.2f} has been deposited to your account"
        else:
            return "Invalid amount. Please enter a positive number"

    def withdraw(self, amount):
        if amount <= 0:
            return "Invalid amount. Please enter a positive number"
        elif amount > self.balance:
            return "Insufficient funds. Transaction declined"
        else:
            self.balance -= amount
            self.cursor.execute('UPDATE users SET balance=? WHERE id=?', (self.balance, self.user_id))
            self.conn.commit()
            return f"${amount:.2f} has been withdrawn from your account"

    def set_pin(self, new_pin):
        if len(new_pin) == 4 and new_pin.isdigit():
            self.pin = new_pin
            self.cursor.execute('UPDATE users SET pin=? WHERE id=?', (self.pin, self.user_id))
            self.conn.commit()
            return "Your PIN has been set/updated successfully"
        else:
            return "Invalid PIN. Please enter a 4-digit number"

    def validate_pin(self, entered_pin):
        if self.pin is None:
            return False, "No PIN set. Please set a PIN first"
        if entered_pin == self.pin:
            return True, ""
        else:
            return False, "Invalid PIN. Access denied"

def initialize_user(user_id, initial_balance, pin):
    conn = sqlite3.connect('atm.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE id=?', (user_id,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (id, balance, pin) VALUES (?, ?, ?)', (user_id, initial_balance, pin))
        conn.commit()
    conn.close()

class ATMUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM System")
        self.root.geometry("400x400")
        self.root.configure(bg="#f0f0f0")
        self.user_id = None
        self.atm = None
        self.show_login_screen()

    def show_login_screen(self):
        self.clear_window()
        self.title_label = tk.Label(self.root, text="Welcome to ATM", bg="#00274d", fg="green", font=("Helvetica", 16, "bold"))
        self.title_label.pack(fill=tk.X, pady=10)

        self.register_button = tk.Button(self.root, text="Register", command=self.show_register_screen, bg="#004c99", fg="green", font=("Helvetica", 12, "bold"))
        self.register_button.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Login", command=self.show_login_prompt, bg="#004c99", fg="green", font=("Helvetica", 12, "bold"))
        self.login_button.pack(pady=5)

    def show_register_screen(self):
        self.clear_window()
        self.title_label = tk.Label(self.root, text="Register", bg="#00274d", fg="green", font=("Helvetica", 16, "bold"))
        self.title_label.pack(fill=tk.X, pady=10)

        self.user_id_label = tk.Label(self.root, text="Enter a new user ID:", bg="#f0f0f0", font=("Helvetica", 12))
        self.user_id_label.pack(pady=5)
        self.user_id_entry = tk.Entry(self.root)
        self.user_id_entry.pack(pady=5)

        self.balance_label = tk.Label(self.root, text="Enter initial balance:", bg="#f0f0f0", font=("Helvetica", 12))
        self.balance_label.pack(pady=5)
        self.balance_entry = tk.Entry(self.root)
        self.balance_entry.pack(pady=5)

        self.pin_label = tk.Label(self.root, text="Enter a new 4-digit PIN:", bg="#f0f0f0", font=("Helvetica", 12))
        self.pin_label.pack(pady=5)
        self.pin_entry = tk.Entry(self.root)
        self.pin_entry.pack(pady=5)

        self.register_button = tk.Button(self.root, text="Register", command=self.register_user, bg="#004c99", fg="green", font=("Helvetica", 12, "bold"))
        self.register_button.pack(pady=5)

        self.back_button = tk.Button(self.root, text="Back", command=self.show_login_screen, bg="#990000", fg="green", font=("Helvetica", 12, "bold"))
        self.back_button.pack(pady=5)

    def show_login_prompt(self):
        self.clear_window()
        self.title_label = tk.Label(self.root, text="Login", bg="#00274d", fg="green", font=("Helvetica", 16, "bold"))
        self.title_label.pack(fill=tk.X, pady=10)

        self.user_id_label = tk.Label(self.root, text="Enter your user ID:", bg="#f0f0f0", font=("Helvetica", 12))
        self.user_id_label.pack(pady=5)
        self.user_id_entry = tk.Entry(self.root)
        self.user_id_entry.pack(pady=5)

        self.pin_label = tk.Label(self.root, text="Enter your PIN:", bg="#f0f0f0", font=("Helvetica", 12))
        self.pin_label.pack(pady=5)
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Login", command=self.login_user, bg="#004c99", fg="green", font=("Helvetica", 12, "bold"))
        self.login_button.pack(pady=5)

        self.back_button = tk.Button(self.root, text="Back", command=self.show_login_screen, bg="#990000", fg="green", font=("Helvetica", 12, "bold"))
        self.back_button.pack(pady=5)

    def show_main_menu(self):
        self.clear_window()
        self.title_label = tk.Label(self.root, text="ATM Main Menu", bg="#00274d", fg="green", font=("Helvetica", 16, "bold"))
        self.title_label.pack(fill=tk.X, pady=10)

        self.balance_button = tk.Button(self.root, text="Check Balance", command=self.check_balance, bg="#004c99", fg="green", font=("Helvetica", 12, "bold"))
        self.balance_button.pack(pady=5)

        self.deposit_button = tk.Button(self.root, text="Deposit Money", command=self.deposit, bg="#004c99", fg="green", font=("Helvetica", 12, "bold"))
        self.deposit_button.pack(pady=5)

        self.withdraw_button = tk.Button(self.root, text="Withdraw Money", command=self.withdraw, bg="#004c99", fg="green", font=("Helvetica", 12, "bold"))
        self.withdraw_button.pack(pady=5)

        self.pin_button = tk.Button(self.root, text="Generate/Change PIN", command=self.set_pin, bg="#004c99", fg="green", font=("Helvetica", 12, "bold"))
        self.pin_button.pack(pady=5)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit, bg="#990000", fg="green", font=("Helvetica", 12, "bold"))
        self.exit_button.pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def register_user(self):
        user_id = self.user_id_entry.get()
        initial_balance = self.balance_entry.get()
        pin = self.pin_entry.get()

        if user_id and initial_balance and pin:
            try:
                user_id = int(user_id)
                initial_balance = float(initial_balance)
                if len(pin) == 4 and pin.isdigit():
                    initialize_user(user_id, initial_balance, pin)
                    messagebox.showinfo("Success", "User registered successfully!")
                    self.show_login_screen()
                else:
                    messagebox.showerror("Error", "Invalid PIN. Please enter a 4-digit number.")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please enter valid values.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def login_user(self):
        user_id = self.user_id_entry.get()
        pin = self.pin_entry.get()

        if user_id and pin:
            try:
                user_id = int(user_id)
                self.atm = ATM(user_id)
                valid, message = self.atm.validate_pin(pin)
                if valid:
                    self.show_main_menu()
                else:
                    messagebox.showerror("Error", message)
            except ValueError:
                messagebox.showerror("Error", "Invalid user ID. Please enter a valid number.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def check_balance(self):
        messagebox.showinfo("Balance", self.atm.check_balance())

    def deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")
        if amount is not None:
            message = self.atm.deposit(amount)
            messagebox.showinfo("Deposit", message)

    def withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter the amount to withdraw:")
        if amount is not None:
            message = self.atm.withdraw(amount)
            messagebox.showinfo("Withdraw", message)

    def set_pin(self):
        new_pin = simpledialog.askstring("Set PIN", "Enter a new 4-digit PIN:")
        if new_pin:
            message = self.atm.set_pin(new_pin)
            messagebox.showinfo("Set PIN", message)

def main():
    initialize_database()
    root = tk.Tk()
    gui = ATMUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
