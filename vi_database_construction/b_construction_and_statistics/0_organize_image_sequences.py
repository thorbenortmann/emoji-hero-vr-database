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


def is_original_side_view_image(image_path):
    return image_path.stem.endswith('-1')


def find_additional_images(original_image, emoji_dir, camera_index, target_count=29):
    is_original_img_side_view = is_original_side_view_image(original_image)
    all_images = sorted(
        [img for img in emoji_dir.glob('*.png') if is_original_img_side_view == is_original_side_view_image(img)],
        key=lambda x: int(x.stem.split('-')[0])
    )
    index = all_images.index(original_image)

    # Collect images before the original_image
    before_images = all_images[max(0, index - target_count):index]

    # If not enough images before, collect images after the original_image
    remaining_count = target_count - len(before_images)
    after_images = all_images[index + 1:index + 1 + remaining_count]

    return before_images + after_images


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

                            # Find additional images to form a sequence of 30, including the original image
                            additional_images = find_additional_images(original_image, emoji_dir, camera_index)
                            image_sequence = [original_image] + additional_images
                            sequence_dir_name = get_new_filename(timestamp, set_id, participant_id, level_id, emoji_id,
                                                                 emotion_id, camera_index).replace('.png', '')
                            sequence_dest_dir = dest_base_path / set_name / emotion_name / sequence_dir_name
                            sequence_dest_dir.mkdir(parents=True, exist_ok=True)

                            for img in image_sequence:
                                new_filename = get_new_filename(
                                    img.stem.split('-')[0], set_id, participant_id, level_id, emoji_id, emotion_id,
                                    camera_index
                                )
                                dest_path = sequence_dest_dir / new_filename
                                shutil.copy2(img, dest_path)
                                print(f"Copied: {img} -> {dest_path}")
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
    dataset_base_path = Path(r'/media/thor/PortableSSD1/mydata/emojohero/dataset/dataset')
    original_base_path = Path(r'/media/thor/PortableSSD1/mydata/emojihero/participant-data/facial-recordings')
    dest_base_path = Path('/media/thor/PortableSSD1/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution')

    process_images(dataset_base_path, original_base_path, dest_base_path)
