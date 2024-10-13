from pathlib import Path
from statistics import mean, pstdev


def calculate_average_max_timestamp_difference(base_path):
    level_max_diffs = {'Level 1': [], 'Level 2': [], 'Level 3': [], 'Level 4': []}
    level_file_counts = {'Level 1': [], 'Level 2': [], 'Level 3': [], 'Level 4': []}

    for participant_dir in base_path.iterdir():
        if participant_dir.is_dir():
            for level_dir in participant_dir.iterdir():
                if level_dir.is_dir() and level_dir.name in level_max_diffs:
                    for emoji_dir in level_dir.iterdir():
                        if emoji_dir.is_dir():
                            timestamps = [int(image_path.stem) for image_path in emoji_dir.iterdir() if
                                          image_path.suffix == '.png' and '-' not in image_path.stem]
                            max_difference = max(timestamps) - min(timestamps)
                            level_max_diffs[level_dir.name].append(max_difference)
                            level_file_counts[level_dir.name].append(len(timestamps))

    for level, max_diffs in level_max_diffs.items():
        print(f'\n{level}: Mean of max differences {int(mean(max_diffs))} Milliseconds')
        print(f'{level}: Max of max differences {max(max_diffs)} Milliseconds')
        print(f'{level}: Min of max differences {min(max_diffs)} Milliseconds')

        print(f'{level}: Standard Deviation of max differences {int(pstdev(max_diffs))} Milliseconds')
        print(f'{level}: Average number of files = {round(mean(level_file_counts[level]), 2)} Images')
        print(f'{level}: Max number of files = {max(level_file_counts[level])} Images')
        print(f'{level}: Min number of files = {min(level_file_counts[level])} Images')
        print(f'{level}: Standard Deviation of number of files {round(pstdev(level_file_counts[level]), 2)} Images')

    print(f'\nTotal number of files: {sum(sum(file_counts) for file_counts in level_file_counts.values())}')


if __name__ == '__main__':
    base_path = Path('facial-recordings')
    calculate_average_max_timestamp_difference(base_path)

# E:\mydata\emojihero\venv\Scripts\python.exe E:\mydata\emojihero\participant-data\recording_window.py
#
# Level 1: Mean of max differences 2131 Milliseconds
# Level 1: Max of max differences 2249 Milliseconds
# Level 1: Min of max differences 2006 Milliseconds
# Level 1: Standard Deviation of max differences 18 Milliseconds
# Level 1: Average number of files = 64.63 Images
# Level 1: Max number of files = 66 Images
# Level 1: Min number of files = 61 Images
# Level 1: Standard Deviation of number of files 0.61 Images
#
# Level 2: Mean of max differences 2133 Milliseconds
# Level 2: Max of max differences 2184 Milliseconds
# Level 2: Min of max differences 2069 Milliseconds
# Level 2: Standard Deviation of max differences 13 Milliseconds
# Level 2: Average number of files = 64.74 Images
# Level 2: Max number of files = 66 Images
# Level 2: Min number of files = 63 Images
# Level 2: Standard Deviation of number of files 0.5 Images
#
# Level 3: Mean of max differences 1978 Milliseconds
# Level 3: Max of max differences 2146 Milliseconds
# Level 3: Min of max differences 1894 Milliseconds
# Level 3: Standard Deviation of max differences 40 Milliseconds
# Level 3: Average number of files = 60.43 Images
# Level 3: Max number of files = 65 Images
# Level 3: Min number of files = 57 Images
# Level 3: Standard Deviation of number of files 1.25 Images
#
# Level 4: Mean of max differences 1594 Milliseconds
# Level 4: Max of max differences 1662 Milliseconds
# Level 4: Min of max differences 1534 Milliseconds
# Level 4: Standard Deviation of max differences 19 Milliseconds
# Level 4: Average number of files = 48.52 Images
# Level 4: Max number of files = 50 Images
# Level 4: Min number of files = 45 Images
# Level 4: Standard Deviation of number of files 0.63 Images
#
# Total number of files: 147490
#
# Process finished with exit code 0
