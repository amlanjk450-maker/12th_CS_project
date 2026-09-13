# CBSE Class 12 Computer Science - Final Projects Suite

This repository contains **3 complete, self-contained single-file projects** designed strictly according to the **CBSE Class 12 Computer Science curriculum**.

All projects use **standard Python 3 library only** (utilizing the `csv` module for persistent file handling, user-defined functions, data structures, and exception handling). **No external database server or external Python packages are required to run.**

---

## 📁 Project Overview

| Project File | Title | Description | Core Class 12 Concepts |
|---|---|---|---|
| [`01_lost_and_found_matcher.py`](file:///c:/all%20projects/cs%20final%20project/01_lost_and_found_matcher.py) | **Lost & Found Matcher** | A system for registering lost and found campus articles, computing rule-based similarity matching scores, and managing item recovery. | CSV File Handling, String manipulation, Heuristic Match Algorithm, Lists of Dictionaries. |
| [`02_school_canteen_ordering_system.py`](file:///c:/all%20projects/cs%20final%20project/02_school_canteen_ordering_system.py) | **School Canteen Ordering System** | Interactive menu catalog, multi-item shopping cart, order placement, and tax invoice receipt generation. | Nested Dictionaries/Lists, CSV I/O, Arithmetic & Financial Formatting, Order State Machine. |
| [`03_student_marketplace.py`](file:///c:/all%20projects/cs%20final%20project/03_student_marketplace.py) | **Student-to-Student Marketplace** | Peer-to-peer campus exchange for textbooks, calculators, blazers, and sports gear with multi-criteria filtering and sorting. | Data Sorting (Lambda / Custom keys), Budget Range Filtering, CSV CRUD Operations. |
| [`main.py`](file:///c:/all%20projects/cs%20final%20project/main.py) | **Master Launcher** | Quick menu interface to launch any of the 3 projects with one command. | Subprocess management, System calls. |

---

## 🚀 How to Run

You can run any project independently using standard Python 3:

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

*Note: On the first run, each project automatically creates its respective `.csv` file populated with sample records so you can immediately test and demonstrate all features.*

---

## 🔍 Detailed Feature Walkthrough

### 1. Project 1: Lost & Found Matcher
- **Features**:
  - Report Lost Item (Name, Category, Color, Location, Date, Contact, Description)
  - Report Found Item (Finder details, drop-off location, condition)
  - View Active Lost Items & Active Found Items (Recovered items are automatically filtered out)
  - Search by keyword, color, or location
  - **Smart Matcher Engine**: Computes compatibility score (0–100%) between all active Lost vs Found records using:
    - Name keywords similarity (+35%)
    - Category match (+20%)
    - Color match (+20%)
    - Location overlap (+15%)
    - Description keyword overlap (+10%)
  - **Mark Item as RECOVERED**: Allows marking a matched pair or individual items as `Recovered`, which automatically removes them from both active Lost and Found lists.
  - **Recovered Items Archive**: Dedicated view to audit and verify historical successful item handovers.
  - Statistical summary and analytics

### 2. Project 2: School Canteen Ordering System
- **Features**:
  - Menu categorized into Snacks, Meals, Beverages, Desserts
  - Interactive multi-item cart with live subtotal calculation
  - Out-of-stock validation
  - Automatic order number generation and timestamping
  - Formatted receipt bill invoice printing
  - Order tracking (`Placed` $\rightarrow$ `Preparing` $\rightarrow$ `Ready` $\rightarrow$ `Collected`)
  - Menu management (Add item, update price, toggle availability, delete item)
  - Daily revenue, average order value, and order count reports

### 3. Project 3: Student Marketplace
- **Features**:
  - Browse available listings with seller contact info
  - Add listings under categories (Books, Calculators, Uniform, Stationery, Sports, Electronics)
  - Multi-criteria search: Keyword search, category filtering, maximum budget filtering
  - Detailed single-listing inspection
  - Sort listings by Price (Low $\rightarrow$ High or High $\rightarrow$ Low) or by Recency
  - Mark items as `Sold` or toggle back to `Available`
  - Analytics: Lowest price item, highest price item, average listing price, category distribution

---

## 🎓 Class 12 Computer Science Viva Preparation

### Common Viva Questions & Answers:

1. **Q: How is data stored persistently in this project?**
   - **A:** Data is stored using standard CSV (Comma-Separated Values) files using Python's built-in `csv` module (`csv.DictReader` and `csv.DictWriter`). This ensures that all records persist even after the program terminates.

2. **Q: Why use `DictReader` and `DictWriter` instead of basic `reader` and `writer`?**
   - **A:** `DictReader` maps each row directly to a Python dictionary using the header column names as keys, making code readable, robust against column order changes, and easy to maintain.

3. **Q: How does the matching algorithm work in Project 1?**
   - **A:** It normalizes text (converts to lowercase, removes special characters and stop words), and applies weighted scoring across key attributes (Name, Category, Color, Location, Description) to compute a confidence percentage from 0% to 100%.

4. **Q: What happens when an item is marked "Recovered"?**
   - **A:** The item's status is updated to `"Recovered"` in the persistent CSV files. Active listing functions automatically filter out items with `"Recovered"` status, removing them from active view while preserving them in the historical recovery archive.

5. **Q: How is input validation handled?**
   - **A:** Using `try-except` blocks for numeric type casting (`float()`, `int()`), checking for non-empty string inputs, and verifying options against valid choices.
