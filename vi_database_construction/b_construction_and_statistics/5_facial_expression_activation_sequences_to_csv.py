import json
from pathlib import Path

import pandas as pd


def load_data(subset_dir: Path):
    feas = []
    labels = []
    timestamps = []
    sequence_ids = []

    for category_dir in subset_dir.iterdir():
        if category_dir.is_dir():
            for sequence_dir in category_dir.iterdir():
                if sequence_dir.is_dir():
                    for file_path in sequence_dir.iterdir():
                        if file_path.is_file():
                            with file_path.open('r') as f:
                                fea_values = json.load(f)
                                feas.append(fea_values)

                            # Extract metadata from the filename
                            filename = file_path.stem  # get filename without extension
                            parts = filename.split('-')

                            if len(parts) != 6:
                                raise ValueError(f'Unexpected filename format: {filename}')

                            timestamp, set_id, participant_id, level_id, emoji_id, emotion_id = parts
                            timestamps.append(timestamp)
                            labels.append(emotion_id)
                            sequence_ids.append(sequence_dir.name)

    return feas, labels, timestamps, sequence_ids


def save_to_csv(feas, labels, timestamps, sequence_ids, output_file):
    df = pd.DataFrame(feas, columns=[f'FEA_{i}' for i in range(len(feas[0]))])
    df.insert(0, 'sequence_id', sequence_ids)
    df.insert(1, 'timestamp', timestamps)
    df['Label'] = labels

    df.to_csv(output_file, index=False)
    print(f'Data saved to {output_file}')


if __name__ == '__main__':
    base_directory = Path(r'/media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-db-facial-expression-activation-sequences')
    output_dir = base_directory.parent / (base_directory.name + '-csv')
    output_dir.mkdir(exist_ok=True)

    for subset_dir in base_directory.iterdir():
        if subset_dir.is_dir():
            feas, labels, timestamps, sequence_ids = load_data(subset_dir)
            output_file = output_dir / f'{subset_dir.name}.csv'
            save_to_csv(feas, labels, timestamps, sequence_ids, output_file)
