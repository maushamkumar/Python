import streamlit as st
from PIL import Image
import os
import threading
import io
import time

# Output folder
output_dir = "resized_images"
os.makedirs(output_dir, exist_ok=True)

# Function to resize and save image
class ResizeThread(threading.Thread):
    def __init__(self, image_data, filename, size, status_dict):
        super().__init__()
        self.image_data = image_data
        self.filename = filename
        self.size = size
        self.status_dict = status_dict

    def run(self):
        try:
            img = Image.open(self.image_data)
            img = img.resize(self.size)
            save_path = os.path.join(output_dir, self.filename)
            img.save(save_path)
            self.status_dict[self.filename] = "✅ Done"
        except Exception as e:
            self.status_dict[self.filename] = f"❌ Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Multithreaded Image Resizer")
st.title("🖼️ Multithreaded Image Resizer")
st.markdown("Upload multiple images and resize them in parallel using threads.")

# Upload files
uploaded_files = st.file_uploader("📤 Upload Images (PNG/JPG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

# Size input
col1, col2 = st.columns(2)
with col1:
    width = st.number_input("📏 Width", min_value=50, max_value=2000, value=200)
with col2:
    height = st.number_input("📐 Height", min_value=50, max_value=2000, value=200)

resize_button = st.button("🚀 Resize Images")

# When button clicked
if resize_button and uploaded_files:
    st.info("⏳ Starting resize with threads...")

    status = {}
    threads = []

    # Start threads
    for uploaded_file in uploaded_files:
        status[uploaded_file.name] = "⏳ Processing..."
        thread = ResizeThread(
            image_data=io.BytesIO(uploaded_file.read()),
            filename=uploaded_file.name,
            size=(width, height),
            status_dict=status
        )
        thread.start()
        threads.append(thread)

    # Progress tracking
    progress_bar = st.progress(0)
    while any(t.is_alive() for t in threads):
        completed = sum(1 for f in status if status[f] != "⏳ Processing...")
        percent = completed / len(uploaded_files)
        progress_bar.progress(percent)
        time.sleep(0.2)

    # Join threads
    for t in threads:
        t.join()
    progress_bar.progress(1.0)

    # Show final status
    st.success("🎉 All images resized!")
    for file, stat in status.items():
        st.write(f"🗂️ {file}: {stat}")

    # Preview resized images
    st.subheader("📂 Preview Resized Images:")
    for file in os.listdir(output_dir):
        st.image(os.path.join(output_dir, file), caption=file, width=200)


