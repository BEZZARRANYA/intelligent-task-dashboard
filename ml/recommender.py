def recommend_employees(task, employees, top_k=3):
    """
    Recommend the best employees for a given task.

    Parameters:
    - task (dict): task information including required_skills, priority, estimated_hours
    - employees (list of dict): employee profiles with skills, rating, workload, availability
    - top_k (int): number of employees to recommend

    Returns:
    - list of recommended employees
    """

    scores = []

    for emp in employees:
        # Skill matching (simple overlap)
        task_skills = set(task.get("required_skills", []))
        emp_skills = set(emp.get("skills", []))
        skill_score = len(task_skills & emp_skills)

        # Performance score
        performance_score = emp.get("avg_rating", 0)

        # Workload penalty
        workload_penalty = emp.get("current_workload", 0)

        # Availability bonus
        availability_bonus = 1 if emp.get("availability", 0) else 0

        total_score = (
            skill_score * 2
            + performance_score
            + availability_bonus
            - workload_penalty * 0.1
        )

        scores.append((total_score, emp))

    scores.sort(reverse=True, key=lambda x: x[0])

    return [emp for _, emp in scores[:top_k]]
