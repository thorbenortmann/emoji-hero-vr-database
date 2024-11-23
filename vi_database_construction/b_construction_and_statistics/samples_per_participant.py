from collections import Counter
from pathlib import Path


def count_samples_by_participant(dataset_path):
    participant_sample_counts = Counter()

    for image_file in dataset_path.rglob('*-0.jpg'):
        participant_id = int(image_file.stem.split('-')[2])
        participant_sample_counts[participant_id] += 1

    for participant_id, count in sorted(participant_sample_counts.items()):
        print(f'Participant {participant_id}: {count} samples')

    print(f'Found {sum(participant_sample_counts.values())} central-view samples in total!')


if __name__ == '__main__':
    dataset_path = Path(r'/media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-db-images-224')
    count_samples_by_participant(dataset_path)

# Participant 1: 47 samples
# Participant 2: 52 samples
# Participant 3: 48 samples
# Participant 4: 62 samples
# Participant 5: 50 samples
# Participant 6: 47 samples
# Participant 7: 50 samples
# Participant 8: 54 samples
# Participant 9: 48 samples
# Participant 10: 46 samples
# Participant 11: 52 samples
# Participant 12: 38 samples
# Participant 13: 46 samples
# Participant 14: 51 samples
# Participant 15: 48 samples
# Participant 16: 42 samples
# Participant 17: 47 samples
# Participant 18: 43 samples
# Participant 19: 49 samples
# Participant 20: 51 samples
# Participant 21: 45 samples
# Participant 22: 29 samples
# Participant 23: 53 samples
# Participant 24: 45 samples
# Participant 25: 56 samples
# Participant 26: 40 samples
# Participant 27: 41 samples
# Participant 28: 47 samples
# Participant 29: 50 samples
# Participant 30: 53 samples
# Participant 31: 55 samples
# Participant 32: 38 samples
# Participant 33: 52 samples
# Participant 34: 47 samples
# Participant 35: 61 samples
# Participant 36: 49 samples
# Participant 37: 46 samples
# Found 1778 central-view samples in total!
