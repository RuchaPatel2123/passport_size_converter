
import os
from process_passport import process_image_to_passport

input_dir = "input_images"
output_dir = "passport_photos"
os.makedirs(output_dir, exist_ok=True)

print("=== STARTING PASSPORT IMAGE PROCESSING ===")
files = os.listdir(input_dir)
print(f"Files found in input folder: {files}")

for filename in files:
    print(f"➡️ Checking: {filename}")
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".png")
        success = process_image_to_passport(input_path, output_path)
        if success:
            print(f"✅ Done: {output_path}")
        else:
            print(f"❌ Failed to process: {filename}")
    else:
        print(f"⚠️ Skipped: {filename} (unsupported type)")

print("=== FINISHED ===")
