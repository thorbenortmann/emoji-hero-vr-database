import math
from pathlib import Path

import cv2
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode


def is_plausible(detection):
    face_width = detection.bounding_box.width
    face_height = detection.bounding_box.height
    aspect_ratio = face_height / face_width
    return face_height >= 150 and face_width >= 150 and 0.5 <= aspect_ratio <= 2


def crop_face(img_path, draw_bbox=False):
    """Erkennt Gesichter und schneidet das Bild auf 720x720 zurecht."""
    options = FaceDetectorOptions(
        base_options=BaseOptions(model_asset_path='blaze_face_short_range.tflite'),
        min_detection_confidence=0.1,
        running_mode=VisionRunningMode.IMAGE)

    with FaceDetector.create_from_options(options) as face_detection:
        # Bild in RGB konvertieren
        np_image = cv2.imread(str(img_path), cv2.IMREAD_UNCHANGED)
        ih, iw, _ = np_image.shape
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGBA, data=np_image)
        results = face_detection.detect(mp_image)

        # Wenn Gesichter erkannt werden, schneide das erste gefundene Gesicht zu
        if results.detections:
            detections = [detection for detection in results.detections if is_plausible(detection)]
            if detections:
                detection = max(detections, key=lambda det: det.categories[0].score)
                # Zugriff auf die BoundingBox direkt
                bbox = detection.bounding_box
                x, y, w, h = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height

                # Berechne den neuen Mittelpunkt
                center_x = x + w/2
                center_y = y + h/2 - h/5

                # Verdopple die Größe der Bounding Box
                crop_width = min(max(w * 1.8, 400), 720) # 2 + 500 worked well (cropped2) -> cropped3 (1.6 + 400)
                crop_height = min(max(h * 1,8, 400), 720) # 2+ 500 worked well
                crop_size = max(crop_width, crop_height)


                # Berechne den neuen Cropping-Bereich, zentriert um das Gesicht
                new_x = max(center_x - crop_size / 2, 0)
                new_y = max(center_y - crop_size / 2, 0)
                if new_x + crop_size > iw:
                    new_x = iw - crop_size
                if new_y + crop_size > ih:
                    new_y = ih - crop_size

                # Stelle sicher, dass das Cropping-Fenster nicht negativ wird
                new_x = math.floor(max(new_x, 0))
                new_y = math.floor(max(new_y, 0))

                return np_image[int(new_y):int(new_y + crop_size), int(new_x):int(new_x + crop_size)]

        print("No plausible face detected")
        start_x = (iw - 600) // 2
        end_x = start_x + 600
        start_y = (ih - 600) // 2
        end_y = start_y + 600
        return np_image[start_y:end_y, start_x:end_x]


def process_images(input_folder, output_folder):
    """Verarbeitet rekursiv alle .png-Bilder im Eingabeordner."""
    input_path = Path(input_folder)
    output_path = Path(output_folder)

    for img_path in input_path.rglob('*.png'):
        cropped_image = crop_face(img_path, True)

        relative_path = img_path.relative_to(input_path)
        new_path = output_path.joinpath(relative_path)
        new_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(new_path), cropped_image)


if __name__ == "__main__":
    input_folder = r'E:\mydata\emoijhero\dataset\dataset'
    output_folder = f'{input_folder}-cropped-face18400'

    process_images(input_folder, output_folder)
