"""
Python Programming.
Pizza Inventory System.
Name:   Brandon Cano
        Fernando Ocon
Date: 11/29/2024
"""

import datetime
#Ingredient class for the inventory
class Ingredient:
    def __init__(self, name, stock, price, date_entered, expiration_date):
        self.name = name
        self.stock = stock
        self.price = price
        self.date_entered = date_entered
        self.expiration_date = expiration_date

    def update_stock(self, amount):
        self.stock += amount
        if self.stock < 0:
            self.stock = 0



#Inventory management
class Inventory:
    def __init__(self):
        self.ingredients = []

#Option #1 in the Main Menu.
    def add_ingredient_to_inventory(self, pizzeria):
        while True:
            name = input("\nIngredient name: ")
            if not name.isalpha():
                print("Please enter a valid ingredient with only letters.\n")               
            else:
                stock = pizzeria.get_valid_int("\nStock quantity: ", 1, 1000)
                while True:
                    try:
                        price = float(input("\nPrice: "))
                        break
                    except ValueError:
                        print("Enter a valid value!\n")
                date_entered = pizzeria.get_valid_date("\nDate Entered (YYYY-MM-DD):")
                expiration_date = pizzeria.get_valid_date("\nExpiration date (YYYY-MM-DD): ")
                self.add_ingredient(Ingredient(name, stock, price,date_entered, expiration_date))
                print(f"\n{name} has been added to the inventory.")
                while True:
                    try:
                        another = input("Do you want to add another ingredient? (yes/no): ").strip().lower()
                        if another not in ["yes", "no"]:
                            raise ValueError("Invalid input. Please enter 'yes' or 'no'.")
                    except ValueError as e:
                        print(e)
                        continue
                    else:
                        if another == "no":
                            return
                        break
                    
    def add_ingredient(self, ingredient):
        if any(i.name == ingredient.name for i in self.ingredients):
            print("Ingredient already exists!")
        else:
            self.ingredients.append(ingredient)

#Option #2 in the Main Menu.
    def view_ingredients(self):
        if not self.ingredients:
            print("No ingredients in inventory.")
        else:
            print(f"\n{'Name':<20} | {'Stock':<10} | {'Price':<10} | {'Date Entered':<15} | {'Expiration Date':<15}")
            print("-" * 80)
            for i in self.ingredients:
                print(f"{i.name:<20} | {i.stock:<10} | ${i.price:<9.2f} | {i.date_entered:<15} | {i.expiration_date:<15}")

#Option #3 in the Main Menu.
    def remove_ingredient(self, name):
        ingredient_to_remove = self.find_ingredient(name)
        if ingredient_to_remove:
            self.ingredients.remove(ingredient_to_remove)
            print(f"\n{name} has been removed from the inventory.")
        else:
            print(f"{name} is not in the inventory.")

###########################################################################################
    def find_ingredient(self, name):
        return next((i for i in self.ingredients if i.name == name), None)

#this creates the buy list when the stock of an ingredient is 
#less than 8
    def generate_buy_list(self, threshold=15, target_quantity=100):
        buy_list = []
        for ingredient in self.ingredients:
            if ingredient.stock < threshold:
                buy_list.append({
                    "name": ingredient.name,
                    "current_stock": ingredient.stock,
                    "needed_quantity": target_quantity,
                    "to_buy": target_quantity - ingredient.stock
                })
        return buy_list

    def reduce_stock(self, ingredient_name, quantity):
        ingredient = self.find_ingredient(ingredient_name)
        if ingredient and ingredient.stock >= quantity:
            ingredient.update_stock(-quantity)
        elif ingredient:
            print(f"Not enough {ingredient_name} in stock!")
            return False
        else:
            print(f"{ingredient_name} not found in inventory!")
            return False
        return True

    def save_inventory_to_file(self, filename="inventory.txt"):
        with open(filename, "w") as file:
            for a in self.ingredients:
                file.write(f"{a.name},{a.stock},{a.price},{a.date_entered},{a.expiration_date}\n")
        print("Inventory saved to file: 'inventory.txt'")



#This class is created to manage the orders 
class Order:
    def __init__(self, table_number):
        self.table_number = table_number
        self.items = []
        self.total = 0.0


    def add_item(self, item, price, quantity= 1):
        self.items.append((item, price, quantity))
        self.total += price * quantity

    def print_receipt(self, payment, log_file="daily_log.txt"):
        change = payment - self.total
        print("\n--- Receipt ---")
        print(f"Table Number: {self.table_number}")

        for item, price, quantity in self.items:
            print(f"{item}: ${price * quantity}")

        print(f"Total: ${self.total:.2f}")
        print(f"Payment: ${payment:.2f}")
        print(f"Change: ${change:.2f}")
        print("----------------\n")

        #To open and save the receipt in a txt file.
        with open(log_file, "a") as log:
            log.write(f"Total: ${self.total:.2f}, Payment: ${payment:.2f}, Change: ${change:.2f}\n")
        return change



#Main application
class Pizzeria:
    def __init__(self):
        self.inventory = Inventory()
        self.orders = {}
        self.daily_income = 0.0
        self.initialize_inventory()


#Option #4 in the Main Menu.
    def take_order(self):
        table_number = self.get_valid_int("Enter table number (1-12): ", 1, 12)
        if table_number not in self.orders:
            self.orders[table_number] = Order(table_number)

        recipes = {
            "Classic Pizza": ["Tomato Sauce", "Mozzarella Cheese", "Dried Oregano"],
            "Supreme Pizza": ["Tomato Sauce", "Cheese", "Pepperoni", "Peppers",],
            "Vegetarian Pizza": ["Tomato Sauce", "Cheese", "Mushrooms", "Peppers", "Onions"],
            "Hawaiian Pizza": ["Tomato Sauce", "Cheese", "Ham", "Pineapple"],
            "Mixed Pizza": ["Tomato Sauce", "Cheese", "Pepperoni", "Ham", "Peppers", "Onions",]
        }

        prices = {
            "Classic Pizza": 10.0,
            "Supreme Pizza": 12.0,
            "Vegetarian Pizza": 11.0,
            "Hawaiian Pizza": 12.0,
            "Mixed Pizza": 13.0
        }

        while True:
            print("\nPizzas Menu:")
            for i, pizza in enumerate(recipes.keys(), 1):
                print(f"{i}. {pizza}: ${prices[pizza]}")
            print("6. Exit")
            choice = self.get_valid_int("\nEnter the number of the pizza or '6' to exit: ", 1, 6)
            if choice == 6:
                break

            pizza_name = list(recipes.keys())[choice - 1]
            self.show_pizza_ingredients(pizza_name, recipes)

            size_choice = input("Do you want 'slices' or a whole pizza? (Enter 'slices', '8', or '12'): ").lower()
            while size_choice not in ["slices", "8", "12"]:
                size_choice = input("Invalid choice. Please enter 'slices', '8', or '12': ").lower()

            if size_choice == "slices":
                slices = self.get_valid_int("Enter the number of slices (1-16): ", 1, 16)
                total_price = slices * 1.5
                quantity = 1
                self.modify_pizza(pizza_name, recipes)
                self.orders[table_number].add_item(f"{pizza_name} ({slices} slices)", total_price)
            else:
                quantity = self.get_valid_int("How many pizzas (1-20)? ", 1, 20)
                total_price = prices[pizza_name] * quantity
                self.modify_pizza(pizza_name, recipes)
                self.orders[table_number].add_item(f"{pizza_name} ({quantity} pizzas)", total_price)
            
            # Deduct ingredients from inventory
            if not self.deduct_ingredients(pizza_name, recipes, quantity):
                print("Order could not be completed due to insufficient ingredients.\n")
                continue

        while True:
            try:
                payment = float(input("Enter the amount paid by the customer: "))
                if payment < total_price:
                    print("Insuficient money.")
                else:
                    break
            except ValueError:
                print("Enter a valid input.")
        self.orders[table_number].print_receipt(payment)
        self.daily_income += self.orders[table_number].total
        #this deletes the order of the table
        del self.orders[table_number]

#Option #5 in the Main Menu.
    def print_buy_list(self):
        buy_list = self.inventory.generate_buy_list()
        if not buy_list:
            print("No items in the buy list. All ingredients have sufficient stock.")
        else:
            print("\nBuy List:")
            for item in buy_list:
                print(f"- {item['name']}: Current Stock: {item['current_stock']}, To Buy: {item['to_buy']}")

#Option #6 in the Main Menu.
    #note that this function adds the necessary ingredients until 100 in the inventory,
    #and it saves it in a txt file.
    def restock_from_buy_list(self):
        buy_list = self.inventory.generate_buy_list()
        if not buy_list:
            print("All ingredients have sufficient stock.")
            return

        print("\nRestocking from buy list...")
        for item in buy_list:
            ingredient = self.inventory.find_ingredient(item['name'])
            if ingredient:
                ingredient.update_stock(item['to_buy'])
            else:
                self.inventory.add_ingredient(Ingredient(
                    name=item['name'],
                    stock=item['to_buy'],
                    price=0.5,  # Default price
                    expiration_date="2025-12-31"
                ))
        self.save_buy_report(buy_list)

#Option #7 in the Main Menu.
    def end_day(self):
        log_filename = "daily_log.txt"
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        daily_income = 0.0
        existing_log = ""

        # Read existing log file if it exists
        try:
            with open(log_filename, "r") as log_file:
                existing_log = log_file.read()
        except FileNotFoundError:
            pass  # If the file doesn't exist, we will create it

        # Split log entries by date and check for current day
        logs_by_date = existing_log.split("\nDaily Log - ")
        today_log = None
        for log in logs_by_date:
            if log.startswith(current_date):
                today_log = log
                break

        # Extract previous orders and income if the current day's log exists
        previous_orders = []
        previous_income = 0.0
        if today_log:
            # Find the orders section and total income
            lines = today_log.splitlines()
            income_found = False
            for line in lines:
                if line.startswith("Total Daily Income:"):
                    previous_income = float(line.split("$")[-1])
                    income_found = True
                elif income_found and line.startswith("Table"):
                    previous_orders.append(line)
        else:
            print(f"Starting a new log for {current_date}.")

        # Calculate new income and append new orders
        daily_income = self.daily_income + previous_income
        new_orders = []
        for table_number, order in self.orders.items():
            order_summary = f"Table {table_number}:\n"
            for item, price, quantity in order.items:
                order_summary += f"  - {quantity}x {item}: ${price * quantity:.2f}\n"
            order_summary += f"  Total: ${order.total:.2f}\n"
            order_summary += "-" * 60 + "\n"
            new_orders.append(order_summary)

        # Create updated log for the day
        with open(log_filename, "w") as log_file:
            # Write all previous logs except today's (if exists)
            for log in logs_by_date:
                if log and not log.startswith(current_date):
                    log_file.write(f"\nDaily Log - {log.strip()}")

            # Write today's log with updated inventory and orders
            log_file.write(f"\nDaily Log - {current_date} {datetime.datetime.now().strftime('%H:%M:%S')}\n")
            log_file.write("=" * 60 + "\n")

            # Add inventory
            log_file.write("End-of-Day Inventory:\n")
            log_file.write(f"{'Name':<20} | {'Stock':<10} | {'Price':<10} | {'Date Entered':<15} | {'Expiration Date':<15}\n")
            log_file.write("-" * 80 + "\n")
            for ingredient in self.inventory.ingredients:
                log_file.write(f"{ingredient.name:<20} | {ingredient.stock:<10} | ${ingredient.price:<9.2f} | {ingredient.date_entered:<15} | {ingredient.expiration_date:<15}\n")

            # Add new and previous orders
            log_file.write("\nOrders Summary:\n")
            for order in previous_orders + new_orders:
                log_file.write(order)

            # Write updated income
            log_file.write(f"Total Daily Income: ${daily_income:.2f}\n")
            log_file.write("=" * 60 + "\n")

        print(f"End-of-day records updated in {log_filename}.")

        # Reset daily income and orders
        self.daily_income = 0.0
        self.orders.clear()

###########################################################################################

    def initialize_inventory(self):
        ingredients_to_add = [
            "Tomato Sauce", "Mozzarella Cheese", "Dried Oregano", "Cheese",
            "Pepperoni", "Peppers", "Mushrooms",
            "Onions", "Ham", "Pineapple"
        ]
        self.inventory.add_ingredient(Ingredient(name= "Flour", stock= 100, price=12.50, date_entered="2024-11-25", expiration_date="2025-12-31"))
        for ingredient in ingredients_to_add:
            self.inventory.add_ingredient(Ingredient(name=ingredient, stock=100, price=0.5, date_entered="2024-11-25", expiration_date="2025-12-31"))

    #this function will contain the initialize inventory
    def initialize_inventory(self):
        ingredients_to_add = [
            "Tomato Sauce", "Mozzarella Cheese", "Dried Oregano", "Cheese",
            "Pepperoni", "Peppers", "Mushrooms",
            "Onions", "Ham", "Pineapple"
        ]
        self.inventory.add_ingredient(Ingredient(name= "Flour", stock= 100, price=12.50, date_entered="2024-11-25", expiration_date="2025-12-31"))
        for ingredient in ingredients_to_add:
            self.inventory.add_ingredient(Ingredient(name=ingredient, stock=100, price=0.5, date_entered="2024-11-25", expiration_date="2025-12-31"))

    def deduct_ingredients(self, pizza_name, recipes, quantity=1):
        if pizza_name in recipes:
            for ingredient in recipes[pizza_name]:
                if not self.inventory.reduce_stock(ingredient, quantity):
                    print(f"Not enough {ingredient} in stock to complete the order.")
                    return False
        return True

    def show_pizza_ingredients(self, pizza_name, recipes):
        if pizza_name in recipes:
            print(f"\nIngredients for {pizza_name}: {', '.join(recipes[pizza_name])}\n")
        else:
            print("Pizza not found.")

    def modify_pizza(self, pizza_name, recipes):
        if pizza_name in recipes:
            while True:
                print(f"\nCurrent ingredients for {pizza_name}: {', '.join(recipes[pizza_name])}")
                print("Options:")
                print("1. Add ingredient")
                print("2. Remove ingredient")
                print("3. Done modifying\n")
                choice = input("Enter your choice: ")
                if choice == "1":
                    available = [i.name for i in self.inventory.ingredients if i.stock > 0]
                    print(f"\nAvailable ingredients: {', '.join(available)}\n")
                    ingredient_to_add = input("Enter the ingredient to add: ")
                    if ingredient_to_add in available:
                        recipes[pizza_name].append(ingredient_to_add)
                        print(f"Added {ingredient_to_add} to {pizza_name}.")
                    else:
                        print("Sorry, we don't have it at the moment. Please choose another ingredient.")
                elif choice == "2":
                    print(f"\nCurrent ingredients for {pizza_name}: {', '.join(recipes[pizza_name])}")
                    ingredient_to_remove = input("Enter the ingredient to remove: ")
                    if ingredient_to_remove in recipes[pizza_name]:
                        recipes[pizza_name].remove(ingredient_to_remove)
                        print(f"Removed {ingredient_to_remove} from {pizza_name}.")
                    else:
                        print(f"{ingredient_to_remove} is not in the recipe.")
                elif choice == "3":
                    print(f"Finished modifying {pizza_name}.")
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Pizza not found.")

    def get_valid_int(self, prompt, min_val, max_val):
        while True:
            try:
                value = int(input(prompt))
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"Please enter a number between {min_val} and {max_val}.\n")
            except ValueError:
                print("Invalid input. Please enter a valid number.\n")

    def get_valid_date(self,prompt):
        while True:
            date_str = input(prompt)
            try:
                valid_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                return date_str  
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    def save_buy_report(self, buy_list, filename="buy_report.txt"):
        with open(filename, "w") as file:
            file.write(f"Buy Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("=" * 50 + "\n")
            for item in buy_list:
                name = item['name']
                current_stock = item['current_stock']
                added_quantity = item['to_buy']
                total_stock = current_stock + added_quantity
                file.write(f"Ingredient: {name}\n")
                file.write(f"Current Stock: {current_stock}\n")
                file.write(f"Added Quantity: {added_quantity}\n")
                file.write(f"Total Stock After Addition: {total_stock}\n")
                file.write("-" * 50 + "\n")
        print("Buy report saved to buy_report.txt.")

    def Menu(self):
        while True:
            print("""
                    Menu:
            1. Add ingredient to inventory
            2. View inventory ingredients
            3. Remove ingredient from inventory
            4. Print buy list      
            5. Restock from buy list
            6. End day and save records
            7. Exit
            """)
            choice = self.get_valid_int("\nEnter your choice: ", 1, 7)
            if choice == 1:
                self.inventory.add_ingredient_to_inventory(self)
            elif choice == 2:
                self.inventory.view_ingredients()
            elif choice == 3:
                self.inventory.view_ingredients()
                name = input("\nEnter the name of the ingredient to remove: ")
                self.inventory.remove_ingredient(name)
            elif choice == 4:
                self.print_buy_list()
            elif choice == 5:
                self.restock_from_buy_list()
            elif choice == 6:
                self.end_day()
            elif choice == 7:
                break                


    def Main_Menu(self):
        while True:
            print("""
                    Main Menu:
            1. Management of Inventory
            2. Take Orders
            3.Exit
            """)
            choice = self.get_valid_int("\nEnter your choice: ", 1, 3)
            if choice == 1:
                self.Menu()
            elif choice == 2:
                self.take_order()
            elif choice == 3:
                print("Exiting the system. Goodbye!")
                break

#Run the application
if __name__ == "__main__":
    pizzeria = Pizzeria()
    pizzeria.Main_Menu()