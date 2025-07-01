import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# Configuration
API_BASE_URL = "http://localhost:8000"  # Change this if your FastAPI runs on different host/port

# Page config
st.set_page_config(
    page_title="Task Tracker",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .task-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    background-color: black;
    color: white; /* Optional: ensures text is visible on black background */
    }

    .status-todo {
        color: #ff6b6b;
        font-weight: bold;
    }
    .status-in-progress {
        color: #4ecdc4;
        font-weight: bold;
    }
    .status-done {
        color: #45b7d1;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def make_request(method, endpoint, data=None):
    """Make HTTP request to the API"""
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        elif method == "PATCH":
            response = requests.patch(url, json=data)
        
        if response.status_code == 200 or response.status_code == 201:
            return response.json(), None
        else:
            return None, f"Error {response.status_code}: {response.text}"
    except requests.exceptions.ConnectionError:
        return None, "❌ Cannot connect to API. Make sure the FastAPI server is running on http://localhost:8000"
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def get_status_emoji(status):
    """Get emoji for status"""
    emoji_map = {
        "todo": "📋",
        "in-progress": "⚡",
        "done": "✅"
    }
    return emoji_map.get(status, "📋")

def format_datetime(dt_str):
    """Format datetime string"""
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%m/%d/%Y %I:%M %p")
    except:
        return dt_str

# Main app
def main():
    st.markdown('<h1 class="main-header">📝 Task Tracker</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎯 Actions")
    
    # Add new task
    with st.sidebar.expander("➕ Add New Task", expanded=True):
        new_task_desc = st.text_area("Task Description", placeholder="Enter your task description...")
        if st.button("Add Task", type="primary"):
            if new_task_desc.strip():
                data, error = make_request("POST", "/tasks", {"description": new_task_desc.strip()})
                if data:
                    st.success(f"✅ Task added successfully!")
                    st.rerun()
                else:
                    st.error(error)
            else:
                st.warning("Please enter a task description.")
    
    # Filter options
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filter Tasks")
    status_filter = st.sidebar.selectbox(
        "Filter by Status",
        ["All", "todo", "in-progress", "done"],
        format_func=lambda x: f"All Tasks" if x == "All" else f"{get_status_emoji(x)} {x.replace('-', ' ').title()}"
    )
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh"):
        st.rerun()
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        # Get all tasks for stats
        all_tasks, error = make_request("GET", "/tasks")
        if all_tasks:
            todo_count = len([t for t in all_tasks if t['status'] == 'todo'])
            progress_count = len([t for t in all_tasks if t['status'] == 'in-progress'])
            done_count = len([t for t in all_tasks if t['status'] == 'done'])
            
            st.metric("📋 To Do", todo_count)
            st.metric("⚡ In Progress", progress_count)
            st.metric("✅ Done", done_count)
            st.metric("📈 Total", len(all_tasks))
        else:
            st.error("Could not load task statistics")
    
    with col1:
        st.markdown("### 📋 Task List")
        
        # Get tasks based on filter
        endpoint = "/tasks" if status_filter == "All" else f"/tasks/status/{status_filter}"
        tasks, error = make_request("GET", endpoint)
        
        if error:
            st.error(error)
            return
        
        if not tasks:
            st.info("📭 No tasks found. Add some tasks to get started!")
            return
        
        # Display tasks
        for task in tasks:
            with st.container():
                st.markdown(f"""
                <div class="task-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4>{get_status_emoji(task['status'])} Task #{task['id']}</h4>
                        <span class="status-{task['status']}">{task['status'].replace('-', ' ').upper()}</span>
                    </div>
                    <p><strong>Description:</strong> {task['description']}</p>
                    <p><small>📅 Created: {format_datetime(task['createdAt'])} | 🕒 Updated: {format_datetime(task['updatedAt'])}</small></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col_edit, col_status, col_delete = st.columns([1, 1, 1])
                
                with col_edit:
                    if st.button(f"✏️ Edit", key=f"edit_{task['id']}"):
                        st.session_state[f"editing_{task['id']}"] = True
                
                with col_status:
                    current_status = task['status']
                    status_options = ['todo', 'in-progress', 'done']
                    other_statuses = [s for s in status_options if s != current_status]
                    
                    if other_statuses:
                        new_status = st.selectbox(
                            "Change Status",
                            [""] + other_statuses,
                            key=f"status_{task['id']}",
                            format_func=lambda x: "Select new status..." if x == "" else f"{get_status_emoji(x)} {x.replace('-', ' ').title()}"
                        )
                        
                        if new_status:
                            data, error = make_request("PATCH", f"/tasks/{task['id']}/status", {"status": new_status})
                            if data:
                                st.success(f"Status updated to {new_status}!")
                                st.rerun()
                            else:
                                st.error(error)
                
                with col_delete:
                    if st.button(f"🗑️ Delete", key=f"delete_{task['id']}", type="secondary"):
                        data, error = make_request("DELETE", f"/tasks/{task['id']}")
                        if data:
                            st.success("Task deleted successfully!")
                            st.rerun()
                        else:
                            st.error(error)
                
                # Edit form
                if st.session_state.get(f"editing_{task['id']}", False):
                    with st.form(f"edit_form_{task['id']}"):
                        new_description = st.text_area(
                            "New Description",
                            value=task['description'],
                            key=f"edit_desc_{task['id']}"
                        )
                        col_save, col_cancel = st.columns(2)
                        
                        with col_save:
                            if st.form_submit_button("💾 Save", type="primary"):
                                if new_description.strip():
                                    data, error = make_request("PUT", f"/tasks/{task['id']}", {"description": new_description.strip()})
                                    if data:
                                        st.success("Task updated successfully!")
                                        st.session_state[f"editing_{task['id']}"] = False
                                        st.rerun()
                                    else:
                                        st.error(error)
                                else:
                                    st.warning("Description cannot be empty.")
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Cancel"):
                                st.session_state[f"editing_{task['id']}"] = False
                                st.rerun()
                
                st.markdown("---")
        
        # Export functionality
        st.markdown("### 📤 Export Tasks")
        if st.button("Download as CSV"):
            if tasks:
                df = pd.DataFrame(tasks)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No tasks to export.")

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True

if __name__ == "__main__":
    main()