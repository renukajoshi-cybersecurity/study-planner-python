# Study Planner

A simple Python command-line app to organize study tasks, track deadlines and see your progress.

## Real-life problem

Students often forget assignments and exam deadlines because tasks are scattered across notebooks, chats and memory. This tool keeps everything in one place, shows what is overdue or due soon, and tracks how much you have completed.

## Features

- Add tasks with subject, due date and priority (High / Medium / Low)
- View pending tasks sorted by due date
- See days left, "due today" or "overdue" status for every task
- Mark tasks as done and delete tasks
- Progress report with a completion bar, overdue count and tasks due within 3 days
- Input validation for dates and menu choices
- Data is saved automatically in `tasks.json`, so nothing is lost when you close the program

## How to run

Requirements: Python 3.8 or newer. No external libraries needed.

```
python main.py
```

## Example

```
=== Study Planner ===
1. Add task
2. View pending tasks
3. View all tasks
4. Mark task as done
5. Delete task
6. Progress report
7. Exit
Choose (1-7): 6

Progress: [###-------] 33%  (1/3 done)
Overdue : 1
Due within 3 days: 1
Tip: finish the overdue tasks first.
```

## Tech used

- Python 3 (standard library only: `json`, `os`, `datetime`)

## Author

YOUR NAME HERE
