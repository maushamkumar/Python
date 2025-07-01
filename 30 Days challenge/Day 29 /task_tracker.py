#!/usr/bin/env python3
import os
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional

@dataclass
class Task:
    id: int
    description: str
    status: str = "todo"
    createdAt: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updatedAt: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class TaskTracker:
    """
    Initialize the TaskTracker
    
    Args: 
        filename (str, optional): The name of the JSON file used to store tasks. 
        Default to tasks.json
        
    Attributes:
        filename(str): Path to the JSON file used for storing task data. 
        allowed_status(List[str]): valid statuses for a task 

    """
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.allowed_statuses = ['todo', 'in-progress', 'done']
        

    def load_data(self) -> List[dict]:
        """
        Load the data from JSON File
        
        Returns: 
            List[dict]: A list of task dictionaries loaded from the file
        """
        
        # Check if the file exists
        if not os.path.exists(self.filename):
            return []
        
        # Open the file and return the parsed data
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []


    def save_data(self, data: List[dict]) -> None:
        """
        Save task to JSON file 
        
        Args: 
            data (List[dict]): A list of task dictionaries to be saved.
        
        Returns: 
            None 
        """
        # Open the file and write the data with indentation. 
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

    def get_next_id(self, data: List[dict]) -> int:
        """
        Get the next available ID
        
        Args: 
            data (List[dict]): A list of task dictionaries.
            
        Returns:
            Int: The next available ID (One higher than current maximum)
        """
        
        return max((task['id'] for task in data), default=0) + 1
    

    def add_task(self, description: str) -> None:
        """
        Add a new task to the tracker
        
        Args: 
            description (str): Description of the task.
            
        Returns: 
            None
        """
        
        
        # Loading the task
        data = self.load_data()
        
        # Generate a new unique ID
        task_id = self.get_next_id(data)
        
        # Create the new task instance 
        new_task = Task(id=task_id, description=description)
        
        # Add new task to existing data 
        data.append(asdict(new_task))
        
        # Save Updated task
        self.save_data(data)
        print(f"\n✅ Task added successfully:\n{json.dumps(asdict(new_task), indent=2)}")
        

    def find_task(self, task_id: int) -> Optional[dict]:
        """
        Find a task in the tracker by its ID.
        
        Args: 
            task_id (int): The ID of the task to find.
            
        Returns: 
            dict | None: The task data found, otherwise None. 
        """
        
        # Load existing task
        tasks = self.load_data()
        
        # search for the task with the provided ID. 
        for task in tasks:
            if task['id'] == task_id:
                return task
        return None
    

    def update_task(self, task_id: int, new_description: str) -> None:
        """
        Update a task's description by its ID.
        
        Args: 
            task_id (int): The ID of the task to update.
            new_description(str): The new description for the task. 
            
        Returns: 
            None
        """
        
        # loding the task
        tasks = self.load_data()
        
        # Search for task and update its description & time
        for task in tasks:
            if task['id'] == task_id:
                task['description'] = new_description
                task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_data(tasks)
                print(f"✏️ Task {task_id} updated successfully.")
                return
        print(f"Task with ID {task_id} not found.")


    def delete_task(self, task_id: int) -> None:
        """
        Delete a task's by it ID. 
        
        Args: 
            task_id (int): The ID of the task to delete. 
            
        Returns: 
            None. 
        """
        
        # load the task
        tasks = self.load_data()
        
        # Filter out the task to be deleted.
        updated_tasks = [task for task in tasks if task['id'] != task_id]
        
        # Save updated list if deletion happened.
        if len(updated_tasks) == len(tasks):
            print(f"Task with ID {task_id} not found.")
        else:
            self.save_data(updated_tasks)
            print(f"🗑️ Task {task_id} deleted successfully.")
            

    def mark_task(self, task_id: int, status: str) -> None:
        """
        Mark a task with a new status.

        Args:
            task_id (int): The ID of the task to update.
            status (str): The new status to assign to the task.

        Returns:
            None
        """
        
        # Validate the status
        if status not in self.allowed_statuses:
            print(f"Invalid status. Allowed: {', '.join(self.allowed_statuses)}")
            return
        
        # Search and update task
        tasks = self.load_data()
        for task in tasks:
            if task['id'] == task_id:
                task['status'] = status
                task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_data(tasks)
                print(f"✅ Task {task_id} marked as '{status}'.")
                return
        # If no task matched
        print(f"Task with ID {task_id} not found.")
        

    def list_tasks(self, status_filter: Optional[str] = None) -> None:
        """
        List all tasks, optionally filtered by status.

        Args:
            status_filter (Optional[str]): A status to filter tasks by.
                                        Must be one of: 'todo', 'in-progress', 'done'.

        Returns:
            None
        """
        
        # Load all tasks
        tasks = self.load_data()
        if not tasks:
            print("📭 No tasks found.")
            return

        # Filter tasks by status if filter is provided
        if status_filter:
            if status_filter not in self.allowed_statuses:
                print(f"Invalid status filter. Allowed: {', '.join(self.allowed_statuses)}")
                return
            tasks = [task for task in tasks if task['status'] == status_filter]

        # Check again if filtered list is empty
        if not tasks:
            print(f"📭 No tasks found with status '{status_filter}'.")
            return

        # Display tasks
        print(f"\n{'='*50}")
        print(f"TASK LIST{' - ' + status_filter.upper() if status_filter else ''}")
        print(f"{'='*50}")
        for task in tasks:
            print(f"🆔 ID: {task['id']}")
            print(f"📝 Description: {task['description']}")
            print(f"📌 Status: {task['status']}")
            print(f"📅 Created: {task['createdAt']}")
            print(f"🕒 Updated: {task['updatedAt']}")
            print("-" * 30)

    def show_usage(self):
        """
        Display the usage instructions for the Task Tracker CLI.
        """
        print("""
    📘 Task Tracker CLI

    Usage:
        python task_tracker.py add "Task description"
        python task_tracker.py update <id> "New description"
        python task_tracker.py delete <id>
        python task_tracker.py mark-in-progress <id>
        python task_tracker.py mark-done <id>
        python task_tracker.py list [status]

    Examples:
        python task_tracker.py add "Finish project"
        python task_tracker.py update 1 "Refactor code"
        python task_tracker.py delete 1
        python task_tracker.py mark-in-progress 1
        python task_tracker.py mark-done 1
        python task_tracker.py list
        python task_tracker.py list done
    """)


def main():
    """
    Main function to parse CLI arguments and call TaskTracker methods.
    """
    tracker = TaskTracker()

    # If no command is passed
    if len(sys.argv) < 2:
        tracker.show_usage()
        return

    command = sys.argv[1].lower()

    try:
        # Add a new task
        if command == "add":
            if len(sys.argv) < 3:
                print("❗ Please provide a task description.")
                return
            description = " ".join(sys.argv[2:])
            tracker.add_task(description)

        # Update existing task
        elif command == "update":
            if len(sys.argv) < 4:
                print("❗ Please provide task ID and new description.")
                return
            task_id = int(sys.argv[2])
            new_description = " ".join(sys.argv[3:])
            tracker.update_task(task_id, new_description)

        # Delete task
        elif command == "delete":
            if len(sys.argv) < 3:
                print("❗ Please provide task ID.")
                return
            tracker.delete_task(int(sys.argv[2]))

        # Mark task as in-progress
        elif command == "mark-in-progress":
            if len(sys.argv) < 3:
                print("❗ Please provide task ID.")
                return
            tracker.mark_task(int(sys.argv[2]), "in-progress")

        # Mark task as done
        elif command == "mark-done":
            if len(sys.argv) < 3:
                print("❗ Please provide task ID.")
                return
            tracker.mark_task(int(sys.argv[2]), "done")

        # List tasks (optionally filtered by status)
        elif command == "list":
            status = sys.argv[2] if len(sys.argv) > 2 else None
            tracker.list_tasks(status)

        # Unknown command
        else:
            print(f"❌ Unknown command: '{command}'")
            tracker.show_usage()

    except ValueError:
        print("❌ Invalid ID. Please enter a numeric task ID.")
    except Exception as e:
        print(f"❗ Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
