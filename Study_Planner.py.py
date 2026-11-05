"""
Study Planner
-------------
Real-life problem: Students often forget assignments and exam deadlines
because everything is scattered across notes and chats. This tool keeps
all study tasks in one place, shows what is due soon, and tracks progress.

Run:  python main.py
Data is saved automatically in tasks.json
"""

import json
import os
from datetime import date, datetime

DATA_FILE = "tasks.json"
PRIORITIES = ["High", "Medium", "Low"]


def load_tasks() -> list:
    """Load saved tasks, or start with an empty list."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks: list) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def ask_date(prompt: str) -> str:
    """Keep asking until the user enters a valid date (YYYY-MM-DD)."""
    while True:
        text = input(prompt).strip()
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("Please use the format YYYY-MM-DD, like 2026-12-25")


def days_left(due: str) -> int:
    return (datetime.strptime(due, "%Y-%m-%d").date() - date.today()).days


def describe_due(task: dict) -> str:
    if task["done"]:
        return "completed"
    d = days_left(task["due"])
    if d < 0:
        return f"OVERDUE by {-d} day(s)"
    if d == 0:
        return "due TODAY"
    return f"{d} day(s) left"


def add_task(tasks: list) -> None:
    title = input("\nTask title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    subject = input("Subject (e.g. Maths): ").strip() or "General"
    due = ask_date("Due date (YYYY-MM-DD): ")

    print("Priority: 1. High  2. Medium  3. Low")
    p = input("Choose (1-3, default 2): ").strip()
    priority = PRIORITIES[int(p) - 1] if p in ("1", "2", "3") else "Medium"

    tasks.append({"title": title, "subject": subject, "due": due,
                  "priority": priority, "done": False})
    save_tasks(tasks)
    print(f"Added: {title} ({priority}, {describe_due(tasks[-1])})")


def view_tasks(tasks: list, only_pending: bool = False) -> None:
    shown = [t for t in tasks if not (only_pending and t["done"])]
    if not shown:
        print("\nNo tasks to show.")
        return
    # Sort: pending first, then by due date
    shown = sorted(shown, key=lambda t: (t["done"], t["due"]))
    print("\nNo.  Status  Priority  Due         Subject     Title / Info")
    print("-" * 70)
    for t in shown:
        num = tasks.index(t) + 1
        mark = "[x]" if t["done"] else "[ ]"
        print(f"{num:<4} {mark:<7} {t['priority']:<9} {t['due']}  "
              f"{t['subject']:<11} {t['title']} ({describe_due(t)})")


def pick_task(tasks: list, action: str):
    if not tasks:
        print("\nNo tasks yet.")
        return None
    view_tasks(tasks)
    num = input(f"\nEnter the task number to {action}: ").strip()
    if num.isdigit() and 1 <= int(num) <= len(tasks):
        return int(num) - 1
    print("Invalid number.")
    return None


def complete_task(tasks: list) -> None:
    i = pick_task(tasks, "mark as done")
    if i is not None:
        tasks[i]["done"] = True
        save_tasks(tasks)
        print(f"Great job! Completed: {tasks[i]['title']}")


def delete_task(tasks: list) -> None:
    i = pick_task(tasks, "delete")
    if i is not None:
        removed = tasks.pop(i)
        save_tasks(tasks)
        print(f"Deleted: {removed['title']}")


def show_progress(tasks: list) -> None:
    if not tasks:
        print("\nNo tasks yet.")
        return
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    overdue = sum(1 for t in tasks if not t["done"] and days_left(t["due"]) < 0)
    soon = sum(1 for t in tasks if not t["done"] and 0 <= days_left(t["due"]) <= 3)
    percent = done / total * 100
    bar = "#" * int(percent / 10) + "-" * (10 - int(percent / 10))
    print(f"\nProgress: [{bar}] {percent:.0f}%  ({done}/{total} done)")
    print(f"Overdue : {overdue}")
    print(f"Due within 3 days: {soon}")
    if overdue:
        print("Tip: finish the overdue tasks first.")


def main() -> None:
    tasks = load_tasks()
    print("=== Study Planner ===")
    while True:
        print("\n1. Add task")
        print("2. View pending tasks")
        print("3. View all tasks")
        print("4. Mark task as done")
        print("5. Delete task")
        print("6. Progress report")
        print("7. Exit")
        choice = input("Choose (1-7): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks, only_pending=True)
        elif choice == "3":
            view_tasks(tasks)
        elif choice == "4":
            complete_task(tasks)
        elif choice == "5":
            delete_task(tasks)
        elif choice == "6":
            show_progress(tasks)
        elif choice == "7":
            print("Bye! Keep studying, one task at a time.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
