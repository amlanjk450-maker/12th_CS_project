"""
================================================================================
PROJECT 3: STUDENT MARKETPLACE (PYTHON + MYSQL)
CBSE CLASS 12 COMPUTER SCIENCE FINAL PROJECT
================================================================================
Syllabus Topics Covered:
- Python-MySQL Connectivity (mysql.connector, connect, cursor, execute, commit)
- SQL Operations (CREATE, INSERT, SELECT, UPDATE, DELETE, ORDER BY, LIKE, AGGREGATES)
- Data Filtering & Multi-criteria Search Queries
- Dynamic Sorting using SQL & Python
- Input Validation (Positive numbers, non-empty fields)
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
    "database": "student_market_db"
}

CATEGORIES = [
    "Books",
    "Calculator",
    "Uniform",
    "Stationery",
    "Sports",
    "Electronics",
    "Other"
]

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
    """Create database 'student_market_db' and 'listings' table with sample records."""
    try:
        conn = get_db_connection(use_database=False)
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS student_market_db")
        cursor.execute("USE student_market_db")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_name VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                condition_status VARCHAR(30) NOT NULL,
                price DECIMAL(10,2) NOT NULL,
                seller_name VARCHAR(100) NOT NULL,
                student_id VARCHAR(50) NOT NULL,
                contact VARCHAR(50) NOT NULL,
                listed_date DATE NOT NULL,
                description TEXT,
                status VARCHAR(30) DEFAULT 'Available'
            )
        """)

        conn.commit()

        # Seed sample listings if empty
        cursor.execute("SELECT COUNT(*) FROM listings")
        if cursor.fetchone()[0] == 0:
            sample_data = [
                ("RD Sharma Class 12 Vol 1 & 2", "Books", "Good", 450.00, "Rahul Verma", "12A-15", "9876501234", "2026-09-02", "Both volumes in neat condition with plastic covers and solved notes", "Available"),
                ("Casio FX-991EX ClassWiz", "Calculator", "Like New", 800.00, "Ananya Sen", "12B-09", "9811223344", "2026-09-04", "Solar powered scientific calculator, used only for 3 months with original box", "Available"),
                ("School Blazer (Size 38)", "Uniform", "Good", 600.00, "Karan Mehra", "12C-22", "9899334455", "2026-09-05", "Navy blue winter blazer with school crest, dry cleaned and spotless", "Available"),
                ("Yonex Nanoray Badminton Racket", "Sports", "Fair", 350.00, "Siddharth Das", "11B-05", "9765432109", "2026-09-07", "Lightweight graphite racket with new grip tape and full cover", "Available"),
                ("HC Verma Concepts of Physics (Part 1)", "Books", "Like New", 220.00, "Pooja Roy", "12A-31", "9822446688", "2026-09-08", "Standard physics reference book without any markings or torn pages", "Sold")
            ]
            cursor.executemany("""
                INSERT INTO listings (item_name, category, condition_status, price, seller_name, student_id, contact, listed_date, description, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, sample_data)
            conn.commit()

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[!] Database Initialization Error: {err}")


# ------------------------------------------------------------------------------
# DISPLAY & FORMATTING HELPERS
# ------------------------------------------------------------------------------

def display_listings_table(listings, title="STUDENT MARKETPLACE LISTINGS"):
    """Render a clean ASCII table of listings from MySQL."""
    print("\n" + "="*96)
    print(f"                               {title.upper()} ({len(listings)} Items)")
    print("="*96)

    if not listings:
        print(" No items found matching criteria.")
        print("-" * 96)
        return

    header = f"{'ID':<6}{'Item Title':<28}{'Category':<14}{'Condition':<12}{'Price (INR)':<14}{'Seller':<12}{'Status':<10}"
    print(header)
    print("-" * 96)
    for item in listings:
        price_str = f"Rs. {float(item[4]):.2f}"
        print(f"#{item[0]:<5}{str(item[1])[:26]:<28}{str(item[2])[:12]:<14}{str(item[3])[:10]:<12}{price_str:<14}{str(item[5])[:10]:<12}{str(item[10])[:10]:<10}")
    print("-" * 96)


# ------------------------------------------------------------------------------
# CORE USER WORKFLOWS (MYSQL)
# ------------------------------------------------------------------------------

def browse_all_listings():
    """Display all available active listings from MySQL."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM listings WHERE status = 'Available' ORDER BY id DESC")
        rows = cursor.fetchall()
        display_listings_table(rows, "Active Items Available for Sale (MySQL)")
        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def add_listing():
    """Create a new student marketplace listing in MySQL."""
    print("\n" + "="*55)
    print("           ADD NEW ITEM LISTING (MYSQL)")
    print("="*55)

    item_name = input("Enter Item Title (e.g. RD Sharma Math Class 12): ").strip()
    if not item_name:
        print("[-] Item title cannot be empty.")
        return

    print("\nSelect Category:")
    for idx, cat in enumerate(CATEGORIES, 1):
        print(f" [{idx}] {cat}")
    cat_choice = input(f"Enter choice (1-{len(CATEGORIES)}): ").strip()
    try:
        cat_idx = int(cat_choice) - 1
        category = CATEGORIES[cat_idx] if 0 <= cat_idx < len(CATEGORIES) else "Other"
    except ValueError:
        category = "Other"

    print("\nSelect Condition: [1] Like New  [2] Good  [3] Fair")
    cond_choice = input("Enter choice (1-3): ").strip()
    cond_map = {"1": "Like New", "2": "Good", "3": "Fair"}
    condition = cond_map.get(cond_choice, "Good")

    try:
        price_val = float(input("Enter Expected Price in INR (e.g. 250.00): "))
        if price_val < 0:
            print("[-] Price cannot be negative.")
            return
    except ValueError:
        print("[-] Invalid numeric price entered.")
        return

    seller_name = input("Enter Seller Name (Student/Teacher) : ").strip()
    student_id = input("Enter Student ID / Roll & Section     : ").strip()
    contact = input("Enter Contact Mobile Number / WhatsApp: ").strip()
    description = input("Enter Detailed Description of the Item: ").strip()
    today_str = datetime.date.today().strftime("%Y-%m-%d")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO listings (item_name, category, condition_status, price, seller_name, student_id, contact, listed_date, description, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Available')
        """
        cursor.execute(sql, (
            item_name,
            category,
            condition,
            price_val,
            seller_name if seller_name else "Anonymous",
            student_id if student_id else "N/A",
            contact if contact else "N/A",
            today_str,
            description
        ))
        conn.commit()
        item_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"\n[+] SUCCESS! Item listed successfully in MySQL with Listing ID #{item_id}.")
    except Error as err:
        print(f"[-] Database Error: {err}")


def search_and_filter():
    """Filter and search items in MySQL by keywords, category, or price range."""
    print("\n" + "="*50)
    print("           SEARCH & FILTER LISTINGS")
    print("="*50)
    print(" [1] Search by Keyword (Title / Description)")
    print(" [2] Filter by Category")
    print(" [3] Filter by Maximum Price Budget")
    print(" [4] View All Items (Available + Sold)")
    choice = input("Select search type (1-4): ").strip()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if choice == "1":
            kw = input("Enter search keyword: ").strip()
            if not kw:
                print("[-] Keyword cannot be empty.")
            else:
                param = f"%{kw}%"
                sql = "SELECT * FROM listings WHERE item_name LIKE %s OR description LIKE %s OR category LIKE %s"
                cursor.execute(sql, (param, param, param))
                display_listings_table(cursor.fetchall(), f"Search Results for '{kw}'")

        elif choice == "2":
            print("\nCategories:")
            for idx, cat in enumerate(CATEGORIES, 1):
                print(f" [{idx}] {cat}")
            c_choice = input(f"Choose category (1-{len(CATEGORIES)}): ").strip()
            try:
                target_cat = CATEGORIES[int(c_choice) - 1]
                sql = "SELECT * FROM listings WHERE category = %s"
                cursor.execute(sql, (target_cat,))
                display_listings_table(cursor.fetchall(), f"Category: {target_cat}")
            except (ValueError, IndexError):
                print("[-] Invalid category choice.")

        elif choice == "3":
            try:
                max_p = float(input("Enter maximum budget limit (INR): "))
                sql = "SELECT * FROM listings WHERE price <= %s AND status = 'Available' ORDER BY price ASC"
                cursor.execute(sql, (max_p,))
                display_listings_table(cursor.fetchall(), f"Items within Budget <= Rs.{max_p:.2f}")
            except ValueError:
                print("[-] Invalid budget amount.")

        elif choice == "4":
            cursor.execute("SELECT * FROM listings ORDER BY id DESC")
            display_listings_table(cursor.fetchall(), "Complete Marketplace Archives")
        else:
            print("[-] Invalid selection.")

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def view_listing_details():
    """View detailed card info for a specific listing from MySQL."""
    print("\n" + "="*50)
    print("             ITEM FULL DETAILS")
    print("="*50)
    item_id = input("Enter Listing ID to view: ").strip()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM listings WHERE id = %s", (item_id,))
        target = cursor.fetchone()
        cursor.close()
        conn.close()

        if not target:
            print(f"[-] Item with ID #{item_id} not found.")
            return

        print("\n" + "*"*50)
        print(f" LISTING #{target[0]} : {str(target[1]).upper()}")
        print("*"*50)
        print(f" Category     : {target[2]}")
        print(f" Condition    : {target[3]}")
        print(f" Listed Price : Rs. {float(target[4]):.2f}")
        print(f" Status       : {target[10].upper()}")
        print(f" Listed Date  : {target[8]}")
        print(f" Seller Name  : {target[5]} (Student ID: {target[6]})")
        print(f" Contact Info : {target[7]}")
        print(f" Description  : {target[9]}")
        print("*"*50)
    except Error as err:
        print(f"[-] Database Error: {err}")


def sort_listings():
    """Sort and display listings using SQL ORDER BY."""
    print("\n" + "="*50)
    print("               SORT LISTINGS")
    print("="*50)
    print(" [1] Price: Low to High")
    print(" [2] Price: High to Low")
    print(" [3] Most Recently Listed")
    sort_choice = input("Enter sorting option (1-3): ").strip()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        if sort_choice == "1":
            cursor.execute("SELECT * FROM listings WHERE status = 'Available' ORDER BY price ASC")
            display_listings_table(cursor.fetchall(), "Items Sorted: Price (Low to High)")
        elif sort_choice == "2":
            cursor.execute("SELECT * FROM listings WHERE status = 'Available' ORDER BY price DESC")
            display_listings_table(cursor.fetchall(), "Items Sorted: Price (High to Low)")
        elif sort_choice == "3":
            cursor.execute("SELECT * FROM listings WHERE status = 'Available' ORDER BY listed_date DESC, id DESC")
            display_listings_table(cursor.fetchall(), "Items Sorted: Most Recent First")
        else:
            print("[-] Invalid sort choice.")

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def mark_item_sold():
    """Mark a listing as Sold in MySQL upon transaction completion."""
    print("\n" + "="*50)
    print("             MARK ITEM AS SOLD")
    print("="*50)
    item_id = input("Enter Listing ID: ").strip()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT item_name, status FROM listings WHERE id = %s", (item_id,))
        target = cursor.fetchone()

        if not target:
            print(f"[-] Listing #{item_id} not found.")
            cursor.close()
            conn.close()
            return

        print(f"Item: {target[0]} | Current Status: {target[1]}")
        if target[1] == "Sold":
            print("[!] Item is already marked as SOLD.")
            reopen = input("Do you want to reopen listing to 'Available'? (y/n): ").strip().lower()
            if reopen == 'y':
                cursor.execute("UPDATE listings SET status = 'Available' WHERE id = %s", (item_id,))
                conn.commit()
                print(f"[+] Listing #{item_id} status updated to 'Available' in MySQL.")
            cursor.close()
            conn.close()
            return

        confirm = input(f"Confirm item '{target[0]}' was SOLD? (y/n): ").strip().lower()
        if confirm == 'y':
            cursor.execute("UPDATE listings SET status = 'Sold' WHERE id = %s", (item_id,))
            conn.commit()
            print(f"[+] Listing #{item_id} marked as SOLD in MySQL.")
        else:
            print("[*] Status not changed.")

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def delete_listing():
    """Delete a listing from MySQL."""
    print("\n" + "="*50)
    print("              DELETE LISTING")
    print("="*50)
    item_id = input("Enter Listing ID to delete: ").strip()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT item_name FROM listings WHERE id = %s", (item_id,))
        target = cursor.fetchone()

        if not target:
            print(f"[-] Listing #{item_id} not found.")
        else:
            confirm = input(f"Permanently remove listing #{item_id} ({target[0]})? (y/n): ").strip().lower()
            if confirm == 'y':
                cursor.execute("DELETE FROM listings WHERE id = %s", (item_id,))
                conn.commit()
                print(f"[+] Listing #{item_id} deleted successfully from MySQL.")
            else:
                print("[*] Deletion cancelled.")

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def marketplace_insights():
    """Display analytics, price highlights, and category breakdowns using SQL aggregates."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM listings")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM listings WHERE status = 'Available'")
        available_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM listings WHERE status = 'Sold'")
        sold_count = cursor.fetchone()[0]

        print("\n" + "="*55)
        print("         STUDENT MARKETPLACE INSIGHTS (MYSQL)")
        print("="*55)
        print(f" Total Items Registered     : {total}")
        print(f" Currently Available        : {available_count}")
        print(f" Items Successfully Sold    : {sold_count}")

        if available_count > 0:
            cursor.execute("SELECT id, item_name, price FROM listings WHERE status = 'Available' ORDER BY price ASC LIMIT 1")
            cheapest = cursor.fetchone()

            cursor.execute("SELECT id, item_name, price FROM listings WHERE status = 'Available' ORDER BY price DESC LIMIT 1")
            priciest = cursor.fetchone()

            cursor.execute("SELECT AVG(price) FROM listings WHERE status = 'Available'")
            avg_price = float(cursor.fetchone()[0])

            print("-" * 55)
            print(f" Lowest Price Item          : Rs. {float(cheapest[2]):.2f} (#{cheapest[0]} - {cheapest[1]})")
            print(f" Highest Price Item         : Rs. {float(priciest[2]):.2f} (#{priciest[0]} - {priciest[1]})")
            print(f" Average Listing Price      : Rs. {avg_price:.2f}")

        print("-" * 55)
        print(" Category Distribution (Active):")
        cursor.execute("SELECT category, COUNT(*) FROM listings WHERE status = 'Available' GROUP BY category ORDER BY COUNT(*) DESC")
        for cat, cnt in cursor.fetchall():
            print(f"  - {cat:<18}: {cnt} item(s)")
        print("="*55)

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


# ------------------------------------------------------------------------------
# MAIN MENU LOOP
# ------------------------------------------------------------------------------

def main():
    """Main program loop and menu driver."""
    initialize_database()
    while True:
        print("\n" + "="*55)
        print("     STUDENT-TO-STUDENT MARKETPLACE (MYSQL)")
        print("      CBSE Class 12 Computer Science Project")
        print("="*55)
        print(" [1]  Browse Available Listings")
        print(" [2]  Add New Listing (Sell an Item)")
        print(" [3]  Search & Filter (Keyword / Category / Budget)")
        print(" [4]  View Detailed Item Information")
        print(" [5]  Sort Listings (By Price / Recent)")
        print(" [6]  Mark Item as SOLD")
        print(" [7]  Delete a Listing")
        print(" [8]  Marketplace Insights & Analytics")
        print(" [9]  Exit")
        print("="*55)

        choice = input("Enter your choice (1-9): ").strip()

        if choice == "1":
            browse_all_listings()
        elif choice == "2":
            add_listing()
        elif choice == "3":
            search_and_filter()
        elif choice == "4":
            view_listing_details()
        elif choice == "5":
            sort_listings()
        elif choice == "6":
            mark_item_sold()
        elif choice == "7":
            delete_listing()
        elif choice == "8":
            marketplace_insights()
        elif choice == "9":
            print("\nThank you for using Student Marketplace. Happy Learning & Trading!")
            break
        else:
            print("\n[-] Invalid selection! Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()
