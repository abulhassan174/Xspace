import csv
from tabulate import tabulate
INVENTORY_FILE_CSV = "inventory.csv"

#Data structure for items
class InventoryItem:
    def __init__(self, item_id, item_name, quantity, price, category):
        self.item_id = item_id
        self.item_name = item_name
        self.quantity = quantity
        self.price = price
        self.category = category

    def __repr__(self):
        return f"InventoryItem({self.item_id}, '{self.item_name}', {self.quantity}, {self.price}, '{self.category}')"

    #Data validation to handle incorrect or missing values
    def validate(self):
        if not isinstance(self.item_id, int) or self.item_id <= 0:
            raise ValueError("Item ID must be a positive integer.")
        if not isinstance(self.item_name, str) or not self.item_name:
            raise ValueError("Item Name must be a non-empty string.")
        if not isinstance(self.quantity, int) or self.quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")
        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("Price must be a non-negative number.")
        if not isinstance(self.category, str) or not self.category:
            raise ValueError("Category must be a non-empty string.")
        

class Inventory:
    def __init__(self, items=None):
        if items is not None:
            self.items = items
        else:
            self.items = {}

    def add_item(self, item):
        if item.item_id in self.items:
            raise ValueError(f"Item with ID {item.item_id} already exists.")
        item.validate()
        self.items[item.item_id] = item
        print(f"Added item: {item.item_name}")

    def remove_item(self, item_id):
        if item_id not in self.items:
            raise ValueError(f"No item with ID {item_id} found.")
        del self.items[item_id]
        print(f"Removed item ID {item_id}")

    def update_item(self, item_id, **kwargs):
        if item_id not in self.items:
            raise ValueError(f"No item with ID {item_id} found.")
        item = self.items[item_id]
        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)
        item.validate()  # Validate the updated item
        self.items[item_id] = item
        print(f"Updated item ID {item_id}")

    def search_item(self, item_id):
        return self.items.get(item_id, None)

    def display_items(self):
        if not self.items:
            print("Inventory is empty.")
        else:
            table = []
            for item_id, item in self.items.items():
                table.append([item_id, item.item_name, item.quantity, item.price, item.category])
            headers = ["Item ID", "Name", "Quantity", "Price", "Category"]
            print(tabulate(table, headers, tablefmt="grid"))
    
   

# Function to add a new item
def add_item(inventory):
    print("\nAdd a New Item:")
    try:
        item_id = int(input("Item ID: "))
        item_name = input("Item Name: ")
        quantity = int(input("Quantity: "))
        price = float(input("Price: "))
        category = input("Category: ")

        new_item = InventoryItem(item_id, item_name, quantity, price, category)
        inventory.add_item(new_item)
        print("Item added successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid number for Item ID, Quantity, and Price.")

# Function to remove an item
def remove_item(inventory):
    try:
        item_id = int(input("\nRemove Item (Enter Item ID): "))
        inventory.remove_item(item_id)
        print("Item removed successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid number for Item ID.")

# Function to update item details
def update_item(inventory):
    try:
        item_id = int(input("\nUpdate Item (Enter Item ID): "))
        item = inventory.search_item(item_id)
        if item:
            print("\nCurrent details for the item:")
            table = [[item_id, item.item_name, item.quantity, item.price, item.category]]
            headers = ["Item ID", "Name", "Quantity", "Price", "Category"]
            print(tabulate(table, headers, tablefmt="grid"))
            
            print("\nEnter new details (leave blank to keep current value):")
            new_quantity = input("New Quantity: ")
            new_price = input("New Price: ")
            new_category = input("New Category: ")
            
            # Only update if a new value is provided
            updates = {}
            if new_quantity:
                updates['quantity'] = int(new_quantity)
            if new_price:
                updates['price'] = float(new_price)
            if new_category:
                updates['category'] = new_category

            inventory.update_item(item_id, **updates)
            print("Item updated successfully!")
        else:
            print(f"No item found with ID {item_id}.")
    except ValueError:
        print("Invalid input. Please enter a valid number for Item ID, Quantity, and Price.")


# Function to search for an item
def search_item(inventory):
    try:
        item_id = int(input("\nSearch for Item (Enter Item ID): "))
        item = inventory.search_item(item_id)
        if item:
            print("\nItem Found:")
            table = [[item_id, item.item_name, item.quantity, item.price, item.category]]
            headers = ["Item ID", "Name", "Quantity", "Price", "Category"]
            print(tabulate(table, headers, tablefmt="grid"))
            

        else:
            print(f"No item found with ID {item_id}.")
    except ValueError:
        print("Invalid input. Please enter a valid number for Item ID.")


# Function to display all items
def display_all_items(inventory):
    print("\nAll Items in Inventory:")
    inventory.display_items()



# Function to save inventory to CSV file
def save_inventory_to_csv(inventory):
    with open(INVENTORY_FILE_CSV, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["item_id", "item_name", "quantity", "price", "category"])
        writer.writeheader()
        for item in inventory.items.values():
            writer.writerow(item.__dict__)

# Function to load CSV file to inventory
def load_inventory_from_csv():
    try:
        with open(INVENTORY_FILE_CSV, 'r') as file:
            reader = csv.DictReader(file)
            items = {}
            for row in reader:
                item_id = int(row["item_id"])
                item_name = row["item_name"]
                quantity = int(row["quantity"])
                price = float(row["price"])
                category = row["category"]
                items[item_id] = InventoryItem(item_id, item_name, quantity, price, category)
            return Inventory(items)
    except FileNotFoundError:
        return Inventory()

# Function to display the menu
def display_menu():
    
    print("---------------Inventory Management System Menu:---------------")
    print("1. Add New Item")
    print("2. Remove Item")
    print("3. Update Item Details")
    print("4. Search for Item")
    print("5. Display All Items")
    print("6. Exit")

# Main function to run the inventory management system
def main():
    print("\n------------WELCOME TO INVENTORY MANAGEMENT SYSTEM-------------")
    inventory = load_inventory_from_csv() 

    # Menu loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            add_item(inventory)
        elif choice == '2':
            remove_item(inventory)
        elif choice == '3':
            update_item(inventory)
        elif choice == '4':
            search_item(inventory)
        elif choice == '5':
            display_all_items(inventory)
        elif choice == '6':
            save_inventory_to_csv(inventory)
            print("Exiting Inventory Management System. Goodbye!")
            print("---------------------------------------------\n")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


main()