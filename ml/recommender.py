# ml/recommender.py

from typing import Any, Dict, List

def recommend_employees(task, employees, top_k=5):
    results = []

    required_skills = set(task.get("required_skills", []))

    for emp in employees:
        reasons = []
        score = 0.0

        # ---- Normalize employee fields ----
        employee = {
            "id": emp.get("id", emp.get("employee_id", "")),
            "name": emp.get("name", emp.get("employee_name", "")),
            "skills": emp.get("skills", []),
            "avg_rating": emp.get("avg_rating", emp.get("rating", 0)),
            "current_workload": emp.get("current_workload", emp.get("workload", 0)),
            "availability": emp.get("availability", 0),
        }

        # 1. Skill match
        emp_skills = set(employee["skills"])
        matched_skills = required_skills & emp_skills
        skill_ratio = len(matched_skills) / max(len(required_skills), 1)

        score += 0.4 * skill_ratio
        if matched_skills:
            reasons.append(
                f"Skills matched ({len(matched_skills)}/{len(required_skills)}): "
                + ", ".join(sorted(matched_skills))
            )

        # 2. Rating
        rating_score = employee["avg_rating"] / 5.0
        score += 0.3 * rating_score
        if employee["avg_rating"] >= 4.0:
            reasons.append(f"High rating ({employee['avg_rating']}/5)")

        # 3. Workload
        workload_score = max(0, 1 - employee["current_workload"] / 40)
        score += 0.2 * workload_score
        if employee["current_workload"] <= 20:
            reasons.append("Low workload")

        # 4. Availability
        if employee["availability"] == 1:
            score += 0.1
            reasons.append("Available")

        results.append({
            "employee": employee,
            "score": round(score, 2),
            "reasons": reasons
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

