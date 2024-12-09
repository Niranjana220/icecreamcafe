import sqlite3
import os

# Database setup
DB_FILE = "icecream_parlour.db"

def initialize_database():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS seasonal_flavors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flavor_name TEXT NOT NULL,
            availability TEXT NOT NULL
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredient_inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            suggestion TEXT NOT NULL,
            allergen TEXT
        )''')

        # Add sample data
        cursor.executemany('''
        INSERT INTO seasonal_flavors (flavor_name, availability)
        VALUES (?, ?)''', [
            ("Pumpkin Spice", "Autumn"),
            ("Peppermint", "Winter"),
            ("Mango", "Summer")
        ])

        cursor.executemany('''
        INSERT INTO ingredient_inventory (ingredient_name, quantity)
        VALUES (?, ?)''', [
            ("Milk", 100),
            ("Sugar", 50),
            ("Chocolate Chips", 25)
        ])

        conn.commit()
        conn.close()

# Menu functions
def add_favorite_product():
    product = input("Enter the flavor to add to your favorites: ")
    print(f"'{product}' has been added to your favorites!")

def search_flavors():
    search = input("Enter a flavor or season to search: ")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM seasonal_flavors
    WHERE flavor_name LIKE ? OR availability LIKE ?''', (f"%{search}%", f"%{search}%"))
    results = cursor.fetchall()
    if results:
        print("Matching Flavors:")
        for row in results:
            print(f"- {row[1]} ({row[2]})")
    else:
        print("No matching flavors found.")
    conn.close()

def add_allergen():
    allergen = input("Enter the allergen to add: ")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO customer_suggestions (suggestion, allergen)
    VALUES (?, ?)''', ("Allergen added by customer", allergen))
    conn.commit()
    print(f"'{allergen}' has been added to the allergen list!")
    conn.close()

# Main program loop
def main():
    initialize_database()
    while True:
        print("\n--- Ice Cream Parlour Menu ---")
        print("1. Add a favorite product")
        print("2. Search seasonal flavors")
        print("3. Add an allergen")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_favorite_product()
        elif choice == "2":
            search_flavors()
        elif choice == "3":
            add_allergen()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
