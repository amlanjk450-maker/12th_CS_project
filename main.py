"""
================================================================================
CBSE CLASS 12 COMPUTER SCIENCE FINAL PROJECT: STUDENT MARKETPLACE
================================================================================
Main menu driver and user interface.
Imports all operations and database logic from 'function.py'.
================================================================================
"""

import sys
from function import (
    initialize_database,
    browse_all_listings,
    add_listing,
    search_and_filter,
    view_listing_details,
    sort_listings,
    mark_item_sold,
    delete_listing,
    marketplace_insights
)

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
