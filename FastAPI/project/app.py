# from fastapi import FastAPI
# from pydantic import BaseModel, Field, computed_field
# from fastapi.responses import JSONResponse
# from typing import Literal, Annotated
# import pickle
# import pandas as pd 


# # Import the ml model 
# with open('model.pkl', 'rb') as f:
#     model = pickle.load(f)
    
    
# app = FastAPI()


# tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
# tier_2_cities = [
#     "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
#     "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
#     "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
#     "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
#     "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
#     "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
# ]
    
# # Build a Pydantic model to Validate incoming data 
# class UserInput(BaseModel): 
    
#     age: Annotated[int, Field(..., gt=0, lt=20, description='Age of the User ')]
#     weight: Annotated[float, Field(..., gt=0, description='Weight of the User ')]
#     height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height of the User ')]
#     income_lpa: Annotated[float, Field(..., gt=0, description='Annual salary of the User in lpa ')]
#     somker: Annotated[bool, Field(...,  description='Is user somker ')]
#     city: Annotated[str, Field(...,  description='The city that the User belongs to')]
#     occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
#        'business_owner', 'unemployed', 'private_job'], Field(...,  description='Occupation of the User ')]
    
    
#     @computed_field
#     @property
#     def bmi(self) -> float:
#         return self.weight / (self.height ** 2 )
    
#     @computed_field
#     @property
#     def lifestyle_risk(self) -> str: 
#         if self.somker and self.bmi > 30:
#             return "high"
#         elif self.somker or self.bmi > 27:
#             return "medium"
#         else:
#             return "low"
        
#     @computed_field
#     @property
#     def age_group(self) -> str:
#         if self.age < 25:
#             return "young"
#         elif self.age < 45:
#             return "adult"
#         elif self.age < 60:
#             return "middle_aged"
#         return "senior"
    
    
    
#     @computed_field
#     @property
#     def city_tier(self) -> str:
#         if self.city in tier_1_cities:
#             return 1
#         elif self.city in tier_2_cities:
#             return 2
#         else:
#             return 3
    
# app.post('/predict')
# def predict_premium(data: UserInput):
#     input_df = pd.DataFrame([{
#         'bmi': data.bmi, 
#         'age_group': data.age_group, 
#         'lifestyle_risk': data.lifestyle_risk, 
#         'city_tier': data.city_tier, 
#         'income_lpa': data.income_lpa, 
#         'occupation': data.occupation
#     }])
    
#     prediction = model.predict(input_df)[0]
#     return JSONResponse(status_code=200, content={'predicted_category': prediction})



from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from schema.user_input import UserInput
from model.predict import predict_output, model, MODEL_VERSION
import pickle
import pandas as pd


app = FastAPI()




        
@app.get('/')
def home(): 
    return {'message': "Insurance Premium Prediction API"}

@app.get('/health')
def health_check(): 
    return {
        'status': 'OK', 
        'version': MODEL_VERSION, 
        "model_loaded": model is True
    }

@app.post('/predict')
def predict_premium(data: UserInput):

    user_input = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])

    prediction = predict_output(user_input)

    return JSONResponse(status_code=200, content={'predicted_category': prediction})




