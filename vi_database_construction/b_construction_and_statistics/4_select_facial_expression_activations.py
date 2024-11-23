import csv
import json
from pathlib import Path


def find_and_save_expression_weights(dataset_path, facial_recordings_path):
    output_path = dataset_path.parent / 'emoji-hero-vr-db-facial-expression-activations'
    output_path.mkdir(parents=True, exist_ok=True)

    for image_file in dataset_path.rglob('*-0.jpg'):

        # jpg file name convention:
        # <timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>-<camera-index>.jpg
        file_name_parts = image_file.stem.split('-')
        file_timestamp = int(file_name_parts[0])
        participant_id = file_name_parts[2]

        csv_file_path = facial_recordings_path / participant_id / 'faceexpressions.csv'

        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            found = False
            reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                if row:
                    row_ts = int(row[0])
                    if abs(file_timestamp - row_ts) <= 5:
                        try:
                            expression_weights = json.loads(row[4])['ExpressionWeights']

                            # Remove camera index from file name
                            json_file_name = '-'.join(file_name_parts[:-1]) + '.json'

                            output_json_path = output_path / image_file.relative_to(dataset_path).parent / json_file_name
                            output_json_path.parent.mkdir(parents=True, exist_ok=True)
                            with open(output_json_path, 'w', encoding='utf-8') as json_file:
                                json.dump(expression_weights, json_file)

                            found = True
                            break
                        except json.JSONDecodeError:
                            print(f'Invalid JSON in {csv_file_path} for timestamp {file_timestamp}. Skipping...')

            if not found:
                print(f'No expression weights found for participant {participant_id} for timestamp {file_timestamp}.')


if __name__ == '__main__':
    dataset_path = Path(r'/media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-db-images-224')
    facial_recordings_path = Path(r'/media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings')
    find_and_save_expression_weights(dataset_path, facial_recordings_path)

# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566360473. Skipping...
# No expression weights found for participant 7 for timestamp 1700566360473.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566368554. Skipping...
# No expression weights found for participant 7 for timestamp 1700566368554.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566370537. Skipping...
# No expression weights found for participant 7 for timestamp 1700566370537.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566575385. Skipping...
# No expression weights found for participant 7 for timestamp 1700566575385.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566591118. Skipping...
# No expression weights found for participant 7 for timestamp 1700566591118.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566750284. Skipping...
# No expression weights found for participant 7 for timestamp 1700566750284.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566756199. Skipping...
# No expression weights found for participant 7 for timestamp 1700566756199.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566763172. Skipping...
# No expression weights found for participant 7 for timestamp 1700566763172.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566776707. Skipping...
# No expression weights found for participant 7 for timestamp 1700566776707.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566378592. Skipping...
# No expression weights found for participant 7 for timestamp 1700566378592.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566582653. Skipping...
# No expression weights found for participant 7 for timestamp 1700566582653.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566584746. Skipping...
# No expression weights found for participant 7 for timestamp 1700566584746.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566601149. Skipping...
# No expression weights found for participant 7 for timestamp 1700566601149.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566739900. Skipping...
# No expression weights found for participant 7 for timestamp 1700566739900.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566768553. Skipping...
# No expression weights found for participant 7 for timestamp 1700566768553.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566365489. Skipping...
# No expression weights found for participant 7 for timestamp 1700566365489.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566375750. Skipping...
# No expression weights found for participant 7 for timestamp 1700566375750.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566380398. Skipping...
# No expression weights found for participant 7 for timestamp 1700566380398.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566578554. Skipping...
# No expression weights found for participant 7 for timestamp 1700566578554.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566593020. Skipping...
# No expression weights found for participant 7 for timestamp 1700566593020.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566604908. Skipping...
# No expression weights found for participant 7 for timestamp 1700566604908.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566748186. Skipping...
# No expression weights found for participant 7 for timestamp 1700566748186.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566757865. Skipping...
# No expression weights found for participant 7 for timestamp 1700566757865.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566780730. Skipping...
# No expression weights found for participant 7 for timestamp 1700566780730.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566451956. Skipping...
# No expression weights found for participant 7 for timestamp 1700566451956.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566469866. Skipping...
# No expression weights found for participant 7 for timestamp 1700566469866.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566480238. Skipping...
# No expression weights found for participant 7 for timestamp 1700566480238.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566569894. Skipping...
# No expression weights found for participant 7 for timestamp 1700566569894.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566594120. Skipping...
# No expression weights found for participant 7 for timestamp 1700566594120.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566599215. Skipping...
# No expression weights found for participant 7 for timestamp 1700566599215.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566741767. Skipping...
# No expression weights found for participant 7 for timestamp 1700566741767.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566745158. Skipping...
# No expression weights found for participant 7 for timestamp 1700566745158.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566747392. Skipping...
# No expression weights found for participant 7 for timestamp 1700566747392.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566769680. Skipping...
# No expression weights found for participant 7 for timestamp 1700566769680.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566457312. Skipping...
# No expression weights found for participant 7 for timestamp 1700566457312.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566471449. Skipping...
# No expression weights found for participant 7 for timestamp 1700566471449.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566577455. Skipping...
# No expression weights found for participant 7 for timestamp 1700566577455.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566596617. Skipping...
# No expression weights found for participant 7 for timestamp 1700566596617.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566609011. Skipping...
# No expression weights found for participant 7 for timestamp 1700566609011.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566743230. Skipping...
# No expression weights found for participant 7 for timestamp 1700566743230.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566771764. Skipping...
# No expression weights found for participant 7 for timestamp 1700566771764.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566785956. Skipping...
# No expression weights found for participant 7 for timestamp 1700566785956.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566460103. Skipping...
# No expression weights found for participant 7 for timestamp 1700566460103.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566468011. Skipping...
# No expression weights found for participant 7 for timestamp 1700566468011.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566603144. Skipping...
# No expression weights found for participant 7 for timestamp 1700566603144.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566754162. Skipping...
# No expression weights found for participant 7 for timestamp 1700566754162.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566782497. Skipping...
# No expression weights found for participant 7 for timestamp 1700566782497.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566462521. Skipping...
# No expression weights found for participant 7 for timestamp 1700566462521.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566589454. Skipping...
# No expression weights found for participant 7 for timestamp 1700566589454.
# Invalid JSON in /media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings/7/faceexpressions.csv for timestamp 1700566738359. Skipping...
# No expression weights found for participant 7 for timestamp 1700566738359.
# No expression weights found for participant 31 for timestamp 1701188073794.
