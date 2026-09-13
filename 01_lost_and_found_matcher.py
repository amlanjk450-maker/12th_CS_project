"""
================================================================================
PROJECT 1: LOST & FOUND MATCHER (PYTHON + MYSQL)
CBSE CLASS 12 COMPUTER SCIENCE FINAL PROJECT
================================================================================
Syllabus Topics Covered:
- Python-MySQL Connectivity (mysql.connector, connect, cursor, execute, commit)
- SQL Queries (CREATE, INSERT, SELECT, UPDATE, DELETE, LIKE, WHERE, COUNT)
- Python Functions (User-defined functions, parameters, return values)
- Data Structures (Dictionaries, Lists, Tuples, Sets)
- Text Normalization and Heuristic Matching Algorithm (Rule-based scoring)
- Error Handling (try-except-finally blocks) & Input Validation
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
    "password": "",  # Default XAMPP / MySQL root password. Change if you set a password.
    "database": "lost_found_db"
}

# ------------------------------------------------------------------------------
# DATABASE CONNECTION & AUTO-INITIALIZATION
# ------------------------------------------------------------------------------

def get_db_connection(use_database=True):
    """
    Establish connection to MySQL server.
    If default connection fails due to password, prompts user to enter MySQL password.
    """
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
            if err.errno == 1045:  # Access denied (wrong password)
                print(f"\n[!] MySQL Access Denied for user '{DB_CONFIG['user']}'.")
                new_pwd = input("Enter your MySQL root password: ")
                DB_CONFIG["password"] = new_pwd
            elif err.errno == 1049:  # Unknown database
                # Initialize database first
                initialize_database()
                use_database = True
            elif err.errno == 2003:  # Can't connect to MySQL server
                print("\n[!] ERROR: Cannot connect to MySQL server at localhost:3306.")
                print("    Please ensure your MySQL service (e.g. MySQL Server / XAMPP / WAMP) is running.")
                sys.exit(1)
            else:
                print(f"\n[!] Database Connection Error: {err}")
                sys.exit(1)


def initialize_database():
    """
    Connects to MySQL server, creates database 'lost_found_db' and tables
    with sample records if they do not exist.
    """
    try:
        conn = get_db_connection(use_database=False)
        cursor = conn.cursor()

        # Create Database
        cursor.execute("CREATE DATABASE IF NOT EXISTS lost_found_db")
        cursor.execute("USE lost_found_db")

        # Table 1: lost_items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lost_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_name VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                color VARCHAR(50) NOT NULL,
                location VARCHAR(100) NOT NULL,
                lost_date DATE NOT NULL,
                reporter VARCHAR(100) NOT NULL,
                contact VARCHAR(50) NOT NULL,
                description TEXT,
                status VARCHAR(30) DEFAULT 'Lost'
            )
        """)

        # Table 2: found_items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS found_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_name VARCHAR(100) NOT NULL,
                category VARCHAR(50) NOT NULL,
                color VARCHAR(50) NOT NULL,
                location VARCHAR(100) NOT NULL,
                found_date DATE NOT NULL,
                finder VARCHAR(100) NOT NULL,
                contact VARCHAR(50) NOT NULL,
                description TEXT,
                status VARCHAR(30) DEFAULT 'Found'
            )
        """)

        conn.commit()

        # Seed sample data if empty
        cursor.execute("SELECT COUNT(*) FROM lost_items")
        if cursor.fetchone()[0] == 0:
            sample_lost = [
                ("Titan Black Watch", "Accessories", "Black", "Physics Lab", "2026-09-01", "Aman Sharma", "9876543210", "Analog watch with silver dial and black leather strap", "Lost"),
                ("Classmate Notebook", "Stationery", "Blue", "Library 2nd Floor", "2026-09-03", "Pooja Verma", "9811223344", "Thick ruled notebook with Chemistry notes and name label", "Lost"),
                ("Wildcraft Water Bottle", "Bags/Bottles", "Blue", "Playground", "2026-09-05", "Rohan Gupta", "9899001122", "Steel insulated bottle with a small dent on the cap", "Lost"),
                ("Casio Scientific Calculator", "Electronics", "Grey", "Room 104", "2026-09-08", "Sneha Roy", "9765432109", "Model fx-991EX with small sticker of Mickey Mouse on back", "Lost")
            ]
            cursor.executemany("""
                INSERT INTO lost_items (item_name, category, color, location, lost_date, reporter, contact, description, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, sample_lost)
            conn.commit()

        cursor.execute("SELECT COUNT(*) FROM found_items")
        if cursor.fetchone()[0] == 0:
            sample_found = [
                ("Black Wrist Watch", "Accessories", "Black", "Physics Lab", "2026-09-02", "Lab Assistant Ravi", "9800112233", "Titan watch found near experiment table #4 with black strap", "Found"),
                ("Blue Steel Bottle", "Bags/Bottles", "Blue", "Sports Ground", "2026-09-06", "Coach Kapoor", "9877001122", "Wildcraft metallic blue bottle picked up from football bench", "Found"),
                ("Red Geometry Box", "Stationery", "Red", "Math Lab", "2026-09-07", "Karan Singh", "9812345678", "Camlin geometry box with complete compass set", "Found"),
                ("Scientific Calculator Casio", "Electronics", "Grey", "Room 104", "2026-09-09", "Neha Sen", "9833445566", "Casio calculator left on back bench", "Found")
            ]
            cursor.executemany("""
                INSERT INTO found_items (item_name, category, color, location, found_date, finder, contact, description, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, sample_found)
            conn.commit()

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[!] Database Initialization Error: {err}")


# ------------------------------------------------------------------------------
# TEXT PROCESSING & SMART MATCHING ALGORITHM
# ------------------------------------------------------------------------------

def normalize_text(text):
    """Clean text by converting to lowercase and removing punctuation."""
    if not text:
        return ""
    clean = ""
    for char in str(text).lower():
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
    """Collect details from user and save new lost item record in MySQL."""
    print("\n" + "="*50)
    print("           REPORT A LOST ITEM")
    print("="*50)

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

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO lost_items (item_name, category, color, location, lost_date, reporter, contact, description, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Lost')
        """
        cursor.execute(sql, (item_name, category, color, location, date_val, reporter, contact, description))
        conn.commit()
        item_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"\n[+] SUCCESS! Lost item reported in MySQL database with ID #{item_id}.")
    except Error as err:
        print(f"[-] Database Error: {err}")


def report_found_item():
    """Collect details from user and save new found item record in MySQL."""
    print("\n" + "="*50)
    print("           REPORT A FOUND ITEM")
    print("="*50)

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

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO found_items (item_name, category, color, location, found_date, finder, contact, description, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Found')
        """
        cursor.execute(sql, (item_name, category, color, location, date_val, finder, contact, description))
        conn.commit()
        item_id = cursor.lastrowid
        cursor.close()
        conn.close()
        print(f"\n[+] SUCCESS! Found item logged in MySQL database with ID #{item_id}.")
    except Error as err:
        print(f"[-] Database Error: {err}")


def display_table(records, title):
    """Print tabular formatted records from MySQL."""
    print("\n" + "="*90)
    print(f"                       {title.upper()} ({len(records)} Records)")
    print("="*90)
    if not records:
        print(" No records found.")
        print("-" * 90)
        return

    header = f"{'ID':<6}{'Item Name':<20}{'Category':<14}{'Color':<10}{'Location':<18}{'Date':<12}{'Status':<10}"
    print(header)
    print("-" * 90)
    for r in records:
        id_val = str(r[0])
        name = str(r[1])[:18]
        cat = str(r[2])[:12]
        color = str(r[3])[:8]
        loc = str(r[4])[:16]
        dt = str(r[5])
        st = str(r[9])[:10]
        print(f"{id_val:<6}{name:<20}{cat:<14}{color:<10}{loc:<18}{dt:<12}{st:<10}")
    print("-" * 90)


def view_lost_items():
    """Display active lost items (excluding Recovered items)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lost_items WHERE status != 'Recovered'")
        records = cursor.fetchall()
        display_table(records, "Active Lost Items List")
        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def view_found_items():
    """Display active found items (excluding Recovered items)."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM found_items WHERE status != 'Recovered'")
        records = cursor.fetchall()
        display_table(records, "Active Found Items List")
        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def view_recovered_archive():
    """Display all recovered items history from both lost and found tables."""
    print("\n" + "="*95)
    print("                      RECOVERED & RETURNED ITEMS ARCHIVE")
    print("="*95)
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM lost_items WHERE status = 'Recovered'")
        recovered_lost = cursor.fetchall()

        cursor.execute("SELECT * FROM found_items WHERE status = 'Recovered'")
        recovered_found = cursor.fetchall()

        if not recovered_lost and not recovered_found:
            print(" No recovered items in the archive yet.")
            print("-" * 95)
            cursor.close()
            conn.close()
            return

        print(f"\n--- RECOVERED LOST ITEMS ({len(recovered_lost)}) ---")
        if recovered_lost:
            header = f"{'ID':<6}{'Item Name':<20}{'Category':<14}{'Color':<10}{'Lost Location':<18}{'Owner/Reporter':<16}"
            print(header)
            print("-" * 95)
            for r in recovered_lost:
                print(f"{r[0]:<6}{str(r[1])[:18]:<20}{str(r[2])[:12]:<14}{str(r[3])[:8]:<10}{str(r[4])[:16]:<18}{str(r[6])[:14]:<16}")
            print("-" * 95)
        else:
            print(" No items.")

        print(f"\n--- RECOVERED / RETURNED FOUND ITEMS ({len(recovered_found)}) ---")
        if recovered_found:
            header = f"{'ID':<6}{'Item Name':<20}{'Category':<14}{'Color':<10}{'Found Location':<18}{'Found By':<16}"
            print(header)
            print("-" * 95)
            for r in recovered_found:
                print(f"{r[0]:<6}{str(r[1])[:18]:<20}{str(r[2])[:12]:<14}{str(r[3])[:8]:<10}{str(r[4])[:16]:<18}{str(r[6])[:14]:<16}")
            print("-" * 95)
        else:
            print(" No items.")

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def search_items():
    """Search records across lost and found MySQL tables using LIKE query."""
    print("\n" + "="*50)
    print("                SEARCH DATABASE")
    print("="*50)
    keyword = input("Enter keyword to search (name, color, location, desc): ").strip()
    if not keyword:
        print("[-] Search keyword cannot be empty.")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        search_param = f"%{keyword}%"

        query_lost = """
            SELECT * FROM lost_items
            WHERE item_name LIKE %s OR category LIKE %s OR color LIKE %s OR location LIKE %s OR description LIKE %s
        """
        cursor.execute(query_lost, (search_param, search_param, search_param, search_param, search_param))
        lost_results = cursor.fetchall()

        query_found = """
            SELECT * FROM found_items
            WHERE item_name LIKE %s OR category LIKE %s OR color LIKE %s OR location LIKE %s OR description LIKE %s
        """
        cursor.execute(query_found, (search_param, search_param, search_param, search_param, search_param))
        found_results = cursor.fetchall()

        print(f"\n>>> Search Results for '{keyword}':")
        display_table(lost_results, f"Lost Items Matching '{keyword}'")
        display_table(found_results, f"Found Items Matching '{keyword}'")

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def row_to_dict(row, is_lost=True):
    """Convert MySQL row tuple to dictionary."""
    if is_lost:
        return {
            "id": str(row[0]),
            "item_name": row[1],
            "category": row[2],
            "color": row[3],
            "location": row[4],
            "date": str(row[5]),
            "reporter": row[6],
            "contact": row[7],
            "description": row[8],
            "status": row[9]
        }
    else:
        return {
            "id": str(row[0]),
            "item_name": row[1],
            "category": row[2],
            "color": row[3],
            "location": row[4],
            "date": str(row[5]),
            "finder": row[6],
            "contact": row[7],
            "description": row[8],
            "status": row[9]
        }


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

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM lost_items WHERE status = 'Lost' OR status = 'Matched'")
        lost_rows = cursor.fetchall()

        cursor.execute("SELECT * FROM found_items WHERE status = 'Found' OR status = 'Matched'")
        found_rows = cursor.fetchall()

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")
        return

    if not lost_rows:
        print("[!] No active 'Lost' items to match.")
        return
    if not found_rows:
        print("[!] No active 'Found' items to match against.")
        return

    lost_records = [row_to_dict(r, is_lost=True) for r in lost_rows]
    found_records = [row_to_dict(r, is_lost=False) for r in found_rows]

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

        bar_len = int(score / 5)
        bar = "#" * bar_len + "-" * (20 - bar_len)

        print(f" MATCH #{idx} | Confidence: {score}% [{bar}]")
        print(f"  LOST  ITEM [ID #{lost['id']}]: {lost['item_name']} ({lost['color']}, {lost['category']})")
        print(f"        Lost At: {lost['location']} on {lost['date']} | Reported By: {lost['reporter']} (Ph: {lost['contact']})")
        print(f"  FOUND ITEM [ID #{found['id']}]: {found['item_name']} ({found['color']}, {found['category']})")
        print(f"        Found At: {found['location']} on {found['date']} | Found By: {found['finder']} (Ph: {found['contact']})")
        print(f"  Match Factors: {'; '.join(m['reasons'])}")
        print("-" * 88)

    prompt_rec = input("\nWould you like to mark any matched pair as RECOVERED now? (y/n): ").strip().lower()
    if prompt_rec == 'y':
        mark_recovered_pair()


def mark_recovered_pair():
    """Mark both a Lost Item and a Found Item as Recovered in MySQL, removing both from active lists."""
    print("\n" + "="*50)
    print("      MARK MATCHED PAIR AS RECOVERED")
    print("="*50)
    lost_id = input("Enter Lost Item ID  (e.g. 1): ").strip()
    found_id = input("Enter Found Item ID (e.g. 1): ").strip()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM lost_items WHERE id = %s", (lost_id,))
        lost_row = cursor.fetchone()

        cursor.execute("SELECT * FROM found_items WHERE id = %s", (found_id,))
        found_row = cursor.fetchone()

        if not lost_row:
            print(f"[-] Lost Item ID #{lost_id} not found.")
            cursor.close()
            conn.close()
            return
        if not found_row:
            print(f"[-] Found Item ID #{found_id} not found.")
            cursor.close()
            conn.close()
            return

        print(f"\nLost Record : #{lost_row[0]} - {lost_row[1]} (Owner: {lost_row[6]})")
        print(f"Found Record: #{found_row[0]} - {found_row[1]} (Finder: {found_row[6]})")

        confirm = input("\nConfirm marking this item as RECOVERED & returned to owner? (y/n): ").strip().lower()
        if confirm == 'y':
            cursor.execute("UPDATE lost_items SET status = 'Recovered' WHERE id = %s", (lost_id,))
            cursor.execute("UPDATE found_items SET status = 'Recovered' WHERE id = %s", (found_id,))
            conn.commit()
            print(f"\n[+] SUCCESS! Lost #{lost_id} & Found #{found_id} updated to 'Recovered' in MySQL.")
            print("[+] Both items have been removed from active Lost and Found lists.")
        else:
            print("[*] Operation cancelled.")

        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def mark_recovered():
    """Menu interface to mark items as Recovered / Returned in MySQL."""
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
        item_id = input("Enter Lost Item ID to mark as Recovered: ").strip()
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT item_name FROM lost_items WHERE id = %s", (item_id,))
            res = cursor.fetchone()
            if not res:
                print(f"[-] Lost Item #{item_id} not found.")
            else:
                cursor.execute("UPDATE lost_items SET status = 'Recovered' WHERE id = %s", (item_id,))
                conn.commit()
                print(f"[+] SUCCESS! Lost Item #{item_id} ({res[0]}) marked as RECOVERED and removed from active list.")
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[-] Database Error: {err}")

    elif choice == "3":
        item_id = input("Enter Found Item ID to mark as Recovered: ").strip()
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT item_name FROM found_items WHERE id = %s", (item_id,))
            res = cursor.fetchone()
            if not res:
                print(f"[-] Found Item #{item_id} not found.")
            else:
                cursor.execute("UPDATE found_items SET status = 'Recovered' WHERE id = %s", (item_id,))
                conn.commit()
                print(f"[+] SUCCESS! Found Item #{item_id} ({res[0]}) marked as RECOVERED and removed from active list.")
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[-] Database Error: {err}")

    elif choice == "4":
        print("[1] Restore Lost Item  [2] Restore Found Item")
        sub_ch = input("Select (1 or 2): ").strip()
        table = "lost_items" if sub_ch == "1" else ("found_items" if sub_ch == "2" else None)
        default_st = "Lost" if sub_ch == "1" else "Found"
        if not table:
            print("[-] Invalid choice.")
            return

        item_id = input("Enter Item ID to restore: ").strip()
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"UPDATE {table} SET status = %s WHERE id = %s", (default_st, item_id))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"[+] Item #{item_id} restored to status '{default_st}' and added back to active list.")
            else:
                print(f"[-] Item #{item_id} not found.")
            cursor.close()
            conn.close()
        except Error as err:
            print(f"[-] Database Error: {err}")

    elif choice == "5":
        return
    else:
        print("[-] Invalid selection.")


def delete_record():
    """Delete a record from Lost or Found table in MySQL."""
    print("\n" + "="*50)
    print("                 DELETE RECORD")
    print("="*50)
    print("[1] Delete from Lost Items")
    print("[2] Delete from Found Items")
    choice = input("Select option (1 or 2): ").strip()

    table = "lost_items" if choice == "1" else ("found_items" if choice == "2" else None)
    if not table:
        print("[-] Invalid choice.")
        return

    item_id = input("Enter Item ID to delete: ").strip()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table} WHERE id = %s", (item_id,))
        record = cursor.fetchone()
        if not record:
            print(f"[-] Item ID #{item_id} not found.")
        else:
            confirm = input(f"Are you sure you want to permanently delete #{item_id} ({record[1]})? (y/n): ").strip().lower()
            if confirm == 'y':
                cursor.execute(f"DELETE FROM {table} WHERE id = %s", (item_id,))
                conn.commit()
                print(f"[+] Record #{item_id} deleted successfully from MySQL.")
            else:
                print("[*] Deletion cancelled.")
        cursor.close()
        conn.close()
    except Error as err:
        print(f"[-] Database Error: {err}")


def display_stats():
    """Display analytics and summary counts using SQL COUNT queries."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM lost_items")
        total_lost = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM lost_items WHERE status != 'Recovered'")
        active_lost = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM lost_items WHERE status = 'Recovered'")
        recovered_lost = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM found_items")
        total_found = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM found_items WHERE status != 'Recovered'")
        active_found = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM found_items WHERE status = 'Recovered'")
        recovered_found = cursor.fetchone()[0]

        print("\n" + "="*50)
        print("           LOST & FOUND PORTAL METRICS (MYSQL)")
        print("="*50)
        print(f" Total Lost Items Reported  : {total_lost}")
        print(f"   - Active in Lost List    : {active_lost}")
        print(f"   - Recovered & Handed Over: {recovered_lost}")
        print("-" * 50)
        print(f" Total Found Items Logged   : {total_found}")
        print(f"   - Active in Found List   : {active_found}")
        print(f"   - Recovered & Handed Over: {recovered_found}")
        print("-" * 50)
        print(f" Total Successful Recoveries: {recovered_lost + recovered_found}")
        print("="*50)

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
        print("\n" + "="*58)
        print("     SCHOOL LOST & FOUND MATCHER SYSTEM (MYSQL)")
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
