# streamlit_app.py - Streamlit Authentication Frontend
import streamlit as st
import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Initialize session state
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def login_user(username, password):
    """Login user and store token"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            token_data = response.json()
            st.session_state.access_token = token_data["access_token"]
            return True, "Login successful!"
        else:
            return False, "Invalid username or password"
    except requests.exceptions.RequestException:
        return False, "Could not connect to authentication server"

def register_user(username, password, email):
    """Register a new user"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/register",
            json={"username": username, "password": password, "email": email}
        )
        if response.status_code == 200:
            return True, "Registration successful! Please login."
        else:
            error_data = response.json()
            return False, error_data.get("detail", "Registration failed")
    except requests.exceptions.RequestException:
        return False, "Could not connect to authentication server"

def get_user_info():
    """Get current user information"""
    if not st.session_state.access_token:
        return None
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        response = requests.get(f"{API_BASE_URL}/me", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            # Token might be expired
            st.session_state.access_token = None
            st.session_state.user_info = None
            return None
    except requests.exceptions.RequestException:
        return None

def access_protected_route():
    """Access a protected route"""
    if not st.session_state.access_token:
        return None
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        response = requests.get(f"{API_BASE_URL}/protected", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Access denied"}
    except requests.exceptions.RequestException:
        return {"error": "Could not connect to server"}

def logout():
    """Logout user"""
    st.session_state.access_token = None
    st.session_state.user_info = None
    st.rerun()

# Main App
def main():
    st.set_page_config(page_title="Authentication System", page_icon="🔐")
    
    st.title("🔐 Authentication System")
    st.markdown("---")
    
    # Check if user is logged in
    if st.session_state.access_token:
        # User is logged in - show dashboard
        if st.session_state.user_info is None:
            st.session_state.user_info = get_user_info()
        
        if st.session_state.user_info:
            st.success(f"Welcome, {st.session_state.user_info['username']}!")
            
            # Sidebar with user info
            with st.sidebar:
                st.header("User Profile")
                st.write(f"**Username:** {st.session_state.user_info['username']}")
                st.write(f"**Email:** {st.session_state.user_info.get('email', 'Not provided')}")
                st.write(f"**User ID:** {st.session_state.user_info['id']}")
                
                if st.button("Logout", type="primary", use_container_width=True):
                    logout()
            
            # Main dashboard content
            tab1, tab2, tab3 = st.tabs(["Dashboard", "Protected Content", "Settings"])
            
            with tab1:
                st.header("Dashboard")
                st.write("You are successfully logged in!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("User ID", st.session_state.user_info['id'])
                with col2:
                    st.metric("Username", st.session_state.user_info['username'])
                with col3:
                    st.metric("Status", "Active", delta="Online")
                
                # Show current time
                st.info(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            with tab2:
                st.header("Protected Content")
                st.write("This content is only accessible to authenticated users.")
                
                if st.button("Access Protected Route"):
                    with st.spinner("Accessing protected content..."):
                        protected_data = access_protected_route()
                        if protected_data and "error" not in protected_data:
                            st.success(protected_data["message"])
                        else:
                            st.error(protected_data.get("error", "Access denied"))
                
                # Sample protected content
                with st.expander("View Protected Data"):
                    st.json({
                        "user_data": st.session_state.user_info,
                        "access_level": "authenticated",
                        "permissions": ["read", "write", "delete"]
                    })
            
            with tab3:
                st.header("Settings")
                st.write("User settings and preferences")
                
                # Placeholder for settings
                theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
                notifications = st.checkbox("Enable notifications", value=True)
                
                if st.button("Save Settings"):
                    st.success("Settings saved successfully!")
        
        else:
            st.error("Failed to load user information. Please login again.")
            if st.button("Logout"):
                logout()
    
    else:
        # User is not logged in - show login/register forms
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.header("Login")
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", type="primary", use_container_width=True)
                
                if submit:
                    if username and password:
                        with st.spinner("Logging in..."):
                            success, message = login_user(username, password)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                    else:
                        st.error("Please enter both username and password")
            
            # Demo credentials info
            with st.expander("Demo Credentials"):
                st.info("""
                **Default Admin Account:**
                - Username: `admin`
                - Password: `admin123`
                """)
        
        with tab2:
            st.header("Register")
            with st.form("register_form"):
                new_username = st.text_input("Username", key="reg_username")
                new_email = st.text_input("Email (optional)", key="reg_email")
                new_password = st.text_input("Password", type="password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
                register_submit = st.form_submit_button("Register", type="secondary", use_container_width=True)
                
                if register_submit:
                    if new_username and new_password:
                        if new_password == confirm_password:
                            with st.spinner("Creating account..."):
                                success, message = register_user(new_username, new_password, new_email)
                                if success:
                                    st.success(message)
                                    st.info("Please switch to the Login tab to sign in.")
                                else:
                                    st.error(message)
                        else:
                            st.error("Passwords do not match")
                    else:
                        st.error("Please enter username and password")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>Authentication System built with FastAPI and Streamlit</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()