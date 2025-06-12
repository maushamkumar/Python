import streamlit as st
from datetime import datetime, timedelta
import json
import os
import pandas as pd

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def parse_datetime(dt_str):
    return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')

def export_csv(task_list, filename="tasks_export.csv"):
    df = pd.DataFrame(task_list)
    return df.to_csv(index=False).encode('utf-8')

st.set_page_config(page_title="Task Tracker", page_icon="🗓️")
st.title("🗓️ My Task Tracker")

# Load and save tasks
tasks = load_tasks()

# Add New Task
st.subheader("➕ Add New Task")
task_text = st.text_input("Task Name")
due_date = st.date_input("Due Date", value=datetime.now().date())
due_time = st.time_input("Due Time", value=datetime.now().time())

if st.button("Add Task"):
    if task_text:
        due_datetime = datetime.combine(due_date, due_time)
        new_task = {
            "task": task_text,
            "due": due_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            "done": False
        }
        tasks.append(new_task)
        save_tasks(tasks)
        st.success(f"✅ Task '{task_text}' added.")
        st.rerun()
    else:
        st.warning("⚠️ Task name cannot be empty!")

# Tabs for Due and Done
tab1, tab2 = st.tabs(["📋 Due Tasks", "✅ Done Tasks"])

# ---------------------- DUE TASKS -------------------------
with tab1:
    st.subheader("📋 Your Tasks")

    filter_option = st.radio("Filter by", ["Today", "This Week", "Later", "All"], key="due_filter")

    now = datetime.now()
    end_of_today = now.replace(hour=23, minute=59, second=59)
    end_of_week = now + timedelta(days=7 - now.weekday())

    filtered_tasks = []

    for i, task in enumerate(tasks):
        if task.get("done"):
            continue  # skip done tasks
        due = parse_datetime(task["due"])

        if filter_option == "Today" and due.date() != now.date():
            continue
        elif filter_option == "This Week" and not (now.date() <= due.date() <= end_of_week.date()):
            continue
        elif filter_option == "Later" and due.date() <= end_of_week.date():
            continue
        # Show task
        time_left = due - now
        overdue = time_left.total_seconds() < 0
        status = f"⏳ Due in {str(time_left).split('.')[0]}" if not overdue else "🔴 Overdue!"
        col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
        with col1:
            st.markdown(f"**{task['task']}** — _Due: {due.strftime('%Y-%m-%d %H:%M')} — {status}_")
        with col2:
            if st.button("✅", key=f"done_{i}"):
                tasks[i]["done"] = True
                save_tasks(tasks)
                st.rerun()
        with col3:
            if st.button("❌", key=f"delete_{i}"):
                tasks.pop(i)
                save_tasks(tasks)
                st.rerun()

        filtered_tasks.append(task)

    # Export Button
    if filtered_tasks:
        csv = export_csv(filtered_tasks)
        st.download_button("⬇️ Download Filtered Tasks", csv, file_name="filtered_tasks.csv", mime="text/csv")
    else:
        st.info("No tasks in this filter.")

# ---------------------- DONE TASKS -------------------------
with tab2:
    st.subheader("✅ Completed Tasks")

    done_filter = st.radio("Filter by", ["Today", "This Week", "Later", "All"], key="done_filter")

    now = datetime.now()
    end_of_today = now.replace(hour=23, minute=59, second=59)
    end_of_week = now + timedelta(days=7 - now.weekday())

    filtered_done_tasks = []

    for i, task in enumerate(tasks):
        if not task.get("done"):
            continue

        due = parse_datetime(task["due"])

        if done_filter == "Today" and due.date() != now.date():
            continue
        elif done_filter == "This Week" and not (now.date() <= due.date() <= end_of_week.date()):
            continue
        elif done_filter == "Later" and due.date() <= end_of_week.date():
            continue

        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown(f"✅ **{task['task']}** — _Originally due: {due.strftime('%Y-%m-%d %H:%M')}_")
        with col2:
            if st.button("❌", key=f"delete_done_{i}"):
                tasks.pop(i)
                save_tasks(tasks)
                st.rerun()

        filtered_done_tasks.append(task)

    # if filtered_done_tasks:
    #     csv = export_csv(filtered_done_tasks)
    #     st.download_button("⬇️ Download Filtered Done Tasks", csv, file_name="filtered_done_tasks.csv", mime="text/csv")
    # else:
    #     st.info("No completed tasks in this filter.")
    
    # https://www.linkedin.com/posts/bhavesh-arora-11b0a319b_revise-statistics-for-free-ugcPost-7338774633493536769-f3xY?utm_source=share&utm_medium=member_desktop&rcm=ACoAAFJ90U4Bm95-BFMilqpC56PSWumtYa9vldw
