import os
from process_passport import process_image_to_passport

input_dir = "input_images"
output_dir = "passport_photos"
os.makedirs(output_dir, exist_ok=True)

print("=== STARTING PASSPORT IMAGE PROCESSING ===")
files = os.listdir(input_dir)

for filename in files:
    print(f"➡️ Checking: {filename}")
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        input_path = os.path.join(input_dir, filename)

        # Keep original filename, change extension to .jpg
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.jpg")

        success = process_image_to_passport(input_path, output_path)
        if success:
            print(f"✅ Done: {output_path}")
        else:
            print(f"❌ Failed to process: {filename}")
    else:
        print(f"⚠️ Skipped: {filename} (unsupported type)")

print("=== FINISHED ===")