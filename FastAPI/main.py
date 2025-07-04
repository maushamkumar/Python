from fastapi import FastAPI, Path, HTTPException, Query
import json 


app = FastAPI()

# First we have define our endpoint 
# To define Endpoint we have create router 
@app.get("/") # This get signify our request will be a get request 
# If you want to fetch data from server then we use get 
# When we want to send data then we use post 
def hello():
    return {'message': 'Patient Management system API '}

@app.get('/about')
def about():
    return {'key': "A Fully function API to manage your patient records"}

# We have to create a endpoint view 
# What ever patient we have we gonna send it to the patient 
# Before create this endpoint we have create another function to load 
# The data form patient.josn 
def load_data():
    with open('patients.json', 'r') as f: 
       data = json.load(f) 
       
    return data 

@app.get('/view')
def view(): 
    # Any request comes inside this route first we'll fetch the data 
    data = load_data()
    return data 

# IF you want you can load the data of specific patient 
# If you want you can sort data based on parameter 
@app.get('/Patient/{patient_id}')
def patient(patient_id:str = Path(..., description="ID of the patient in the DB", example='P001')): 
    data = load_data()
    # for i in data: 
    #     if i == patient_id:
    #         return data[i]
    # else: 
    #     return "Error aa raha h "
    if patient_id in data: 
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patient(sort_by:str=Query(..., description="Sort on the basis of height, weight or EMI"), order: str=Query('asc', description="Sort in asc or desc order")): 
    
    valid_fields = ['height', 'weight', 'bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f"Invalid field select from {valid_fields}")
    
    
    if order not in ['asc', 'desc']: 
        raise HTTPException(status_code=400, detail="Invalid Order select between asc or desc ")
    
    data = load_data()
    
    sort_order = True if order == 'desc' else False
    
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    
    return sorted_data