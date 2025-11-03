# ------------------------------------------------------------
# STUDENT GRADE MANAGEMENT SYSTEM (CSV-BASED)
# ------------------------------------------------------------
# This program manages student records stored in a CSV file.
# Features:
#   ✅ Add new student data with validation
#   ✅ View all records or specific rows/columns
#   ✅ Delete a student by ID
#   ✅ Compute weighted grades (via imported module 'weight')
#   ✅ Simple text-based menu for navigation
#
# Author: [Your Name]
# Date: [Your Date]
# ------------------------------------------------------------
#this is AI yung nasataas
import csv       # for reading/writing CSV files
import os        # for file existence checking
import weight    # custom module to compute weighted grades

# --- Constants ---
FILENAME = "ano.csv"  # Default CSV file name
HEADER = [
    "student_id",
    "last_name",
    "first_name",
    "section",
    "quiz1",
    "quiz2",
    "quiz3",
    "quiz4",
    "quiz5",
    "midterm",
    "final",
    "attendance_percent"
]

# --- Grade Weights (customizable) ---
QUIZ_WEIGHT = 0.20       # 20% for quizzes average
MIDTERM_WEIGHT = 0.30    # 30% for midterm exam
FINAL_WEIGHT = 0.40      # 40% for final exam
ATTENDANCE_WEIGHT = 0.10 # 10% for attendance


# ------------------------------------------------------------
# Function: save_to_csv()
# Purpose: Save a list of new student rows to the CSV file.
# Notes: Creates file with header if it doesn't exist yet.
# ------------------------------------------------------------
def save_to_csv(data, filename=FILENAME):
    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(HEADER)  # Write header only once
        writer.writerows(data)

    print(f"💾 Data saved to {filename}")


# ------------------------------------------------------------
# Function: read_csv()
# Purpose: Display all contents of the CSV file.
# ------------------------------------------------------------
def read_csv(filename=FILENAME):
    if not os.path.exists(filename):
        print("⚠️ File not found. Please save data first.")
        return

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        print("\n📘 Contents of file:")
        for row in reader:
            print(row)


# ------------------------------------------------------------
# Function: add_data()
# Purpose: Add new student records with input validation.
# ------------------------------------------------------------
def add_data():
    new_rows = []
    n = int(input("How many students to add? "))

    for i in range(n):
        print(f"\n--- Student #{i+1} ---")
        student = [] 

        # Loop through each column name in the header
        for h in HEADER:
            while True:
                val = input(f"Enter {h}: ").strip()

                # Handle name and section (string fields)
                if h in ["last_name", "first_name", "section"]:
                    if not val.isalpha():
                        print("❌ Please enter letters only (no numbers). Try again.")
                        continue
                    student.append(val)                             
                    break

                # Handle numeric fields (quizzes, exams, attendance)
                elif h in ["quiz1", "quiz2", "quiz3", "quiz4", "quiz5",
                           "midterm", "final", "attendance_percent"]:
                    try:
                        num_val = float(val) if val else None   #If they left it blank, store None instead (represents “no value”).
                        if num_val is not None and not (0 <= num_val <= 100):
                            print("❌ Score must be between 0 and 100. Try again.")
                            continue
                        # Store as string for writing into CSV
                        student.append(str(num_val) if num_val is not None else "None")     #short way of creating if-else
                        break
                    except ValueError:
                        print("❌ Invalid number. Try again.")
                        continue

                # Default case: student_id or others
                else:
                    student.append(val) #take the user’s input (val) and store it directly
                    break

        new_rows.append(student)

    save_to_csv(new_rows)


# ------------------------------------------------------------
# Function: delete_data()
# Purpose: Delete a student record using student_id.
# ------------------------------------------------------------
def delete_data(filename=FILENAME):     #FILENAME accessing the ano.csv
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    student_id = input("Enter student_id to delete: ")

    # Read all existing data
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    header = reader[0]
    rows = reader[1:]

    # Keep only rows that do NOT match the entered ID
    updated_rows = []
    for row in rows:        
        if row[0] != student_id:    # any row whose row[0] == userinput will be excluded from the new list.
            updated_rows.append(row)


    if len(rows) == len(updated_rows):
        print("❌ No student found with that ID.")
        return

    # Overwrite file with updated data
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(updated_rows)

    print(f"🗑️ Deleted student_id {student_id} successfully.")


# ------------------------------------------------------------
# Function: select_column()
# Purpose: Display values from a chosen column.
# ------------------------------------------------------------
def select_column(filename=FILENAME):
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        header = reader[0]
        rows = reader[1:]

    # Display available column names
    print("\nAvailable columns:")
    for i, col in enumerate(header):
        print(f"{i+1}. {col}")      # Ex. 1. student_id

    col_name = input("Enter column name to view: ").strip()

    if col_name not in header:
        print("❌ Invalid column name.")
        return

    index = header.index(col_name)  #index of col_name  example, student_id then index[0]

    # Print all values in the selected column
    print(f"\n📊 Values under '{col_name}':")
    for row in rows:        ##rows = reader[1:]
        print(row[index])


# ------------------------------------------------------------
# Function: select_row()
# Purpose: Display one student's full record using their ID.
# ------------------------------------------------------------
def select_row(filename=FILENAME):
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    student_id = input("Enter student_id to view: ")

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        header = reader[0]
        rows = reader[1:]

    for row in rows:
        if row[0] == student_id:
            print("\n📋 Student Information:")
            for h, v in zip(header, row):
                print(f"{h}: {v}")
            return

    print("❌ No student found with that ID.")


# ------------------------------------------------------------
# Function: menu()
# Purpose: Main menu interface for user interaction.
# ------------------------------------------------------------
def menu():
    while True:
        print("\n=== STUDENT CSV MENU ===")
        print("1. Add and Save Student(s)")
        print("2. Read CSV File")
        print("3. Delete Student by ID")
        print("4. Select Column")
        print("5. Select Row by Student ID")
        print("6. Compute Weighted Grades")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_data()
        elif choice == "2":
            read_csv()
        elif choice == "3":
            delete_data()
        elif choice == "4":
            select_column()
        elif choice == "5":
            select_row()
        elif choice == "6":
            weight.compute_grades()  # Calls external module
        elif choice == "7":
            print("👋 Exiting program.")
            break
        else:
            print("❌ Invalid choice. Try again.")


# ------------------------------------------------------------
# Run the Program
# ------------------------------------------------------------
menu()
