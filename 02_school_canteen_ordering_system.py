"""
================================================================================
PROJECT 2: SCHOOL CANTEEN ORDERING & BILLING SYSTEM
CBSE CLASS 12 COMPUTER SCIENCE FINAL PROJECT (SINGLE FILE SYSTEM)
================================================================================
Syllabus Topics Covered:
- Python Functions (Modular programming, parameter passing, return values)
- File Handling (CSV module - reader, writer, DictReader, DictWriter)
- Nested Data Structures (Lists, Dictionaries, Nested Cart structures)
- String Formatting & Printable Invoice Generation
- Input Validation, Arithmetic Calculations & Financial Reports
- Error Handling with try-except blocks
================================================================================
"""

import csv
import os
import datetime

# CSV File Constants
MENU_FILE = "canteen_menu.csv"
ORDERS_FILE = "canteen_orders.csv"

MENU_FIELDS = ["id", "name", "category", "price", "available"]
ORDER_FIELDS = ["order_id", "student_name", "student_id", "items_summary", "total_amount", "order_date", "status"]

# ------------------------------------------------------------------------------
# DATABASE / FILE INITIALIZATION & HELPERS
# ------------------------------------------------------------------------------

def initialize_files():
    """Create CSV files with sample menu and order data if not existing."""
    if not os.path.exists(MENU_FILE):
        with open(MENU_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=MENU_FIELDS)
            writer.writeheader()
            sample_menu = [
                {"id": "1", "name": "Veg Cheese Burger", "category": "Snacks", "price": "60.00", "available": "Yes"},
                {"id": "2", "name": "Crispy Veg Momos (6 pcs)", "category": "Snacks", "price": "50.00", "available": "Yes"},
                {"id": "3", "name": "Grilled Paneer Sandwich", "category": "Snacks", "price": "55.00", "available": "Yes"},
                {"id": "4", "name": "Classic Samosa (2 pcs)", "category": "Snacks", "price": "30.00", "available": "Yes"},
                {"id": "5", "name": "Veg Fried Rice with Gravy", "category": "Meals", "price": "90.00", "available": "Yes"},
                {"id": "6", "name": "Chole Bhature Platter", "category": "Meals", "price": "80.00", "available": "Yes"},
                {"id": "7", "name": "Cold Coffee with Ice Cream", "category": "Beverages", "price": "45.00", "available": "Yes"},
                {"id": "8", "name": "Fresh Lime Soda", "category": "Beverages", "price": "30.00", "available": "Yes"},
                {"id": "9", "name": "Chocolate Brownie", "category": "Desserts", "price": "40.00", "available": "Yes"},
                {"id": "10", "name": "Fruit Juice (Tetra Pack)", "category": "Beverages", "price": "25.00", "available": "No"}
            ]
            writer.writerows(sample_menu)

    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=ORDER_FIELDS)
            writer.writeheader()
            sample_orders = [
                {
                    "order_id": "1001",
                    "student_name": "Aman Sharma",
                    "student_id": "12A-04",
                    "items_summary": "Veg Cheese Burger (1 x Rs.60.00), Cold Coffee with Ice Cream (1 x Rs.45.00)",
                    "total_amount": "105.00",
                    "order_date": "2026-09-10 11:30:15",
                    "status": "Collected"
                },
                {
                    "order_id": "1002",
                    "student_name": "Riya Sen",
                    "student_id": "12B-18",
                    "items_summary": "Grilled Paneer Sandwich (2 x Rs.55.00), Fresh Lime Soda (1 x Rs.30.00)",
                    "total_amount": "140.00",
                    "order_date": "2026-09-11 13:10:40",
                    "status": "Ready"
                }
            ]
            writer.writerows(sample_orders)


def read_menu():
    """Read menu items from CSV."""
    menu = []
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                menu.append(row)
    return menu


def write_menu(menu):
    """Write menu items to CSV."""
    with open(MENU_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=MENU_FIELDS)
        writer.writeheader()
        writer.writerows(menu)


def read_orders():
    """Read orders from CSV."""
    orders = []
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                orders.append(row)
    return orders


def write_orders(orders):
    """Write orders to CSV."""
    with open(ORDERS_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=ORDER_FIELDS)
        writer.writeheader()
        writer.writerows(orders)


def get_next_order_id(orders):
    """Auto-generate next unique Order ID."""
    if not orders:
        return "1001"
    try:
        max_id = max(int(o["order_id"]) for o in orders if o["order_id"].isdigit())
        return str(max_id + 1)
    except ValueError:
        return str(1000 + len(orders) + 1)


# ------------------------------------------------------------------------------
# MENU DISPLAY & MANAGEMENT
# ------------------------------------------------------------------------------

def display_menu():
    """Print the formatted canteen menu organized by categories."""
    menu = read_menu()
    print("\n" + "="*75)
    print("                       SCHOOL CANTEEN MENU")
    print("="*75)
    
    if not menu:
        print(" Menu is currently empty.")
        print("="*75)
        return

    categories = {}
    for item in menu:
        cat = item["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)

    print(f"{'ID':<6}{'Item Name':<32}{'Price (INR)':<14}{'Status':<12}")
    print("-" * 75)

    for cat, items in categories.items():
        print(f"\n--- {cat.upper()} ---")
        for item in items:
            status = "AVAILABLE" if item["available"].lower() == "yes" else "OUT OF STOCK"
            price_str = f"Rs. {float(item['price']):.2f}"
            print(f"[{item['id']:<3}] {item['name']:<30} {price_str:<14} {status:<12}")

    print("="*75)


def add_menu_item():
    """Add a new food item to the canteen menu."""
    print("\n" + "="*50)
    print("             ADD NEW MENU ITEM")
    print("="*50)
    menu = read_menu()
    
    # Generate new item ID
    next_id = "1"
    if menu:
        try:
            next_id = str(max(int(m["id"]) for m in menu if m["id"].isdigit()) + 1)
        except ValueError:
            next_id = str(len(menu) + 1)

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

    new_item = {
        "id": next_id,
        "name": name,
        "category": category,
        "price": f"{price_val:.2f}",
        "available": avail_str
    }
    menu.append(new_item)
    write_menu(menu)
    print(f"\n[+] SUCCESS! '{name}' added with Item ID #{next_id} at Rs. {price_val:.2f}.")


def update_menu_item():
    """Update price or availability of a menu item."""
    print("\n" + "="*50)
    print("           UPDATE MENU ITEM")
    print("="*50)
    display_menu()
    menu = read_menu()
    
    item_id = input("\nEnter Menu Item ID to update: ").strip()
    target = None
    for item in menu:
        if item["id"] == item_id:
            target = item
            break

    if not target:
        print(f"[-] Menu item #{item_id} not found.")
        return

    print(f"\nEditing: {target['name']} | Current Price: Rs.{target['price']} | Avail: {target['available']}")
    print("[1] Update Price")
    print("[2] Toggle Availability (In Stock / Out of Stock)")
    print("[3] Update Item Name")
    choice = input("Enter choice (1-3): ").strip()

    if choice == "1":
        try:
            new_price = float(input("Enter new price (INR): "))
            if new_price > 0:
                target["price"] = f"{new_price:.2f}"
                write_menu(menu)
                print(f"[+] Price updated to Rs. {new_price:.2f}.")
            else:
                print("[-] Price must be greater than zero.")
        except ValueError:
            print("[-] Invalid price input.")
    elif choice == "2":
        target["available"] = "No" if target["available"] == "Yes" else "Yes"
        write_menu(menu)
        print(f"[+] Availability updated to '{target['available']}'.")
    elif choice == "3":
        new_name = input("Enter new item name: ").strip()
        if new_name:
            target["name"] = new_name
            write_menu(menu)
            print(f"[+] Item name updated to '{new_name}'.")
    else:
        print("[-] Invalid choice.")


def delete_menu_item():
    """Remove a menu item from the catalog."""
    print("\n" + "="*50)
    print("           DELETE MENU ITEM")
    print("="*50)
    menu = read_menu()
    item_id = input("Enter Item ID to remove: ").strip()
    
    updated = [m for m in menu if m["id"] != item_id]
    if len(updated) == len(menu):
        print(f"[-] Item ID #{item_id} not found.")
    else:
        confirm = input(f"Are you sure you want to delete item #{item_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            write_menu(updated)
            print(f"[+] Item #{item_id} deleted successfully.")
        else:
            print("[*] Action cancelled.")


# ------------------------------------------------------------------------------
# ORDERING & BILLING WORKFLOW
# ------------------------------------------------------------------------------

def place_order():
    """Interactive food ordering workflow with cart and invoice generation."""
    print("\n" + "="*65)
    print("               PLACE CANTEEN FOOD ORDER")
    print("="*65)
    
    student_name = input("Enter Student / Staff Name : ").strip()
    if not student_name:
        print("[-] Name cannot be empty.")
        return
    student_id = input("Enter Student Roll No / ID  : ").strip()
    if not student_id:
        student_id = "N/A"

    menu = read_menu()
    menu_dict = {m["id"]: m for m in menu}

    cart = []  # List of dicts: {"item": m, "quantity": qty, "line_total": total}

    while True:
        display_menu()
        print("\n--- Current Cart Items: " + str(len(cart)) + " ---")
        if cart:
            for idx, c in enumerate(cart, 1):
                print(f"  {idx}. {c['item']['name']} - {c['quantity']} x Rs.{float(c['item']['price']):.2f} = Rs.{c['line_total']:.2f}")
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
        if selected_item["available"].lower() != "yes":
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

        # Check if already in cart -> update qty
        already_in_cart = False
        for c in cart:
            if c["item"]["id"] == item_id:
                c["quantity"] += qty
                c["line_total"] = c["quantity"] * float(c["item"]["price"])
                already_in_cart = True
                print(f"[+] Updated quantity of '{selected_item['name']}' to {c['quantity']}.")
                break

        if not already_in_cart:
            price = float(selected_item["price"])
            cart.append({
                "item": selected_item,
                "quantity": qty,
                "line_total": qty * price
            })
            print(f"[+] Added {qty}x '{selected_item['name']}' to cart.")

    # Checkout & Save Order
    orders = read_orders()
    order_id = get_next_order_id(orders)
    order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_bill = sum(c["line_total"] for c in cart)
    items_summary = ", ".join([f"{c['item']['name']} ({c['quantity']} x Rs.{float(c['item']['price']):.2f})" for c in cart])

    new_order = {
        "order_id": order_id,
        "student_name": student_name,
        "student_id": student_id,
        "items_summary": items_summary,
        "total_amount": f"{total_bill:.2f}",
        "order_date": order_time,
        "status": "Placed"
    }
    orders.append(new_order)
    write_orders(orders)

    # Print Official Bill Invoice
    print_invoice(new_order, cart)


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
            name = c['item']['name'][:24]
            qty = c['quantity']
            rate = f"{float(c['item']['price']):.2f}"
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
    """Display all orders placed with their status."""
    orders = read_orders()
    print("\n" + "="*95)
    print(f"                              ALL CANTEEN ORDERS ({len(orders)} Orders)")
    print("="*95)
    
    if not orders:
        print(" No orders placed yet.")
        print("-" * 95)
        return

    print(f"{'ID':<7}{'Customer':<18}{'Student ID':<12}{'Total':<12}{'Date/Time':<20}{'Status':<12}")
    print("-" * 95)
    for o in orders:
        print(f"#{o['order_id']:<6}{o['student_name'][:16]:<18}{o['student_id'][:10]:<12}Rs.{float(o['total_amount']):<9.2f}{o['order_date'][:19]:<20}{o['status']:<12}")
    print("-" * 95)


def search_order():
    """Search order by Order ID or Student Name."""
    print("\n" + "="*50)
    print("              SEARCH ORDERS")
    print("="*50)
    query = input("Enter Order ID or Student Name to search: ").strip().lower()
    if not query:
        print("[-] Search term cannot be empty.")
        return

    orders = read_orders()
    results = [o for o in orders if query in o["order_id"].lower() or query in o["student_name"].lower()]

    if not results:
        print(f"[-] No orders found matching '{query}'.")
        return

    for o in results:
        print("\n" + "-"*50)
        print(f"Order ID       : #{o['order_id']}")
        print(f"Student Name   : {o['student_name']} (ID: {o['student_id']})")
        print(f"Date & Time    : {o['order_date']}")
        print(f"Items Ordered  : {o['items_summary']}")
        print(f"Total Amount   : Rs. {float(o['total_amount']):.2f}")
        print(f"Current Status : {o['status']}")
        print("-"*50)


def update_order_status():
    """Canteen staff status update tool."""
    print("\n" + "="*50)
    print("           UPDATE ORDER STATUS")
    print("="*50)
    orders = read_orders()
    order_id = input("Enter Order ID (e.g. 1001): ").strip()

    target = None
    for o in orders:
        if o["order_id"] == order_id:
            target = o
            break

    if not target:
        print(f"[-] Order #{order_id} not found.")
        return

    print(f"Order #{order_id} for {target['student_name']} | Current Status: {target['status']}")
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
        target["status"] = status_map[choice]
        write_orders(orders)
        print(f"[+] Order #{order_id} status updated to '{target['status']}'.")
    else:
        print("[-] Invalid selection.")


def view_sales_report():
    """Display revenue metrics and order analytics."""
    orders = read_orders()
    menu = read_menu()

    total_orders = len(orders)
    total_revenue = sum(float(o["total_amount"]) for o in orders if o["status"] != "Cancelled")
    completed_orders = sum(1 for o in orders if o["status"] in ["Ready", "Collected"])

    print("\n" + "="*50)
    print("          CANTEEN DAILY SALES & REVENUE REPORT")
    print("="*50)
    print(f" Total Orders Logged     : {total_orders}")
    print(f" Completed / Collected   : {completed_orders}")
    print(f" Total Menu Items Active : {sum(1 for m in menu if m['available'].lower() == 'yes')} / {len(menu)}")
    print(f" Total Gross Revenue     : Rs. {total_revenue:.2f}")
    if total_orders > 0:
        avg_order = total_revenue / max(1, (total_orders - sum(1 for o in orders if o['status'] == 'Cancelled')))
        print(f" Average Order Value     : Rs. {avg_order:.2f}")
    print("="*50)


# ------------------------------------------------------------------------------
# MAIN MENU LOOP
# ------------------------------------------------------------------------------

def main():
    """Main execution loop."""
    initialize_files()
    while True:
        print("\n" + "="*55)
        print("      SCHOOL CANTEEN ORDERING & BILLING SYSTEM")
        print("      CBSE Class 12 Computer Science Project")
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
