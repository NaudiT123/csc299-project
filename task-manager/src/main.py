import argparse
import json
import os
from pathlib import Path

class TaskManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_data_directory()
        
    def _ensure_data_directory(self):
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        # Create empty JSON file if it doesn't exist
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)

    def add_task(self, title, description):
        tasks = self._load_tasks()
        new_id = len(tasks) + 1
        task = {
            'id': new_id,
            'title': title,
            'description': description
        }
        tasks.append(task)
        self._save_tasks(tasks)
        return task

    def list_tasks(self):
        return self._load_tasks()

    def _load_tasks(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_tasks(self, tasks):
        with open(self.file_path, 'w') as f:
            json.dump(tasks, f, indent=2)

def main():
    # Initialize the task manager
    task_manager = TaskManager('data/tasks.json')

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Task Manager CLI')
    parser.add_argument('--add', nargs=2, metavar=('TITLE', 'DESCRIPTION'), 
                        help='Add a new task with TITLE and DESCRIPTION')
    parser.add_argument('--list', action='store_true', 
                        help='List all existing tasks')

    args = parser.parse_args()

    if args.add:
        title, description = args.add
        task_manager.add_task(title, description)
        print(f'Task added: {title}')
    elif args.list:
        tasks = task_manager.list_tasks()
        if tasks:
            for task in tasks:
                print(f"ID: {task['id']}, Title: {task['title']}, Description: {task['description']}")
        else:
            print('No tasks found.')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()