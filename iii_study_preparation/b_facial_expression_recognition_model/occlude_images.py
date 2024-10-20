import time
from concurrent.futures import ThreadPoolExecutor
from itertools import chain
from math import atan2, degrees
from pathlib import Path
from typing import Tuple, Union, List

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python.components.containers.bounding_box import BoundingBox
from mediapipe.tasks.python.components.containers.keypoint import NormalizedKeypoint
from mediapipe.tasks.python.vision.face_detector import FaceDetectorResult

BaseOptions = mp.tasks.BaseOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode


def draw_keypoints(image: np.ndarray,
                   right_eye_tragion: Tuple[int, int],
                   right_eye: Tuple[int, int],
                   left_eye: Tuple[int, int],
                   left_eye_tragion: Tuple[int, int]) -> None:
    cv2.circle(image, right_eye_tragion, 5, (255, 0, 0), -1)
    cv2.circle(image, right_eye, 5, (0, 255, 0), -1)
    cv2.circle(image, left_eye, 5, (0, 255, 0), -1)
    cv2.circle(image, left_eye_tragion, 5, (255, 0, 0), -1)


def euclidean_distance(point1, point2) -> float:
    return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


def add_vr_headset_simulation(image: np.ndarray,
                              right_eye_tragion: Tuple[int, int],
                              right_eye: Tuple[int, int],
                              left_eye: Tuple[int, int],
                              left_eye_tragion: Tuple[int, int]) -> np.ndarray:
    h, w, _ = image.shape

    # Oculus Quest 2 height-to-width ratio, adjust as needed
    ratio = 0.6

    # Calculate the center of the eyes
    center_eye_x, center_eye_y = (right_eye[0] + left_eye[0]) // 2, (right_eye[1] + left_eye[1]) // 2

    # Calculate width of the rectangle as the Euclidean distance between the face border points
    rect_width = int(euclidean_distance(right_eye_tragion, left_eye_tragion))
    rect_height = int(rect_width * ratio)

    # Calculate rotation angle based on the face boarder points
    rotation_angle = degrees(
        atan2(right_eye_tragion[1] - left_eye_tragion[1], right_eye_tragion[0] - left_eye_tragion[0]))

    # Draw the rotated rectangle
    pts = cv2.boxPoints(((center_eye_x, center_eye_y), (rect_width, rect_height), rotation_angle))
    pts = np.intp(pts)
    cv2.fillPoly(image, [pts], (0, 0, 0))

    return image


def to_pixel_space(p: NormalizedKeypoint, w: int, h: int) -> Tuple[int, int]:
    return int(p.x * w), int(p.y * h)


def is_plausible(detection):
    face_width = detection.bounding_box.width
    face_height = detection.bounding_box.height
    aspect_ratio = face_height / face_width
    return face_height >= 48 and face_width >= 48 and 0.5 <= aspect_ratio <= 2


def find_plausibel_face_detector_result(detection_result: FaceDetectorResult) -> Union[
    Tuple[BoundingBox, List[NormalizedKeypoint]], Tuple[None, None]]:
    if detection_result.detections:
        plausible_detections = [detection for detection in detection_result.detections if is_plausible(detection)]
        if plausible_detections:
            best_detection = max(plausible_detections, key=lambda det: det.categories[0].score)
            return best_detection.bounding_box, best_detection.keypoints

    return None, None


def crop_to_face(image: np.ndarray, bounding_box: BoundingBox, padding: float) -> np.ndarray:
    h, w, _ = image.shape
    if padding > 0:
        dx = int(bounding_box.width * padding)
        dy = int(bounding_box.height * padding)
        bounding_box.origin_x = max(0, bounding_box.origin_x - dx)
        bounding_box.origin_y = max(0, bounding_box.origin_y - dy)
        bounding_box.width = min(w - bounding_box.origin_x, bounding_box.width + 2 * dx)
        bounding_box.height = min(h - bounding_box.origin_y, bounding_box.height + 2 * dy)

    x, y, width, height = bounding_box.origin_x, bounding_box.origin_y, bounding_box.width, bounding_box.height
    return image[y:y + height, x:x + width]


def occlude_image(input_dir: Path,
                  image_path: Path,
                  output_dir: Path,
                  keypoint_detector: FaceDetector,
                  crop: bool,
                  debug: bool) -> None:
    np_image = cv2.imread(str(image_path))
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np_image)
    h, w, _ = np_image.shape

    detection_result = keypoint_detector.detect(mp_image)
    bounding_box, keypoints = find_plausibel_face_detector_result(detection_result)

    if keypoints is None:
        output_error_path = output_dir / 'errors' / image_path.relative_to(input_dir)
        print(f'Could not detect face for {image_path}')
        output_error_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_error_path), np_image)
        return

    right_eye_tragion = to_pixel_space(keypoints[4], w, h)
    right_eye = to_pixel_space(keypoints[1], w, h)
    left_eye = to_pixel_space(keypoints[0], w, h)
    left_eye_tragion = to_pixel_space(keypoints[5], w, h)

    output_image = add_vr_headset_simulation(np_image, right_eye_tragion, right_eye, left_eye, left_eye_tragion)

    if debug:
        draw_keypoints(output_image, right_eye_tragion, right_eye, left_eye, left_eye_tragion)

    if crop:
        output_image = crop_to_face(output_image, bounding_box, 0.2)

    output_path = output_dir / image_path.relative_to(input_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), output_image)


def main(input_dir: Path, output_dir: Path, keypoint_detector: FaceDetector, crop: bool = False, debug: bool = False) -> None:
    image_paths = list(chain(
        input_dir.rglob('*.png'),
        input_dir.rglob('*.PNG'),
        input_dir.rglob('*.jpg'),
        input_dir.rglob('*.JPG'),
        input_dir.rglob('*.jpeg'),
        input_dir.rglob('*.JPEG'),
        input_dir.rglob('*.tiff'),
        input_dir.rglob('*.TIFF')
    ))
    number_of_images = len(image_paths)

    start_time = time.time()
    print(f'Starting to process {number_of_images} image files...')

    with ThreadPoolExecutor() as executor:
        for i, image_path in enumerate(image_paths):
            if i % 1000 == 0:
                print(f'Starting to process image {i} of {number_of_images} images...')
            executor.submit(occlude_image, input_dir, image_path, output_dir, keypoint_detector, crop, debug)

    end_time = time.time()
    print(f'Processed {number_of_images} images in  {(end_time - start_time):.2f} seconds')


if __name__ == '__main__':
    input_dir = Path(r'/path/to/input')
    output_dir = input_dir.with_name(f'{input_dir.name}_occluded')
    output_dir.mkdir(parents=True, exist_ok=True)

    crop = False
    debug = False

    model_path = 'blaze_face_short_range.tflite'
    options = FaceDetectorOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.IMAGE,
        min_detection_confidence=0.4)
    with FaceDetector.create_from_options(options) as keypoint_detector:
        main(input_dir, output_dir, keypoint_detector, crop, debug)
