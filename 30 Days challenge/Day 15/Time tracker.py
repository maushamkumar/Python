import streamlit as st
import time

# Decorator to measure execution time
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        st.success(f"⏱️ Function '{func.__name__}' took {end - start:.4f} seconds")
        return result
    return wrapper

# Functions to decorate
@timer
def slow_function():
    time.sleep(2)
    st.write("✅ Slow function completed!")

@timer
def add_numbers(a, b):
    time.sleep(1)
    result = a + b
    st.write(f"✅ Result: {a} + {b} = {result}")
    return result

@timer
def Multi(a, b):
    time.sleep(1)
    result = a * b
    st.write(f"✅ Result: {a} * {b} = {result}")
    return result

# Streamlit UI
st.title("⏱️ Decorator Demo: Execution Time Tracker")
st.write("This app shows how decorators can be used to measure the execution time of functions.")

task = st.selectbox("Choose a task to run", ["Select", "Slow Function", "Add Numbers", "Multi"])

if task == "Slow Function":
    if st.button("Run Slow Function"):
        slow_function()

elif task == "Add Numbers":
    a = st.number_input("Enter first number", value=0)
    b = st.number_input("Enter second number", value=0)
    if st.button("Add Numbers"):
        add_numbers(a, b)
        
elif task == "Multi":
    a = st.number_input("Enter first number", value=0)
    b = st.number_input("Enter second number", value=0)
    if st.button("Multi"):
        Multi(a, b)
