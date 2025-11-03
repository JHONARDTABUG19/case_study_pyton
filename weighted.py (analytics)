# ------------------------------------------------------------
# weight.py — Analytics Module for Student Grade Management
# ------------------------------------------------------------
# Features:
#   ✅ Compute weighted grades for each student
#   ✅ Show grade distributions (A-F)
#   ✅ Show top/bottom 10% (percentiles)
#   ✅ Detect grade outliers (±2 SD)
#   ✅ Show improvement (Final - Midterm)
#
# Author: [Your Name]
# ------------------------------------------------------------

import csv
import os
import statistics

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
FILENAME = "ano.csv"

# Use consistent weights (same as main.py)
QUIZ_WEIGHT = 0.20
MIDTERM_WEIGHT = 0.30
FINAL_WEIGHT = 0.40
ATTENDANCE_WEIGHT = 0.10


# ------------------------------------------------------------
# Helper — Compute weighted grade for one row
# ------------------------------------------------------------
def compute_weighted(row):
    """Return weighted grade given a student's record row."""
    try:
        quizzes = [
            float(row[f"quiz{i}"]) for i in range(1, 6)
            if row[f"quiz{i}"] != "None"
        ]
        midterm = float(row["midterm"]) if row["midterm"] != "None" else 0
        final = float(row["final"]) if row["final"] != "None" else 0
        attendance = float(row["attendance_percent"]) if row["attendance_percent"] != "None" else 0

        avg_quiz = sum(quizzes) / len(quizzes) if quizzes else 0
        weighted = (
            avg_quiz * QUIZ_WEIGHT
            + midterm * MIDTERM_WEIGHT
            + final * FINAL_WEIGHT
            + attendance * ATTENDANCE_WEIGHT
        )
        return round(weighted, 2)
    except Exception:
        return None


# ------------------------------------------------------------
# Main Analytics Functions
# ------------------------------------------------------------

def compute_grades(filename=FILENAME):
    """Compute and display weighted grades for all students."""
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("\n📘 Weighted Grades:")
        print("-" * 50)
        print(f"{'ID':<10}{'Name':<20}{'Weighted Grade':>15}")
        print("-" * 50)
        for row in reader:
            grade = compute_weighted(row)
            name = f"{row['last_name']}, {row['first_name']}"
            print(f"{row['student_id']:<10}{name:<20}{grade:>10}")
        print("-" * 50)


def grade_distribution(filename=FILENAME):
    """Compute grade distribution (A–F)."""
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        grades = [compute_weighted(r) for r in reader if compute_weighted(r) is not None]

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


def percentiles(filename=FILENAME):
    """Show top and bottom 10% students."""
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    results = [
        (r["student_id"], compute_weighted(r))
        for r in reader
        if compute_weighted(r) is not None
    ]

    results.sort(key=lambda x: x[1], reverse=True)
    n = len(results)
    top = results[:max(1, n // 10)]
    bottom = results[-max(1, n // 10):]

    print("\n🏅 Top 10% Students:")
    for sid, g in top:
        print(f"{sid}: {g:.2f}")
    print("\n📉 Bottom 10% Students:")
    for sid, g in bottom:
        print(f"{sid}: {g:.2f}")


def outliers(filename=FILENAME):
    """Detect grades ±2 standard deviations away from mean."""
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    grades = [compute_weighted(r) for r in reader if compute_weighted(r) is not None]
    ids = [r["student_id"] for r in reader if compute_weighted(r) is not None]

    if len(grades) < 2:
        print("⚠️ Not enough data.")
        return

    mean = statistics.mean(grades)
    stdev = statistics.stdev(grades)

    print("\n🚨 Outliers (±2 SD from mean):")
    for sid, g in zip(ids, grades):
        if abs(g - mean) > 1.5 * stdev:
            print(f"{sid}: {g:.2f} (mean={mean:.2f}, standarddeviation={stdev:.2f})")


def improvement(filename=FILENAME):
    """Compare midterm and final to measure improvement."""
    if not os.path.exists(filename):
        print("⚠️ File not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        print("\n📈 Improvement (Final - Midterm):")
        for r in reader:
            try:
                mid = float(r["midterm"]) if r["midterm"] != "None" else 0
                fin = float(r["final"]) if r["final"] != "None" else 0
                diff = fin - mid
                print(f"{r['student_id']}: {'+' if diff >= 0 else ''}{diff:.2f}")
            except:
                continue
