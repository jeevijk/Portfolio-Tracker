import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import csv
from datetime import datetime

STOCK_PRICES = {
    "GOOGL": 180,
    "INFY": 150,
    "TCS": 140,
    "MSFT": 400,
    "TSLA": 250,
}

class StockTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.portfolio = {}

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Available symbols: " + ", ".join(STOCK_PRICES.keys())).pack(pady=5)

        self.symbol_entry = tk.Entry(self.root)
        self.symbol_entry.pack(pady=5)
        self.symbol_entry.insert(0, "Enter stock symbol")

        self.qty_entry = tk.Entry(self.root)
        self.qty_entry.pack(pady=5)
        self.qty_entry.insert(0, "Enter quantity")

        tk.Button(self.root, text="Add Stock", command=self.add_stock).pack(pady=5)
        tk.Button(self.root, text="Show Portfolio", command=self.show_portfolio).pack(pady=5)
        tk.Button(self.root, text="Save Portfolio", command=self.save_portfolio).pack(pady=5)

        self.output_text = tk.Text(self.root, width=50, height=15)
        self.output_text.pack(pady=10)

    def add_stock(self):
        symbol = self.symbol_entry.get().upper().strip()
        if symbol not in STOCK_PRICES:
            messagebox.showerror("Error", f"Symbol {symbol} not in price list!")
            return

        try:
            qty = int(self.qty_entry.get().strip())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer!")
            return

        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + qty
        messagebox.showinfo("Success", f"Added {qty} shares of {symbol}")
        self.symbol_entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)

    def show_portfolio(self):
        if not self.portfolio:
            messagebox.showinfo("Portfolio", "No stocks in portfolio.")
            return

        self.output_text.delete("1.0", tk.END)
        total_value = 0
        self.output_text.insert(tk.END, "=== Portfolio Summary ===\n")
        for symbol, qty in self.portfolio.items():
            price = STOCK_PRICES[symbol]
            value = qty * price
            total_value += value
            self.output_text.insert(tk.END, f"{symbol}: {qty} shares × {price} = {value}\n")
        self.output_text.insert(tk.END, f"\nTotal investment value: {total_value}\n")

    def save_portfolio(self):
        if not self.portfolio:
            messagebox.showinfo("Save", "Portfolio is empty, nothing to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
        if not file_path:
            return

        rows = []
        total_value = 0
        for symbol, qty in self.portfolio.items():
            price = STOCK_PRICES[symbol]
            value = price * qty
            total_value += value
            rows.append([symbol, qty, price, value])

        if file_path.endswith(".csv"):
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Symbol", "Quantity", "Price", "Value"])
                writer.writerows(rows)
                writer.writerow([])
                writer.writerow(["TOTAL", "", "", total_value])
        else:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("Symbol,Quantity,Price,Value\n")
                for row in rows:
                    f.write(",".join(map(str, row)) + "\n")
                f.write(f"\nTotal investment value: {total_value}\n")

        messagebox.showinfo("Saved", f"Portfolio saved to {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StockTrackerApp(root)
    root.mainloop()