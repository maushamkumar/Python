from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, validator
from kuch import TaskTracker
from typing import Optional
from datetime import datetime


app = FastAPI()

task = TaskTracker()

@app.get('/')
def home():
    return "Chalo Ajj ka kamm pure siddat ke sath suru karte h"

# class status(BaseModel):
#     todo = 'todo'
#     progress='in-progress' 
#     done='done'
    
    
class TaskCreate(BaseModel):
    task_name: str
    task_description : str
    

class Task(BaseModel):
    id: int
    task_name: str 
    description: str
    status: str
    created_time: str
    updated_time: str
    
    @validator("status")
    def check_status(cls, v):
        allowed = {'todo', 'in-progress', 'done'}
        if v not in allowed:
            raise ValueError(f"status must be one of: {', '.join(allowed)}")
        return v
    


@app.post('/task')
def add_task(task_input: TaskCreate):
    data = task.load_data()
    next_id = task.get_next_id(data)
    
    new_task = Task(
        id=next_id,
        task_name=task_input.task_name,
        description=task_input.task_description,
        status="todo",
        created_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        updated_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    
    data.append(new_task.dict())
    task.save_data(data)
    return {"data": new_task}

def find_task(id):
    data = task.load_data()
    for p in data:
        if p['id'] == id:
            return p

@app.get('/task/{id}')
def get_task_by_id(id:int):
    task = find_task(id)
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task with {id} not found")
    return {'task': task}
    
    
class UpdateTask(BaseModel):
    update_status:str
    description: str
    @validator("update_status")
    def check_status(cls, v):
        allowed = {'todo', 'in-progress', 'done'}
        if v not in allowed:
            raise ValueError(f"status must be one of: {', '.join(allowed)}")
        return v
        

def find_task_index(id):
    data = task.load_data()
    for i, p in enumerate(data):
        if p['id'] == id:
            return i 

@app.put('/task/{id}')
def update_task(id:int, update_task: UpdateTask):
    data = task.load_data()
    index = find_task_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post with id {id} not found")
    
    # Update the task
    task_to_update = data[index]
    task_to_update.update(update_task.dict())
    task_to_update['updated_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save changes
    task.save_data(data)
    return {"data": task_to_update}