import streamlit as st
from PIL import Image
import os
from io import BytesIO
from zipfile import ZipFile
from process_passport import process_image_to_passport

# Set paths
INPUT_DIR = "input_images"
OUTPUT_DIR = "passport_photos"

# Ensure directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.set_page_config(page_title="Passport Photo Batch Tool", layout="centered")
st.title("🪪 Bulk Passport Photo Generator")

st.markdown("Upload one or more images. The app will:")
st.markdown("- Detect the face")
st.markdown("- Expand to include face, hair & shoulders")
st.markdown("- Apply white background")
st.markdown("- Resize to 600x600 px")
st.markdown("- Compress and save as `.jpg` (≤ 20 KB each)")

uploaded_files = st.file_uploader("Upload multiple photos", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    # Save input files
    saved_paths = []
    for uploaded_file in uploaded_files:
        input_path = os.path.join(INPUT_DIR, uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())
        saved_paths.append(input_path)

    st.info(f"📂 {len(saved_paths)} image(s) uploaded. Starting processing...")

    # Process images
    processed_files = []
    for input_path in saved_paths:
        filename = os.path.basename(input_path)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(OUTPUT_DIR, base_name + ".jpg")

        success = process_image_to_passport(input_path, output_path)
        if success:
            st.success(f"✅ Processed: {filename}")
            processed_files.append(output_path)
        else:
            st.error(f"❌ Failed to process: {filename}")

    # ZIP and download
    if processed_files:
        st.markdown("### 📥 Download All Processed Photos")
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            for file_path in processed_files:
                zip_file.write(file_path, os.path.basename(file_path))
        zip_buffer.seek(0)

        st.download_button(
            label="📦 Download All as ZIP",
            data=zip_buffer,
            file_name="passport_photos.zip",
            mime="application/zip"
        )
