#gui.py
import tkinter as tk
from five_nights import Pizzeria, Inventory

Pizza = Pizzeria()
Inven = Inventory()

root = tk.Tk()
root.title("Pizza Inventory System")
root.geometry("800x600")
root.iconbitmap(r"C:\Users\brand\Desktop\rep\pizza-inventory-gui\src\assets\Pizza -.ico")
root.configure(bg="#1E1E1E")

def options_A():
    clear()
    btnA1 = tk.Button(root, text="Add ingredient to inventory", command=add_ingre_inven)
    btnA1.pack(pady=10)
    btnA2 = tk.Button(root, text="View inventory ingredients", command=Inven.view_ingredients)
    btnA2.pack(pady=10)
    btnA3 = tk.Button(root, text="Remove ingredient from inventory", command=Inven.view_ingredients)
    btnA3.pack(pady=10)
    btnA4 = tk.Button(root, text="Print buy list", command=Pizza.print_buy_list)
    btnA4.pack(pady=10)
    btnA5 = tk.Button(root, text="Restock from buy list", command=Pizza.restock_from_buy_list)
    btnA5.pack(pady=10)
    btnA6 = tk.Button(root, text="End day and save records", command=Pizza.end_day)
    btnA6.pack(pady=10)
    btnA7 = tk.Button(root, text="Exit to main menu", command=breakpoint)
    btnA7.pack(pady=10)

def options_B():
    clear()
    btnB1 = tk.Button(root, text="Take order")

def add_ingre_inven():
    clear()

    #Labels and Entries
    Ingre_L = tk.Label(root, text="Ingredient name", bg="#1E1E1E", fg="white")
    Ingre_L.pack(pady=10, ipady=10)
    ingredient_E = tk.Entry(root)
    ingredient_E.pack(pady=5)

    Stock_L = tk.Label(root, text="Stock", bg="#1E1E1E", fg="white")
    Stock_L.pack(pady=10)
    stock_E = tk.Entry(root)
    stock_E.pack(pady=5)

    Price_L = tk.Label(root, text="Price", bg="#1E1E1E", fg="white")
    Price_L.pack(pady=10)
    price_E = tk.Entry(root)
    price_E.pack(pady=5)

    Expiration_L = tk.Label(root, text="Expiration date (YYYY-MM-DD)", bg="#1E1E1E", fg="white")
    Expiration_L.pack(pady=10)
    expiration_E = tk.Entry(root)
    expiration_E.pack(pady=5)

    result_label = tk.Label(root, text="", bg="#1E1E1E", fg="white")
    result_label.pack(pady=10)

    #Define the function that runs on button click
    def submit_ingredient():
        try:
            ingredient = ingredient_E.get()
            stock = stock_E.get()
            price = price_E.get()
            expiration = expiration_E.get()

            result = Inven.add_ingredient_to_inventory(ingredient, stock, price, expiration)
            result_label.config(text=result)
        except Exception as e:
            result_label.config(text=f"Error: {e}")

    #Pass the function reference (no parentheses!)
    submit_btn = tk.Button(root, text="Submit", command=submit_ingredient)
    submit_btn.pack()

def clear():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()
    for l in root.winfo_children():
        if isinstance(l, tk.Label):
            l.destroy()
    for s in root.winfo_children():
        if isinstance(s, tk.Entry):
            s.destroy()

label1 = tk.Label(root, text="Main Menu", font=("Arial", 24), bg="#1E1E1E", fg="white")
label1.pack(pady=100)
btnA = tk.Button(root, text="Management of Inventory", command=options_A, font=("Arial", 16), bg="#00568F", fg="white")
btnA.pack(pady=20)
btnB = tk.Button(root, text="Take Orders", command=Pizza.take_order, font=("Arial", 16), bg="#007ACC", fg="white")
btnB.pack(pady=20)
root.mainloop()

