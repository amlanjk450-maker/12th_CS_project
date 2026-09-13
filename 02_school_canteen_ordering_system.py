"""
================================================================================
PROJECT 2: SCHOOL CANTEEN ORDERING & BILLING SYSTEM (PYTHON + MYSQL)
CBSE CLASS 12 COMPUTER SCIENCE FINAL PROJECT
================================================================================
Syllabus Topics Covered:
- Python-MySQL Connectivity (mysql.connector, connect, cursor, execute, commit)
- SQL Operations (CREATE, INSERT, SELECT, UPDATE, DELETE, AUTO_INCREMENT, AGGREGATES)
- Nested Data Structures (Lists, Dictionaries, Multi-item Shopping Carts)
- String Formatting & Printable Invoice Generation
- Arithmetic Calculations, Discounts & Daily Revenue Analytics
- Error Handling with try-except-finally blocks
================================================================================
"""

import sys
import datetime

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print("\n[!] 'mysql-connector-python' is not installed.")
    print("    Please install it using: pip install mysql-connector-python")
    sys.exit(1)

# Default Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "canteen_db"
}

# ------------------------------------------------------------------------------
# DATABASE CONNECTION & INITIALIZATION
# ------------------------------------------------------------------------------

def get_db_connection(use_database=True):
    """Establish connection to MySQL server with error handling."""
    while True:
        try:
            if use_database:
                conn = mysql.connector.connect(
                    host=DB_CONFIG["host"],
                    user=DB_CONFIG["user"],
                    password=DB_CONFIG["password"],
                    database=DB_CONFIG["database"]
                )
            else:
                conn = mysql.connector.connect(
                    host=DB_CONFIG["host"],
                    user=DB_CONFIG["user"],
                    password=DB_CONFIG["password"]
                )
            if conn.is_connected():
                return conn
        except Error as err:
            if err.errno == 1045:
                print(f"\n[!] MySQL Access Denied for user '{DB_CONFIG['user']}'.")
                new_pwd = input("Enter your MySQL root password: ")
                DB_CONFIG["password"] = new_pwd
            elif err.errno == 1049:
                initialize_database()
                use_database = True
            elif err.errno == 2003:
                print("\n[!] ERROR: Cannot connect to MySQL server at localhost:3306.")
                print("    Please ensure your MySQL service is running.")
                sys.exit(1)
            else:
                print(f"\n[!] Database Connection Error: {err}")
                sys.exit(1)


def initialize_database():
    """Create database 'canteen_db' and tables with sample menu if not existing."""
    try:
        conn = get_db_connection(use_database=False)
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS canteen_db")
        cursor.execute("USE canteen_db")

        # Table 1: menu
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                available VARCHAR(10) DEFAULT 'Yes'
            )
        """)

        # Table 2: orders
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                student_name VARCHAR(100) NOT NULL,
                student_id VARCHAR(50) NOT NULL,
                items_summary TEXT NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                order_date DATETIME NOT NULL,
                status VARCHAR(30) DEFAULT 'Placed'
            )
        """)

        conn.commit()

        # Seed sample menu items if empty
        cursor.execute("SELECT COUNT(*) FROM menu")
        if cursor.fetchone()[0] == 0:
            sample_menu = [
                ("Veg Cheese Burger", "Snacks", 60.00, "Yes"),
                ("Crispy Veg Momos (6 pcs)", "Snacks", 50.00, "Yes"),
                ("Grilled Paneer Sandwich", "Snacks", 55.00, "Yes"),
                ("Classic Samosa (2 pcs)", "Snacks", 30.00, "Yes"),
                ("Veg Fried Rice with Gravy", "Meals", 90.00, "Yes"),
                ("Chole Bhature Platter", "Meals", 80.00, "Yes"),
                ("Cold Coffee with Ice Cream", "Beverages", 45.00, "Yes"),
                ("Fresh Lime Soda", "Beverages", 30.00, "Yes"),
                ("Chocolate Brownie", "Desserts", 40.00, "Yes"),
                ("Fruit Juice (Tetra Pack)", "Beverages", 25.00, "No")
            ]
            cursor.executemany("""
                INSERT INTO menu (name, category, price, available)
                VALUES (%s, %s, %s, %s)
            """, sample_menu)
            conn.commit()

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[!] Database Initialization Error: {err}")


# ------------------------------------------------------------------------------
# MENU DISPLAY & MANAGEMENT (MYSQL)
# ------------------------------------------------------------------------------

def display_menu():
    """Print the formatted canteen menu from MySQL organized by categories."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu ORDER BY category, id")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        print("\n" + "="*75)
        print("                   SCHOOL CANTEEN MENU (MYSQL)")
        print("="*75)
        if not rows:
            print(" Menu is currently empty.")
            print("="*75)
            return

        categories = {}
        for r in rows:
            cat = r[2]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(r)

        print(f"{'ID':<6}{'Item Name':<32}{'Price (INR)':<14}{'Status':<12}")
        print("-" * 75)

        for cat, items in categories.items():
            print(f"\n--- {cat.upper()} ---")
            for item in items:
                status = "AVAILABLE" if str(item[4]).lower() == "yes" else "OUT OF STOCK"
                price_str = f"Rs. {float(item[3]):.2f}"
                print(f"[{item[0]:<3}] {item[1]:<30} {price_str:<14} {status:<12}")

        print("="*75)
    except Error as err:
        print(f"[-] Database Error: {err}")


def add_menu_item():
    """Add a new food item to MySQL menu table."""
    print("\n" + "="*50)
    print("             ADD NEW MENU ITEM")
    print("="*50)
    name = input("Enter Item Name (e.g. Pasta, Samosa): ").strip()
    if not name:
        print("[-] Item name cannot be empty.")
        return

    print("Categories: [1] Snacks  [2] Meals  [3] Beverages  [4] Desserts  [5] Other")
    cat_choice = input("Select category (1-5): ").strip()
    cat_map = {"1": "Snacks", "2": "Meals", "3": "Beverages", "4": "Desserts", "5": "Other"}
    category = cat_map.get(cat_choice, "Snacks")

    try:
        price_val = float(input("Enter Price in INR (e.g. 50.00): "))
        if price_val <= 0:
            print("[-] Price must be positive.")
            return
    except ValueError:
        print("[-] Invalid price entered.")
        return

    avail = input("Is this item currently available? (y/n, default=y): ").strip().lower()
    avail_str = "No" if avail == 'n' else "Yes"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO menu (name, category, price, available) VALUES (%s, %s, %s, %s)",
                       (name, category, price_val, avail_str))
        conn.commit()
        item_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"\n[+] SUCCESS! '{name}' added to MySQL menu with Item ID #{item_id} at Rs. {price_val:.2f}.")
    except Error as err:
        print(f"[-] Database Error: {err}")


def update_menu_item():
    """Update price or availability of a menu item in MySQL."""
    print("\n" + "="*50)
    print("           UPDATE MENU ITEM")
    print("="*50)
    display_menu()
    item_id = input("\nEnter Menu Item ID to update: ").strip()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu WHERE id = %s", (item_id,))
        target = cursor.fetchone()

        if not target:
            print(f"[-] Menu item #{item_id} not found.")
            cursor.close()
            conn.close()
            return

        print(f"\nEditing: {target[1]} | Current Price: Rs.{target[3]} | Avail: {target[4]}")
        print("[1] Update Price")
        print("[2] Toggle Availability (In Stock / Out of Stock)")
        print("[3] Update Item Name")
        choice = input("Enter choice (1-3): ").strip()

        if choice == "1":
            try:
                new_price = float(input("Enter new price (INR): "))
                if new_price > 0:
                    cursor.execute("UPDATE menu SET price = %s WHERE id = %s", (new_price, item_id))
                    conn.commit()
                    print(f"[+] Price updated to Rs. {new_price:.2f}.")
                else:
                    print("[-] Price must be greater than zero.")
            except ValueError:
                print("[-] Invalid price input.")
        elif choice == "2":
            new_avail = "No" if str(target[4]).lower() == "yes" else "Yes"
            cursor.execute("UPDATE menu SET available = %s WHERE id = %s", (new_avail, item_id))
            conn.commit()
            print(f"[+] Availability updated to '{new_avail}'.")
        elif choice == "3":
            new_name = input("Enter new item name: ").strip()
            if new_name:
                cursor.execute("UPDATE menu SET name = %s WHERE id = %s", (new_name, item_id))
                conn.commit()
                print(f"[+] Item name updated to '{new_name}'.")
        else:
            print("[-] Invalid choice.")

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def delete_menu_item():
    """Remove a menu item from MySQL."""
    print("\n" + "="*50)
    print("           DELETE MENU ITEM")
    print("="*50)
    item_id = input("Enter Item ID to remove: ").strip()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM menu WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        if not item:
            print(f"[-] Item ID #{item_id} not found.")
        else:
            confirm = input(f"Are you sure you want to delete item #{item_id} ({item[0]})? (y/n): ").strip().lower()
            if confirm == 'y':
                cursor.execute("DELETE FROM menu WHERE id = %s", (item_id,))
                conn.commit()
                print(f"[+] Item #{item_id} deleted successfully from MySQL.")
            else:
                print("[*] Action cancelled.")
        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


# ------------------------------------------------------------------------------
# ORDERING & BILLING WORKFLOW (MYSQL)
# ------------------------------------------------------------------------------

def place_order():
    """Interactive food ordering workflow with cart and invoice generation."""
    print("\n" + "="*65)
    print("           PLACE CANTEEN FOOD ORDER (MYSQL)")
    print("="*65)

    student_name = input("Enter Student / Staff Name : ").strip()
    if not student_name:
        print("[-] Name cannot be empty.")
        return
    student_id = input("Enter Student Roll No / ID  : ").strip()
    if not student_id:
        student_id = "N/A"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM menu")
        menu_rows = cursor.fetchall()
        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")
        return

    menu_dict = {str(r[0]): {"id": r[0], "name": r[1], "category": r[2], "price": float(r[3]), "available": r[4]} for r in menu_rows}
    cart = []

    while True:
        display_menu()
        print("\n--- Current Cart Items: " + str(len(cart)) + " ---")
        if cart:
            for idx, c in enumerate(cart, 1):
                print(f"  {idx}. {c['name']} - {c['quantity']} x Rs.{c['price']:.2f} = Rs.{c['line_total']:.2f}")
            subtotal = sum(c['line_total'] for c in cart)
            print(f"  CURRENT TOTAL: Rs. {subtotal:.2f}")
            print("-" * 40)

        item_id = input("\nEnter Menu Item ID to add to cart (or 'C' to checkout, 'Q' to cancel): ").strip()

        if item_id.upper() == 'Q':
            print("[*] Order cancelled.")
            return
        if item_id.upper() == 'C':
            if not cart:
                print("[-] Cart is empty! Add at least one item before checkout.")
                continue
            break

        if item_id not in menu_dict:
            print(f"[-] Item ID '{item_id}' does not exist in menu.")
            continue

        selected_item = menu_dict[item_id]
        if str(selected_item["available"]).lower() != "yes":
            print(f"[!] Sorry, '{selected_item['name']}' is currently OUT OF STOCK.")
            continue

        try:
            qty_input = input(f"Enter quantity for '{selected_item['name']}' (Default 1): ").strip()
            qty = int(qty_input) if qty_input else 1
            if qty <= 0:
                print("[-] Quantity must be at least 1.")
                continue
        except ValueError:
            print("[-] Invalid quantity entered.")
            continue

        already_in_cart = False
        for c in cart:
            if str(c["id"]) == item_id:
                c["quantity"] += qty
                c["line_total"] = c["quantity"] * c["price"]
                already_in_cart = True
                print(f"[+] Updated quantity of '{selected_item['name']}' to {c['quantity']}.")
                break

        if not already_in_cart:
            cart.append({
                "id": selected_item["id"],
                "name": selected_item["name"],
                "price": selected_item["price"],
                "quantity": qty,
                "line_total": qty * selected_item["price"]
            })
            print(f"[+] Added {qty}x '{selected_item['name']}' to cart.")

    # Save to MySQL
    order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_bill = sum(c["line_total"] for c in cart)
    items_summary = ", ".join([f"{c['name']} ({c['quantity']} x Rs.{c['price']:.2f})" for c in cart])

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO orders (student_name, student_id, items_summary, total_amount, order_date, status)
            VALUES (%s, %s, %s, %s, %s, 'Placed')
        """
        cursor.execute(sql, (student_name, student_id, items_summary, total_bill, order_time))
        conn.commit()
        order_id = cursor.lastrowid
        cursor.close()
        conn.close()

        order_data = {
            "order_id": str(order_id),
            "student_name": student_name,
            "student_id": student_id,
            "items_summary": items_summary,
            "total_amount": total_bill,
            "order_date": order_time,
            "status": "Placed"
        }
        print_invoice(order_data, cart)
    except Error as err:
        print(f"[-] Database Error: {err}")


def print_invoice(order, cart=None):
    """Print an aesthetic, receipt-style bill invoice."""
    print("\n" + "#"*52)
    print("              SPRINGFIELD HIGH SCHOOL")
    print("             CANTEEN CASH BILL RECEIPT")
    print("#"*52)
    print(f" Order ID : #{order['order_id']:<15} Date: {order['order_date']}")
    print(f" Customer : {order['student_name']:<15} ID  : {order['student_id']}")
    print(f" Status   : {order['status'].upper()}")
    print("-" * 52)
    print(f"{'Item Description':<26}{'Qty':<6}{'Rate':<10}{'Total':<10}")
    print("-" * 52)

    if cart:
        for c in cart:
            name = c['name'][:24]
            qty = c['quantity']
            rate = f"{c['price']:.2f}"
            amt = f"{c['line_total']:.2f}"
            print(f"{name:<26}{qty:<6}{rate:<10}{amt:<10}")
    else:
        print(f"{order['items_summary']}")

    print("-" * 52)
    print(f" GRAND TOTAL AMOUNT TO PAY               Rs. {float(order['total_amount']):.2f}")
    print("#"*52)
    print("        Please collect your token at the counter!   ")
    print("                 Thank You & Enjoy!                 ")
    print("#"*52 + "\n")


def view_all_orders():
    """Display all orders stored in MySQL."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders ORDER BY order_id DESC")
        orders = cursor.fetchall()
        cursor.close()
        conn.close()

        print("\n" + "="*95)
        print(f"                           ALL CANTEEN ORDERS ({len(orders)} Orders)")
        print("="*95)
        if not orders:
            print(" No orders placed yet.")
            print("-" * 95)
            return

        print(f"{'ID':<7}{'Customer':<18}{'Student ID':<12}{'Total':<12}{'Date/Time':<20}{'Status':<12}")
        print("-" * 95)
        for o in orders:
            print(f"#{o[0]:<6}{str(o[1])[:16]:<18}{str(o[2])[:10]:<12}Rs.{float(o[4]):<9.2f}{str(o[5])[:19]:<20}{str(o[6]):<12}")
        print("-" * 95)
    except Error as err:
        print(f"[-] Database Error: {err}")


def search_order():
    """Search order by Order ID or Student Name in MySQL."""
    print("\n" + "="*50)
    print("              SEARCH ORDERS")
    print("="*50)
    query = input("Enter Order ID or Student Name to search: ").strip()
    if not query:
        print("[-] Search term cannot be empty.")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT * FROM orders WHERE order_id = %s OR student_name LIKE %s"
        cursor.execute(sql, (query, f"%{query}%"))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            print(f"[-] No orders found matching '{query}'.")
            return

        for o in results:
            print("\n" + "-"*50)
            print(f"Order ID       : #{o[0]}")
            print(f"Student Name   : {o[1]} (ID: {o[2]})")
            print(f"Date & Time    : {o[5]}")
            print(f"Items Ordered  : {o[3]}")
            print(f"Total Amount   : Rs. {float(o[4]):.2f}")
            print(f"Current Status : {o[6]}")
            print("-"*50)
    except Error as err:
        print(f"[-] Database Error: {err}")


def update_order_status():
    """Canteen staff status update tool in MySQL."""
    print("\n" + "="*50)
    print("           UPDATE ORDER STATUS")
    print("="*50)
    order_id = input("Enter Order ID (e.g. 1): ").strip()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        target = cursor.fetchone()

        if not target:
            print(f"[-] Order #{order_id} not found.")
            cursor.close()
            conn.close()
            return

        print(f"Order #{order_id} for {target[1]} | Current Status: {target[6]}")
        print("Select new status:")
        print("[1] Placed  [2] Preparing  [3] Ready for Pickup  [4] Collected / Completed  [5] Cancelled")
        choice = input("Enter option (1-5): ").strip()
        status_map = {
            "1": "Placed",
            "2": "Preparing",
            "3": "Ready",
            "4": "Collected",
            "5": "Cancelled"
        }

        if choice in status_map:
            new_st = status_map[choice]
            cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s", (new_st, order_id))
            conn.commit()
            print(f"[+] Order #{order_id} status updated to '{new_st}' in MySQL.")
        else:
            print("[-] Invalid selection.")

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def view_sales_report():
    """Display revenue metrics and order analytics from MySQL."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status != 'Cancelled'")
        total_revenue = float(cursor.fetchone()[0])

        cursor.execute("SELECT COUNT(*) FROM orders WHERE status IN ('Ready', 'Collected')")
        completed_orders = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM menu WHERE available = 'Yes'")
        active_items = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM menu")
        total_items = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        print("\n" + "="*50)
        print("      CANTEEN DAILY SALES & REVENUE REPORT (MYSQL)")
        print("="*50)
        print(f" Total Orders Logged     : {total_orders}")
        print(f" Completed / Collected   : {completed_orders}")
        print(f" Total Menu Items Active : {active_items} / {total_items}")
        print(f" Total Gross Revenue     : Rs. {total_revenue:.2f}")
        if total_orders > 0:
            avg_order = total_revenue / max(1, total_orders)
            print(f" Average Order Value     : Rs. {avg_order:.2f}")
        print("="*50)
    except Error as err:
        print(f"[-] Database Error: {err}")


# ------------------------------------------------------------------------------
# MAIN MENU LOOP
# ------------------------------------------------------------------------------

def main():
    """Main execution loop."""
    initialize_database()
    while True:
        print("\n" + "="*55)
        print("   SCHOOL CANTEEN ORDERING & BILLING SYSTEM (MYSQL)")
        print("        CBSE Class 12 Computer Science Project")
        print("="*55)
        print(" [1]  View Canteen Menu")
        print(" [2]  Place New Food Order (Interactive Cart)")
        print(" [3]  View All Orders")
        print(" [4]  Search Order by ID or Name")
        print(" [5]  Update Order Status (Canteen Staff)")
        print(" [6]  Add Item to Canteen Menu")
        print(" [7]  Update Menu Item (Price / Availability)")
        print(" [8]  Delete Menu Item")
        print(" [9]  View Daily Sales & Revenue Report")
        print(" [10] Exit")
        print("="*55)

        choice = input("Enter your choice (1-10): ").strip()

        if choice == "1":
            display_menu()
        elif choice == "2":
            place_order()
        elif choice == "3":
            view_all_orders()
        elif choice == "4":
            search_order()
        elif choice == "5":
            update_order_status()
        elif choice == "6":
            add_menu_item()
        elif choice == "7":
            update_menu_item()
        elif choice == "8":
            delete_menu_item()
        elif choice == "9":
            view_sales_report()
        elif choice == "10":
            print("\nThank you for visiting School Canteen System. Have a nice day!")
            break
        else:
            print("\n[-] Invalid selection! Please enter a number between 1 and 10.")


if __name__ == "__main__":
    main()
