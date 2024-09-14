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

                # Berechne Mittelpunkt des Gesichts horizontal
                center_x = x + w // 2

                # Berechne den neuen Cropping-Bereich, zentriert um das Gesicht
                start_x = max(center_x - 360, 0)
                end_x = min(center_x + 360, iw)

                if draw_bbox:
                    # Zeichne die Bounding Box auf das Bild
                    cv2.rectangle(np_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Stelle sicher, dass der Cropping-Bereich 720 Pixel breit ist
                if (end_x - start_x) < 720:
                    diff = 720 - (end_x - start_x)
                    start_x = max(0, start_x - diff // 2)
                    end_x = min(iw, end_x + (diff - diff // 2))

                # Zuschneiden, ohne die Höhe zu ändern
                return np_image[:, start_x:end_x]

        print("No plausible face detected")
        start_x = (iw - 720) // 2
        end_x = start_x + 720
        return np_image[:, start_x:end_x]


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
    output_folder = f'{input_folder}-cropped'

    process_images(input_folder, output_folder)
