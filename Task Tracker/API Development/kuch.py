import os 
import json 
from datetime import datetime
# Let's i have look for a file name task.json 
# How i gonna find it out. 
# FILE_NAME = "task.json"
# if not os.path.isfile(FILE_NAME):
#     with open(FILE_NAME, 'w') as f:
#         f.close()
#         print(f"A file {FILE_NAME} created")
    
    
# def load_data(FILE_NAME):
#     if not os.path.exists(FILE_NAME):
#         return []
    
#     try: 
#         with open(FILE_NAME, 'r') as f:
#             json.load(f)
#     except (json.JSONDecoder, ValueError):
#         return []

class TaskTracker:
    def __init__(self, filename="task.json"):
        self.filename = filename
        self.allowed_statuses = ['todo', 'in-progress', 'done']
        
    def load_data(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)
            return []
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []
        
    def save_data(self, data ):
        """
        Save task to JSON file
        """
        with open (self.filename, 'w') as f:
            json.dump(data, f, indent=2)
            
    def get_next_id(self, data):
        """
        Get the next id for your task
        """
        if not data:
            return 1
        return max(task['id'] for task in data) + 1
    
    def add_task(self, task_name, task_description):
        """
        Add a new task
        """
        data = self.load_data()
        next_id = self.get_next_id(data)
        
        task = {
            'id': next_id, 
            'task_name': task_name, 
            'description': task_description, 
            'status': 'todo',
            'created_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'update_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        data.append(task)
        self.save_data(data)
        print(f"Task added successfully (ID: {next_id})")
        
    def update_task(self, task_id, new_description):
        """
        Update the Task based on ID 
        """
        data = self.load_data()
        
        for task in data:
            if task['id'] == task_id:
                task['description'] = new_description
                task['update_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_data(data)
                print(f"Task {task_id} updated successfully")
                return
        
        print(f"Task with ID {task_id} not found")
        
    def delete_task(self, task_id):
        """
        Delete a Task 
        """
        data = self.load_data()
        original_length = len(data)
        
        data = [task for task in data if task['id'] != task_id]
        if len(data) < original_length:
            self.save_data(data)
            print(f"Task {task_id} deleted successfully")
        else:
            print(f"Task with ID {task_id} not found")
            
    def mark_task(self, task_id, status):
        """
        Change the status of your task 
        """
        data = self.load_data()
        if status not in self.allowed_statuses:
            print(f"Invalid allowed statuses {', '.join(self.allowed_statuses)}")
            return
        
        for task in data:
            if task['id'] == task_id:
                task['status'] = status
                task['update_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
            
            
        
