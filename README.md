# CBSE Class 12 Computer Science - Final Project: Student Marketplace

A modular, syllabus-friendly project designed strictly according to the **CBSE Class 12 Computer Science curriculum** using **Python 3 with `mysql.connector`**.

---

## 📁 Project Architecture

- **`function.py`**: [`function.py`](file:///c:/all%20projects/cs%20final%20project/function.py) — Contains all database connection logic, table initialization, CRUD operations, searching, filtering, and reporting functions.
- **`main.py`**: [`main.py`](file:///c:/all%20projects/cs%20final%20project/main.py) — Clean main menu interface that imports and invokes the functions from `function.py`.
- **Database Used**: `student_market_db` (Table: `listings`)

---

## 🛠️ Prerequisites

1. **Install MySQL Connector**:
   ```bash
   pip install mysql-connector-python
   ```

2. **Ensure MySQL Server is Running**:
   - Start MySQL using **XAMPP**, **WAMP**, or standard **MySQL Server**.
   - Default credentials used: `host="localhost"`, `user="root"`, `password="root"`.

---

## 🚀 How to Run

```bash
# Run the main program
python main.py
```

*Note: On first run, the program automatically connects to MySQL, creates the database `student_market_db`, creates the `listings` table, and seeds demo records.*

---

## 🔍 Module Breakdown

### `function.py`
- `get_db_connection()`: Connects to MySQL with automatic error recovery and password prompts.
- `initialize_database()`: Creates database, table, and seeds demo listings if empty.
- `browse_all_listings()`: Displays all available active items in an ASCII table.
- `add_listing()`: Inserts a new student listing with validation.
- `search_and_filter()`: Implements keyword search (`LIKE`), category filtering, and max-price budget constraints.
- `view_listing_details()`: Displays single item card with seller contact information.
- `sort_listings()`: Dynamic SQL sorting (`ORDER BY price ASC`, `ORDER BY price DESC`, `ORDER BY listed_date DESC`).
- `mark_item_sold()`: Updates listing status to `Sold`.
- `delete_listing()`: Removes listing from MySQL.
- `marketplace_insights()`: Computes lowest, highest, average prices, and category statistics via SQL aggregates.

### `main.py`
- Clean, menu-driven CLI interface that imports and calls the required functions based on user choices (1–9).

---

## 🎓 Class 12 CS Viva Voce Q&A

1. **Q: Why separate the code into `main.py` and `function.py`?**
   - **A:** This follows the **modular programming approach** taught in Class 12 CBSE CS. It improves code readability, makes maintenance easier, avoids code repetition, and keeps the user interface separate from business/database logic.

2. **Q: How does `main.py` access functions from `function.py`?**
   - **A:** Using Python's `from function import ...` statement.

3. **Q: What is the benefit of parameterized SQL queries (`%s`)?**
   - **A:** They protect against SQL Injection vulnerabilities and properly escape special characters and quotes.
