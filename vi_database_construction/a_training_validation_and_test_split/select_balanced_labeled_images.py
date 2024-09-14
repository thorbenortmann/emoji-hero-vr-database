import csv
import random
import shutil
from collections import defaultdict
from pathlib import Path


def main():
    csv_file_path = Path(r'E:\mydata\emojihero\dataset\label.csv')
    base_dir = Path(r'E:\mydata\emojihero\participant-data\facial-recordings')
    dest_base_dir = Path(r'E:\mydata\emojihero\dataset')
    dest_base_dir.mkdir(parents=True, exist_ok=True)

    TRAIN_SET = 'training_set'
    VAL_SET = 'validation_set'
    TEST_SET = 'test_set'

    train_base_dir = dest_base_dir / TRAIN_SET
    train_base_dir.mkdir(parents=True, exist_ok=True)
    val_base_dir = dest_base_dir / VAL_SET
    val_base_dir.mkdir(parents=True, exist_ok=True)
    test_base_dir = dest_base_dir / TEST_SET
    test_base_dir.mkdir(parents=True, exist_ok=True)

    source_paths_train = defaultdict(lambda: defaultdict(list))
    source_paths_val = defaultdict(lambda: defaultdict(list))
    source_paths_test = defaultdict(lambda: defaultdict(list))

    emotion_count_per_participant = defaultdict(lambda: defaultdict(int))

    with csv_file_path.open(mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            participant = str(row['participant'])
            emotion = row['label']

            emotion_count_per_participant[participant][emotion] += 2

            source_path = base_dir / participant / f"Level {row['level']}" / f"{row['emoji']}-{emotion}" / row['image']

            if participant in ["2", "5", "6", "9", "14", "29", "32", "36"]:
                source_paths_val[emotion][participant].append(source_path)

            elif participant in ["1", "8", "10", "13", "15", "18", "23", "27"]:
                source_paths_test[emotion][participant].append(source_path)

            else:
                source_paths_train[emotion][participant].append(source_path)

    print('\n' + TRAIN_SET)
    emotion_counts_train = {}
    for emotion, participant_dict in sorted(source_paths_train.items()):
        num_samples = sum(len(paths) for paths in participant_dict.values())
        print(f'{emotion}: {num_samples}')
        emotion_counts_train[emotion] = num_samples

    print(f'train label distribution: {emotion_counts_train}')
    print(f'total number of labels: {sum(emotion_counts_train.values())}')

    print('\n' + VAL_SET)
    emotion_counts_val = {}
    for emotion, participant_dict in sorted(source_paths_val.items()):
        num_samples = sum(len(paths) for paths in participant_dict.values())
        print(f'{emotion}: {num_samples}')
        emotion_counts_val[emotion] = num_samples

    min_samples_val = min(emotion_counts_val.values())
    samples_to_remove_val = {emotion: count - min_samples_val for emotion, count in emotion_counts_val.items()}
    print(f'validation label distribution: {emotion_counts_val}')
    print(f'total number of labels: {sum(emotion_counts_val.values())}')
    print(f'validation removal distribution {samples_to_remove_val}')
    print(f'total number of labels to remove: {sum(samples_to_remove_val.values())}')

    for emotion, samples_to_remove in samples_to_remove_val.items():
        participant_dict = source_paths_val[emotion]
        for i in range(samples_to_remove):
            best_represented_participant = max(participant_dict, key=lambda k: len(participant_dict[k]))
            random_index = random.randint(0, len(participant_dict[best_represented_participant]) - 1)
            del participant_dict[best_represented_participant][random_index]

    print('\n' + TEST_SET)
    emotion_counts_test = {}
    for emotion, participant_dict in sorted(source_paths_test.items()):
        num_samples = sum(len(paths) for paths in participant_dict.values())
        print(f'{emotion}: {num_samples}')
        emotion_counts_test[emotion] = num_samples

    min_samples_test = min(emotion_counts_test.values())
    samples_to_remove_test = {emotion: count - min_samples_test for emotion, count in emotion_counts_test.items()}
    print(f'test label distribution {emotion_counts_test}')
    print(f'total number of labels: {sum(emotion_counts_test.values())}')
    print(f'test removal distribution {samples_to_remove_test}')
    print(f'total number of labels to remove: {sum(samples_to_remove_test.values())}')

    for emotion, samples_to_remove in samples_to_remove_test.items():
        participant_dict = source_paths_test[emotion]
        for i in range(samples_to_remove):
            best_represented_participant = max(participant_dict, key=lambda k: len(participant_dict[k]))
            random_index = random.randint(0, len(participant_dict[best_represented_participant]) - 1)
            del participant_dict[best_represented_participant][random_index]

    def copy_images_to_set(source_paths, base_dir):
        for emotion, participants in source_paths.items():
            emotion_dir = base_dir / emotion
            emotion_dir.mkdir(parents=True, exist_ok=True)

            for participant, paths in participants.items():
                for source_path_central in paths:
                    source_path_side_view = source_path_central.parent / f'{source_path_central.stem}-1{source_path_central.suffix}'
                    dest_path_central = emotion_dir / f'{source_path_central.stem}-{participant}-0{source_path_central.suffix}'
                    dest_path_side_view = emotion_dir / f'{source_path_central.stem}-{participant}-1{source_path_central.suffix}'

                    shutil.copy2(source_path_central, dest_path_central)
                    shutil.copy2(source_path_side_view, dest_path_side_view)

    print(f"\nCopying images for the {TRAIN_SET}")
    copy_images_to_set(source_paths_train, train_base_dir)

    print(f"\nCopying images for the {VAL_SET}")
    copy_images_to_set(source_paths_val, val_base_dir)

    print(f"\nCopying images for the {TEST_SET}")
    copy_images_to_set(source_paths_test, test_base_dir)


if __name__ == '__main__':
    main()
