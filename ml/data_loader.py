import csv
from pathlib import Path

def load_employees(csv_path: Path):
    employees = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            employees.append({
                "employee_id": row["employee_id"],
                "name": row["name"],
                "skills": [s.strip() for s in row["skills"].split(",")],
                "experience_years": float(row["experience_years"]),
                "avg_rating": float(row["avg_rating"]),
                "current_workload": float(row["current_workload"]),
                "availability": int(row["availability"]),
            })
    return employees

def load_tasks(csv_path: Path):
    tasks = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tasks.append({
                "task_id": row["task_id"],
                "title": row["title"],
                "category": row["category"],
                "required_skills": [s.strip() for s in row["required_skills"].split(",")],
                "priority": int(row["priority"]),
                "estimated_hours": float(row["estimated_hours"]),
            })
    return tasks

