# CBSE Class 12 Computer Science - Final Projects Suite (Python + MySQL Connector)

This repository contains **3 self-contained, single-file projects** designed strictly according to the **CBSE Class 12 Computer Science curriculum** using **Python 3 with `mysql.connector`**.

**No external `.sql` files or manual database setup required.** Each single Python file automatically handles database creation, table initialization, and queries directly through `mysql.connector`.

---

## 📁 Project Overview

| Project File | Title | Description | Core Class 12 Concepts |
|---|---|---|---|
| [`01_lost_and_found_matcher.py`](file:///c:/all%20projects/cs%20final%20project/01_lost_and_found_matcher.py) | **Lost & Found Matcher** | A system for registering lost and found campus articles, computing rule-based similarity matching scores, and managing item recovery. | `mysql.connector`, Parameterized SQL Queries, Heuristic Match Algorithm, Exception Handling. |
| [`02_school_canteen_ordering_system.py`](file:///c:/all%20projects/cs%20final%20project/02_school_canteen_ordering_system.py) | **School Canteen Ordering System** | Interactive menu catalog, multi-item shopping cart, order placement, and receipt bill invoice generation. | MySQL Transactions (`conn.commit()`), Auto-increment IDs, SQL Aggregate functions, Multi-item Carts. |
| [`03_student_marketplace.py`](file:///c:/all%20projects/cs%20final%20project/03_student_marketplace.py) | **Student-to-Student Marketplace** | Peer-to-peer campus exchange for textbooks, calculators, blazers, and sports gear with multi-criteria filtering and sorting. | SQL `LIKE`, `ORDER BY`, `GROUP BY`, Budget Range Filtering, Database CRUD operations. |
| [`main.py`](file:///c:/all%20projects/cs%20final%20project/main.py) | **Master Launcher** | Quick menu interface to launch any of the 3 projects with one command. | Subprocess management, System calls. |

---

## 🛠️ Prerequisites

1. **Install MySQL Connector**:
   ```bash
   pip install mysql-connector-python
   ```

2. **Ensure MySQL Server is Running**:
   - Start MySQL using **XAMPP**, **WAMP**, or standard **MySQL Server**.
   - Default credentials used: `host="localhost"`, `user="root"`, `password=""`. *(If your MySQL server has a password, the program will automatically prompt you once and connect).*

---

## 🚀 How to Run

Each file is 100% self-contained:

```bash
# Run Project 1 (Lost & Found Matcher)
python 01_lost_and_found_matcher.py

# Run Project 2 (School Canteen Ordering)
python 02_school_canteen_ordering_system.py

# Run Project 3 (Student Marketplace)
python 03_student_marketplace.py

# Or launch the unified menu
python main.py
```

---

## 🔍 Features & Python-MySQL Integration

### 1. Project 1: Lost & Found Matcher (`lost_found_db`)
- **Tables Created Automatically**: `lost_items`, `found_items`
- **Features**:
  - Insert lost and found reports using parameterized `cursor.execute()`.
  - Display active lost and found items.
  - Pattern search with SQL `LIKE`.
  - **Smart Matcher Engine**: Computes similarity confidence score (0–100%) between active lost and found items.
  - **Mark Item as RECOVERED**: Updates status to `Recovered` in MySQL for lost and found records simultaneously, automatically removing them from active view.
  - **Recovered Items Archive**: Dedicated view to audit and verify historical successful item handovers.

### 2. Project 2: School Canteen Ordering System (`canteen_db`)
- **Tables Created Automatically**: `menu`, `orders`
- **Features**:
  - Interactive multi-item cart with live subtotal calculation.
  - Out-of-stock validation.
  - Automatic order ID generation using MySQL `AUTO_INCREMENT`.
  - Formatted receipt bill invoice printing.
  - Order state tracking (`Placed` $\rightarrow$ `Preparing` $\rightarrow$ `Ready` $\rightarrow$ `Collected`).
  - Daily revenue analytics using SQL `SUM()`, `COUNT()`, `COALESCE()`.

### 3. Project 3: Student Marketplace (`student_market_db`)
- **Tables Created Automatically**: `listings`
- **Features**:
  - Browse available listings with seller contact info.
  - Multi-criteria search and price budget filtering (`WHERE price <= %s`).
  - Sorting via SQL: `ORDER BY price ASC`, `ORDER BY price DESC`, `ORDER BY listed_date DESC`.
  - Mark listings as `Sold` (`UPDATE listings SET status = 'Sold' WHERE id = %s`).
  - Analytics via SQL aggregates: `MIN(price)`, `MAX(price)`, `AVG(price)`, `GROUP BY category`.

---

## 🎓 Class 12 Computer Science Viva Preparation

### Common Viva Questions & Answers:

1. **Q: How does Python connect to MySQL?**
   - **A:** Using `mysql.connector`:
     ```python
     import mysql.connector
     conn = mysql.connector.connect(host="localhost", user="root", password="", database="lost_found_db")
     cursor = conn.cursor()
     ```

2. **Q: What is the purpose of `conn.commit()`?**
   - **A:** `commit()` saves and makes permanent the changes made by `INSERT`, `UPDATE`, or `DELETE` SQL queries to the database.

3. **Q: Why use parameterized queries with `%s` instead of string formatting?**
   - **A:** Parameterized queries prevent SQL Injection attacks, safely handle special characters/quotes in user inputs, and ensure data integrity.

4. **Q: What is the difference between `cursor.fetchone()` and `cursor.fetchall()`?**
   - **A:** `fetchone()` retrieves the next single record from the query result set as a tuple, whereas `fetchall()` retrieves all rows as a list of tuples.

5. **Q: How is the 'Recovered' feature implemented in MySQL?**
   - **A:** When an item is marked as recovered, an `UPDATE` query sets `status = 'Recovered'`. Active view functions query `WHERE status != 'Recovered'`, which excludes recovered items from the active list while preserving them in the historical archive.
