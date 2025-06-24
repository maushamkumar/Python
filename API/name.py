from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()


task_db = []

# To add a task we need to create or send a task 
# To get all task, we don't need to send anything

class TaskCreater(BaseModel):
    title: str
    description: str
    owner: str
    date: str
    priority: int
    status: str
    task_id: int
    
    
class TaskResponse(TaskCreater):
    id: int
    is_completed: bool = False
    
@app.get("/")
def home():
    return {"message": "Welcome to the Task Management API"}
    
@app.post("/addtask/", response_model=TaskResponse)
def add_task(task: TaskCreater):
    task_dict = task.dict()
    task_dict["id"] = len(task_db) + 1  
    task_dict["is_completed"] = False
    task_db.append(task_dict)
    return task_dict

@app.get("/gettask/")
def get_task():
    if not task_db:
        raise HTTPException(status_code=404, detail="No tasks found")
    return task_db

@app.get("gettask/{owner}")
def get_task(owner:str):
    tasks = [task for task in task_db if task["owner"] == owner]
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this owner")
    return tasks

@app.put('/completetask/{task_id}')
def complete_task(task_id: int):
    for task in task_db:
        if task["id"] == task_id:
            task["is_completed"] = True
            return {"message": "Task completed successfully"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete('/deletetask/{task_id}')
def delete_task(task_id: int):
    global task_db
    task_db = [task for task in task_db if task["id"] != task_id]
    return {"message": "Task deleted successfully"}