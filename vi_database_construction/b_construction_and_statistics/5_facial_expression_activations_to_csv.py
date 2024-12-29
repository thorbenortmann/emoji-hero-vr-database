import json
from pathlib import Path

import pandas as pd

# Below are the names of the 63 Face Expressions we captured using the Face Tracking API.
# We used version 59.0 of the Meta XR Core SDK, which included the Face Tracking API.
# Unfortunately, the API reference for version 59.0, released 24.10.2023, is not available anymore.
# The oldest Unity Reference Guide available today (29.12.2024) is for version 63, released 05.03.2024.
# The API reference for version 63 contains 7 additional Face Expressions in comparison to version 59,
# namely Tongue_Tip_Interdental, TongueTipAlveolar, TongueFrontDorsalPalate, TongueMidDorsalPalate,
# TongueBackDorsalVelar, TongueOut, TongueRetreat.
# Sources:
# https://developers.meta.com/horizon/documentation/unity/move-face-tracking/
# https://developers.meta.com/horizon/reference/unity/v63/class_o_v_r_face_expressions#detailed-description
# https://developers.meta.com/horizon/downloads/package/meta-xr-core-sdk/59.0
# https://www.meta.com/en-gb/help/quest/articles/whats-new/release-notes/

fea_names = [
    'BrowLowererL', 'BrowLowererR',
    'CheekPuffL', 'CheekPuffR', 'CheekRaiserL', 'CheekRaiserR', 'CheekSuckL', 'CheekSuckR',
    'ChinRaiserB', 'ChinRaiserT',
    'DimplerL', 'DimplerR',
    'EyesClosedL', 'EyesClosedR', 'EyesLookDownL', 'EyesLookDownR', 'EyesLookLeftL', 'EyesLookLeftR', 'EyesLookRightL',
    'EyesLookRightR', 'EyesLookUpL', 'EyesLookUpR',
    'InnerBrowRaiserL', 'InnerBrowRaiserR',
    'JawDrop', 'JawSidewaysLeft', 'JawSidewaysRight', 'JawThrust',
    'LidTightenerL', 'LidTightenerR',
    'LipCornerDepressorL', 'LipCornerDepressorR', 'LipCornerPullerL', 'LipCornerPullerR',
    'LipFunnelerLB', 'LipFunnelerLT', 'LipFunnelerRB', 'LipFunnelerRT', 'LipPressorL', 'LipPressorR',
    'LipPuckerL', 'LipPuckerR', 'LipStretcherL', 'LipStretcherR', 'LipSuckLB', 'LipSuckLT', 'LipSuckRB', 'LipSuckRT',
    'LipTightenerL', 'LipTightenerR', 'LipsToward', 'LowerLipDepressorL', 'LowerLipDepressorR',
    'MouthLeft', 'MouthRight',
    'NoseWrinklerL', 'NoseWrinklerR',
    'OuterBrowRaiserL', 'OuterBrowRaiserR',
    'UpperLidRaiserL', 'UpperLidRaiserR', 'UpperLipRaiserL', 'UpperLipRaiserR'
]


def load_data(subset_dir: Path):
    feas = []
    labels = []
    timestamps = []
    file_ids = []

    for category_dir in subset_dir.iterdir():
        if category_dir.is_dir():
            for file_path in category_dir.iterdir():
                if file_path.is_file():
                    with file_path.open('r') as f:
                        fea_values = json.load(f)
                        feas.append(fea_values)

                    # Extract metadata from the filename
                    file_name = file_path.stem  # get filename without extension
                    parts = file_name.split('-')

                    if len(parts) != 6:
                        raise ValueError(f'Unexpected filename format: {file_name}')

                    timestamp, set_id, participant_id, level_id, emoji_id, emotion_id = parts
                    timestamps.append(timestamp)
                    labels.append(emotion_id)
                    file_ids.append(file_name)

    return feas, labels, timestamps, file_ids


def save_to_csv(feas, labels, timestamps, file_ids, output_file):
    if len(feas[0]) != len(fea_names) != 63:
        raise ValueError('Number of FEAs is not as expected (63))')

    df = pd.DataFrame(feas, columns=fea_names)
    df.insert(0, 'file_id', file_ids)
    df.insert(1, 'timestamp', timestamps)
    df['Label'] = labels

    df.to_csv(output_file, index=False)
    print(f'Data saved to {output_file}')


if __name__ == '__main__':
    base_directory = Path(r'/media/thor/PortableSSD/emoji-hero-vr-db/dataset/emoji-hero-vr-db/emoji-hero-vr-db-sfea')
    output_dir = base_directory.parent / (base_directory.name + '-as-csv')
    output_dir.mkdir(exist_ok=True)

    for subset_dir in base_directory.iterdir():
        if subset_dir.is_dir():
            feas, labels, timestamps, file_ids = load_data(subset_dir)
            output_file = output_dir / f'{subset_dir.name}.csv'
            save_to_csv(feas, labels, timestamps, file_ids, output_file)
