import argparse
import csv
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image

from fer.posterv2.face_detector import FaceDetector, NoFaceDetectedException
from fer.posterv2.posterv2_recognizer import PosterV2Recognizer


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to the directory to process')
    return parser.parse_args()


def custom_sort_key(key):
    level, emotion = key.split(' - ')
    num, _ = emotion.split('-', 1)
    return int(level.split(' ')[1]), int(num)


def process_emote_dir(args):
    emote_dir, face_detector, emotion_recognizer = args
    target_emotion = emote_dir.name.split('-')[-1].lower()
    best_score = 0
    best_image_data = (None, None)  # Tuple of (best_image_path, best_score)

    sorted_files = sorted([file for file in emote_dir.glob('*.png') if not file.name.endswith('-1.png')],
                          key=lambda x: x.name)

    for file in sorted_files[15:]:
        try:
            image = Image.open(file)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image = np.array(image)
            cropped_face, _ = face_detector.detect_face(image)
            probabilities = emotion_recognizer.predict_emotions(cropped_face)
            emotion_index = emotion_recognizer.emotion_labels.index(target_emotion)
            score = probabilities[emotion_index]

            if score > best_score:
                best_score = score
                best_image_data = (file, score)

        except NoFaceDetectedException:
            continue

    return emote_dir.parent.name + ' - ' + emote_dir.name, best_image_data


def process_directory(path: Path):
    face_detector = FaceDetector()
    emotion_recognizer = PosterV2Recognizer()
    tasks = []

    for level_dir in path.iterdir():
        if level_dir.is_dir() and level_dir.name in ['Level 1', 'Level 2', 'Level 3', 'Level 4']:
            for emote_dir in level_dir.iterdir():
                if emote_dir.is_dir() and emote_dir.name.split('-')[0].isdigit():
                    tasks.append((emote_dir, face_detector, emotion_recognizer))

    best_images = {}
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_emote_dir, tasks)

    for emotion, (image_path, score) in results:
        best_images[emotion] = (image_path, score)

    return dict(sorted(best_images.items(), key=lambda item: custom_sort_key(item[0])))


def create_labeling_directory(input_path: Path, best_images: dict):
    labeling_dir = input_path.parent / (input_path.name + '-for-labeling')
    labeling_dir.mkdir(exist_ok=True)

    images_dir = labeling_dir / 'images'
    images_dir.mkdir(exist_ok=True)

    details_path = labeling_dir / 'details.csv'
    with details_path.open('w', newline='') as csvfile:
        fieldnames = ['level', 'emote_id', 'complete_path', 'image_name', 'emotion', 'probability']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for key, (image_path, probability) in best_images.items():
            level, emotion_part = key.split(' - ')
            emote_id, emotion = emotion_part.split('-', 1)
            writer.writerow({
                'level': level.split(' ')[1],
                'emote_id': emote_id,
                'complete_path': image_path,
                'image_name': image_path.name,
                'emotion': emotion,
                'probability': f'{probability:.4f}'
            })
            shutil.copy(image_path, images_dir / image_path.name)


def main():
    args = parse_args()
    path = Path(args.path)
    if not path.is_dir():
        print(f'The path {path} is not a valid directory.')
        return

    best_images = process_directory(path)
    create_labeling_directory(path, best_images)
    for emotion, (image_path, _) in best_images.items():
        print(f'Best image for {emotion}: {image_path}')


if __name__ == '__main__':
    main()
