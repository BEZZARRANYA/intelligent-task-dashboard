from pathlib import Path
from flask import Flask, render_template, request

from ml.data_loader import load_employees, load_tasks
from ml.recommender import recommend_employees

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

app = Flask(__name__)

def normalize_tasks(tasks):
    """
    Ensure every task has 'id', 'name', 'category', 'required_skills'.
    Your CSV likely uses task_id/title/category/required_skills.
    """
    normalized = []
    for t in tasks:
        task_id = t.get("id") or t.get("task_id") or ""
        name = t.get("name") or t.get("title") or t.get("task_name") or "Untitled Task"
        category = t.get("category", "")
        req = t.get("required_skills", [])

        # required_skills might be a string in CSV: "python, ml"
        if isinstance(req, str):
            req_list = [s.strip() for s in req.replace(";", ",").split(",") if s.strip()]
        else:
            req_list = list(req)

        normalized.append({
            "id": task_id,
            "name": name,
            "category": category,
            "required_skills": req_list
        })
    return normalized


def get_task_by_id(tasks, task_id):
    """Find task in list by its normalized 'id'."""
    return next((t for t in tasks if t.get("id") == task_id), None)

@app.route("/")
def dashboard():
    employees = load_employees("data/employees.csv")
    tasks = load_tasks("data/tasks.csv")

    total_employees = len(employees)
    total_tasks = len(tasks)
    available_employees = sum(1 for e in employees if int(e.get("availability", 0)) == 1)

    categories = {}
    for t in tasks:
        cat = t.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    return render_template(
        "dashboard.html",
        total_employees=total_employees,
        total_tasks=total_tasks,
        available_employees=available_employees,
        categories=categories,
    )

@app.route("/recommend", methods=["GET", "POST"])
def recommend_page():
    tasks = load_tasks("data/tasks.csv")
    employees = load_employees("data/employees.csv")

    selected_task_id = None
    task_obj = None
    recs = []

    if request.method == "POST":
        selected_task_id = request.form.get("task_id")

        task_obj = next(
            (t for t in tasks if (t.get("id") or t.get("task_id")) == selected_task_id),
            None
        )

        if task_obj:
            recs = recommend_employees(task_obj, employees, top_k=5)

    return render_template(
        "recommend.html",
        title="Recommend",
        tasks=tasks,
        selected_task_id=selected_task_id,
        task_obj=task_obj,
        recs=recs
    )

@app.route("/analytics")
def analytics():
    # Model metrics from our experiments
    metrics = {
        "Logistic Regression": {"accuracy": 0.625, "f1": 0.769},
        "Random Forest": {"accuracy": 0.875, "f1": 0.933},
    }

    # Load real data for charts
    employees = load_employees(DATA_DIR / "employees.csv")
    tasks = load_tasks(DATA_DIR / "tasks.csv")

    # Task category counts
    category_counts = {}
    for t in tasks:
        category_counts[t["category"]] = category_counts.get(t["category"], 0) + 1

    # Employee workloads (name -> workload)
    workload = {e["name"]: e["current_workload"] for e in employees}

    return render_template(
        "analytics.html",
        title="Analytics",
        metrics=metrics,
        category_counts=category_counts,
        workload=workload,
    )
@app.route("/employees")
def employees_page():
    employees = load_employees("data/employees.csv")
    return render_template("employees.html", employees=employees, title="Employees")
@app.route("/tasks")
def tasks_page():
    tasks = load_tasks("data/tasks.csv")
    return render_template("tasks.html", tasks=tasks, title="Tasks")

if __name__ == "__main__":
    app.run(debug=True)

