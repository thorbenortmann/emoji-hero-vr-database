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


def crop_face(img_path):
    options = FaceDetectorOptions(
        base_options=BaseOptions(model_asset_path='blaze_face_short_range.tflite'),
        min_detection_confidence=0.1,
        running_mode=VisionRunningMode.IMAGE)

    with FaceDetector.create_from_options(options) as face_detection:
        np_image = cv2.imread(str(img_path), cv2.IMREAD_UNCHANGED)
        ih, iw, _ = np_image.shape
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGBA, data=np_image)
        results = face_detection.detect(mp_image)

        if results.detections:
            detections = [detection for detection in results.detections if is_plausible(detection)]
            if detections:
                detection = max(detections, key=lambda det: det.categories[0].score)
                bbox = detection.bounding_box
                x, y, w, h = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height

                center_x = x + w / 2
                center_y = y + h / 2 - h / 5

                crop_width = min(max(w * 1.8, 400), 720)  # these numbers are heuristics
                crop_height = min(max(h * 1, 8, 400), 720)  # these numbers are heuristics
                crop_size = max(crop_width, crop_height)

                new_x = max(center_x - crop_size / 2, 0)
                new_y = max(center_y - crop_size / 2, 0)
                if new_x + crop_size > iw:
                    new_x = iw - crop_size
                if new_y + crop_size > ih:
                    new_y = ih - crop_size

                new_x = math.floor(max(new_x, 0))
                new_y = math.floor(max(new_y, 0))

                return np_image[int(new_y):int(new_y + crop_size), int(new_x):int(new_x + crop_size)]

        print("No plausible face detected")
        start_x = (iw - 600) // 2
        end_x = start_x + 600
        start_y = (ih - 600) // 2
        end_y = start_y + 600
        return np_image[start_y:end_y, start_x:end_x]


def process_images(input_path, output_path):
    for img_path in input_path.rglob('*.png'):
        cropped_image = crop_face(img_path)

        relative_path = img_path.relative_to(input_path)
        new_path = output_path.joinpath(relative_path)
        new_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(new_path), cropped_image)
        print(f'Cropped {img_path} and saved as {new_path}.')

    print(f'Finished processing images from {input_path}. Saved to {output_path}')


if __name__ == "__main__":
    input_path = Path(r'/media/thor/PortableSSD/emoji-hero-vr-db/emoji-hero-vr-image-sequences-original-resolution')
    output_path = input_path.parent / 'intermediate_versions' / 'emoji-hero-vr-db-image-sequences-faces-png'

    process_images(input_path, output_path)
