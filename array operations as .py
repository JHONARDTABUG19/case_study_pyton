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

def clean_ingest(filename=FILENAME):
    """
    Reads a CSV file, validates each row, and separates good rows from bad rows.
    Blanks or invalid numeric fields (quiz1–attendance) are converted to None.
    Returns: tuple (valid_rows, bad_rows)
    """
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return [], []

    valid_rows = []
    bad_rows = []

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return [], []

    header = rows[0]
    data_rows = rows[1:]

    for row in data_rows:
        try:
            # Ensure correct number of columns
            while len(row) < len(header):
                row.append("")

            # Validate student_id
            if not row[0].strip():
                raise ValueError("Missing student_id")

            # Validate numeric fields (quiz1–quiz5=4–8, midterm=9, final=10, attendance=11)
            for i in range(4, 12):
                val = row[i].strip() if isinstance(row[i], str) else row[i]
                
                # ✅ Blank or "none" → set to None
                if val == "" or str(val).lower() == "none":
                    row[i] = None
                else:
                    try:
                        num_val = float(val)
                        # ✅ Range check still applies
                        if not (0 <= num_val <= 100):
                            raise ValueError(f"{header[i]} out of range")
                        row[i] = num_val
                    except ValueError:
                        # ✅ Invalid → None instead of 0.0
                        row[i] = None

            # Validate names/section (last_name=1, first_name=2, section=3)
            for i in range(1, 4):
                if not row[i].strip():
                    row[i] = "none"

            valid_rows.append(row)

        except Exception as e:
            row.append(str(e))
            bad_rows.append(row)

    print(f"\n✅ Valid rows: {len(valid_rows)}")
    print(f"⚠️ Bad rows: {len(bad_rows)}")
    if bad_rows:
        print("\nBad rows:")
        for r in bad_rows:
            print(r)

    return valid_rows, bad_rows



def save_to_csv(data, filename=FILENAME):
    """Append data to CSV, create header if file doesn't exist"""
    file_exists = os.path.exists(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(HEADER)
        writer.writerows(data)
    print(f"💾 Data saved to {filename}")


def save_cleaned_csv(valid_rows, filename=FILENAME):
    """Overwrite CSV with only valid rows"""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(valid_rows)
    print(f"💾 Cleaned data saved to {filename}")


# ----------------------
# CRUD Operations
# ----------------------
def add_data():
    """
    Adds one or more students interactively with name validation (no numbers).
    """
    new_rows = []
    n = int(input("How many students to add? "))

    for i in range(n):
        print(f"\n--- Student #{i+1} ---")
        print(f"--- student_id is required ---\n")
        student = []

        for idx, h in enumerate(HEADER):
            while True:
                val = input(f"Enter {h} (leave blank for 'none'): ").strip()

                # Validate student_id
                if idx == 0:
                    if not val:
                        print("❌ student_id cannot be empty. Try again.")
                        continue
                    student.append(val)
                    break

                # Validate names & section
                elif idx in [1, 2, 3]:
                    if val == "":
                        val = "none"
                    elif any(char.isdigit() for char in val):
                        print("❌ Names and section cannot contain numbers. Try again.")
                        continue
                    student.append(val)
                    break

                # Validate numeric fields (quiz–attendance)
                elif idx in range(4, 12):
                    if val == "" or val.lower() == "none":
                        student.append("none")
                        break
                    try:
                        num_val = float(val)
                        if not (0 <= num_val <= 100):
                            print("❌ Score must be between 0 and 100. Try again.")
                            continue
                        student.append(num_val)
                        break
                    except ValueError:
                        print("❌ Invalid number. Enter 0–100 or leave blank for 'none'.")
                        continue

        new_rows.append(student)

    save_to_csv(new_rows)



def delete_data(filename=FILENAME):
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    student_id = input("Enter student_id to delete: ")
    valid_rows, _ = clean_ingest(filename)
    updated_rows = [row for row in valid_rows if row[0] != student_id]

    if len(updated_rows) == len(valid_rows):
        print("❌ No student found with that ID.")
        return

    save_cleaned_csv(updated_rows)
    print(f"🗑️ Deleted student_id {student_id} successfully.")


def select_column(filename=FILENAME):
    valid_rows, _ = clean_ingest(filename)
    if not valid_rows:
        print("⚠️ No valid data.")
        return

    print("\nAvailable columns:")
    for i, col in enumerate(HEADER):
        print(f"{i+1}. {col}")

    col_name = input("Enter column name to view: ").strip()
    if col_name not in HEADER:
        print("❌ Invalid column name.")
        return

    index = HEADER.index(col_name)
    print(f"\n📊 Values under '{col_name}':")
    for row in valid_rows:
        print(row[index])


def select_row(filename=FILENAME):
    valid_rows, _ = clean_ingest(filename)
    if not valid_rows:
        print("⚠️ No valid data.")
        return

    student_id = input("Enter student_id to view: ")
    for row in valid_rows:
        if row[0] == student_id:
            print("\n📋 Student Information:")
            for h, v in zip(HEADER, row):
                print(f"{h}: {v}")
            return

    print("❌ No student found with that ID.")
