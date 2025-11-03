import csv
import os
import weighted

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

# Weights for grade calculation (customize as needed)
QUIZ_WEIGHT = 0.20  # 20% for average of quizzes
MIDTERM_WEIGHT = 0.30  # 30% for midterm
FINAL_WEIGHT = 0.40  # 40% for final
ATTENDANCE_WEIGHT = 0.10  # 10% for attendance

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
# --- Add new student(s) ---
def add_data():
    new_rows = []
    n = int(input("How many students to add? "))

    for i in range(n):
        print(f"\n--- Student #{i+1} ---")
        student = []
        for h in HEADER:
            while True:  # Loop until valid input
                val = input(f"Enter {h}: ").strip()  # Always strip input
                
                if h in ["last_name", "first_name", "section"]:
                    # Trim spaces (already stripped above, but ensure no internal issues)
                    student.append(val)
                    break
                elif h in ["quiz1", "quiz2", "quiz3", "quiz4", "quiz5", "midterm", "final", "attendance_percent"]:
                    # Validate numeric fields
                    try:
                        num_val = float(val) if val else None  # Default to None if empty
                        if num_val is not None and not (0 <= num_val <= 100):
                            print("❌ Score must be between 0 and 100. Try again.")
                            continue
                        student.append(str(num_val) if num_val is not None else "")  # Store as string for CSV
                        break
                    except ValueError:
                        print("❌ Invalid number. Try again.")
                        continue
                else:
                    # For student_id or other non-validated fields
                    student.append(val)
                    break
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

# ------------------------------------------------------------
# ANALYTICS SECTION
# ------------------------------------------------------------
def compute_distribution(filename=FILENAME):
    """Compute grade distribution (A, B, C, D, F)."""
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    grades = []
    for row in reader:
        try:
            q = [float(row[f"quiz{i}"]) for i in range(1, 6) if row[f"quiz{i}"] != "None"]
            mid = float(row["midterm"]) if row["midterm"] != "None" else 0
            fin = float(row["final"]) if row["final"] != "None" else 0
            att = float(row["attendance_percent"]) if row["attendance_percent"] != "None" else 0
            avg_quiz = sum(q) / len(q) if q else 0
            grade = (avg_quiz * 0.20) + (mid * 0.30) + (fin * 0.40) + (att * 0.10)
            grades.append(grade)
        except:
            continue

    bins = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for g in grades:
        if g >= 90: bins["A"] += 1
        elif g >= 80: bins["B"] += 1
        elif g >= 70: bins["C"] += 1
        elif g >= 60: bins["D"] += 1
        else: bins["F"] += 1

    print("\n📊 Grade Distribution:")
    for k, v in bins.items():
        print(f"{k}: {v}")


def compute_percentiles(filename=FILENAME):
    """Show top and bottom 10% students by total grade."""
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    results = []
    for row in reader:
        try:
            q = [float(row[f"quiz{i}"]) for i in range(1, 6) if row[f"quiz{i}"] != "None"]
            mid = float(row["midterm"]) if row["midterm"] != "None" else 0
            fin = float(row["final"]) if row["final"] != "None" else 0
            att = float(row["attendance_percent"]) if row["attendance_percent"] != "None" else 0
            avg_quiz = sum(q) / len(q) if q else 0
            grade = (avg_quiz * 0.20) + (mid * 0.30) + (fin * 0.40) + (att * 0.10)
            results.append((row["student_id"], grade))
        except:
            continue

    results.sort(key=lambda x: x[1], reverse=True)
    n = len(results)
    top = results[:max(1, n//10)]
    bottom = results[-max(1, n//10):]

    print("\n🏅 Top 10% Students:")
    for sid, g in top:
        print(f"{sid}: {g:.2f}")
    print("\n📉 Bottom 10% Students:")
    for sid, g in bottom:
        print(f"{sid}: {g:.2f}")


def find_outliers(filename=FILENAME):
    """Detect outlier grades (2 SD away from mean)."""
    import statistics
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    grades = []
    ids = []
    for row in reader:
        try:
            q = [float(row[f"quiz{i}"]) for i in range(1, 6) if row[f"quiz{i}"] != "None"]
            mid = float(row["midterm"]) if row["midterm"] != "None" else 0
            fin = float(row["final"]) if row["final"] != "None" else 0
            att = float(row["attendance_percent"]) if row["attendance_percent"] != "None" else 0
            avg_quiz = sum(q) / len(q) if q else 0
            grade = (avg_quiz * 0.20) + (mid * 0.30) + (fin * 0.40) + (att * 0.10)
            grades.append(grade)
            ids.append(row["student_id"])
        except:
            continue

    if not grades:
        print("⚠️ No valid grades found.")
        return

    mean = statistics.mean(grades)
    stdev = statistics.stdev(grades)
    print("\n🚨 Outliers (±2 SD from mean):")
    for sid, g in zip(ids, grades):
        if abs(g - mean) > 2 * stdev:
            print(f"{sid}: {g:.2f} (mean={mean:.2f}, stdev={stdev:.2f})")


def compute_improvement(filename=FILENAME):
    """Compare midterm and final to show improvement."""
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    print("\n📈 Student Improvement (Final - Midterm):")
    for row in reader:
        try:
            mid = float(row["midterm"]) if row["midterm"] != "None" else 0
            fin = float(row["final"]) if row["final"] != "None" else 0
            diff = fin - mid
            print(f"{row['student_id']}: {'+' if diff >= 0 else ''}{diff:.2f}")
        except:
            continue


# --- Menu ---
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
        print("6. Analytics and Reports")
        print("7. Exit")

        choice = input("Enter choice: ").strip()

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

        # --- Submenu for analytics ---
        elif choice == "6":
            while True:
                print("\n📊 ANALYTICS MENU")
                print("a. Compute Weighted Grades")
                print("b. Grade Distribution (A–F)")
                print("c. Percentiles (Top/Bottom 10%)")
                print("d. Outlier Detection (±2 SD)")
                print("e. Improvement (Final vs Midterm)")
                print("f. Back to Main Menu")

                sub = input("Select an option (a–f): ").lower().strip()

                if sub == "a":
                    weighted.compute_grades()
                elif sub == "b":
                    weighted.grade_distribution()
                elif sub == "c":
                    weighted.percentiles()
                elif sub == "d":
                    weighted.outliers()
                elif sub == "e":
                    weighted.improvement()
                elif sub == "f":
                    break
                else:
                    print("❌ Invalid choice. Try again.")

        elif choice == "7":
            print("👋 Exiting program.")
            break
        else:
            print("❌ Invalid choice. Try again.")


# --- Run program ---
menu()
