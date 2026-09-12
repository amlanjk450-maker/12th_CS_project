"""
================================================================================
CBSE CLASS 12 COMPUTER SCIENCE FINAL PROJECTS LAUNCHER
================================================================================
This master launcher allows you to select and run any of the 3 single-file 
projects directly from this menu, or you can run each file individually:

  1. python 01_lost_and_found_matcher.py
  2. python 02_school_canteen_ordering_system.py
  3. python 03_student_marketplace.py

All projects strictly adhere to the CBSE Class 12 CS Curriculum:
- Pure Python 3 (Standard Library only - No external dependencies or MySQL required)
- File Handling with CSV Module
- Modular User-Defined Functions
- Clean Menu-Driven CLI & Error Handling
================================================================================
"""

import sys
import subprocess
import os

def main():
    while True:
        print("\n" + "="*60)
        print("     CBSE CLASS 12 CS FINAL PROJECTS SUITE")
        print("="*60)
        print(" [1] Project 1: Lost & Found Matcher System")
        print(" [2] Project 2: School Canteen Ordering & Billing System")
        print(" [3] Project 3: Student-to-Student Marketplace")
        print(" [4] Exit")
        print("="*60)

        choice = input("Select a project to run (1-4): ").strip()

        if choice == "1":
            print("\nLaunching Project 1: Lost & Found Matcher...\n")
            subprocess.run([sys.executable, "01_lost_and_found_matcher.py"])
        elif choice == "2":
            print("\nLaunching Project 2: School Canteen Ordering System...\n")
            subprocess.run([sys.executable, "02_school_canteen_ordering_system.py"])
        elif choice == "3":
            print("\nLaunching Project 3: Student Marketplace...\n")
            subprocess.run([sys.executable, "03_student_marketplace.py"])
        elif choice == "4":
            print("\nExiting Launcher. All the best for your Class 12 CS Practical & Viva!")
            break
        else:
            print("[-] Invalid selection! Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
