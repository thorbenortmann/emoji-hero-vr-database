import csv
from collections import defaultdict
from pathlib import Path


def calculate_expression_weights_frequency(base_path):
    timestamps_per_level = ['Level 1', 'Level 2', 'Level 3', 'Level 4']
    timestamps_per_participant_per_level = defaultdict(lambda: defaultdict(list))

    for participant_dir in base_path.iterdir():
        if participant_dir.is_dir():
            participant_id = participant_dir.name
            csv_file_path = participant_dir / 'faceexpressions.csv'
            if csv_file_path.exists():
                with open(csv_file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=';')
                    for row in reader:
                        if row:
                            timestamp, level, _, _, _ = row
                            if level in timestamps_per_level:
                                timestamps_per_participant_per_level[participant_id][level].append(int(timestamp))

    total_timedelta = 0
    total_num_timestamps = 0
    weighted_sum_of_frequencies = 0
    for participant_id, timestamps_per_level in timestamps_per_participant_per_level.items():
        for level, timestamps in timestamps_per_level.items():
            num_timestamps = len(timestamps)
            total_num_timestamps += num_timestamps
            timedelta = max(timestamps) - min(timestamps)
            frequency = num_timestamps / timedelta
            weighted_sum_of_frequencies += frequency * timedelta
            total_timedelta += timedelta

    total_average_frequency = weighted_sum_of_frequencies / total_timedelta
    print(f'Total number of timestamps: {total_num_timestamps}')
    print(f'Total recording duration: {total_timedelta / 1000 / 60:.4f} Minutes')
    print(f'Average frequency across all levels: {total_average_frequency * 1000:.4f} Timestamps per Second')


if __name__ == '__main__':
    base_path = Path(r'facial-recordings')
    calculate_expression_weights_frequency(base_path)

# E:\mydata\emojihero\venv\Scripts\python.exe E:\mydata\emojihero\participant-data\face_expressions_per_second.py
# Total number of timestamps: 332734
# Total recording duration: 88.3357 Minutes
# Average frequency across all levels: 62.7783 Timestamps per Second
