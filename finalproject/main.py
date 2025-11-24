import argparse
from pathlib import Path
from dotenv import load_dotenv
from task_manager import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    search_tasks,
    prioritize_task,
    set_priority,
    edit_task,
    suggest_tasks,
    clear_tasks,
    get_overview,
)

# Load environment variables (search common locations)
_env_search_order = [
    "key.env",  # legacy filename
    ".env",     # conventional filename
    Path(".venv") / "key.env",  # user placed inside virtual environment
]
for _candidate in _env_search_order:
    candidate_path = Path(__file__).parent / _candidate
    if candidate_path.exists():
        load_dotenv(candidate_path)  # stop at first found
        break


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI Task Manager with optional AI summarization"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add
    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("--title", required=True, help="Title of the task")
    p_add.add_argument("--description", default="", help="Detailed description")
    p_add.add_argument("--due", help="Due date (YYYY-MM-DD)")
    # No default so we know if user omitted and can prompt interactively
    p_add.add_argument(
        "--priority", type=int, help="Priority 1 (high) - 5 (low); will prompt if omitted"
    )
    p_add.add_argument(
        "--summarize", action="store_true", help="Generate AI summary if possible"
    )
    p_add.add_argument(
        "--quick",
        action="store_true",
        help="Skip asking for due date/priority; sets no due and priority 3",
    )

    # list
    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument(
        "--filter",
        choices=["all", "pending", "completed"],
        default="all",
        help="Filter tasks by status",
    )
    p_list.add_argument(
        "--sort",
        choices=["priority", "due"],
        default="priority",
        help="Sort order",
    )
    p_list.add_argument(
        "--show-summary",
        action="store_true",
        help="Display AI-generated summaries (if available)",
    )

    # complete
    p_complete = sub.add_parser("complete", help="Mark task complete")
    p_complete.add_argument("--id", type=int, required=True, help="Task ID")

    # delete
    p_delete = sub.add_parser("delete", help="Delete a task")
    p_delete.add_argument("--id", type=int, required=True, help="Task ID")

    # search
    p_search = sub.add_parser("search", help="Search tasks by text")
    p_search.add_argument("--query", required=True, help="Search text")

    # prioritize (AI-powered)
    p_prio = sub.add_parser("prioritize", help="AI-powered task prioritization")
    p_prio.add_argument("--id", type=int, required=True, help="Task ID")

    # set-priority (manual)
    p_set_prio = sub.add_parser("set-priority", help="Manually set task priority")
    p_set_prio.add_argument("--id", type=int, required=True, help="Task ID")
    p_set_prio.add_argument(
        "--priority", type=int, required=True, help="Priority 1-5"
    )

    # edit
    p_edit = sub.add_parser("edit", help="Edit an existing task")
    p_edit.add_argument("--id", type=int, required=True, help="Task ID")
    p_edit.add_argument("--title", help="New title")
    p_edit.add_argument("--description", help="New description")
    p_edit.add_argument("--due", help="New due date (YYYY-MM-DD)")

    # suggest
    p_suggest = sub.add_parser("suggest", help="Get AI task suggestions")
    p_suggest.add_argument(
        "--context",
        default="",
        help="Optional context for suggestions (e.g., 'work project', 'personal goals')",
    )

    # clear
    p_clear = sub.add_parser("clear", help="Delete all tasks")
    p_clear.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt",
    )

    # overview
    sub.add_parser("overview", help="Show task statistics summary")

    # options (list available commands)
    sub.add_parser("options", help="List all available commands")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    store_path = Path(__file__).parent / "data" / "tasks.json"

    if args.command == "add":
        # Decide due date
        due = args.due
        if due is None and not args.quick:
            entered = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip()
            if entered:
                due = entered

        # Decide priority
        priority = args.priority
        if priority is None:
            if args.quick:
                priority = 3  # default silently
            else:
                entered = input("Enter priority 1 (high) - 5 (low) or press Enter for 3: ").strip()
                if entered:
                    try:
                        priority = int(entered)
                    except ValueError:
                        priority = 3
                else:
                    priority = 3

        task = add_task(
            store_path,
            title=args.title,
            description=args.description,
            due_date=due,
            priority=priority,
            summarize=args.summarize,
        )
        print(f"Added task #{task['id']}: {task['title']}")
        if task.get('summary'):
            print(f"  Summary: {task['summary']}")
    elif args.command == "list":
        tasks = list_tasks(store_path, filter_mode=args.filter, sort_mode=args.sort)
        if not tasks:
            print("No tasks found.")
        else:
            for t in tasks:
                status_icon = "✔" if t["status"] == "complete" else "✘"
                due = t["due_date"] or "-"
                print(
                    f"[{status_icon}] #{t['id']} (P{t['priority']}) due:{due} title:{t['title']}"
                )
                if args.show_summary and t.get('summary'):
                    print(f"    Summary: {t['summary']}")
    elif args.command == "complete":
        if complete_task(store_path, args.id):
            print(f"Task #{args.id} marked complete.")
        else:
            print(f"Task #{args.id} not found.")
    elif args.command == "delete":
        if delete_task(store_path, args.id):
            print(f"Task #{args.id} deleted.")
        else:
            print(f"Task #{args.id} not found.")
    elif args.command == "search":
        results = search_tasks(store_path, args.query)
        if not results:
            print("No matching tasks.")
        else:
            for t in results:
                status_icon = "✔" if t["status"] == "complete" else "✘"
                print(f"[{status_icon}] #{t['id']} {t['title']} :: {t['description']}")
    elif args.command == "prioritize":
        priority = prioritize_task(store_path, args.id)
        if priority is not None:
            print(f"Task #{args.id} priority set to {priority} (AI-determined).")
        else:
            print(f"Could not prioritize task #{args.id}. Check OpenAI API key or task ID.")
    elif args.command == "set-priority":
        if set_priority(store_path, args.id, args.priority):
            print(f"Task #{args.id} priority manually set to {args.priority}.")
        else:
            print(f"Task #{args.id} not found or invalid priority.")
    elif args.command == "edit":
        if edit_task(
            store_path,
            args.id,
            title=args.title,
            description=args.description,
            due_date=args.due,
        ):
            print(f"Task #{args.id} updated.")
        else:
            print(f"Task #{args.id} not found.")
    elif args.command == "suggest":
        suggestions = suggest_tasks(store_path, context=args.context)
        print("AI Task Suggestions:\n")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
        print("\nUse 'python main.py add --title \"<suggestion>\"' to add a task.")
    elif args.command == "clear":
        if not args.yes:
            confirm = input("Are you sure you want to delete ALL tasks? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("Clear cancelled.")
                return
        count = clear_tasks(store_path)
        print(f"Cleared {count} task(s).")
    elif args.command == "overview":
        stats = get_overview(store_path)
        print(f"You have {stats['total']} task(s).")
        parts = []
        if stats['high_priority'] > 0:
            parts.append(f"{stats['high_priority']} high priority")
        if stats['overdue'] > 0:
            parts.append(f"{stats['overdue']} overdue")
        if stats['incomplete'] > 0:
            parts.append(f"{stats['incomplete']} incomplete")
        if parts:
            print(", ".join(parts) + ".")
    elif args.command == "options":
        # Rebuild parser to introspect subcommands
        parser2 = build_parser()
        print("Available commands:\n")
        for name, sp in parser2._subparsers._group_actions[0].choices.items():  # type: ignore[attr-defined]
            if name == "add":
                desc = "Add a new task"
            elif name == "list":
                desc = "List tasks (filter/sort)"
            elif name == "complete":
                desc = "Mark a task complete"
            elif name == "delete":
                desc = "Delete a task"
            elif name == "search":
                desc = "Search tasks by text"
            elif name == "prioritize":
                desc = "AI-powered task prioritization"
            elif name == "set-priority":
                desc = "Manually set task priority"
            elif name == "edit":
                desc = "Edit an existing task"
            elif name == "suggest":
                desc = "Get AI task suggestions"
            elif name == "clear":
                desc = "Delete all tasks"
            elif name == "overview":
                desc = "Show task statistics summary"
            elif name == "options":
                desc = "Show this command list"
            else:
                desc = sp.description or "(no description)"
            print(f" - {name}: {desc}")
        print("\nUse 'python main.py <command> --help' for details.")


if __name__ == "__main__":
    main()
