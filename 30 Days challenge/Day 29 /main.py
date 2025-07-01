#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import json
from dataclasses import dataclass, asdict
from datetime import datetime

# Pydantic models for request/response
class TaskCreate(BaseModel):
    description: str

class TaskUpdate(BaseModel):
    description: str

class TaskStatus(BaseModel):
    status: str

class TaskResponse(BaseModel):
    id: int
    description: str
    status: str
    createdAt: str
    updatedAt: str

@dataclass
class Task:
    id: int
    description: str
    status: str = "todo"
    createdAt: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updatedAt: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class TaskTracker:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.allowed_statuses = ['todo', 'in-progress', 'done']

    def load_data(self) -> List[dict]:
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return []

    def save_data(self, data: List[dict]) -> None:
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

    def get_next_id(self, data: List[dict]) -> int:
        return max((task['id'] for task in data), default=0) + 1

    def add_task(self, description: str) -> dict:
        data = self.load_data()
        task_id = self.get_next_id(data)
        new_task = Task(id=task_id, description=description)
        task_dict = asdict(new_task)
        data.append(task_dict)
        self.save_data(data)
        return task_dict

    def find_task(self, task_id: int) -> Optional[dict]:
        tasks = self.load_data()
        for task in tasks:
            if task['id'] == task_id:
                return task
        return None

    def update_task(self, task_id: int, new_description: str) -> Optional[dict]:
        tasks = self.load_data()
        for task in tasks:
            if task['id'] == task_id:
                task['description'] = new_description
                task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_data(tasks)
                return task
        return None

    def delete_task(self, task_id: int) -> bool:
        tasks = self.load_data()
        updated_tasks = [task for task in tasks if task['id'] != task_id]
        if len(updated_tasks) == len(tasks):
            return False
        self.save_data(updated_tasks)
        return True

    def mark_task(self, task_id: int, status: str) -> Optional[dict]:
        if status not in self.allowed_statuses:
            return None
        
        tasks = self.load_data()
        for task in tasks:
            if task['id'] == task_id:
                task['status'] = status
                task['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_data(tasks)
                return task
        return None

    def list_tasks(self, status_filter: Optional[str] = None) -> List[dict]:
        tasks = self.load_data()
        if status_filter:
            if status_filter not in self.allowed_statuses:
                return []
            tasks = [task for task in tasks if task['status'] == status_filter]
        return tasks

# Initialize FastAPI app and TaskTracker
app = FastAPI(title="Task Tracker API", version="1.0.0")
tracker = TaskTracker()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Task Tracker API is running!"}

@app.post("/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    """Create a new task"""
    new_task = tracker.add_task(task.description)
    return TaskResponse(**new_task)

@app.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(status: Optional[str] = None):
    """Get all tasks, optionally filtered by status"""
    if status and status not in tracker.allowed_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Allowed: {', '.join(tracker.allowed_statuses)}")
    
    tasks = tracker.list_tasks(status)
    return [TaskResponse(**task) for task in tasks]

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    """Get a specific task by ID"""
    task = tracker.find_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(**task)

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    """Update a task's description"""
    updated_task = tracker.update_task(task_id, task_update.description)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(**updated_task)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    """Delete a task"""
    if not tracker.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted successfully"}

@app.patch("/tasks/{task_id}/status", response_model=TaskResponse)
async def update_task_status(task_id: int, status_update: TaskStatus):
    """Update a task's status"""
    updated_task = tracker.mark_task(task_id, status_update.status)
    if not updated_task:
        if status_update.status not in tracker.allowed_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Allowed: {', '.join(tracker.allowed_statuses)}")
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(**updated_task)

@app.get("/tasks/status/{status}", response_model=List[TaskResponse])
async def get_tasks_by_status(status: str):
    """Get tasks filtered by specific status"""
    if status not in tracker.allowed_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Allowed: {', '.join(tracker.allowed_statuses)}")
    
    tasks = tracker.list_tasks(status)
    return [TaskResponse(**task) for task in tasks]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)