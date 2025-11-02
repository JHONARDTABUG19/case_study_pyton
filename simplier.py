import csv
import os

FILENAME = "ano.csv"
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


# --- Save to CSV (append mode, keep header) ---
def save_to_csv(data, filename=FILENAME):
    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(HEADER)
        writer.writerows(data)

    print(f"💾 Data saved to {filename}")


# --- Read/display CSV contents ---
def read_csv(filename=FILENAME):
    if not os.path.exists(filename):
        print("⚠️ File not found. Please save data first.")
        return

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        print("\n📘 Contents of file:")
        for row in reader:
            print(row)


# --- Add new student(s) ---
def add_data():
    new_rows = []
    n = int(input("How many students to add? "))

    for i in range(n):
        print(f"\n--- Student #{i+1} ---")
        student = []
        for h in HEADER:
            val = input(f"Enter {h}: ")
            student.append(val)
        new_rows.append(student)

    save_to_csv(new_rows)


# --- Delete a row by student_id ---
def delete_data(filename=FILENAME):
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    student_id = input("Enter student_id to delete: ")

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))

    header = reader[0]
    rows = reader[1:]  # skip header

    updated_rows = [row for row in rows if row[0] != student_id]

    if len(rows) == len(updated_rows):
        print("❌ No student found with that ID.")
        return

    # Rewrite file with updated content
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(updated_rows)

    print(f"🗑️ Deleted student_id {student_id} successfully.")


# --- Select and display one column ---
def select_column(filename=FILENAME):
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        header = reader[0]
        rows = reader[1:]

    print("\nAvailable columns:")
    for i, col in enumerate(header):
        print(f"{i+1}. {col}")

    col_name = input("Enter column name to view: ").strip()

    if col_name not in header:
        print("❌ Invalid column name.")
        return

    index = header.index(col_name)

    print(f"\n📊 Values under '{col_name}':")
    for row in rows:
        print(row[index])


# --- Select and display one row by student_id ---
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


# --- Menu ---
def menu():
    while True:
        print("\n=== STUDENT CSV MENU ===")
        print("1. Add and Save Student(s)")
        print("2. Read CSV File")
        print("3. Delete Student by ID")
        print("4. Select Column")
        print("5. Select Row by Student ID")
        print("6. Exit")

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
            print("👋 Exiting program.")
            break
        else:
            print("❌ Invalid choice. Try again.")


# --- Run program ---
menu()
