# # import cv2
# # from PIL import Image
# # import mediapipe as mp
# # import io

# # mp_face_detection = mp.solutions.face_detection
# # face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)


# # def process_image_to_passport(input_path, output_path, max_size_kb=20):
# #     image = cv2.imread(input_path)
# #     h, w, _ = image.shape
# #     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# #     result = face_detection.process(image_rgb)

# #     if result.detections:
# #         for detection in result.detections:
# #             bboxC = detection.location_data.relative_bounding_box
# #             x, y, bw, bh = bboxC.xmin, bboxC.ymin, bboxC.width, bboxC.height

# #             # Convert to pixel coordinates
# #             x1 = int(x * w)
# #             y1 = int(y * h)
# #             x2 = int((x + bw) * w)
# #             y2 = int((y + bh) * h)

# #             # Expand in all directions to include shoulders and hair
# #             box_width = x2 - x1
# #             box_height = y2 - y1

# #             expand_top = int(box_height * 0.6)     # add space for hair
# #             expand_bottom = int(box_height * 1.4)  # add more for shoulders
# #             expand_side = int(box_width * 0.5)     # sides for balance

# #             new_x1 = max(0, x1 - expand_side)
# #             new_y1 = max(0, y1 - expand_top)
# #             new_x2 = min(w, x2 + expand_side)
# #             new_y2 = min(h, y2 + expand_bottom)

# #             # Crop and resize to passport size
# #             crop = image[new_y1:new_y2, new_x1:new_x2]
# #             resized = cv2.resize(crop, (600, 600))
# #             rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
# #             pil_img = Image.fromarray(rgb_image)
# #             pil_img.save(output_path, format="PNG")
# #             return True
        

# #     else:
# #         print(f" No face detected in {input_path}")
# #         return False

# import os
# import cv2
# import io
# from PIL import Image, ImageDraw
# import mediapipe as mp

# # Setup Mediapipe face detection
# mp_face_detection = mp.solutions.face_detection
# face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)

# INPUT_DIR = "input_images"
# OUTPUT_DIR = "passport_photos"
# MAX_SIZE_KB = 20


# def compress_to_target_size(pil_img, max_kb=20, min_quality=60):
#     """Compress to target size using JPEG."""
#     buffer = io.BytesIO()
#     quality = 95
#     step = 5

#     while quality >= min_quality:
#         buffer.seek(0)
#         buffer.truncate()
#         pil_img.save(buffer, format="JPEG", quality=quality)
#         size_kb = len(buffer.getvalue()) / 1024
#         if size_kb <= max_kb:
#             return buffer.getvalue()
#         quality -= step

#     return buffer.getvalue()  # Return lowest quality if needed


# def process_image_to_passport(input_path, output_path, max_size_kb=20):
#     image = cv2.imread(input_path)
#     if image is None:
#         print(f"⚠️ Failed to read image: {input_path}")
#         return False

#     h, w, _ = image.shape
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     result = face_detection.process(image_rgb)

#     if result.detections:
#         for detection in result.detections:
#             bboxC = detection.location_data.relative_bounding_box
#             x, y, bw, bh = bboxC.xmin, bboxC.ymin, bboxC.width, bboxC.height

#             # Convert to pixel coordinates
#             x1 = int(x * w)
#             y1 = int(y * h)
#             x2 = int((x + bw) * w)
#             y2 = int((y + bh) * h)

#             # Expand for hair and shoulders
#             box_width = x2 - x1
#             box_height = y2 - y1

#             expand_top = int(box_height * 0.6)
#             expand_bottom = int(box_height * 1.4)
#             expand_side = int(box_width * 0.5)

#             new_x1 = max(0, x1 - expand_side)
#             new_y1 = max(0, y1 - expand_top)
#             new_x2 = min(w, x2 + expand_side)
#             new_y2 = min(h, y2 + expand_bottom)

#             crop = image[new_y1:new_y2, new_x1:new_x2]
#             resized = cv2.resize(crop, (600, 600))

#             # Convert to PIL
#             fg = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))

#             # Create circular mask
#             mask = Image.new("L", (600, 600), 0)
#             draw = ImageDraw.Draw(mask)
#             draw.ellipse((0, 0, 600, 600), fill=255)

#             # White background
#             background = Image.new("RGB", (600, 600), (255, 255, 255))
#             circular_img = Image.new("RGB", (600, 600), (255, 255, 255))
#             circular_img.paste(fg, (0, 0), mask)

#             final_img = Image.composite(circular_img, background, mask)

#             # Compress and save
#             compressed = compress_to_target_size(final_img, max_kb=max_size_kb)
#             with open(output_path, "wb") as f:
#                 f.write(compressed)

#             #print(f"✅ Saved: {output_path}")
#             return True

#     print(f"❌ No face detected in: {input_path}")
#     return False


# # ========== MAIN LOOP ==========
# if __name__ == "__main__":
#     os.makedirs(OUTPUT_DIR, exist_ok=True)

#     for filename in os.listdir(INPUT_DIR):
#         if filename.lower().endswith((".jpg", ".jpeg", ".png")):
#             input_path = os.path.join(INPUT_DIR, filename)
#             output_path = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + ".jpg")
#             process_image_to_passport(input_path, output_path)
import cv2
from PIL import Image
import numpy as np
import mediapipe as mp
import io
import os

# Initialize Mediapipe models once
mp_face_detection = mp.solutions.face_detection
mp_selfie_segmentation = mp.solutions.selfie_segmentation

face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)


def compress_to_target_size(pil_img, max_kb=20, min_quality=30):
    max_bytes = max_kb * 1024
    quality = 95
    step = 5
    min_quality = 10
    min_size = 300  # don't go below 300x300

    img = pil_img.copy()
    
    while True:
        buffer = io.BytesIO()
        q = quality
        while q >= min_quality:
            buffer.seek(0)
            buffer.truncate()
            img.save(buffer, format="JPEG", quality=q)
            if buffer.tell() <= max_bytes:
                return buffer.getvalue()
            q -= step

        # If compression fails at all qualities, reduce image size
        new_w = int(img.width * 0.9)
        new_h = int(img.height * 0.9)
        if new_w < min_size or new_h < min_size:
            # Can't shrink further; return best effort
            buffer.seek(0)
            buffer.truncate()
            img.save(buffer, format="JPEG", quality=min_quality)
            return buffer.getvalue()
        
        img = img.resize((new_w, new_h), Image.ANTIALIAS)


def process_image_to_passport(input_path, output_path, max_size_kb=20):
    image = cv2.imread(input_path)
    if image is None:
        print(f"⚠️ Failed to read image: {input_path}")
        return False

    h, w, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_result = face_detection.process(image_rgb)

    if face_result.detections:
        for detection in face_result.detections:
            bboxC = detection.location_data.relative_bounding_box
            x, y, bw, bh = bboxC.xmin, bboxC.ymin, bboxC.width, bboxC.height

            # Convert to pixel coordinates
            x1 = int(x * w)
            y1 = int(y * h)
            x2 = int((x + bw) * w)
            y2 = int((y + bh) * h)

            # Expand bounding box
            box_width = x2 - x1
            box_height = y2 - y1
            expand_top = int(box_height * 0.6)
            expand_bottom = int(box_height * 1.4)
            expand_side = int(box_width * 0.5)

            new_x1 = max(0, x1 - expand_side)
            new_y1 = max(0, y1 - expand_top)
            new_x2 = min(w, x2 + expand_side)
            new_y2 = min(h, y2 + expand_bottom)

            crop = image[new_y1:new_y2, new_x1:new_x2]

            # ✅ Background removal starts here
            crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            seg_result = selfie_segmentation.process(crop_rgb)
            mask = seg_result.segmentation_mask > 0.1

            # White background
            white_bg = np.ones_like(crop, dtype=np.uint8) * 255
            cleaned = np.where(mask[..., None], crop, white_bg)

            # Resize and convert
            resized = cv2.resize(cleaned, (600, 600))
            final_img = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))

            # Compress and save
            compressed = compress_to_target_size(final_img, max_kb=max_size_kb)
            with open(output_path, "wb") as f:
                f.write(compressed)

            # print(f"✅ Saved: {output_path}")
            return True

    else:
        print(f"❌ No face detected in: {input_path}")
        return False
