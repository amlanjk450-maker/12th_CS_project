"""
================================================================================
PROJECT 1: LOST & FOUND MATCHER
CBSE CLASS 12 COMPUTER SCIENCE FINAL PROJECT (SINGLE FILE SYSTEM)
================================================================================
Syllabus Topics Covered:
- Python Functions (User-defined functions, default parameters, return values)
- File Handling (CSV module - reader, writer, DictReader, DictWriter)
- Data Structures (Lists, Dictionaries, Tuples, Strings)
- Text Normalization and Heuristic Matching Algorithm (Rule-based scoring)
- Error Handling (try-except blocks) & Input Validation
================================================================================
"""

import csv
import os
import datetime

# CSV File Constants
LOST_FILE = "lost_items.csv"
FOUND_FILE = "found_items.csv"

LOST_FIELDS = ["id", "item_name", "category", "color", "location", "date", "reporter", "contact", "description", "status"]
FOUND_FIELDS = ["id", "item_name", "category", "color", "location", "date", "finder", "contact", "description", "status"]

# ------------------------------------------------------------------------------
# DATABASE / FILE INITIALIZATION & HELPERS
# ------------------------------------------------------------------------------

def initialize_files():
    """Create CSV files with sample data if they do not exist."""
    if not os.path.exists(LOST_FILE):
        with open(LOST_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=LOST_FIELDS)
            writer.writeheader()
            sample_lost = [
                {
                    "id": "101",
                    "item_name": "Titan Black Watch",
                    "category": "Accessories",
                    "color": "Black",
                    "location": "Physics Lab",
                    "date": "2026-09-01",
                    "reporter": "Aman Sharma",
                    "contact": "9876543210",
                    "description": "Analog watch with silver dial and black leather strap",
                    "status": "Lost"
                },
                {
                    "id": "102",
                    "item_name": "Classmate Notebook",
                    "category": "Stationery",
                    "color": "Blue",
                    "location": "Library 2nd Floor",
                    "date": "2026-09-03",
                    "reporter": "Pooja Verma",
                    "contact": "9811223344",
                    "description": "Thick ruled notebook with Chemistry notes and name label",
                    "status": "Lost"
                },
                {
                    "id": "103",
                    "item_name": "Wildcraft Water Bottle",
                    "category": "Bottles",
                    "color": "Blue",
                    "location": "Playground",
                    "date": "2026-09-05",
                    "reporter": "Rohan Gupta",
                    "contact": "9899001122",
                    "description": "Steel insulated bottle with a small dent on the cap",
                    "status": "Lost"
                },
                {
                    "id": "104",
                    "item_name": "Casio Scientific Calculator",
                    "category": "Electronics",
                    "color": "Grey",
                    "location": "Room 104",
                    "date": "2026-09-08",
                    "reporter": "Sneha Roy",
                    "contact": "9765432109",
                    "description": "Model fx-991EX with small sticker of Mickey Mouse on back",
                    "status": "Lost"
                }
            ]
            writer.writerows(sample_lost)

    if not os.path.exists(FOUND_FILE):
        with open(FOUND_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FOUND_FIELDS)
            writer.writeheader()
            sample_found = [
                {
                    "id": "201",
                    "item_name": "Black Wrist Watch",
                    "category": "Accessories",
                    "color": "Black",
                    "location": "Physics Lab",
                    "date": "2026-09-02",
                    "finder": "Lab Assistant Ravi",
                    "contact": "9800112233",
                    "description": "Titan watch found near experiment table #4 with black strap",
                    "status": "Found"
                },
                {
                    "id": "202",
                    "item_name": "Blue Steel Bottle",
                    "category": "Bottles",
                    "color": "Blue",
                    "location": "Sports Ground",
                    "date": "2026-09-06",
                    "finder": "Coach Kapoor",
                    "contact": "9877001122",
                    "description": "Wildcraft metallic blue bottle picked up from football bench",
                    "status": "Found"
                },
                {
                    "id": "203",
                    "item_name": "Red Geometry Box",
                    "category": "Stationery",
                    "color": "Red",
                    "location": "Math Lab",
                    "date": "2026-09-07",
                    "finder": "Karan Singh",
                    "contact": "9812345678",
                    "description": "Camlin geometry box with complete compass set",
                    "status": "Found"
                },
                {
                    "id": "204",
                    "item_name": "Scientific Calculator Casio",
                    "category": "Electronics",
                    "color": "Grey",
                    "location": "Room 104",
                    "date": "2026-09-09",
                    "finder": "Neha Sen",
                    "contact": "9833445566",
                    "description": "Casio calculator left on back bench",
                    "status": "Found"
                }
            ]
            writer.writerows(sample_found)


def read_records(filename):
    """Read all records from a CSV file and return as list of dicts."""
    records = []
    if os.path.exists(filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
    return records


def write_records(filename, fieldnames, records):
    """Overwrite a CSV file with updated records."""
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def get_next_id(records, prefix="10"):
    """Generate next auto-increment integer ID."""
    if not records:
        return f"{prefix}1"
    try:
        max_id = max(int(r["id"]) for r in records if r["id"].isdigit())
        return str(max_id + 1)
    except ValueError:
        return f"{prefix}{len(records) + 1}"


# ------------------------------------------------------------------------------
# TEXT PROCESSING & SMART MATCHING ALGORITHM
# ------------------------------------------------------------------------------

def normalize_text(text):
    """Clean text by converting to lowercase and removing punctuation."""
    if not text:
        return ""
    clean = ""
    for char in text.lower():
        if char.isalnum() or char.isspace():
            clean += char
        else:
            clean += " "
    return clean.strip()


def calculate_match_score(lost_item, found_item):
    """
    Class 12 Heuristic Matcher:
    Compares Lost vs Found item attributes and returns a confidence percentage (0 - 100).
    Scoring Weightage:
    - Item Name / Substring match: up to 35 points
    - Category match: 20 points
    - Color match: 20 points
    - Location similarity: 15 points
    - Description keyword overlap: up to 10 points
    """
    score = 0
    reasons = []

    lost_name = normalize_text(lost_item.get("item_name", ""))
    found_name = normalize_text(found_item.get("item_name", ""))
    lost_words = set(lost_name.split())
    found_words = set(found_name.split())

    # 1. Item Name Matching (Up to 35 pts)
    common_words = lost_words.intersection(found_words)
    stop_words = {"the", "a", "an", "and", "with", "in", "of", "for", "have", "has"}
    meaningful_common = [w for w in common_words if w not in stop_words and len(w) > 1]
    if lost_name == found_name and lost_name:
        score += 35
        reasons.append("Exact name match (+35%)")
    elif len(meaningful_common) >= 2:
        score += 30
        reasons.append(f"Name keywords matched: {', '.join(meaningful_common)} (+30%)")
    elif len(meaningful_common) == 1:
        score += 20
        reasons.append(f"Name keyword matched: {meaningful_common[0]} (+20%)")
    elif any(word in found_name for word in lost_words if len(word) > 2) or any(word in lost_name for word in found_words if len(word) > 2):
        score += 15
        reasons.append("Partial name match (+15%)")

    # 2. Category Match (20 pts)
    lost_cat = normalize_text(lost_item.get("category", ""))
    found_cat = normalize_text(found_item.get("category", ""))
    if lost_cat and found_cat and lost_cat == found_cat:
        score += 20
        reasons.append(f"Same category: {lost_item['category']} (+20%)")

    # 3. Color Match (20 pts)
    lost_color = normalize_text(lost_item.get("color", ""))
    found_color = normalize_text(found_item.get("color", ""))
    if lost_color and found_color:
        if lost_color == found_color:
            score += 20
            reasons.append(f"Exact color match: {lost_item['color']} (+20%)")
        elif lost_color in found_color or found_color in lost_color:
            score += 15
            reasons.append("Similar color (+15%)")

    # 4. Location Match (15 pts)
    lost_loc = normalize_text(lost_item.get("location", ""))
    found_loc = normalize_text(found_item.get("location", ""))
    if lost_loc and found_loc:
        lost_loc_words = set(lost_loc.split()) - stop_words
        found_loc_words = set(found_loc.split()) - stop_words
        loc_overlap = lost_loc_words.intersection(found_loc_words)
        if lost_loc == found_loc:
            score += 15
            reasons.append(f"Exact location: {lost_item['location']} (+15%)")
        elif len(loc_overlap) > 0:
            score += 10
            reasons.append(f"Nearby location ({', '.join(loc_overlap)}) (+10%)")

    # 5. Description Keyword Overlap (Up to 10 pts)
    lost_desc_words = set(normalize_text(lost_item.get("description", "")).split()) - stop_words
    found_desc_words = set(normalize_text(found_item.get("description", "")).split()) - stop_words
    desc_overlap = lost_desc_words.intersection(found_desc_words)
    meaningful_desc = [w for w in desc_overlap if len(w) > 2]
    if len(meaningful_desc) >= 2:
        score += 10
        reasons.append(f"Description keywords: {', '.join(meaningful_desc[:3])} (+10%)")
    elif len(meaningful_desc) == 1:
        score += 5
        reasons.append(f"Description keyword: {meaningful_desc[0]} (+5%)")

    return min(score, 100), reasons


# ------------------------------------------------------------------------------
# CORE APPLICATION FUNCTIONS
# ------------------------------------------------------------------------------

def report_lost_item():
    """Collect details from user and save new lost item record."""
    print("\n" + "="*50)
    print("           REPORT A LOST ITEM")
    print("="*50)
    
    records = read_records(LOST_FILE)
    item_id = get_next_id(records, prefix="10")

    item_name = input("Enter Item Name (e.g. Titan Watch, Calculator) : ").strip()
    if not item_name:
        print("[-] Item name cannot be empty. Aborted.")
        return

    print("Categories: [1] Electronics  [2] Stationery  [3] Accessories  [4] Bags/Bottles  [5] Clothing  [6] Other")
    cat_choice = input("Select category (1-6) or type custom category: ").strip()
    cat_map = {"1": "Electronics", "2": "Stationery", "3": "Accessories", "4": "Bags/Bottles", "5": "Clothing", "6": "Other"}
    category = cat_map.get(cat_choice, cat_choice if cat_choice else "Other")

    color = input("Enter Primary Color : ").strip()
    location = input("Where was it lost? (e.g. Physics Lab, Library) : ").strip()
    
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    date_input = input(f"Enter Date Lost [YYYY-MM-DD] (Press Enter for today: {today_str}): ").strip()
    date_val = date_input if date_input else today_str

    reporter = input("Enter Your Name (Student/Staff) : ").strip()
    contact = input("Enter Contact Number / Roll No : ").strip()
    description = input("Detailed Description / Distinguishing marks : ").strip()

    new_record = {
        "id": item_id,
        "item_name": item_name,
        "category": category,
        "color": color,
        "location": location,
        "date": date_val,
        "reporter": reporter,
        "contact": contact,
        "description": description,
        "status": "Lost"
    }

    records.append(new_record)
    write_records(LOST_FILE, LOST_FIELDS, records)
    print(f"\n[+] SUCCESS! Lost item reported successfully with ID #{item_id}.")


def report_found_item():
    """Collect details from user and save new found item record."""
    print("\n" + "="*50)
    print("           REPORT A FOUND ITEM")
    print("="*50)
    
    records = read_records(FOUND_FILE)
    item_id = get_next_id(records, prefix="20")

    item_name = input("Enter Item Name (e.g. Blue Bottle, Watch) : ").strip()
    if not item_name:
        print("[-] Item name cannot be empty. Aborted.")
        return

    print("Categories: [1] Electronics  [2] Stationery  [3] Accessories  [4] Bags/Bottles  [5] Clothing  [6] Other")
    cat_choice = input("Select category (1-6) or type custom category: ").strip()
    cat_map = {"1": "Electronics", "2": "Stationery", "3": "Accessories", "4": "Bags/Bottles", "5": "Clothing", "6": "Other"}
    category = cat_map.get(cat_choice, cat_choice if cat_choice else "Other")

    color = input("Enter Primary Color : ").strip()
    location = input("Where was it found? (e.g. Playground bench) : ").strip()
    
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    date_input = input(f"Enter Date Found [YYYY-MM-DD] (Press Enter for today: {today_str}): ").strip()
    date_val = date_input if date_input else today_str

    finder = input("Enter Finder's Name / Submitter : ").strip()
    contact = input("Enter Contact Number / Deposit Location : ").strip()
    description = input("Detailed Description / Condition : ").strip()

    new_record = {
        "id": item_id,
        "item_name": item_name,
        "category": category,
        "color": color,
        "location": location,
        "date": date_val,
        "finder": finder,
        "contact": contact,
        "description": description,
        "status": "Found"
    }

    records.append(new_record)
    write_records(FOUND_FILE, FOUND_FIELDS, records)
    print(f"\n[+] SUCCESS! Found item registered with ID #{item_id}.")


def display_table(records, title, is_lost=True):
    """Print tabular formatted records."""
    print("\n" + "="*88)
    print(f"                       {title.upper()} ({len(records)} Records)")
    print("="*88)
    if not records:
        print(" No records found.")
        print("-" * 88)
        return

    person_label = "Reporter" if is_lost else "Finder"
    header = f"{'ID':<6}{'Item Name':<20}{'Category':<14}{'Color':<10}{'Location':<18}{'Date':<12}{'Status':<8}"
    print(header)
    print("-" * 88)
    for r in records:
        print(f"{r['id']:<6}{r['item_name'][:18]:<20}{r['category'][:12]:<14}{r['color'][:8]:<10}{r['location'][:16]:<18}{r['date']:<12}{r['status']:<8}")
    print("-" * 88)


def view_lost_items():
    """Display active lost items (excluding Recovered ones)."""
    records = read_records(LOST_FILE)
    # Recovered items are removed from the active list
    active_lost = [r for r in records if r.get("status") != "Recovered"]
    display_table(active_lost, "Active Lost Items List", is_lost=True)


def view_found_items():
    """Display active found items (excluding Recovered ones)."""
    records = read_records(FOUND_FILE)
    # Recovered items are removed from the active list
    active_found = [r for r in records if r.get("status") != "Recovered"]
    display_table(active_found, "Active Found Items List", is_lost=False)


def view_recovered_archive():
    """Display all recovered items history from both lost and found records."""
    print("\n" + "="*95)
    print("                      RECOVERED & RETURNED ITEMS ARCHIVE")
    print("="*95)
    lost_records = read_records(LOST_FILE)
    found_records = read_records(FOUND_FILE)

    recovered_lost = [r for r in lost_records if r.get("status") == "Recovered"]
    recovered_found = [r for r in found_records if r.get("status") == "Recovered"]

    if not recovered_lost and not recovered_found:
        print(" No recovered items in the archive yet.")
        print("-" * 95)
        return

    print(f"\n--- RECOVERED LOST ITEMS ({len(recovered_lost)}) ---")
    if recovered_lost:
        header = f"{'ID':<6}{'Item Name':<20}{'Category':<14}{'Color':<10}{'Lost Location':<18}{'Owner/Reporter':<16}"
        print(header)
        print("-" * 95)
        for r in recovered_lost:
            print(f"{r['id']:<6}{r['item_name'][:18]:<20}{r['category'][:12]:<14}{r['color'][:8]:<10}{r['location'][:16]:<18}{r['reporter'][:14]:<16}")
        print("-" * 95)
    else:
        print(" No items.")

    print(f"\n--- RECOVERED / RETURNED FOUND ITEMS ({len(recovered_found)}) ---")
    if recovered_found:
        header = f"{'ID':<6}{'Item Name':<20}{'Category':<14}{'Color':<10}{'Found Location':<18}{'Found By':<16}"
        print(header)
        print("-" * 95)
        for r in recovered_found:
            print(f"{r['id']:<6}{r['item_name'][:18]:<20}{r['category'][:12]:<14}{r['color'][:8]:<10}{r['location'][:16]:<18}{r['finder'][:14]:<16}")
        print("-" * 95)
    else:
        print(" No items.")


def search_items():
    """Search records across lost and found databases."""
    print("\n" + "="*50)
    print("                SEARCH DATABASE")
    print("="*50)
    keyword = input("Enter keyword to search (name, color, location, desc): ").strip().lower()
    if not keyword:
        print("[-] Search keyword cannot be empty.")
        return

    lost_records = read_records(LOST_FILE)
    found_records = read_records(FOUND_FILE)

    matched_lost = [r for r in lost_records if keyword in (r['item_name'] + r['color'] + r['location'] + r['description'] + r['category']).lower()]
    matched_found = [r for r in found_records if keyword in (r['item_name'] + r['color'] + r['location'] + r['description'] + r['category']).lower()]

    print(f"\n>>> Search Results for '{keyword}':")
    display_table(matched_lost, f"Lost Items Matching '{keyword}'", is_lost=True)
    display_table(matched_found, f"Found Items Matching '{keyword}'", is_lost=False)


def find_possible_matches():
    """
    Core Matcher Engine:
    Compares all active 'Lost' items against active 'Found' items,
    computes heuristic match scores, and ranks potential pairs.
    Allows directly marking verified matches as Recovered on the spot.
    """
    print("\n" + "="*88)
    print("                 SMART LOST & FOUND MATCHER ENGINE")
    print("="*88)

    lost_records = [r for r in read_records(LOST_FILE) if r.get("status") == "Lost" or r.get("status") == "Matched"]
    found_records = [r for r in read_records(FOUND_FILE) if r.get("status") == "Found" or r.get("status") == "Matched"]

    if not lost_records:
        print("[!] No active 'Lost' items to match.")
        return
    if not found_records:
        print("[!] No active 'Found' items to match against.")
        return

    matches = []

    for lost in lost_records:
        for found in found_records:
            score, reasons = calculate_match_score(lost, found)
            if score >= 35:  # Match threshold
                matches.append({
                    "score": score,
                    "lost": lost,
                    "found": found,
                    "reasons": reasons
                })

    # Sort matches by highest score first
    matches.sort(key=lambda x: x["score"], reverse=True)

    if not matches:
        print(" No strong matches found between active Lost and Found items yet.")
        print(" Tip: Check back after new found items are registered.")
        print("-" * 88)
        return

    print(f" Found {len(matches)} potential match pair(s) above threshold:\n")

    for idx, m in enumerate(matches, 1):
        score = m["score"]
        lost = m["lost"]
        found = m["found"]

        # Visual confidence bar
        bar_len = int(score / 5)
        bar = "#" * bar_len + "-" * (20 - bar_len)

        print(f" MATCH #{idx} | Confidence: {score}% [{bar}]")
        print(f"  LOST  ITEM [ID #{lost['id']}]: {lost['item_name']} ({lost['color']}, {lost['category']})")
        print(f"        Lost At: {lost['location']} on {lost['date']} | Reported By: {lost['reporter']} (Ph: {lost['contact']})")
        print(f"  FOUND ITEM [ID #{found['id']}]: {found['item_name']} ({found['color']}, {found['category']})")
        print(f"        Found At: {found['location']} on {found['date']} | Found By: {found['finder']} (Ph: {found['contact']})")
        print(f"  Match Factors: {'; '.join(m['reasons'])}")
        print("-" * 88)

    # Fast action: mark match as recovered
    prompt_rec = input("\nWould you like to mark any matched pair as RECOVERED now? (y/n): ").strip().lower()
    if prompt_rec == 'y':
        mark_recovered_pair()


def mark_recovered_pair():
    """Mark both a Lost Item and a Found Item as Recovered, removing both from active lists."""
    print("\n" + "="*50)
    print("      MARK MATCHED PAIR AS RECOVERED")
    print("="*50)
    lost_id = input("Enter Lost Item ID  (e.g. 101): ").strip()
    found_id = input("Enter Found Item ID (e.g. 201): ").strip()

    lost_records = read_records(LOST_FILE)
    found_records = read_records(FOUND_FILE)

    lost_item = next((r for r in lost_records if r["id"] == lost_id), None)
    found_item = next((r for r in found_records if r["id"] == found_id), None)

    if not lost_item:
        print(f"[-] Lost Item ID #{lost_id} not found.")
        return
    if not found_item:
        print(f"[-] Found Item ID #{found_id} not found.")
        return

    print(f"\nLost Record : #{lost_item['id']} - {lost_item['item_name']} (Owner: {lost_item['reporter']})")
    print(f"Found Record: #{found_item['id']} - {found_item['item_name']} (Finder: {found_item['finder']})")
    
    confirm = input("\nConfirm marking this item as RECOVERED & returned to owner? (y/n): ").strip().lower()
    if confirm == 'y':
        lost_item["status"] = "Recovered"
        found_item["status"] = "Recovered"
        write_records(LOST_FILE, LOST_FIELDS, lost_records)
        write_records(FOUND_FILE, FOUND_FIELDS, found_records)
        print(f"\n[+] SUCCESS! Lost #{lost_id} & Found #{found_id} marked as RECOVERED.")
        print("[+] Both items have been safely removed from active Lost and Found lists.")
    else:
        print("[*] Operation cancelled.")


def mark_recovered():
    """Menu interface to mark items as Recovered / Returned."""
    print("\n" + "="*50)
    print("          MARK ITEM AS RECOVERED / RETURNED")
    print("="*50)
    print(" [1] Mark Matched Pair as Recovered (Removes both from active lists)")
    print(" [2] Mark Single Lost Item as Recovered (Removes from active Lost list)")
    print(" [3] Mark Single Found Item as Recovered (Removes from active Found list)")
    print(" [4] Reopen / Restore a Recovered Item")
    print(" [5] Return to Main Menu")
    print("="*50)

    choice = input("Select option (1-5): ").strip()

    if choice == "1":
        mark_recovered_pair()

    elif choice == "2":
        lost_records = read_records(LOST_FILE)
        item_id = input("Enter Lost Item ID to mark as Recovered: ").strip()
        target = next((r for r in lost_records if r["id"] == item_id), None)
        if not target:
            print(f"[-] Lost Item #{item_id} not found.")
            return
        target["status"] = "Recovered"
        write_records(LOST_FILE, LOST_FIELDS, lost_records)
        print(f"[+] SUCCESS! Lost Item #{item_id} ({target['item_name']}) marked as RECOVERED and removed from active Lost list.")

    elif choice == "3":
        found_records = read_records(FOUND_FILE)
        item_id = input("Enter Found Item ID to mark as Recovered: ").strip()
        target = next((r for r in found_records if r["id"] == item_id), None)
        if not target:
            print(f"[-] Found Item #{item_id} not found.")
            return
        target["status"] = "Recovered"
        write_records(FOUND_FILE, FOUND_FIELDS, found_records)
        print(f"[+] SUCCESS! Found Item #{item_id} ({target['item_name']}) marked as RECOVERED and removed from active Found list.")

    elif choice == "4":
        print("[1] Restore Lost Item  [2] Restore Found Item")
        sub_ch = input("Select (1 or 2): ").strip()
        if sub_ch == "1":
            filename, fields, default_st = LOST_FILE, LOST_FIELDS, "Lost"
        elif sub_ch == "2":
            filename, fields, default_st = FOUND_FILE, FOUND_FIELDS, "Found"
        else:
            print("[-] Invalid choice.")
            return

        records = read_records(filename)
        item_id = input("Enter Item ID to restore: ").strip()
        target = next((r for r in records if r["id"] == item_id), None)
        if target:
            target["status"] = default_st
            write_records(filename, fields, records)
            print(f"[+] Item #{item_id} restored to status '{default_st}' and added back to active list.")
        else:
            print(f"[-] Item #{item_id} not found.")

    elif choice == "5":
        return
    else:
        print("[-] Invalid selection.")


def delete_record():
    """Delete a record from Lost or Found file."""
    print("\n" + "="*50)
    print("                 DELETE RECORD")
    print("="*50)
    print("[1] Delete from Lost Items")
    print("[2] Delete from Found Items")
    choice = input("Select option (1 or 2): ").strip()

    if choice == "1":
        filename = LOST_FILE
        fields = LOST_FIELDS
        item_type = "Lost"
    elif choice == "2":
        filename = FOUND_FILE
        fields = FOUND_FIELDS
        item_type = "Found"
    else:
        print("[-] Invalid choice.")
        return

    records = read_records(filename)
    item_id = input(f"Enter {item_type} Item ID to delete: ").strip()

    updated_records = [r for r in records if r["id"] != item_id]
    if len(updated_records) == len(records):
        print(f"[-] ID #{item_id} not found.")
    else:
        confirm = input(f"Are you sure you want to permanently delete #{item_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            write_records(filename, fields, updated_records)
            print(f"[+] Record #{item_id} deleted successfully.")
        else:
            print("[*] Deletion cancelled.")


def display_stats():
    """Display analytics and summary counts."""
    lost = read_records(LOST_FILE)
    found = read_records(FOUND_FILE)

    active_lost = sum(1 for r in lost if r.get("status") == "Lost" or r.get("status") == "Matched")
    recovered_lost = sum(1 for r in lost if r.get("status") == "Recovered" or r.get("status") == "Claimed")
    active_found = sum(1 for r in found if r.get("status") == "Found" or r.get("status") == "Matched")
    recovered_found = sum(1 for r in found if r.get("status") == "Recovered" or r.get("status") == "Claimed")

    print("\n" + "="*50)
    print("           LOST & FOUND PORTAL METRICS")
    print("="*50)
    print(f" Total Lost Items Reported  : {len(lost)}")
    print(f"   - Active in Lost List    : {active_lost}")
    print(f"   - Recovered & Handed Over: {recovered_lost}")
    print("-" * 50)
    print(f" Total Found Items Logged   : {len(found)}")
    print(f"   - Active in Found List   : {active_found}")
    print(f"   - Recovered & Handed Over: {recovered_found}")
    print("-" * 50)
    print(f" Total Successful Recoveries: {recovered_lost + recovered_found}")
    print("="*50)


# ------------------------------------------------------------------------------
# MAIN MENU LOOP
# ------------------------------------------------------------------------------

def main():
    """Main program loop and menu driver."""
    initialize_files()
    while True:
        print("\n" + "="*58)
        print("        SCHOOL LOST & FOUND MATCHER SYSTEM")
        print("      CBSE Class 12 Computer Science Project")
        print("="*58)
        print(" [1]  Report a Lost Item")
        print(" [2]  Report a Found Item")
        print(" [3]  View Active Lost Items")
        print(" [4]  View Active Found Items")
        print(" [5]  Search Database (Keyword / Location / Color)")
        print(" [6]  Run Smart Matcher Engine (Auto-Match)")
        print(" [7]  Mark Item as RECOVERED (Remove from Active Lists)")
        print(" [8]  View Recovered Items Archive / History")
        print(" [9]  Delete a Record")
        print(" [10] View System Analytics & Statistics")
        print(" [11] Exit")
        print("="*58)

        choice = input("Enter your choice (1-11): ").strip()

        if choice == "1":
            report_lost_item()
        elif choice == "2":
            report_found_item()
        elif choice == "3":
            view_lost_items()
        elif choice == "4":
            view_found_items()
        elif choice == "5":
            search_items()
        elif choice == "6":
            find_possible_matches()
        elif choice == "7":
            mark_recovered()
        elif choice == "8":
            view_recovered_archive()
        elif choice == "9":
            delete_record()
        elif choice == "10":
            display_stats()
        elif choice == "11":
            print("\nThank you for using School Lost & Found Matcher. Goodbye!")
            break
        else:
            print("\n[-] Invalid option! Please choose a number between 1 and 11.")


if __name__ == "__main__":
    main()
