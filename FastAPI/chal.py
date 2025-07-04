from fastapi import FastAPI, Path, HTTPException, Query
import json 
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
from fastapi.responses import JSONResponse

app = FastAPI()

class Patient(BaseModel): 
    id: Annotated[str, Field(..., description="Id of the Patient")]
    name: Annotated[str, Field(..., description="name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient is living ")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient ")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in mtrs")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in Kgs")]
      

    
    @computed_field
    @property
    def bmi(self) -> float: 
        return round(self.weight / (self.height ** 2), 2)
    
    
    @computed_field
    @property
    def verdict(self) -> str: 
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Normal"
        else: 
            return "Obese"
        
class PatientUpdate(BaseModel): 
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

      

def load_data():
    with open('patients.json', 'r') as f: 
       data = json.load(f) 
       
    return data 

def save_data(data): 
    with open('patients.json', 'w') as f: 
        json.dump(data, f)

@app.post('/create')
def create_patient(patient:Patient): 
    # Load the existing data 
    data = load_data()
    
    # Check if the patient already exist 
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exist")
    
    # new patient add to the database 
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    # save into the json file 
    
    save_data(data)
    
    return JSONResponse(status_code=202, content={'message': "Patient created Sucessfully"})


@app.put('/update{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate): 
    
    # First we'll load the data 
    data = load_data()
    
    if patient_id not in data: 
        raise HTTPException(status_code=404, detail="Patient ID not found ")  
    
    existing_patient_info = data[patient_id]
    # We have find new value of city and weight 
    # For this we have patient update currently this is a pydantic object
    # we have convert this into dictonary 
    
    # 1. convert patient object into dictonary 
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    # The motive behind using exclude_unset True is inside the patient_update we all 
    # the data into None which is not provide by user 
    
    for key, value in updated_patient_info.items(): 
        existing_patient_info[key] = value
        
    # existing_patient_info -> Pydantic object -> updated bmi + verdict
    # -> Pydantic object -> dict
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_object.model_dump(exclude='id')
    
    # Add this dict to data   
    data[patient_id] = existing_patient_info
    
    # Save data 
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message': "patient updated"})

@app.delete('/delete{patient_id}')
def delete_patient(patient_id:str):
    data = load_data()
    
    if patient_id not in data: 
        raise HTTPException(status_code=404, detail="Patient ID not found ") 
    
    del data[patient_id]
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message': "Patient delet/"})