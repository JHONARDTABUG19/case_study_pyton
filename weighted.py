import csv
import os
from another import FILENAME, HEADER, QUIZ_WEIGHT, MIDTERM_WEIGHT, FINAL_WEIGHT, ATTENDANCE_WEIGHT  # Import from main script

# --- Compute weighted grades ---
def compute_grades(filename=FILENAME):
    if not os.path.exists(filename):
        print("⚠️ File not found. Please save data first.")
        return

    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        header = reader[0]
        rows = reader[1:]

    print("\n📊 Computed Weighted Grades:")
    print("Student ID | Weighted Grade")
    print("-" * 30)

    grades_data = []  # To store grades if we want to save them

    for row in rows:
        try:
            # Extract values (assuming they are numeric)
            quiz1 = float(row[4])  # quiz1
            quiz2 = float(row[5])  # quiz2
            quiz3 = float(row[6])  # quiz3
            quiz4 = float(row[7])  # quiz4
            quiz5 = float(row[8])  # quiz5
            midterm = float(row[9])  # midterm
            final = float(row[10])  # final
            attendance = float(row[11])  # attendance_percent

            # Compute quiz average
            quiz_avg = (quiz1 + quiz2 + quiz3 + quiz4 + quiz5) / 5

            # Compute weighted grade
            weighted_grade = (quiz_avg * QUIZ_WEIGHT) + (midterm * MIDTERM_WEIGHT) + (final * FINAL_WEIGHT) + (attendance * ATTENDANCE_WEIGHT)

            # Display
            print(f"{row[0]} | {weighted_grade:.2f}")

            # Prepare for saving (add to row if desired)
            grades_data.append(row + [f"{weighted_grade:.2f}"])

        except (ValueError, IndexError):
            print(f"{row[0]} | ❌ Invalid data (skipped)")

    # Optional: Save grades to a new column
    save_choice = input("\nSave grades to CSV as new column 'weighted_grade'? (y/n): ").strip().lower()
    if save_choice == "y":
        new_header = HEADER + ["weighted_grade"]
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(new_header)
            writer.writerows(grades_data)
        print("💾 Grades saved to CSV.")
