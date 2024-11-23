from pathlib import Path
import shutil


def get_new_filename(timestamp, set_id, participant_id, level_id, emoji_id, emotion_id, camera_index):
    return f"{timestamp}-{set_id}-{participant_id}-{level_id}-{emoji_id}-{emotion_id}-{camera_index}.png"


def set_name_to_id(set_name):
    set_mapping = {
        'training_set': 0,
        'validation_set': 1,
        'test_set': 2,
    }
    return set_mapping[set_name]


def map_emotion_to_id(emotion_name):
    emotion_mapping = {
        'Anger': 0,
        'Disgust': 1,
        'Fear': 2,
        'Happiness': 3,
        'Neutral': 4,
        'Sadness': 5,
        'Surprise': 6
    }
    return emotion_mapping.get(emotion_name, -1)


def process_image(image_path, original_base_path, dest_base_path, set_name):
    set_id = set_name_to_id(set_name)
    parts = image_path.stem.split('-')
    if len(parts) < 3:
        print(f'Invalid image name: {image_path}')
        return
    timestamp, participant_id, camera_index = parts[0], parts[1], parts[2]
    emotion_name = image_path.parent.name
    emotion_id = map_emotion_to_id(emotion_name)
    original_camera_suffix = '' if camera_index == '0' else '-1'

    # Search for the original image
    participant_dir = original_base_path / participant_id
    for level_dir in participant_dir.iterdir():
        if level_dir.is_dir():
            for emoji_dir in level_dir.iterdir():
                if emoji_dir.is_dir() and emotion_name == emoji_dir.name.split('-')[1]:
                    for original_image in emoji_dir.glob('*.png'):
                        if original_image.stem == f'{timestamp}{original_camera_suffix}':
                            level_id = level_dir.name.split()[-1]
                            emoji_id = emoji_dir.name.split('-')[0]

                            # Prepare the new filename and path
                            new_filename = get_new_filename(
                                timestamp, set_id, participant_id, level_id, emoji_id, emotion_id, camera_index
                            )
                            dest_dir = dest_base_path / set_name / emotion_name
                            dest_dir.mkdir(parents=True, exist_ok=True)
                            dest_path = dest_dir / new_filename

                            # Copy the image to the new path
                            shutil.copy2(original_image, dest_path)
                            print(f"Copied: {original_image} -> {dest_path}")
                            return


def process_images(src_base_path, original_base_path, dest_base_path):
    for set_dir in src_base_path.iterdir():
        if set_dir.is_dir():
            for emotion_dir in set_dir.iterdir():
                if emotion_dir.is_dir():
                    for image in emotion_dir.glob('*.png'):
                        process_image(image, original_base_path, dest_base_path, set_dir.name)


if __name__ == '__main__':
    # Input paths
    dataset_base_path = Path(r'/media/thor/PortableSSD1/mydata/emojihero/dataset/dataset')
    original_base_path = Path(r'/media/thor/PortableSSD1/mydata/emojihero/participant-data/facial-recordings')
    dest_base_path = Path('/media/thor/PortableSSD1/mydata/emojihero/dataset/emoji-hero-vr-db-images-original-resolution')

    process_images(dataset_base_path, original_base_path, dest_base_path)
