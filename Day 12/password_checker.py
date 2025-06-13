# password_strength_checker.py

import streamlit as st
import re

st.set_page_config(page_title="Password Strength Checker", page_icon="🔐")

st.title("🔐 Password Strength Checker")
st.write("Enter a password to check its strength using Regular Expressions.")

def check_password_strength(password):
    length_error = len(password) < 8
    lowercase_error = re.search(r"[a-z]", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    digit_error = re.search(r"\d", password) is None
    special_char_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None

    errors = {
        "Length (min 8 characters)": length_error,
        "At least one lowercase letter": lowercase_error,
        "At least one uppercase letter": uppercase_error,
        "At least one digit": digit_error,
        "At least one special character": special_char_error
    }

    return errors

def rate_password(password):
    errors = check_password_strength(password)
    failed_checks = sum(errors.values())

    if failed_checks == 0:
        return "Strong 💪", "green"
    elif failed_checks <= 2:
        return "Moderate 😐", "orange"
    else:
        return "Weak ⚠️", "red"

password = st.text_input("Enter your password", type="password")

if password:
    result, color = rate_password(password)
    st.markdown(f"**Password Strength:** <span style='color:{color}'>{result}</span>", unsafe_allow_html=True)

    st.subheader("Checklist")
    checks = check_password_strength(password)
    for check, failed in checks.items():
        if failed:
            st.error(f"❌ {check}")
        else:
            st.success(f"✅ {check}")
