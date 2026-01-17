# Intelligent Task Dashboard (Flask + ML)

A Flask-based intelligent task management dashboard with ML-powered task-to-employee recommendations and analytics visualizations.

## Features
- Web dashboard UI (Bootstrap)
- Task-to-employee recommendation page (Top-K recommendations)
- Analytics dashboard with charts (Chart.js)
  - Model metrics comparison (Accuracy, F1-score)
  - Tasks by category
  - Employee workload distribution

## Tech Stack
- Python, Flask
- scikit-learn (for ML pipeline results)
- Bootstrap 5 (UI)
- Chart.js (visualization)

## Project Structure
- `app.py` Flask application
- `ml/` ML modules (recommender + CSV loader)
- `data/` synthetic enterprise datasets
- `templates/` HTML templates

## How to Run (macOS)
```bash
cd intelligent-task-dashboard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py

