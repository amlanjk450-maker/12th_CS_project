"""
================================================================================
PROJECT 3: STUDENT MARKETPLACE (PEER-TO-PEER STUDENT EXCHANGE)
CBSE CLASS 12 COMPUTER SCIENCE FINAL PROJECT (SINGLE FILE SYSTEM)
================================================================================
Syllabus Topics Covered:
- Python Functions (User-defined functions, arguments, return values)
- File Handling (CSV module - reader, writer, DictReader, DictWriter)
- Data Filtering & Sorting Algorithms (Lambda keys, comparisons, price bounds)
- String Manipulation and Text Formatting
- Input Validation (Positive numeric bounds, non-empty text, option verification)
- Error Handling with try-except blocks
================================================================================
"""

import csv
import os
import datetime

# CSV File Constants
MARKETPLACE_FILE = "student_marketplace.csv"

FIELDS = [
    "id",
    "item_name",
    "category",
    "condition",
    "price",
    "seller_name",
    "student_id",
    "contact",
    "listed_date",
    "description",
    "status"
]

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
# DATABASE / FILE INITIALIZATION & HELPERS
# ------------------------------------------------------------------------------

def initialize_files():
    """Create CSV file with initial sample listings if not present."""
    if not os.path.exists(MARKETPLACE_FILE):
        with open(MARKETPLACE_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            sample_data = [
                {
                    "id": "1",
                    "item_name": "RD Sharma Class 12 Vol 1 & 2",
                    "category": "Books",
                    "condition": "Good",
                    "price": "450.00",
                    "seller_name": "Rahul Verma",
                    "student_id": "12A-15",
                    "contact": "9876501234",
                    "listed_date": "2026-09-02",
                    "description": "Both volumes in neat condition with plastic covers and solved notes",
                    "status": "Available"
                },
                {
                    "id": "2",
                    "item_name": "Casio FX-991EX ClassWiz",
                    "category": "Calculator",
                    "condition": "Like New",
                    "price": "800.00",
                    "seller_name": "Ananya Sen",
                    "student_id": "12B-09",
                    "contact": "9811223344",
                    "listed_date": "2026-09-04",
                    "description": "Solar powered scientific calculator, used only for 3 months with original box",
                    "status": "Available"
                },
                {
                    "id": "3",
                    "item_name": "School Blazer (Size 38)",
                    "category": "Uniform",
                    "condition": "Good",
                    "price": "600.00",
                    "seller_name": "Karan Mehra",
                    "student_id": "12C-22",
                    "contact": "9899334455",
                    "listed_date": "2026-09-05",
                    "description": "Navy blue winter blazer with school crest, dry cleaned and spotless",
                    "status": "Available"
                },
                {
                    "id": "4",
                    "item_name": "Yonex Nanoray Badminton Racket",
                    "category": "Sports",
                    "condition": "Fair",
                    "price": "350.00",
                    "seller_name": "Siddharth Das",
                    "student_id": "11B-05",
                    "contact": "9765432109",
                    "listed_date": "2026-09-07",
                    "description": "Lightweight graphite racket with new grip tape and full cover",
                    "status": "Available"
                },
                {
                    "id": "5",
                    "item_name": "HC Verma Concepts of Physics (Part 1)",
                    "category": "Books",
                    "condition": "Like New",
                    "price": "220.00",
                    "seller_name": "Pooja Roy",
                    "student_id": "12A-31",
                    "contact": "9822446688",
                    "listed_date": "2026-09-08",
                    "description": "Standard physics reference book without any markings or torn pages",
                    "status": "Sold"
                }
            ]
            writer.writerows(sample_data)


def read_listings():
    """Read all listings from the CSV file."""
    listings = []
    if os.path.exists(MARKETPLACE_FILE):
        with open(MARKETPLACE_FILE, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                listings.append(row)
    return listings


def write_listings(listings):
    """Write listings back to CSV."""
    with open(MARKETPLACE_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(listings)


def get_next_id(listings):
    """Generate next sequential integer ID."""
    if not listings:
        return "1"
    try:
        max_id = max(int(item["id"]) for item in listings if item["id"].isdigit())
        return str(max_id + 1)
    except ValueError:
        return str(len(listings) + 1)


# ------------------------------------------------------------------------------
# DISPLAY & FORMATTING HELPERS
# ------------------------------------------------------------------------------

def display_listings_table(listings, title="STUDENT MARKETPLACE LISTINGS"):
    """Render a clean ASCII table of listings."""
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
        price_str = f"Rs. {float(item['price']):.2f}"
        print(f"#{item['id']:<5}{item['item_name'][:26]:<28}{item['category'][:12]:<14}{item['condition'][:10]:<12}{price_str:<14}{item['seller_name'][:10]:<12}{item['status']:<10}")
    print("-" * 96)


# ------------------------------------------------------------------------------
# CORE USER WORKFLOWS
# ------------------------------------------------------------------------------

def browse_all_listings():
    """Display all available active listings."""
    listings = read_listings()
    available = [item for item in listings if item.get("status") == "Available"]
    display_listings_table(available, "Active Items Available for Sale")


def add_listing():
    """Create a new student marketplace listing."""
    print("\n" + "="*55)
    print("               ADD NEW ITEM LISTING")
    print("="*55)
    
    listings = read_listings()
    item_id = get_next_id(listings)

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

    new_listing = {
        "id": item_id,
        "item_name": item_name,
        "category": category,
        "condition": condition,
        "price": f"{price_val:.2f}",
        "seller_name": seller_name if seller_name else "Anonymous",
        "student_id": student_id if student_id else "N/A",
        "contact": contact if contact else "N/A",
        "listed_date": today_str,
        "description": description,
        "status": "Available"
    }

    listings.append(new_listing)
    write_listings(listings)
    print(f"\n[+] SUCCESS! Item listed successfully with Listing ID #{item_id}.")


def search_and_filter():
    """Filter and search items by keywords, category, or price range."""
    print("\n" + "="*50)
    print("           SEARCH & FILTER LISTINGS")
    print("="*50)
    print(" [1] Search by Keyword (Title / Description)")
    print(" [2] Filter by Category")
    print(" [3] Filter by Maximum Price Budget")
    print(" [4] View All Items (Available + Sold)")
    choice = input("Select search type (1-4): ").strip()

    listings = read_listings()

    if choice == "1":
        kw = input("Enter search keyword: ").strip().lower()
        if not kw:
            print("[-] Keyword cannot be empty.")
            return
        results = [i for i in listings if kw in (i['item_name'] + i['description'] + i['category']).lower()]
        display_listings_table(results, f"Search Results for '{kw}'")

    elif choice == "2":
        print("\nCategories:")
        for idx, cat in enumerate(CATEGORIES, 1):
            print(f" [{idx}] {cat}")
        c_choice = input(f"Choose category (1-{len(CATEGORIES)}): ").strip()
        try:
            target_cat = CATEGORIES[int(c_choice) - 1]
            results = [i for i in listings if i['category'].lower() == target_cat.lower()]
            display_listings_table(results, f"Category: {target_cat}")
        except (ValueError, IndexError):
            print("[-] Invalid category choice.")

    elif choice == "3":
        try:
            max_p = float(input("Enter maximum budget limit (INR): "))
            results = [i for i in listings if float(i['price']) <= max_p and i['status'] == "Available"]
            display_listings_table(results, f"Items within Budget <= Rs.{max_p:.2f}")
        except ValueError:
            print("[-] Invalid budget amount.")

    elif choice == "4":
        display_listings_table(listings, "Complete Marketplace Archives")
    else:
        print("[-] Invalid selection.")


def view_listing_details():
    """View detailed card info for a specific listing."""
    print("\n" + "="*50)
    print("             ITEM FULL DETAILS")
    print("="*50)
    item_id = input("Enter Listing ID to view: ").strip()
    
    listings = read_listings()
    target = next((i for i in listings if i["id"] == item_id), None)

    if not target:
        print(f"[-] Item with ID #{item_id} not found.")
        return

    print("\n" + "*"*50)
    print(f" LISTING #{target['id']} : {target['item_name'].upper()}")
    print("*"*50)
    print(f" Category     : {target['category']}")
    print(f" Condition    : {target['condition']}")
    print(f" Listed Price : Rs. {float(target['price']):.2f}")
    print(f" Status       : {target['status'].upper()}")
    print(f" Listed Date  : {target['listed_date']}")
    print(f" Seller Name  : {target['seller_name']} (Student ID: {target['student_id']})")
    print(f" Contact Info : {target['contact']}")
    print(f" Description  : {target['description']}")
    print("*"*50)


def sort_listings():
    """Sort and display listings based on user preference."""
    print("\n" + "="*50)
    print("               SORT LISTINGS")
    print("="*50)
    print(" [1] Price: Low to High")
    print(" [2] Price: High to Low")
    print(" [3] Most Recently Listed")
    sort_choice = input("Enter sorting option (1-3): ").strip()

    listings = [i for i in read_listings() if i.get("status") == "Available"]

    if sort_choice == "1":
        listings.sort(key=lambda x: float(x["price"]))
        display_listings_table(listings, "Items Sorted: Price (Low to High)")
    elif sort_choice == "2":
        listings.sort(key=lambda x: float(x["price"]), reverse=True)
        display_listings_table(listings, "Items Sorted: Price (High to Low)")
    elif sort_choice == "3":
        listings.sort(key=lambda x: x.get("listed_date", ""), reverse=True)
        display_listings_table(listings, "Items Sorted: Most Recent First")
    else:
        print("[-] Invalid sort choice.")


def mark_item_sold():
    """Mark a listing as Sold upon transaction completion."""
    print("\n" + "="*50)
    print("             MARK ITEM AS SOLD")
    print("="*50)
    item_id = input("Enter Listing ID: ").strip()

    listings = read_listings()
    target = next((i for i in listings if i["id"] == item_id), None)

    if not target:
        print(f"[-] Listing #{item_id} not found.")
        return

    print(f"Item: {target['item_name']} | Current Status: {target['status']}")
    if target["status"] == "Sold":
        print("[!] Item is already marked as SOLD.")
        reopen = input("Do you want to reopen listing to 'Available'? (y/n): ").strip().lower()
        if reopen == 'y':
            target["status"] = "Available"
            write_listings(listings)
            print(f"[+] Listing #{item_id} status updated to 'Available'.")
        return

    confirm = input(f"Confirm item '{target['item_name']}' was SOLD? (y/n): ").strip().lower()
    if confirm == 'y':
        target["status"] = "Sold"
        write_listings(listings)
        print(f"[+] Listing #{item_id} marked as SOLD.")
    else:
        print("[*] Status not changed.")


def delete_listing():
    """Delete a listing from the marketplace."""
    print("\n" + "="*50)
    print("              DELETE LISTING")
    print("="*50)
    item_id = input("Enter Listing ID to delete: ").strip()

    listings = read_listings()
    updated = [i for i in listings if i["id"] != item_id]

    if len(updated) == len(listings):
        print(f"[-] Listing #{item_id} not found.")
    else:
        confirm = input(f"Permanently remove listing #{item_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            write_listings(updated)
            print(f"[+] Listing #{item_id} deleted successfully.")
        else:
            print("[*] Deletion cancelled.")


def marketplace_insights():
    """Display analytics, price highlights, and category breakdowns."""
    listings = read_listings()
    if not listings:
        print("\nNo listings available for analysis.")
        return

    total = len(listings)
    available_items = [i for i in listings if i["status"] == "Available"]
    sold_count = sum(1 for i in listings if i["status"] == "Sold")

    print("\n" + "="*55)
    print("            STUDENT MARKETPLACE INSIGHTS")
    print("="*55)
    print(f" Total Items Registered     : {total}")
    print(f" Currently Available        : {len(available_items)}")
    print(f" Items Successfully Sold    : {sold_count}")

    if available_items:
        cheapest = min(available_items, key=lambda x: float(x["price"]))
        priciest = max(available_items, key=lambda x: float(x["price"]))
        avg_price = sum(float(i["price"]) for i in available_items) / len(available_items)

        print("-" * 55)
        print(f" Lowest Price Item          : Rs. {float(cheapest['price']):.2f} (#{cheapest['id']} - {cheapest['item_name']})")
        print(f" Highest Price Item         : Rs. {float(priciest['price']):.2f} (#{priciest['id']} - {priciest['item_name']})")
        print(f" Average Listing Price      : Rs. {avg_price:.2f}")

    print("-" * 55)
    print(" Category Distribution (Active):")
    cat_counts = {}
    for i in available_items:
        cat_counts[i["category"]] = cat_counts.get(i["category"], 0) + 1
    for cat, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {cat:<18}: {count} item(s)")
    print("="*55)


# ------------------------------------------------------------------------------
# MAIN MENU LOOP
# ------------------------------------------------------------------------------

def main():
    """Main program loop and menu driver."""
    initialize_files()
    while True:
        print("\n" + "="*55)
        print("         STUDENT-TO-STUDENT MARKETPLACE")
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
