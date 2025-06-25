import streamlit as st
from pydantic import BaseModel, EmailStr, AnyUrl, Field, ValidationError
from typing import List, Dict, Optional, Annotated

# ---------------------------
# 🧬 Define the Pydantic Model
# ---------------------------
class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Mausham', 'Sona'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]

# ------------------------
# 🧠 Define the update logic
# ------------------------
def update_patient_data(patient: Patient):
    st.success("✅ Patient data updated successfully!")
    st.write("**Name:**", patient.name)
    st.write("**Age:**", patient.age)
    st.write("**Allergies:**", patient.allergies)
    st.write("**Married:**", patient.married)
    st.write("**Contact Details:**", patient.contact_details)
    st.write("**Status:** updated")


# ------------------------
# 🖥️ Streamlit Form UI
# ------------------------
st.title("🧑‍⚕️ Patient Registration Form")

with st.form("patient_form"):
    name = st.text_input("Name", max_chars=50)
    email = st.text_input("Email")
    linkedin_url = st.text_input("LinkedIn URL")
    age = st.number_input("Age", min_value=1, max_value=119, step=1)
    weight = st.number_input("Weight (kg)", min_value=1.0)
    married = st.radio("Married?", options=[True, False], index=0)
    
    allergies = st.multiselect("Allergies (max 5)", options=['Dust', 'Pollen', 'Gluten', 'Lactose', 'Nuts', 'Seafood'])
    if len(allergies) > 5:
        st.warning("You can select at most 5 allergies.")

    phone = st.text_input("Phone Number")

    submitted = st.form_submit_button("Submit")

    if submitted:
        try:
            patient_data = {
                "name": name,
                "email": email,
                "linkedin_url": linkedin_url,
                "age": age,
                "weight": weight,
                "married": married,
                "allergies": allergies if allergies else None,
                "contact_details": {"phone": phone}
            }

            patient = Patient(**patient_data)
            update_patient_data(patient)

        except ValidationError as e:
            st.error("❌ Validation Error:")
            st.json(e.errors())
