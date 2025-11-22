import json
import os
import sys
import argparse

TASKS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'tasks.json')

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2)

def add_task(title):
    tasks = load_tasks()
    next_id = (max([t.get('id', 0) for t in tasks]) + 1) if tasks else 1
    task = {"id": next_id, "title": title, "completed": False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added: [{task['id']}] {task['title']}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks.")
        return
    for t in tasks:
        status = "✓" if t.get("completed") else "✗"
        print(f"[{status}] {t['id']}: {t['title']}")

def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t.get('id') == task_id:
            if t.get('completed'):
                print(f"Already completed: {task_id}")
            else:
                t['completed'] = True
                print(f"Completed: {task_id}")
            save_tasks(tasks)
            return
    print(f"Not found: {task_id}")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t.get('id') != task_id]
    if len(new_tasks) == len(tasks):
        print(f"Not found: {task_id}")
        return
    save_tasks(new_tasks)
    print(f"Deleted: {task_id}")

def build_parser():
    p = argparse.ArgumentParser(prog="task-manager", description="CLI Task Manager")
    sub = p.add_subparsers(dest="command", required=True)

    pa = sub.add_parser("add", help="Add a task")
    pa.add_argument("title", nargs="+", help="Task title words")

    sub.add_parser("list", help="List tasks")

    pc = sub.add_parser("complete", help="Mark task complete")
    pc.add_argument("id", type=int, help="Task id")

    pd = sub.add_parser("delete", help="Delete task")
    pd.add_argument("id", type=int, help="Task id")

    return p

def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "add":
        add_task(" ".join(args.title))
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    return 0

if __name__ == "__main__":
    sys.exit(main())
