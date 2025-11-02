import csv

FILENAME = "pra.csv"

# ------------------------------------------------------------
# 1) Load and Save
# ------------------------------------------------------------
def load_csv(filename):
    """Load CSV into a list of dictionaries."""
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")
        return list(reader), reader.fieldnames

def save_csv(filename, rows, fieldnames):
    """Save list of dictionaries back to CSV."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        writer.writerows(rows)
    print(f"💾 Saved to {filename}\n")

# ------------------------------------------------------------
# 2) Insert new student function
# ------------------------------------------------------------
def create_student(fieldnames):
    """Ask user for new student info and return it as a dictionary."""
    new_student = {}
    print("\n--- Add New Student ---")
    for field in fieldnames:
        value = input(f"Enter {field}: ").strip()
        new_student[field] = value
    print("✅ New student created in memory!")
    return new_student

# ------------------------------------------------------------
# 3) Menu system
# ------------------------------------------------------------
def menu():
    students, fieldnames = load_csv(FILENAME)
    print(f"Loaded {len(students)} student(s) from {FILENAME}\n")

    while True:
        print("""
========= STUDENT MENU =========
1. View all students
2. Create new student
3. Save changes
0. Exit
""")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n--- All Students ---")
            for s in students:
                print(s)
            print(f"Total: {len(students)} record(s)\n")

        elif choice == "2":
            new_stu = create_student(fieldnames)
            students.append(new_stu)
            print("✅ Student added (not yet saved).\n")

        elif choice == "3":
            save_csv(FILENAME, students, fieldnames)

        elif choice == "0":
            print("👋 Exiting program.")
            break

        else:
            print("❌ Invalid choice, please try again.\n")

# ------------------------------------------------------------
# 4) Run the program
# ------------------------------------------------------------
if __name__ == "__main__":
    menu()
