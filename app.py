import os
from flask import Flask, request, redirect, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from waitress import serve

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "Docker Task Manager")
PORT = int(os.getenv("PORT", "5000"))

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

tasks = []

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ app_name }}</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            color: #252344;
            background: linear-gradient(135deg, #eef2ff, #f8f7ff, #e8f5ff);
            padding: 40px 16px;
        }

        .container {
            width: 100%;
            max-width: 850px;
            margin: auto;
        }

        .header {
            margin-bottom: 28px;
        }

        .tag {
            display: inline-block;
            background: #e0e7ff;
            color: #4338ca;
            padding: 7px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 0.5px;
        }

        h1 {
            font-size: clamp(28px, 5vw, 40px);
            margin: 16px 0 8px;
            color: #312e81;
        }

        .subtitle {
            color: #77758f;
            line-height: 1.6;
            margin: 0;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-bottom: 22px;
        }

        .stat {
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border: 1px solid #e7e7f5;
            border-radius: 18px;
            box-shadow: 0 8px 25px rgba(55, 48, 120, 0.05);
        }

        .stat-label {
            font-size: 13px;
            color: #77758f;
            margin-bottom: 12px;
        }

        .stat-number {
            font-size: 30px;
            font-weight: bold;
        }

        .purple { color: #5b4be8; }
        .green { color: #0f9f79; }
        .orange { color: #dd8527; }

        .panel {
            background: #fff;
            padding: 26px;
            border-radius: 22px;
            border: 1px solid #e8e7f5;
            box-shadow: 0 12px 35px rgba(55, 48, 120, 0.07);
        }

        .panel-heading {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 20px;
        }

        h2 {
            font-size: 21px;
            margin: 0;
        }

        .count-badge {
            background: #f0efff;
            color: #5145cd;
            border-radius: 20px;
            padding: 6px 10px;
            font-size: 12px;
            font-weight: bold;
        }

        .add-form {
            display: flex;
            gap: 10px;
            margin-bottom: 26px;
        }

        .add-form input {
            flex: 1;
            min-width: 0;
            padding: 14px 15px;
            border: 1px solid #deddf0;
            border-radius: 12px;
            font-size: 15px;
            outline: none;
            background: #fafaff;
        }

        .add-form input:focus {
            border-color: #8275f5;
            box-shadow: 0 0 0 3px #8275f51c;
        }

        button {
            border: 0;
            border-radius: 11px;
            padding: 12px 16px;
            font-size: 13px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.15s, opacity 0.15s;
        }

        button:hover {
            opacity: 0.88;
            transform: translateY(-1px);
        }

        .add-button {
            background: #5948e8;
            color: white;
            white-space: nowrap;
        }

        .task-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .task-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 14px;
            padding: 17px 0;
            border-bottom: 1px solid #efeff6;
        }

        .task-item:last-child {
            border-bottom: 0;
        }

        .task-info {
            min-width: 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .task-dot {
            width: 10px;
            height: 10px;
            flex-shrink: 0;
            border-radius: 50%;
            background: #8b7cf6;
        }

        .task-text {
            overflow-wrap: anywhere;
            line-height: 1.5;
        }

        .done .task-dot {
            background: #16a779;
        }

        .done .task-text {
            color: #9897a9;
            text-decoration: line-through;
        }

        .task-actions {
            flex-shrink: 0;
        }

        .complete-button {
            color: #087c5a;
            background: #dff8ed;
        }

        .undo-button {
            color: #5b4be8;
            background: #eeecff;
        }

        .empty {
            text-align: center;
            padding: 35px 12px;
            color: #88869e;
            background: #fafaff;
            border-radius: 14px;
        }

        .empty-icon {
            font-size: 32px;
            margin-bottom: 12px;
        }

        .footer {
            text-align: center;
            color: #85839b;
            font-size: 12px;
            margin-top: 22px;
            line-height: 1.8;
        }

        @media (max-width: 550px) {
            body {
                padding: 25px 12px;
            }

            .stats {
                gap: 8px;
            }

            .stat {
                padding: 13px 10px;
                border-radius: 14px;
            }

            .stat-label {
                font-size: 11px;
            }

            .stat-number {
                font-size: 25px;
            }

            .panel {
                padding: 18px;
                border-radius: 18px;
            }

            .add-form {
                flex-direction: column;
            }

            .add-button {
                padding: 14px;
            }

            .task-item {
                align-items: flex-start;
            }

            .task-item button {
                padding: 10px;
                font-size: 12px;
            }
        }
    </style>
</head>

<body>
    <main class="container">

        <header class="header">
            <span class="tag">✦ MY PRODUCTIVITY SPACE</span>
            <h1>{{ app_name }}</h1>
            <p class="subtitle">
                Small steps every day. Great things get done.
            </p>
        </header>

        <section class="stats">
            <div class="stat">
                <div class="stat-label">Total Tasks</div>
                <div class="stat-number purple">{{ tasks|length }}</div>
            </div>

            <div class="stat">
                <div class="stat-label">Completed</div>
                <div class="stat-number green">{{ completed }}</div>
            </div>

            <div class="stat">
                <div class="stat-label">Pending</div>
                <div class="stat-number orange">{{ pending }}</div>
            </div>
        </section>

        <section class="panel">
            <div class="panel-heading">
                <h2>My Tasks</h2>
                <span class="count-badge">{{ pending }} pending</span>
            </div>

            <form class="add-form" action="/add" method="post">
                <input
                    type="text"
                    name="task"
                    placeholder="What would you like to do?"
                    maxlength="120"
                    required
                    aria-label="New task"
                >
                <button class="add-button" type="submit">
                    + Add Task
                </button>
            </form>

            <ul class="task-list">
                {% for task in tasks %}
                <li class="task-item {{ 'done' if task.done else '' }}">
                    <div class="task-info">
                        <span class="task-dot"></span>
                        <span class="task-text">{{ task.text }}</span>
                    </div>

                    <form
                        class="task-actions"
                        action="/toggle/{{ task.id }}"
                        method="post"
                    >
                        <button
                            class="{{ 'undo-button' if task.done else 'complete-button' }}"
                            type="submit"
                        >
                            {{ '↶ Undo' if task.done else '✓ Complete' }}
                        </button>
                    </form>
                </li>
                {% else %}
                <li class="empty">
                    <div class="empty-icon">📝</div>
                    <strong>No tasks yet</strong>
                    <p>Add your first task and get started!</p>
                </li>
                {% endfor %}
            </ul>
        </section>

        <footer class="footer">
            Built with Python, Flask, Flask-Limiter, Waitress and Docker
            <br>
            Stay focused. One task at a time.
        </footer>

    </main>
</body>
</html>
"""


@app.get("/")
def home():
    completed = sum(1 for task in tasks if task["done"])
    pending = len(tasks) - completed

    return render_template_string(
        HTML,
        app_name=APP_NAME,
        tasks=tasks,
        completed=completed,
        pending=pending
    )


@app.post("/add")
def add_task():
    task_text = request.form.get("task", "").strip()

    if task_text and len(task_text) <= 120:
        tasks.append({
            "id": max((t["id"] for t in tasks), default=0) + 1,
            "text": task_text,
            "done": False
        })

    return redirect("/")


@app.post("/toggle/<int:task_id>")
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            break

    return redirect("/")


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=PORT)