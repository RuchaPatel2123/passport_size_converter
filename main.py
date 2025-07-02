# import os
# from process_passport import process_image_to_passport

# input_dir = "input_images"
# output_dir = "passport_photos"
# os.makedirs(output_dir, exist_ok=True)

# print("=== STARTING PASSPORT IMAGE PROCESSING ===")
# files = os.listdir(input_dir)

# for filename in files:
#     print(f"➡️ Checking: {filename}")
#     if filename.lower().endswith((".jpg", ".jpeg", ".png")):
#         input_path = os.path.join(input_dir, filename)

#         # Keep original filename, change extension to .jpg
#         base_name = os.path.splitext(filename)[0]
#         output_path = os.path.join(output_dir, f"{base_name}.jpg")

#         success = process_image_to_passport(input_path, output_path)
#         if success:
#             print(f"✅ Done: {output_path}")
#         else:
#             print(f"❌ Failed to process: {filename}")
#     else:
#         print(f"⚠️ Skipped: {filename} (unsupported type)")

# print("=== FINISHED ===")

import os
from process_passport import process_image_to_passport
from zipfile import ZipFile
import math
import logging

# Setup logger
logging.basicConfig(
    filename="passport_batch.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

input_dir = "input_images"
output_dir = "passport_photos"
output_zip = "passport_photos.zip"
batch_size = 10

os.makedirs(output_dir, exist_ok=True)

# Get all image files
all_files = [
    f for f in os.listdir(input_dir)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

print("=== STARTING BATCH PASSPORT IMAGE PROCESSING ===")
logger.info("Starting batch passport image processing")
print(f"Total files: {len(all_files)}")
logger.info(f"Total files: {len(all_files)}")

# Process in batches
total_batches = math.ceil(len(all_files) / batch_size)

for i in range(total_batches):
    start = i * batch_size
    end = min(start + batch_size, len(all_files))
    batch_files = all_files[start:end]
    print(f"\n📦 Batch {i+1}/{total_batches} (files {start+1} to {end})")
    logger.info(f"Batch {i+1}/{total_batches} (files {start+1} to {end})")

    for filename in batch_files:
        input_path = os.path.join(input_dir, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(output_dir, base_name + ".jpg")

        try:
            success = process_image_to_passport(input_path, output_path)
            if success:
                print(f"✅ Done: {filename}")
                logger.info(f"Done: {filename}")
            else:
                print(f"❌ Failed: {filename}")
                logger.error(f"Failed: {filename}")
        except Exception as e:
            print(f"❌ Exception for {filename}: {e}")
            logger.exception(f"Exception for {filename}")

print("\n📁 All batches processed. Creating ZIP...")
logger.info("All batches processed. Creating ZIP...")


# Zip all results
with ZipFile(output_zip, "w") as zipf:
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        zipf.write(file_path, arcname=filename)

print(f"✅ Final ZIP created: {output_zip}")
logger.info(f"Final ZIP created: {output_zip}")
print("=== FINISHED ===")
logger.info("FINISHED")
