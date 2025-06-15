import streamlit as st
import os

# Recursive function to explore files/folders
def explore(path, indent=0):
    items = []
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                items.append('  ' * indent + f'📁 {item}/')
                items.extend(explore(item_path, indent + 1))
            else:
                items.append('  ' * indent + f'📄 {item}')
    except Exception as e:
        items.append('  ' * indent + f'❌ Error: {e}')
    return items

# Streamlit UI
st.set_page_config(page_title="Recursive File Explorer", layout="wide")
st.title("📂 Recursive File Explorer")

folder_path = st.text_input("Enter absolute path of folder:")

if folder_path:
    folder_path = folder_path.strip().strip('"')
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        st.success(f"✅ Folder found: {folder_path}")
        structure = explore(folder_path)
        st.code("\n".join(structure), language='text')
    else:
        st.error("❌ Invalid folder path. Please check again.")

# https://www.linkedin.com/posts/bhavesh-arora-11b0a319b_leetcode-sql-solutions-activity-7339869190830333952-BKJq?utm_source=share&utm_medium=member_desktop&rcm=ACoAAFJ90U4Bm95-BFMilqpC56PSWumtYa9vldw