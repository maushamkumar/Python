import streamlit as st
import json
import os

TASKS_FILE = "tasks.json"

# --- Load tasks from file ---
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

# --- Save tasks to file ---
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

# --- Initialize session state ---
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

st.title("✅ To-Do List App with JSON Storage")

# --- Add Task ---
new_task = st.text_input("Enter a new task")
if st.button("Add Task"):
    if new_task:
        st.session_state.tasks.append(new_task)
        save_tasks(st.session_state.tasks)
        st.success("Task added!")
        st.rerun()
    else:
        st.warning("Task cannot be empty.")

# --- Show Tasks ---
st.subheader("Your Tasks")
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])

        # Display the task
        with col1:
            st.write(f"{i+1}. {task}")

        # Edit task
        with col2:
            if st.button("✏️ Edit", key=f"edit_{i}"):
                st.session_state.edit_index = i

        # Delete task
        with col3:
            if st.button("❌ Delete", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                save_tasks(st.session_state.tasks)
                st.rerun()
else:
    st.info("No tasks yet. Add one above!")

# --- Edit Section ---
if "edit_index" in st.session_state:
    st.subheader("✍️ Edit Task")
    index = st.session_state.edit_index
    updated_task = st.text_input("Update task:", st.session_state.tasks[index])

    if st.button("Update Task"):
        if updated_task:
            st.session_state.tasks[index] = updated_task
            save_tasks(st.session_state.tasks)
            del st.session_state["edit_index"]
            st.success("Task updated!")
            st.rerun()
        else:
            st.warning("Updated task cannot be empty.")

    if st.button("Cancel Edit"):
        del st.session_state["edit_index"]
