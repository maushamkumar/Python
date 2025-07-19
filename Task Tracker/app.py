#!/usr/bin/env python3
import os
import json
import sys
from datetime import datetime

class TaskTracker:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.allowed_statuses = ['todo', 'in-progress', 'done']
    
    def load_data(self):
        """Load tasks from JSON file"""
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
    
    def save_data(self, data):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_next_id(self, data):
        """Get the next available ID"""
        if not data:
            return 1
        return max(task['id'] for task in data) + 1
    
    def add_task(self, description):
        """Add a new task"""
        data = self.load_data()
        task_id = self.get_next_id(data)
        
        new_task = {
            "id": task_id,
            "description": description,
            "status": "todo",
            "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        data.append(new_task)
        self.save_data(data)
        print(f"Task added successfully (ID: {task_id})")
    
    def update_task(self, task_id, new_description):
        """Update task description"""
        data = self.load_data()
        
        for task in data:
            if task['id'] == task_id:
                task['description'] = new_description
                task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_data(data)
                print(f"Task {task_id} updated successfully")
                return
        
        print(f"Task with ID {task_id} not found")
    
    def delete_task(self, task_id):
        """Delete a task by ID"""
        data = self.load_data()
        original_length = len(data)
        
        data = [task for task in data if task['id'] != task_id]
        
        if len(data) < original_length:
            self.save_data(data)
            print(f"Task {task_id} deleted successfully")
        else:
            print(f"Task with ID {task_id} not found")
    
    def mark_task(self, task_id, status):
        """Mark task with a specific status"""
        if status not in self.allowed_statuses:
            print(f"Invalid status. Allowed statuses: {', '.join(self.allowed_statuses)}")
            return
        
        data = self.load_data()
        
        for task in data:
            if task['id'] == task_id:
                task['status'] = status
                task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_data(data)
                print(f"Task {task_id} marked as {status}")
                return
        
        print(f"Task with ID {task_id} not found")
    
    def list_tasks(self, status_filter=None):
        """List tasks, optionally filtered by status"""
        data = self.load_data()
        
        if not data:
            print("No tasks found")
            return
        
        filtered_tasks = data
        if status_filter:
            if status_filter not in self.allowed_statuses:
                print(f"Invalid status filter. Allowed: {', '.join(self.allowed_statuses)}")
                return
            filtered_tasks = [task for task in data if task['status'] == status_filter]
        
        if not filtered_tasks:
            status_msg = f" with status '{status_filter}'" if status_filter else ""
            print(f"No tasks found{status_msg}")
            return
        
        print(f"\n{'='*50}")
        print(f"TASKS{' (' + status_filter.upper() + ')' if status_filter else ''}")
        print(f"{'='*50}")
        
        for task in filtered_tasks:
            print(f"ID: {task['id']}")
            print(f"Description: {task['description']}")
            print(f"Status: {task['status']}")
            print(f"Created: {task['createdAt']}")
            print(f"Updated: {task['updatedAt']}")
            print("-" * 30)
    
    def show_usage(self):
        """Show usage instructions"""
        usage = """
Task Tracker CLI

Usage:
    python app.py add "Task description"
    python app.py update <id> "New description"
    python app.py delete <id>
    python app.py mark-in-progress <id>
    python app.py mark-done <id>
    python app.py list [status]

Examples:
    python app.py add "Buy groceries"
    python app.py update 1 "Buy groceries and cook dinner"
    python app.py delete 1
    python app.py mark-in-progress 1
    python app.py mark-done 1
    python app.py list
    python app.py list done
    python app.py list todo
    python app.py list in-progress
        """
        print(usage)

def main():
    tracker = TaskTracker()
    
    if len(sys.argv) < 2:
        tracker.show_usage()
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("Error: Please provide a task description")
                return
            description = " ".join(sys.argv[2:])
            tracker.add_task(description)
        
        elif command == "update":
            if len(sys.argv) < 4:
                print("Error: Please provide task ID and new description")
                return
            task_id = int(sys.argv[2])
            new_description = " ".join(sys.argv[3:])
            tracker.update_task(task_id, new_description)
        
        elif command == "delete":
            if len(sys.argv) < 3:
                print("Error: Please provide task ID")
                return
            task_id = int(sys.argv[2])
            tracker.delete_task(task_id)
        
        elif command == "mark-in-progress":
            if len(sys.argv) < 3:
                print("Error: Please provide task ID")
                return
            task_id = int(sys.argv[2])
            tracker.mark_task(task_id, "in-progress")
        
        elif command == "mark-done":
            if len(sys.argv) < 3:
                print("Error: Please provide task ID")
                return
            task_id = int(sys.argv[2])
            tracker.mark_task(task_id, "done")
        
        elif command == "list":
            status_filter = sys.argv[2] if len(sys.argv) > 2 else None
            tracker.list_tasks(status_filter)
        
        else:
            print(f"Unknown command: {command}")
            tracker.show_usage()
    
    except ValueError as e:
        print(f"Error: Invalid task ID. Please provide a valid number.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    