import pickle
import pandas as pd

# import the ml model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

MODEL_VERSION = '1.0.0'

def predict_output(user_input: dict): 
    input_df = pd.DataFrame(user_input)
    
    output = model.predict(input_df)
    
    return output 