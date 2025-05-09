import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import csv
from datetime import datetime
from collections import defaultdict

# ---------- Window Setup ----------
root = tk.Tk()
root.title("💰 Personal Expense Tracker")
root.geometry("600x400")
root.resizable(False, False)

# ---------- Header ----------
header_label = tk.Label(root, text="Expense Tracker", font=("Arial", 20, "bold"))
header_label.pack(pady=10)

# ---------- Input Frame ----------
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

tk.Label(input_frame, text="Category:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
category_entry = tk.Entry(input_frame, font=("Arial", 12))
category_entry.grid(row=0, column=1, padx=10)

tk.Label(input_frame, text="Amount ($):", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
amount_entry = tk.Entry(input_frame, font=("Arial", 12))
amount_entry.grid(row=1, column=1, padx=10)

# ---------- Status Label ----------
status_label = tk.Label(root, text="Status: Waiting for input...", font=("Arial", 10), fg="gray")
status_label.pack(side="bottom", pady=15)

# ---------- Function to Add Expense ----------
def add_expense():
    category = category_entry.get()
    amount = amount_entry.get()
    date = datetime.now().strftime("%Y-%m-%d")

    if not category or not amount:
        messagebox.showwarning("Input Error", "Please fill in both Category and Amount.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number.")
        return

    # Save to CSV
    with open("expenses.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])

    # Clear input fields and update status
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    status_label.config(text=f"✔️ Added: {category} - ${amount:.2f} on {date}", fg="green")

def show_table():
    # Read data from CSV
    try:
        with open("expenses.csv", "r") as file:
            lines = file.readlines()
            rows = [line.strip().split(",") for line in lines if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("Error", "No expenses.csv file found.")
        return

    # Create new popup window
    table_window = tk.Toplevel(root)
    table_window.title("📋 Expense Table")
    table_window.geometry("500x300")

    # Treeview for table
    columns = ("Date", "Category", "Amount")
    tree = ttk.Treeview(table_window, columns=columns, show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount ($)")
    tree.pack(fill=tk.BOTH, expand=True)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Insert rows (skip header if present)
    for row in rows:
        if len(row) == 3 and row[0] != "Date":
            tree.insert("", tk.END, values=(row[0], row[1], row[2]))

def export_expenses():
    try:
        with open("expenses.csv", "r") as source:
            data = source.read()
    except FileNotFoundError:
        messagebox.showerror("Error", "No expenses to export.")
        return

    export_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv")],
                                               title="Save as")
    if export_path:
        with open(export_path, "w") as target:
            target.write(data)
        status_label.config(text=f"✔️ Exported to: {export_path}", fg="blue")



# ---------- Button Frame ----------
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

add_button = tk.Button(button_frame, text="Add Expense", font=("Arial", 12), width=15, command=add_expense)
add_button.grid(row=0, column=0, padx=5)

table_button = tk.Button(button_frame, text="Show Table", font=("Arial", 12), width=15, command=show_table)
table_button.grid(row=0, column=1, padx=5)

export_button = tk.Button(button_frame, text="Export CSV", font=("Arial", 12), width=15, command=export_expenses)
export_button.grid(row=1, column=1, padx=5, pady=10)

# ---------- Run ----------
root.mainloop()
