import cv2
from PIL import Image
import mediapipe as mp
import io

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)


def process_image_to_passport(input_path, output_path, max_size_kb=20):
    image = cv2.imread(input_path)
    h, w, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = face_detection.process(image_rgb)

    if result.detections:
        for detection in result.detections:
            bboxC = detection.location_data.relative_bounding_box
            x, y, bw, bh = bboxC.xmin, bboxC.ymin, bboxC.width, bboxC.height

            # Convert to pixel coordinates
            x1 = int(x * w)
            y1 = int(y * h)
            x2 = int((x + bw) * w)
            y2 = int((y + bh) * h)

            # Expand in all directions to include shoulders and hair
            box_width = x2 - x1
            box_height = y2 - y1

            expand_top = int(box_height * 0.6)     # add space for hair
            expand_bottom = int(box_height * 1.4)  # add more for shoulders
            expand_side = int(box_width * 0.5)     # sides for balance

            new_x1 = max(0, x1 - expand_side)
            new_y1 = max(0, y1 - expand_top)
            new_x2 = min(w, x2 + expand_side)
            new_y2 = min(h, y2 + expand_bottom)

            # Crop and resize to passport size
            crop = image[new_y1:new_y2, new_x1:new_x2]
            resized = cv2.resize(crop, (600, 600))
            rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_image)
            pil_img.save(output_path, format="PNG")
            return True
        

    else:
        print(f" No face detected in {input_path}")
        return False

