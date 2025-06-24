# streamlit_student_report.py

import streamlit as st
from dataclasses import dataclass
from typing import Union

# Define dataclass
@dataclass
class Student:
    first_name: str
    roll: int
    math: Union[int, float]
    science: Union[int, float]
    english: Union[int, float]

    def __post_init__(self):
        if not isinstance(self.first_name, str):
            raise TypeError("First name must be a string.")
        if not isinstance(self.roll, int):
            raise TypeError("Roll number must be an integer.")
        if self.roll < 0:
            raise ValueError("Roll number cannot be negative.")
        for subject, mark in {
            "Math": self.math,
            "Science": self.science,
            "English": self.english
        }.items():
            if not isinstance(mark, (int, float)):
                raise TypeError(f"{subject} marks must be a number (int or float).")
            if mark < 0:
                raise ValueError(f"{subject} marks cannot be negative.")

    def total(self):
        return self.math + self.science + self.english

    def average(self):
        return self.total() / 3

    def grade(self):
        avg = self.average()
        if avg >= 90:
            return 'A+'
        elif avg >= 75:
            return 'A'
        elif avg >= 60:
            return 'B'
        elif avg >= 40:
            return 'C'
        else:
            return 'F'

# Streamlit UI
st.set_page_config(page_title="🎓 Student Report Card", layout="centered")
st.title("📋 Student Report Card Generator")

with st.form("student_form"):
    first_name = st.text_input("Student First Name")
    roll = st.number_input("Roll Number", min_value=0, step=1)
    math = st.number_input("Math Marks", min_value=0.0, step=1.0)
    science = st.number_input("Science Marks", min_value=0.0, step=1.0)
    english = st.number_input("English Marks", min_value=0.0, step=1.0)
    
    submitted = st.form_submit_button("Generate Report Card")

if submitted:
    try:
        student = Student(
            first_name=first_name,
            roll=int(roll),
            math=math,
            science=science,
            english=english
        )
        
        st.success(f"✅ Report card for {student.first_name} (Roll #{student.roll})")
        st.write(f"**Total Marks:** {student.total()}")
        st.write(f"**Average Marks:** {student.average():.2f}")
        st.write(f"**Grade:** 🎖️ {student.grade()}")

    except Exception as e:
        st.error(f"❌ Error: {e}")
