import csv
import json
from collections import defaultdict
from pathlib import Path

def find_and_save_expression_weights(dataset_path, facial_recordings_path):
    output_path = dataset_path.parent / 'emoji-hero-vr-db-facial-expression-activation-sequences'
    output_path.mkdir(parents=True, exist_ok=True)
    error_collection = defaultdict(list)

    time_differences = [5, 10, 15, 20, 30]
    td_counter = defaultdict(int)

    i = 0
    for image_file in dataset_path.rglob('*-0.png'):
        i += 1
        if i % 500 == 0:
            print(f'Processing file {i} : {image_file}')

        # png file name convention:
        # <timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>-<camera-index>.png
        file_name_parts = image_file.stem.split('-')
        file_timestamp = int(file_name_parts[0])
        participant_id = file_name_parts[2]

        csv_file_path = facial_recordings_path / participant_id / 'faceexpressions.csv'

        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            found = False
            reader = csv.reader(csv_file, delimiter=';')
            rows = list(reader)

            for max_diff in time_differences:
                for row in rows:
                    if not row:
                        continue
                    row_ts = int(row[0])
                    if abs(file_timestamp - row_ts) <= max_diff:
                        try:
                            expression_weights = json.loads(row[4])['ExpressionWeights']

                            # Remove camera index from file name
                            json_file_name = '-'.join(file_name_parts[:-1]) + '.json'

                            # Remove camera index from directory name
                            output_json_path = output_path / (str(image_file.relative_to(dataset_path).parent)[:-2]) / json_file_name
                            output_json_path.parent.mkdir(parents=True, exist_ok=True)

                            with open(output_json_path, 'w', encoding='utf-8') as json_file:
                                json.dump(expression_weights, json_file)

                            found = True
                            td_counter[max_diff] += 1

                            if max_diff >= 15:
                                print(f'Found expression weights for participant {participant_id} for timestamp {file_timestamp} with difference >= {max_diff} milliseconds.')
                            break
                        except json.JSONDecodeError:
                            continue
                if found:
                    break

            if not found:
                error_collection[participant_id].append(file_timestamp)
                print(f'No expression weights found for participant {participant_id} for timestamp {file_timestamp}.')

    print("\nTime Difference Categories:")
    for max_diff in sorted(td_counter.keys()):
        print(f"  <= {max_diff} ms: {td_counter[max_diff]} files")

    for participant_id, file_timestamps in sorted(error_collection.items()):
        print(f'No expression weights found for {len(file_timestamps)} timestamps of participant {participant_id}: {file_timestamps}')

if __name__ == '__main__':
    dataset_path = Path(r'/media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution')
    facial_recordings_path = Path(r'/media/thor/PortableSSD/mydata/emojihero/participant-data/facial-recordings')
    find_and_save_expression_weights(dataset_path, facial_recordings_path)

# Manually removed /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-db-facial-expression-activation-sequences/training_set/Disgust/1701188073794-0-31-2-5-1 after execution
# because 1701188073794-0-31-2-5-1 is not included in the static version
# because, for the static version, we defined that abs(file_timestamp - row_ts) <= 5 had to be true for all included samples.
# This way, the result is exactly 1,727 sequences, each of exactly 30 elements.
#
# Console output:
# Processing file 500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Anger/1700577843732-2-10-3-2-0-0/1700577843374-2-10-3-2-0-0.png
# Processing file 1000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Anger/1700756280474-2-18-1-3-0-0/1700756280015-2-18-1-3-0-0.png
# Processing file 1500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Anger/1701094445452-2-27-1-3-0-0/1701094445425-2-27-1-3-0-0.png
# Found expression weights for participant 27 for timestamp 1701094656197 with difference >= 15 milliseconds.
# Processing file 2000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Sadness/1700568077758-2-8-4-1-5-0/1700568077495-2-8-4-1-5-0.png
# Found expression weights for participant 10 for timestamp 1700577851443 with difference >= 15 milliseconds.
# Processing file 2500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Sadness/1700747359928-2-15-3-7-5-0/1700747359662-2-15-3-7-5-0.png
# Processing file 3000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Sadness/1701085633973-2-23-3-15-5-0/1701085633933-2-23-3-15-5-0.png
# Processing file 3500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Happiness/1700567708570-2-8-1-8-3-0/1700567708194-2-8-1-8-3-0.png
# Processing file 4000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Happiness/1700584244435-2-13-4-24-3-0/1700584243740-2-13-4-24-3-0.png
# Processing file 4500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Happiness/1701085409026-2-23-1-6-3-0/1701085408985-2-23-1-6-3-0.png
# Processing file 5000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Neutral/1700479265444-2-1-3-14-4-0/1700479265541-2-1-3-14-4-0.png
# Processing file 5500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Neutral/1700583999169-2-13-3-0-4-0/1700583998664-2-13-3-0-4-0.png
# Processing file 6000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Neutral/1700756711213-2-18-4-4-4-0/1700756711556-2-18-4-4-4-0.png
# Processing file 6500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Disgust/1700479106931-2-1-2-1-1-0/1700479106569-2-1-2-1-1-0.png
# Processing file 7000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Disgust/1700568121727-2-8-4-26-1-0/1700568121019-2-8-4-26-1-0.png
# Processing file 7500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Disgust/1700747240521-2-15-2-5-1-0/1700747240479-2-15-2-5-1-0.png
# Processing file 8000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Disgust/1701085829241-2-23-4-26-1-0/1701085828875-2-23-4-26-1-0.png
# Processing file 8500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Surprise/1700577751365-2-10-2-8-6-0/1700577750666-2-10-2-8-6-0.png
# Processing file 9000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Surprise/1700747352492-2-15-3-3-6-0/1700747352464-2-15-3-3-6-0.png
# Processing file 9500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Surprise/1701085830697-2-23-4-27-6-0/1701085830327-2-23-4-27-6-0.png
# Processing file 10000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Fear/1700567809324-2-8-2-10-2-0/1700567808822-2-8-2-10-2-0.png
# Processing file 10500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Fear/1700583891213-2-13-2-3-2-0/1700583891160-2-13-2-3-2-0.png
# Found expression weights for participant 15 for timestamp 1700747252797 with difference >= 15 milliseconds.
# Processing file 11000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/test_set/Fear/1701085635772-2-23-3-16-2-0/1701085635405-2-23-3-16-2-0.png
# Processing file 11500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Anger/1700489875595-0-4-3-10-0-0/1700489874900-0-4-3-10-0-0.png
# No expression weights found for participant 7 for timestamp 1700566360473.
# No expression weights found for participant 7 for timestamp 1700566359501.
# No expression weights found for participant 7 for timestamp 1700566359542.
# No expression weights found for participant 7 for timestamp 1700566359571.
# No expression weights found for participant 7 for timestamp 1700566359624.
# No expression weights found for participant 7 for timestamp 1700566359653.
# No expression weights found for participant 7 for timestamp 1700566359666.
# No expression weights found for participant 7 for timestamp 1700566359708.
# No expression weights found for participant 7 for timestamp 1700566359736.
# No expression weights found for participant 7 for timestamp 1700566359778.
# No expression weights found for participant 7 for timestamp 1700566359805.
# No expression weights found for participant 7 for timestamp 1700566359833.
# No expression weights found for participant 7 for timestamp 1700566359876.
# No expression weights found for participant 7 for timestamp 1700566359903.
# No expression weights found for participant 7 for timestamp 1700566359955.
# No expression weights found for participant 7 for timestamp 1700566359974.
# No expression weights found for participant 7 for timestamp 1700566359999.
# No expression weights found for participant 7 for timestamp 1700566360041.
# No expression weights found for participant 7 for timestamp 1700566360068.
# No expression weights found for participant 7 for timestamp 1700566360110.
# No expression weights found for participant 7 for timestamp 1700566360139.
# No expression weights found for participant 7 for timestamp 1700566360195.
# No expression weights found for participant 7 for timestamp 1700566360261.
# No expression weights found for participant 7 for timestamp 1700566360318.
# No expression weights found for participant 7 for timestamp 1700566360370.
# No expression weights found for participant 7 for timestamp 1700566360397.
# No expression weights found for participant 7 for timestamp 1700566360408.
# No expression weights found for participant 7 for timestamp 1700566360420.
# No expression weights found for participant 7 for timestamp 1700566360433.
# No expression weights found for participant 7 for timestamp 1700566360446.
# No expression weights found for participant 7 for timestamp 1700566368554.
# No expression weights found for participant 7 for timestamp 1700566367595.
# No expression weights found for participant 7 for timestamp 1700566367623.
# No expression weights found for participant 7 for timestamp 1700566367650.
# No expression weights found for participant 7 for timestamp 1700566367692.
# No expression weights found for participant 7 for timestamp 1700566367722.
# No expression weights found for participant 7 for timestamp 1700566367748.
# No expression weights found for participant 7 for timestamp 1700566367789.
# No expression weights found for participant 7 for timestamp 1700566367816.
# No expression weights found for participant 7 for timestamp 1700566367858.
# No expression weights found for participant 7 for timestamp 1700566367886.
# No expression weights found for participant 7 for timestamp 1700566367927.
# No expression weights found for participant 7 for timestamp 1700566367956.
# No expression weights found for participant 7 for timestamp 1700566367983.
# No expression weights found for participant 7 for timestamp 1700566368027.
# No expression weights found for participant 7 for timestamp 1700566368054.
# No expression weights found for participant 7 for timestamp 1700566368094.
# No expression weights found for participant 7 for timestamp 1700566368122.
# No expression weights found for participant 7 for timestamp 1700566368148.
# No expression weights found for participant 7 for timestamp 1700566368201.
# No expression weights found for participant 7 for timestamp 1700566368255.
# No expression weights found for participant 7 for timestamp 1700566368310.
# No expression weights found for participant 7 for timestamp 1700566368380.
# No expression weights found for participant 7 for timestamp 1700566368401.
# No expression weights found for participant 7 for timestamp 1700566368421.
# No expression weights found for participant 7 for timestamp 1700566368435.
# No expression weights found for participant 7 for timestamp 1700566368449.
# No expression weights found for participant 7 for timestamp 1700566368462.
# No expression weights found for participant 7 for timestamp 1700566368489.
# No expression weights found for participant 7 for timestamp 1700566368515.
# No expression weights found for participant 7 for timestamp 1700566370537.
# No expression weights found for participant 7 for timestamp 1700566369566.
# No expression weights found for participant 7 for timestamp 1700566369593.
# No expression weights found for participant 7 for timestamp 1700566369635.
# No expression weights found for participant 7 for timestamp 1700566369660.
# No expression weights found for participant 7 for timestamp 1700566369704.
# No expression weights found for participant 7 for timestamp 1700566369732.
# No expression weights found for participant 7 for timestamp 1700566369760.
# No expression weights found for participant 7 for timestamp 1700566369800.
# No expression weights found for participant 7 for timestamp 1700566369827.
# No expression weights found for participant 7 for timestamp 1700566369869.
# No expression weights found for participant 7 for timestamp 1700566369897.
# No expression weights found for participant 7 for timestamp 1700566369938.
# No expression weights found for participant 7 for timestamp 1700566369966.
# No expression weights found for participant 7 for timestamp 1700566369993.
# No expression weights found for participant 7 for timestamp 1700566370035.
# No expression weights found for participant 7 for timestamp 1700566370063.
# No expression weights found for participant 7 for timestamp 1700566370106.
# No expression weights found for participant 7 for timestamp 1700566370134.
# No expression weights found for participant 7 for timestamp 1700566370161.
# No expression weights found for participant 7 for timestamp 1700566370204.
# No expression weights found for participant 7 for timestamp 1700566370234.
# No expression weights found for participant 7 for timestamp 1700566370261.
# No expression weights found for participant 7 for timestamp 1700566370301.
# No expression weights found for participant 7 for timestamp 1700566370329.
# No expression weights found for participant 7 for timestamp 1700566370370.
# No expression weights found for participant 7 for timestamp 1700566370399.
# No expression weights found for participant 7 for timestamp 1700566370426.
# No expression weights found for participant 7 for timestamp 1700566370468.
# No expression weights found for participant 7 for timestamp 1700566370496.
# No expression weights found for participant 7 for timestamp 1700566575385.
# No expression weights found for participant 7 for timestamp 1700566574480.
# No expression weights found for participant 7 for timestamp 1700566574534.
# No expression weights found for participant 7 for timestamp 1700566574546.
# No expression weights found for participant 7 for timestamp 1700566574560.
# No expression weights found for participant 7 for timestamp 1700566574573.
# No expression weights found for participant 7 for timestamp 1700566574600.
# No expression weights found for participant 7 for timestamp 1700566574620.
# No expression weights found for participant 7 for timestamp 1700566574654.
# No expression weights found for participant 7 for timestamp 1700566574694.
# No expression weights found for participant 7 for timestamp 1700566574721.
# No expression weights found for participant 7 for timestamp 1700566574749.
# No expression weights found for participant 7 for timestamp 1700566574790.
# No expression weights found for participant 7 for timestamp 1700566574818.
# No expression weights found for participant 7 for timestamp 1700566574859.
# No expression weights found for participant 7 for timestamp 1700566574886.
# No expression weights found for participant 7 for timestamp 1700566574930.
# No expression weights found for participant 7 for timestamp 1700566574956.
# No expression weights found for participant 7 for timestamp 1700566574983.
# No expression weights found for participant 7 for timestamp 1700566575025.
# No expression weights found for participant 7 for timestamp 1700566575053.
# No expression weights found for participant 7 for timestamp 1700566575095.
# No expression weights found for participant 7 for timestamp 1700566575122.
# No expression weights found for participant 7 for timestamp 1700566575150.
# No expression weights found for participant 7 for timestamp 1700566575193.
# No expression weights found for participant 7 for timestamp 1700566575218.
# No expression weights found for participant 7 for timestamp 1700566575259.
# No expression weights found for participant 7 for timestamp 1700566575287.
# No expression weights found for participant 7 for timestamp 1700566575315.
# No expression weights found for participant 7 for timestamp 1700566575358.
# No expression weights found for participant 7 for timestamp 1700566591118.
# No expression weights found for participant 7 for timestamp 1700566590150.
# No expression weights found for participant 7 for timestamp 1700566590191.
# No expression weights found for participant 7 for timestamp 1700566590219.
# No expression weights found for participant 7 for timestamp 1700566590246.
# No expression weights found for participant 7 for timestamp 1700566590288.
# No expression weights found for participant 7 for timestamp 1700566590329.
# No expression weights found for participant 7 for timestamp 1700566590345.
# No expression weights found for participant 7 for timestamp 1700566590384.
# No expression weights found for participant 7 for timestamp 1700566590412.
# No expression weights found for participant 7 for timestamp 1700566590454.
# No expression weights found for participant 7 for timestamp 1700566590482.
# No expression weights found for participant 7 for timestamp 1700566590511.
# No expression weights found for participant 7 for timestamp 1700566590555.
# No expression weights found for participant 7 for timestamp 1700566590598.
# No expression weights found for participant 7 for timestamp 1700566590650.
# No expression weights found for participant 7 for timestamp 1700566590721.
# No expression weights found for participant 7 for timestamp 1700566590732.
# No expression weights found for participant 7 for timestamp 1700566590746.
# No expression weights found for participant 7 for timestamp 1700566590760.
# No expression weights found for participant 7 for timestamp 1700566590786.
# No expression weights found for participant 7 for timestamp 1700566590814.
# No expression weights found for participant 7 for timestamp 1700566590855.
# No expression weights found for participant 7 for timestamp 1700566590883.
# No expression weights found for participant 7 for timestamp 1700566590911.
# No expression weights found for participant 7 for timestamp 1700566590954.
# No expression weights found for participant 7 for timestamp 1700566590979.
# No expression weights found for participant 7 for timestamp 1700566591021.
# No expression weights found for participant 7 for timestamp 1700566591048.
# No expression weights found for participant 7 for timestamp 1700566591090.
# No expression weights found for participant 7 for timestamp 1700566750284.
# No expression weights found for participant 7 for timestamp 1700566749385.
# No expression weights found for participant 7 for timestamp 1700566749423.
# No expression weights found for participant 7 for timestamp 1700566749464.
# No expression weights found for participant 7 for timestamp 1700566749492.
# No expression weights found for participant 7 for timestamp 1700566749520.
# No expression weights found for participant 7 for timestamp 1700566749562.
# No expression weights found for participant 7 for timestamp 1700566749589.
# No expression weights found for participant 7 for timestamp 1700566749631.
# No expression weights found for participant 7 for timestamp 1700566749659.
# No expression weights found for participant 7 for timestamp 1700566749687.
# No expression weights found for participant 7 for timestamp 1700566749728.
# No expression weights found for participant 7 for timestamp 1700566749756.
# No expression weights found for participant 7 for timestamp 1700566749798.
# No expression weights found for participant 7 for timestamp 1700566749826.
# No expression weights found for participant 7 for timestamp 1700566749854.
# No expression weights found for participant 7 for timestamp 1700566749897.
# No expression weights found for participant 7 for timestamp 1700566749923.
# No expression weights found for participant 7 for timestamp 1700566749965.
# No expression weights found for participant 7 for timestamp 1700566749992.
# No expression weights found for participant 7 for timestamp 1700566750020.
# No expression weights found for participant 7 for timestamp 1700566750062.
# No expression weights found for participant 7 for timestamp 1700566750090.
# No expression weights found for participant 7 for timestamp 1700566750131.
# No expression weights found for participant 7 for timestamp 1700566750159.
# No expression weights found for participant 7 for timestamp 1700566750187.
# No expression weights found for participant 7 for timestamp 1700566750227.
# No expression weights found for participant 7 for timestamp 1700566750336.
# No expression weights found for participant 7 for timestamp 1700566750390.
# No expression weights found for participant 7 for timestamp 1700566750456.
# No expression weights found for participant 7 for timestamp 1700566756199.
# No expression weights found for participant 7 for timestamp 1700566755241.
# No expression weights found for participant 7 for timestamp 1700566755268.
# No expression weights found for participant 7 for timestamp 1700566755296.
# No expression weights found for participant 7 for timestamp 1700566755338.
# No expression weights found for participant 7 for timestamp 1700566755366.
# No expression weights found for participant 7 for timestamp 1700566755407.
# No expression weights found for participant 7 for timestamp 1700566755433.
# No expression weights found for participant 7 for timestamp 1700566755476.
# No expression weights found for participant 7 for timestamp 1700566755505.
# No expression weights found for participant 7 for timestamp 1700566755531.
# No expression weights found for participant 7 for timestamp 1700566755574.
# No expression weights found for participant 7 for timestamp 1700566755601.
# No expression weights found for participant 7 for timestamp 1700566755629.
# No expression weights found for participant 7 for timestamp 1700566755670.
# No expression weights found for participant 7 for timestamp 1700566755698.
# No expression weights found for participant 7 for timestamp 1700566755741.
# No expression weights found for participant 7 for timestamp 1700566755770.
# No expression weights found for participant 7 for timestamp 1700566755797.
# No expression weights found for participant 7 for timestamp 1700566755837.
# No expression weights found for participant 7 for timestamp 1700566755865.
# No expression weights found for participant 7 for timestamp 1700566755907.
# No expression weights found for participant 7 for timestamp 1700566755935.
# No expression weights found for participant 7 for timestamp 1700566755963.
# No expression weights found for participant 7 for timestamp 1700566756004.
# No expression weights found for participant 7 for timestamp 1700566756032.
# No expression weights found for participant 7 for timestamp 1700566756060.
# No expression weights found for participant 7 for timestamp 1700566756103.
# No expression weights found for participant 7 for timestamp 1700566756129.
# No expression weights found for participant 7 for timestamp 1700566756171.
# No expression weights found for participant 7 for timestamp 1700566763172.
# No expression weights found for participant 7 for timestamp 1700566762199.
# No expression weights found for participant 7 for timestamp 1700566762226.
# No expression weights found for participant 7 for timestamp 1700566762267.
# No expression weights found for participant 7 for timestamp 1700566762296.
# No expression weights found for participant 7 for timestamp 1700566762323.
# No expression weights found for participant 7 for timestamp 1700566762365.
# No expression weights found for participant 7 for timestamp 1700566762393.
# No expression weights found for participant 7 for timestamp 1700566762435.
# No expression weights found for participant 7 for timestamp 1700566762463.
# No expression weights found for participant 7 for timestamp 1700566762490.
# No expression weights found for participant 7 for timestamp 1700566762531.
# No expression weights found for participant 7 for timestamp 1700566762559.
# No expression weights found for participant 7 for timestamp 1700566762601.
# No expression weights found for participant 7 for timestamp 1700566762628.
# No expression weights found for participant 7 for timestamp 1700566762657.
# No expression weights found for participant 7 for timestamp 1700566762698.
# No expression weights found for participant 7 for timestamp 1700566762726.
# No expression weights found for participant 7 for timestamp 1700566762767.
# No expression weights found for participant 7 for timestamp 1700566762798.
# No expression weights found for participant 7 for timestamp 1700566762823.
# No expression weights found for participant 7 for timestamp 1700566762865.
# No expression weights found for participant 7 for timestamp 1700566762894.
# No expression weights found for participant 7 for timestamp 1700566762950.
# No expression weights found for participant 7 for timestamp 1700566762994.
# No expression weights found for participant 7 for timestamp 1700566763038.
# No expression weights found for participant 7 for timestamp 1700566763119.
# No expression weights found for participant 7 for timestamp 1700566763136.
# No expression weights found for participant 7 for timestamp 1700566763144.
# No expression weights found for participant 7 for timestamp 1700566763158.
# No expression weights found for participant 7 for timestamp 1700566776707.
# No expression weights found for participant 7 for timestamp 1700566775769.
# No expression weights found for participant 7 for timestamp 1700566775806.
# No expression weights found for participant 7 for timestamp 1700566775848.
# No expression weights found for participant 7 for timestamp 1700566775876.
# No expression weights found for participant 7 for timestamp 1700566775904.
# No expression weights found for participant 7 for timestamp 1700566775945.
# No expression weights found for participant 7 for timestamp 1700566775973.
# No expression weights found for participant 7 for timestamp 1700566776015.
# No expression weights found for participant 7 for timestamp 1700566776043.
# No expression weights found for participant 7 for timestamp 1700566776070.
# No expression weights found for participant 7 for timestamp 1700566776112.
# No expression weights found for participant 7 for timestamp 1700566776140.
# No expression weights found for participant 7 for timestamp 1700566776182.
# No expression weights found for participant 7 for timestamp 1700566776209.
# No expression weights found for participant 7 for timestamp 1700566776237.
# No expression weights found for participant 7 for timestamp 1700566776289.
# No expression weights found for participant 7 for timestamp 1700566776307.
# No expression weights found for participant 7 for timestamp 1700566776347.
# No expression weights found for participant 7 for timestamp 1700566776376.
# No expression weights found for participant 7 for timestamp 1700566776403.
# No expression weights found for participant 7 for timestamp 1700566776445.
# No expression weights found for participant 7 for timestamp 1700566776473.
# No expression weights found for participant 7 for timestamp 1700566776514.
# No expression weights found for participant 7 for timestamp 1700566776542.
# No expression weights found for participant 7 for timestamp 1700566776570.
# No expression weights found for participant 7 for timestamp 1700566776610.
# No expression weights found for participant 7 for timestamp 1700566776637.
# No expression weights found for participant 7 for timestamp 1700566776679.
# No expression weights found for participant 7 for timestamp 1700566776749.
# Processing file 12000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Anger/1700580678854-0-11-4-7-0-0/1700580679179-0-11-4-7-0-0.png
# Processing file 12500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Anger/1700825936279-0-20-3-8-0-0/1700825935916-0-20-3-8-0-0.png
# Processing file 13000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Anger/1701092964618-0-26-4-10-0-0/1701092964215-0-26-4-10-0-0.png
# Processing file 13500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Anger/1701429635504-0-35-4-14-0-0/1701429635477-0-35-4-14-0-0.png
# Processing file 14000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Sadness/1700489885562-0-4-3-15-5-0/1700489885227-0-4-3-15-5-0.png
# No expression weights found for participant 7 for timestamp 1700566378592.
# No expression weights found for participant 7 for timestamp 1700566377634.
# No expression weights found for participant 7 for timestamp 1700566377662.
# No expression weights found for participant 7 for timestamp 1700566377689.
# No expression weights found for participant 7 for timestamp 1700566377731.
# No expression weights found for participant 7 for timestamp 1700566377759.
# No expression weights found for participant 7 for timestamp 1700566377800.
# No expression weights found for participant 7 for timestamp 1700566377828.
# No expression weights found for participant 7 for timestamp 1700566377856.
# No expression weights found for participant 7 for timestamp 1700566377898.
# No expression weights found for participant 7 for timestamp 1700566377925.
# No expression weights found for participant 7 for timestamp 1700566377967.
# No expression weights found for participant 7 for timestamp 1700566377995.
# No expression weights found for participant 7 for timestamp 1700566378023.
# No expression weights found for participant 7 for timestamp 1700566378067.
# No expression weights found for participant 7 for timestamp 1700566378092.
# No expression weights found for participant 7 for timestamp 1700566378134.
# No expression weights found for participant 7 for timestamp 1700566378162.
# No expression weights found for participant 7 for timestamp 1700566378189.
# No expression weights found for participant 7 for timestamp 1700566378231.
# No expression weights found for participant 7 for timestamp 1700566378259.
# No expression weights found for participant 7 for timestamp 1700566378301.
# No expression weights found for participant 7 for timestamp 1700566378329.
# No expression weights found for participant 7 for timestamp 1700566378356.
# No expression weights found for participant 7 for timestamp 1700566378398.
# No expression weights found for participant 7 for timestamp 1700566378425.
# No expression weights found for participant 7 for timestamp 1700566378467.
# No expression weights found for participant 7 for timestamp 1700566378495.
# No expression weights found for participant 7 for timestamp 1700566378522.
# No expression weights found for participant 7 for timestamp 1700566378564.
# No expression weights found for participant 7 for timestamp 1700566582653.
# No expression weights found for participant 7 for timestamp 1700566581692.
# No expression weights found for participant 7 for timestamp 1700566581720.
# No expression weights found for participant 7 for timestamp 1700566581747.
# No expression weights found for participant 7 for timestamp 1700566581789.
# No expression weights found for participant 7 for timestamp 1700566581816.
# No expression weights found for participant 7 for timestamp 1700566581858.
# No expression weights found for participant 7 for timestamp 1700566581886.
# No expression weights found for participant 7 for timestamp 1700566581915.
# No expression weights found for participant 7 for timestamp 1700566581956.
# No expression weights found for participant 7 for timestamp 1700566581984.
# No expression weights found for participant 7 for timestamp 1700566582014.
# No expression weights found for participant 7 for timestamp 1700566582054.
# No expression weights found for participant 7 for timestamp 1700566582080.
# No expression weights found for participant 7 for timestamp 1700566582122.
# No expression weights found for participant 7 for timestamp 1700566582151.
# No expression weights found for participant 7 for timestamp 1700566582192.
# No expression weights found for participant 7 for timestamp 1700566582220.
# No expression weights found for participant 7 for timestamp 1700566582248.
# No expression weights found for participant 7 for timestamp 1700566582290.
# No expression weights found for participant 7 for timestamp 1700566582332.
# No expression weights found for participant 7 for timestamp 1700566582355.
# No expression weights found for participant 7 for timestamp 1700566582387.
# No expression weights found for participant 7 for timestamp 1700566582415.
# No expression weights found for participant 7 for timestamp 1700566582456.
# No expression weights found for participant 7 for timestamp 1700566582484.
# No expression weights found for participant 7 for timestamp 1700566582526.
# No expression weights found for participant 7 for timestamp 1700566582553.
# No expression weights found for participant 7 for timestamp 1700566582581.
# No expression weights found for participant 7 for timestamp 1700566582624.
# No expression weights found for participant 7 for timestamp 1700566584746.
# No expression weights found for participant 7 for timestamp 1700566583788.
# No expression weights found for participant 7 for timestamp 1700566583816.
# No expression weights found for participant 7 for timestamp 1700566583857.
# No expression weights found for participant 7 for timestamp 1700566583885.
# No expression weights found for participant 7 for timestamp 1700566583913.
# No expression weights found for participant 7 for timestamp 1700566583955.
# No expression weights found for participant 7 for timestamp 1700566583983.
# No expression weights found for participant 7 for timestamp 1700566584029.
# No expression weights found for participant 7 for timestamp 1700566584049.
# No expression weights found for participant 7 for timestamp 1700566584091.
# No expression weights found for participant 7 for timestamp 1700566584119.
# No expression weights found for participant 7 for timestamp 1700566584147.
# No expression weights found for participant 7 for timestamp 1700566584190.
# No expression weights found for participant 7 for timestamp 1700566584218.
# No expression weights found for participant 7 for timestamp 1700566584245.
# No expression weights found for participant 7 for timestamp 1700566584288.
# No expression weights found for participant 7 for timestamp 1700566584318.
# No expression weights found for participant 7 for timestamp 1700566584357.
# No expression weights found for participant 7 for timestamp 1700566584385.
# No expression weights found for participant 7 for timestamp 1700566584413.
# No expression weights found for participant 7 for timestamp 1700566584455.
# No expression weights found for participant 7 for timestamp 1700566584482.
# No expression weights found for participant 7 for timestamp 1700566584524.
# No expression weights found for participant 7 for timestamp 1700566584552.
# No expression weights found for participant 7 for timestamp 1700566584580.
# No expression weights found for participant 7 for timestamp 1700566584623.
# No expression weights found for participant 7 for timestamp 1700566584652.
# No expression weights found for participant 7 for timestamp 1700566584692.
# No expression weights found for participant 7 for timestamp 1700566584720.
# No expression weights found for participant 7 for timestamp 1700566601149.
# No expression weights found for participant 7 for timestamp 1700566600186.
# No expression weights found for participant 7 for timestamp 1700566600214.
# No expression weights found for participant 7 for timestamp 1700566600256.
# No expression weights found for participant 7 for timestamp 1700566600283.
# No expression weights found for participant 7 for timestamp 1700566600311.
# No expression weights found for participant 7 for timestamp 1700566600355.
# No expression weights found for participant 7 for timestamp 1700566600382.
# No expression weights found for participant 7 for timestamp 1700566600439.
# No expression weights found for participant 7 for timestamp 1700566600489.
# No expression weights found for participant 7 for timestamp 1700566600543.
# No expression weights found for participant 7 for timestamp 1700566600596.
# No expression weights found for participant 7 for timestamp 1700566600623.
# No expression weights found for participant 7 for timestamp 1700566600636.
# No expression weights found for participant 7 for timestamp 1700566600662.
# No expression weights found for participant 7 for timestamp 1700566600679.
# No expression weights found for participant 7 for timestamp 1700566600689.
# No expression weights found for participant 7 for timestamp 1700566600717.
# No expression weights found for participant 7 for timestamp 1700566600743.
# No expression weights found for participant 7 for timestamp 1700566600784.
# No expression weights found for participant 7 for timestamp 1700566600812.
# No expression weights found for participant 7 for timestamp 1700566600852.
# No expression weights found for participant 7 for timestamp 1700566600880.
# No expression weights found for participant 7 for timestamp 1700566600922.
# No expression weights found for participant 7 for timestamp 1700566600952.
# No expression weights found for participant 7 for timestamp 1700566600975.
# No expression weights found for participant 7 for timestamp 1700566601015.
# No expression weights found for participant 7 for timestamp 1700566601042.
# No expression weights found for participant 7 for timestamp 1700566601082.
# No expression weights found for participant 7 for timestamp 1700566601110.
# No expression weights found for participant 7 for timestamp 1700566739900.
# No expression weights found for participant 7 for timestamp 1700566738942.
# No expression weights found for participant 7 for timestamp 1700566738969.
# No expression weights found for participant 7 for timestamp 1700566738998.
# No expression weights found for participant 7 for timestamp 1700566739039.
# No expression weights found for participant 7 for timestamp 1700566739066.
# No expression weights found for participant 7 for timestamp 1700566739108.
# No expression weights found for participant 7 for timestamp 1700566739161.
# No expression weights found for participant 7 for timestamp 1700566739213.
# No expression weights found for participant 7 for timestamp 1700566739269.
# No expression weights found for participant 7 for timestamp 1700566739323.
# No expression weights found for participant 7 for timestamp 1700566739337.
# No expression weights found for participant 7 for timestamp 1700566739364.
# No expression weights found for participant 7 for timestamp 1700566739377.
# No expression weights found for participant 7 for timestamp 1700566739405.
# No expression weights found for participant 7 for timestamp 1700566739418.
# No expression weights found for participant 7 for timestamp 1700566739431.
# No expression weights found for participant 7 for timestamp 1700566739470.
# No expression weights found for participant 7 for timestamp 1700566739497.
# No expression weights found for participant 7 for timestamp 1700566739538.
# No expression weights found for participant 7 for timestamp 1700566739565.
# No expression weights found for participant 7 for timestamp 1700566739606.
# No expression weights found for participant 7 for timestamp 1700566739634.
# No expression weights found for participant 7 for timestamp 1700566739662.
# No expression weights found for participant 7 for timestamp 1700566739699.
# No expression weights found for participant 7 for timestamp 1700566739742.
# No expression weights found for participant 7 for timestamp 1700566739768.
# No expression weights found for participant 7 for timestamp 1700566739796.
# No expression weights found for participant 7 for timestamp 1700566739834.
# No expression weights found for participant 7 for timestamp 1700566739875.
# No expression weights found for participant 7 for timestamp 1700566768553.
# No expression weights found for participant 7 for timestamp 1700566767569.
# No expression weights found for participant 7 for timestamp 1700566767597.
# No expression weights found for participant 7 for timestamp 1700566767640.
# No expression weights found for participant 7 for timestamp 1700566767667.
# No expression weights found for participant 7 for timestamp 1700566767709.
# No expression weights found for participant 7 for timestamp 1700566767737.
# No expression weights found for participant 7 for timestamp 1700566767764.
# No expression weights found for participant 7 for timestamp 1700566767812.
# No expression weights found for participant 7 for timestamp 1700566767833.
# No expression weights found for participant 7 for timestamp 1700566767875.
# No expression weights found for participant 7 for timestamp 1700566767903.
# No expression weights found for participant 7 for timestamp 1700566767930.
# No expression weights found for participant 7 for timestamp 1700566767972.
# No expression weights found for participant 7 for timestamp 1700566768000.
# No expression weights found for participant 7 for timestamp 1700566768043.
# No expression weights found for participant 7 for timestamp 1700566768070.
# No expression weights found for participant 7 for timestamp 1700566768098.
# No expression weights found for participant 7 for timestamp 1700566768139.
# No expression weights found for participant 7 for timestamp 1700566768166.
# No expression weights found for participant 7 for timestamp 1700566768209.
# No expression weights found for participant 7 for timestamp 1700566768238.
# No expression weights found for participant 7 for timestamp 1700566768294.
# No expression weights found for participant 7 for timestamp 1700566768346.
# No expression weights found for participant 7 for timestamp 1700566768401.
# No expression weights found for participant 7 for timestamp 1700566768484.
# No expression weights found for participant 7 for timestamp 1700566768497.
# No expression weights found for participant 7 for timestamp 1700566768511.
# No expression weights found for participant 7 for timestamp 1700566768525.
# No expression weights found for participant 7 for timestamp 1700566768539.
# Processing file 14500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Sadness/1700582340968-0-12-4-8-5-0/1700582340258-0-12-4-8-5-0.png
# Processing file 15000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Sadness/1700825725786-0-20-1-1-5-0/1700825725731-0-20-1-1-5-0.png
# Processing file 15500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Sadness/1700827982043-0-21-4-8-5-0/1700827981732-0-21-4-8-5-0.png
# Processing file 16000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Sadness/1701170403137-0-28-1-1-5-0/1701170402433-0-28-1-1-5-0.png
# Processing file 16500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Sadness/1701178073468-0-30-4-8-5-0/1701178073413-0-30-4-8-5-0.png
# Processing file 17000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Sadness/1701350610834-0-33-4-8-5-0/1701350610538-0-33-4-8-5-0.png
# Processing file 17500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Sadness/1701429645979-0-35-4-20-5-0/1701429645283-0-35-4-20-5-0.png
# Processing file 18000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1700489639217-0-4-1-2-3-0/1700489639176-0-4-1-2-3-0.png
# No expression weights found for participant 7 for timestamp 1700566365489.
# No expression weights found for participant 7 for timestamp 1700566364525.
# No expression weights found for participant 7 for timestamp 1700566364554.
# No expression weights found for participant 7 for timestamp 1700566364581.
# No expression weights found for participant 7 for timestamp 1700566364628.
# No expression weights found for participant 7 for timestamp 1700566364653.
# No expression weights found for participant 7 for timestamp 1700566364681.
# No expression weights found for participant 7 for timestamp 1700566364721.
# No expression weights found for participant 7 for timestamp 1700566364748.
# No expression weights found for participant 7 for timestamp 1700566364790.
# No expression weights found for participant 7 for timestamp 1700566364818.
# No expression weights found for participant 7 for timestamp 1700566364860.
# No expression weights found for participant 7 for timestamp 1700566364887.
# No expression weights found for participant 7 for timestamp 1700566364918.
# No expression weights found for participant 7 for timestamp 1700566364958.
# No expression weights found for participant 7 for timestamp 1700566364986.
# No expression weights found for participant 7 for timestamp 1700566365026.
# No expression weights found for participant 7 for timestamp 1700566365054.
# No expression weights found for participant 7 for timestamp 1700566365082.
# No expression weights found for participant 7 for timestamp 1700566365123.
# No expression weights found for participant 7 for timestamp 1700566365151.
# No expression weights found for participant 7 for timestamp 1700566365193.
# No expression weights found for participant 7 for timestamp 1700566365248.
# No expression weights found for participant 7 for timestamp 1700566365302.
# No expression weights found for participant 7 for timestamp 1700566365351.
# No expression weights found for participant 7 for timestamp 1700566365408.
# No expression weights found for participant 7 for timestamp 1700566365421.
# No expression weights found for participant 7 for timestamp 1700566365436.
# No expression weights found for participant 7 for timestamp 1700566365449.
# No expression weights found for participant 7 for timestamp 1700566365463.
# No expression weights found for participant 7 for timestamp 1700566375750.
# No expression weights found for participant 7 for timestamp 1700566374733.
# No expression weights found for participant 7 for timestamp 1700566374761.
# No expression weights found for participant 7 for timestamp 1700566374802.
# No expression weights found for participant 7 for timestamp 1700566374830.
# No expression weights found for participant 7 for timestamp 1700566374858.
# No expression weights found for participant 7 for timestamp 1700566374900.
# No expression weights found for participant 7 for timestamp 1700566374928.
# No expression weights found for participant 7 for timestamp 1700566374961.
# No expression weights found for participant 7 for timestamp 1700566374996.
# No expression weights found for participant 7 for timestamp 1700566375024.
# No expression weights found for participant 7 for timestamp 1700566375066.
# No expression weights found for participant 7 for timestamp 1700566375094.
# No expression weights found for participant 7 for timestamp 1700566375136.
# No expression weights found for participant 7 for timestamp 1700566375163.
# No expression weights found for participant 7 for timestamp 1700566375192.
# No expression weights found for participant 7 for timestamp 1700566375233.
# No expression weights found for participant 7 for timestamp 1700566375261.
# No expression weights found for participant 7 for timestamp 1700566375303.
# No expression weights found for participant 7 for timestamp 1700566375331.
# No expression weights found for participant 7 for timestamp 1700566375358.
# No expression weights found for participant 7 for timestamp 1700566375400.
# No expression weights found for participant 7 for timestamp 1700566375427.
# No expression weights found for participant 7 for timestamp 1700566375468.
# No expression weights found for participant 7 for timestamp 1700566375495.
# No expression weights found for participant 7 for timestamp 1700566375550.
# No expression weights found for participant 7 for timestamp 1700566375604.
# No expression weights found for participant 7 for timestamp 1700566375655.
# No expression weights found for participant 7 for timestamp 1700566375710.
# No expression weights found for participant 7 for timestamp 1700566375738.
# No expression weights found for participant 7 for timestamp 1700566380398.
# No expression weights found for participant 7 for timestamp 1700566379427.
# No expression weights found for participant 7 for timestamp 1700566379455.
# No expression weights found for participant 7 for timestamp 1700566379497.
# No expression weights found for participant 7 for timestamp 1700566379524.
# No expression weights found for participant 7 for timestamp 1700566379566.
# No expression weights found for participant 7 for timestamp 1700566379594.
# No expression weights found for participant 7 for timestamp 1700566379622.
# No expression weights found for participant 7 for timestamp 1700566379668.
# No expression weights found for participant 7 for timestamp 1700566379693.
# No expression weights found for participant 7 for timestamp 1700566379734.
# No expression weights found for participant 7 for timestamp 1700566379761.
# No expression weights found for participant 7 for timestamp 1700566379788.
# No expression weights found for participant 7 for timestamp 1700566379830.
# No expression weights found for participant 7 for timestamp 1700566379858.
# No expression weights found for participant 7 for timestamp 1700566379900.
# No expression weights found for participant 7 for timestamp 1700566379927.
# No expression weights found for participant 7 for timestamp 1700566379971.
# No expression weights found for participant 7 for timestamp 1700566380029.
# No expression weights found for participant 7 for timestamp 1700566380083.
# No expression weights found for participant 7 for timestamp 1700566380127.
# No expression weights found for participant 7 for timestamp 1700566380181.
# No expression weights found for participant 7 for timestamp 1700566380209.
# No expression weights found for participant 7 for timestamp 1700566380222.
# No expression weights found for participant 7 for timestamp 1700566380235.
# No expression weights found for participant 7 for timestamp 1700566380248.
# No expression weights found for participant 7 for timestamp 1700566380276.
# No expression weights found for participant 7 for timestamp 1700566380298.
# No expression weights found for participant 7 for timestamp 1700566380330.
# No expression weights found for participant 7 for timestamp 1700566380357.
# No expression weights found for participant 7 for timestamp 1700566578554.
# No expression weights found for participant 7 for timestamp 1700566577594.
# No expression weights found for participant 7 for timestamp 1700566577622.
# No expression weights found for participant 7 for timestamp 1700566577650.
# No expression weights found for participant 7 for timestamp 1700566577692.
# No expression weights found for participant 7 for timestamp 1700566577720.
# No expression weights found for participant 7 for timestamp 1700566577747.
# No expression weights found for participant 7 for timestamp 1700566577789.
# No expression weights found for participant 7 for timestamp 1700566577817.
# No expression weights found for participant 7 for timestamp 1700566577859.
# No expression weights found for participant 7 for timestamp 1700566577886.
# No expression weights found for participant 7 for timestamp 1700566577915.
# No expression weights found for participant 7 for timestamp 1700566577956.
# No expression weights found for participant 7 for timestamp 1700566577984.
# No expression weights found for participant 7 for timestamp 1700566578028.
# No expression weights found for participant 7 for timestamp 1700566578051.
# No expression weights found for participant 7 for timestamp 1700566578094.
# No expression weights found for participant 7 for timestamp 1700566578122.
# No expression weights found for participant 7 for timestamp 1700566578150.
# No expression weights found for participant 7 for timestamp 1700566578193.
# No expression weights found for participant 7 for timestamp 1700566578221.
# No expression weights found for participant 7 for timestamp 1700566578248.
# No expression weights found for participant 7 for timestamp 1700566578290.
# No expression weights found for participant 7 for timestamp 1700566578320.
# No expression weights found for participant 7 for timestamp 1700566578360.
# No expression weights found for participant 7 for timestamp 1700566578388.
# No expression weights found for participant 7 for timestamp 1700566578416.
# No expression weights found for participant 7 for timestamp 1700566578457.
# No expression weights found for participant 7 for timestamp 1700566578484.
# No expression weights found for participant 7 for timestamp 1700566578526.
# No expression weights found for participant 7 for timestamp 1700566593020.
# No expression weights found for participant 7 for timestamp 1700566592050.
# No expression weights found for participant 7 for timestamp 1700566592091.
# No expression weights found for participant 7 for timestamp 1700566592115.
# No expression weights found for participant 7 for timestamp 1700566592143.
# No expression weights found for participant 7 for timestamp 1700566592184.
# No expression weights found for participant 7 for timestamp 1700566592211.
# No expression weights found for participant 7 for timestamp 1700566592252.
# No expression weights found for participant 7 for timestamp 1700566592279.
# No expression weights found for participant 7 for timestamp 1700566592318.
# No expression weights found for participant 7 for timestamp 1700566592358.
# No expression weights found for participant 7 for timestamp 1700566592398.
# No expression weights found for participant 7 for timestamp 1700566592411.
# No expression weights found for participant 7 for timestamp 1700566592453.
# No expression weights found for participant 7 for timestamp 1700566592480.
# No expression weights found for participant 7 for timestamp 1700566592522.
# No expression weights found for participant 7 for timestamp 1700566592549.
# No expression weights found for participant 7 for timestamp 1700566592577.
# No expression weights found for participant 7 for timestamp 1700566592619.
# No expression weights found for participant 7 for timestamp 1700566592649.
# No expression weights found for participant 7 for timestamp 1700566592688.
# No expression weights found for participant 7 for timestamp 1700566592716.
# No expression weights found for participant 7 for timestamp 1700566592743.
# No expression weights found for participant 7 for timestamp 1700566592785.
# No expression weights found for participant 7 for timestamp 1700566592813.
# No expression weights found for participant 7 for timestamp 1700566592855.
# No expression weights found for participant 7 for timestamp 1700566592883.
# No expression weights found for participant 7 for timestamp 1700566592910.
# No expression weights found for participant 7 for timestamp 1700566592953.
# No expression weights found for participant 7 for timestamp 1700566592978.
# No expression weights found for participant 7 for timestamp 1700566604908.
# No expression weights found for participant 7 for timestamp 1700566603951.
# No expression weights found for participant 7 for timestamp 1700566603978.
# No expression weights found for participant 7 for timestamp 1700566604020.
# No expression weights found for participant 7 for timestamp 1700566604048.
# No expression weights found for participant 7 for timestamp 1700566604077.
# No expression weights found for participant 7 for timestamp 1700566604116.
# No expression weights found for participant 7 for timestamp 1700566604143.
# No expression weights found for participant 7 for timestamp 1700566604185.
# No expression weights found for participant 7 for timestamp 1700566604214.
# No expression weights found for participant 7 for timestamp 1700566604255.
# No expression weights found for participant 7 for timestamp 1700566604282.
# No expression weights found for participant 7 for timestamp 1700566604311.
# No expression weights found for participant 7 for timestamp 1700566604352.
# No expression weights found for participant 7 for timestamp 1700566604382.
# No expression weights found for participant 7 for timestamp 1700566604419.
# No expression weights found for participant 7 for timestamp 1700566604447.
# No expression weights found for participant 7 for timestamp 1700566604475.
# No expression weights found for participant 7 for timestamp 1700566604515.
# No expression weights found for participant 7 for timestamp 1700566604542.
# No expression weights found for participant 7 for timestamp 1700566604583.
# No expression weights found for participant 7 for timestamp 1700566604608.
# No expression weights found for participant 7 for timestamp 1700566604648.
# No expression weights found for participant 7 for timestamp 1700566604675.
# No expression weights found for participant 7 for timestamp 1700566604717.
# No expression weights found for participant 7 for timestamp 1700566604742.
# No expression weights found for participant 7 for timestamp 1700566604784.
# No expression weights found for participant 7 for timestamp 1700566604811.
# No expression weights found for participant 7 for timestamp 1700566604853.
# No expression weights found for participant 7 for timestamp 1700566604881.
# No expression weights found for participant 7 for timestamp 1700566748186.
# No expression weights found for participant 7 for timestamp 1700566747648.
# No expression weights found for participant 7 for timestamp 1700566747686.
# No expression weights found for participant 7 for timestamp 1700566747727.
# No expression weights found for participant 7 for timestamp 1700566747755.
# No expression weights found for participant 7 for timestamp 1700566747783.
# No expression weights found for participant 7 for timestamp 1700566747825.
# No expression weights found for participant 7 for timestamp 1700566747853.
# No expression weights found for participant 7 for timestamp 1700566747895.
# No expression weights found for participant 7 for timestamp 1700566747922.
# No expression weights found for participant 7 for timestamp 1700566747950.
# No expression weights found for participant 7 for timestamp 1700566747991.
# No expression weights found for participant 7 for timestamp 1700566748020.
# No expression weights found for participant 7 for timestamp 1700566748062.
# No expression weights found for participant 7 for timestamp 1700566748089.
# No expression weights found for participant 7 for timestamp 1700566748131.
# No expression weights found for participant 7 for timestamp 1700566748159.
# No expression weights found for participant 7 for timestamp 1700566748227.
# No expression weights found for participant 7 for timestamp 1700566748256.
# No expression weights found for participant 7 for timestamp 1700566748283.
# No expression weights found for participant 7 for timestamp 1700566748326.
# No expression weights found for participant 7 for timestamp 1700566748353.
# No expression weights found for participant 7 for timestamp 1700566748395.
# No expression weights found for participant 7 for timestamp 1700566748423.
# No expression weights found for participant 7 for timestamp 1700566748450.
# No expression weights found for participant 7 for timestamp 1700566748485.
# No expression weights found for participant 7 for timestamp 1700566748519.
# No expression weights found for participant 7 for timestamp 1700566748561.
# No expression weights found for participant 7 for timestamp 1700566748589.
# No expression weights found for participant 7 for timestamp 1700566748617.
# No expression weights found for participant 7 for timestamp 1700566757865.
# No expression weights found for participant 7 for timestamp 1700566756894.
# No expression weights found for participant 7 for timestamp 1700566756941.
# No expression weights found for participant 7 for timestamp 1700566756964.
# No expression weights found for participant 7 for timestamp 1700566756992.
# No expression weights found for participant 7 for timestamp 1700566757033.
# No expression weights found for participant 7 for timestamp 1700566757060.
# No expression weights found for participant 7 for timestamp 1700566757102.
# No expression weights found for participant 7 for timestamp 1700566757129.
# No expression weights found for participant 7 for timestamp 1700566757171.
# No expression weights found for participant 7 for timestamp 1700566757199.
# No expression weights found for participant 7 for timestamp 1700566757227.
# No expression weights found for participant 7 for timestamp 1700566757267.
# No expression weights found for participant 7 for timestamp 1700566757296.
# No expression weights found for participant 7 for timestamp 1700566757337.
# No expression weights found for participant 7 for timestamp 1700566757365.
# No expression weights found for participant 7 for timestamp 1700566757393.
# No expression weights found for participant 7 for timestamp 1700566757435.
# No expression weights found for participant 7 for timestamp 1700566757463.
# Processing file 18500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1700566757865-0-7-4-11-3-0/1700566757504-0-7-4-11-3-0.png
# No expression weights found for participant 7 for timestamp 1700566757504.
# No expression weights found for participant 7 for timestamp 1700566757532.
# No expression weights found for participant 7 for timestamp 1700566757561.
# No expression weights found for participant 7 for timestamp 1700566757601.
# No expression weights found for participant 7 for timestamp 1700566757629.
# No expression weights found for participant 7 for timestamp 1700566757670.
# No expression weights found for participant 7 for timestamp 1700566757698.
# No expression weights found for participant 7 for timestamp 1700566757726.
# No expression weights found for participant 7 for timestamp 1700566757768.
# No expression weights found for participant 7 for timestamp 1700566757796.
# No expression weights found for participant 7 for timestamp 1700566757838.
# No expression weights found for participant 7 for timestamp 1700566780730.
# No expression weights found for participant 7 for timestamp 1700566779764.
# No expression weights found for participant 7 for timestamp 1700566779806.
# No expression weights found for participant 7 for timestamp 1700566779829.
# No expression weights found for participant 7 for timestamp 1700566779875.
# No expression weights found for participant 7 for timestamp 1700566779903.
# No expression weights found for participant 7 for timestamp 1700566779930.
# No expression weights found for participant 7 for timestamp 1700566779972.
# No expression weights found for participant 7 for timestamp 1700566780000.
# No expression weights found for participant 7 for timestamp 1700566780042.
# No expression weights found for participant 7 for timestamp 1700566780069.
# No expression weights found for participant 7 for timestamp 1700566780098.
# No expression weights found for participant 7 for timestamp 1700566780140.
# No expression weights found for participant 7 for timestamp 1700566780167.
# No expression weights found for participant 7 for timestamp 1700566780208.
# No expression weights found for participant 7 for timestamp 1700566780236.
# No expression weights found for participant 7 for timestamp 1700566780263.
# No expression weights found for participant 7 for timestamp 1700566780305.
# No expression weights found for participant 7 for timestamp 1700566780333.
# No expression weights found for participant 7 for timestamp 1700566780375.
# No expression weights found for participant 7 for timestamp 1700566780402.
# No expression weights found for participant 7 for timestamp 1700566780430.
# No expression weights found for participant 7 for timestamp 1700566780469.
# No expression weights found for participant 7 for timestamp 1700566780497.
# No expression weights found for participant 7 for timestamp 1700566780540.
# No expression weights found for participant 7 for timestamp 1700566780568.
# No expression weights found for participant 7 for timestamp 1700566780596.
# No expression weights found for participant 7 for timestamp 1700566780638.
# No expression weights found for participant 7 for timestamp 1700566780666.
# No expression weights found for participant 7 for timestamp 1700566780709.
# Processing file 19000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1700582337973-0-12-4-6-3-0/1700582337277-0-12-4-6-3-0.png
# Processing file 19500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1700754197592-0-17-4-11-3-0/1700754197563-0-17-4-11-3-0.png
# Processing file 20000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1700825942878-0-20-3-11-3-0/1700825942513-0-20-3-11-3-0.png
# Processing file 20500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1700829960945-0-22-1-6-3-0/1700829960247-0-22-1-6-3-0.png
# Processing file 21000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1701087618852-0-24-4-13-3-0/1701087618827-0-24-4-13-3-0.png
# Processing file 21500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1701092797053-0-26-3-17-3-0/1701092796679-0-26-3-17-3-0.png
# Processing file 22000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1701177618243-0-30-1-8-3-0/1701177617543-0-30-1-8-3-0.png
# Processing file 22500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1701188375722-0-31-4-13-3-0/1701188375684-0-31-4-13-3-0.png
# Processing file 23000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1701357598871-0-34-3-17-3-0/1701357598513-0-34-3-17-3-0.png
# Processing file 23500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Happiness/1701440203645-0-37-1-8-3-0/1701440202932-0-37-1-8-3-0.png
# Processing file 24000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1700488283344-0-3-4-18-4-0/1700488283315-0-3-4-18-4-0.png
# No expression weights found for participant 7 for timestamp 1700566451956.
# No expression weights found for participant 7 for timestamp 1700566450988.
# No expression weights found for participant 7 for timestamp 1700566451016.
# No expression weights found for participant 7 for timestamp 1700566451057.
# No expression weights found for participant 7 for timestamp 1700566451085.
# No expression weights found for participant 7 for timestamp 1700566451127.
# No expression weights found for participant 7 for timestamp 1700566451155.
# No expression weights found for participant 7 for timestamp 1700566451183.
# No expression weights found for participant 7 for timestamp 1700566451224.
# No expression weights found for participant 7 for timestamp 1700566451252.
# No expression weights found for participant 7 for timestamp 1700566451294.
# No expression weights found for participant 7 for timestamp 1700566451321.
# No expression weights found for participant 7 for timestamp 1700566451349.
# No expression weights found for participant 7 for timestamp 1700566451391.
# No expression weights found for participant 7 for timestamp 1700566451419.
# No expression weights found for participant 7 for timestamp 1700566451460.
# No expression weights found for participant 7 for timestamp 1700566451488.
# No expression weights found for participant 7 for timestamp 1700566451516.
# No expression weights found for participant 7 for timestamp 1700566451557.
# No expression weights found for participant 7 for timestamp 1700566451588.
# No expression weights found for participant 7 for timestamp 1700566451620.
# No expression weights found for participant 7 for timestamp 1700566451659.
# No expression weights found for participant 7 for timestamp 1700566451687.
# No expression weights found for participant 7 for timestamp 1700566451717.
# No expression weights found for participant 7 for timestamp 1700566451760.
# No expression weights found for participant 7 for timestamp 1700566451789.
# No expression weights found for participant 7 for timestamp 1700566451817.
# No expression weights found for participant 7 for timestamp 1700566451859.
# No expression weights found for participant 7 for timestamp 1700566451888.
# No expression weights found for participant 7 for timestamp 1700566451929.
# No expression weights found for participant 7 for timestamp 1700566469866.
# No expression weights found for participant 7 for timestamp 1700566468894.
# No expression weights found for participant 7 for timestamp 1700566468936.
# No expression weights found for participant 7 for timestamp 1700566468964.
# No expression weights found for participant 7 for timestamp 1700566469005.
# No expression weights found for participant 7 for timestamp 1700566469034.
# No expression weights found for participant 7 for timestamp 1700566469061.
# No expression weights found for participant 7 for timestamp 1700566469103.
# No expression weights found for participant 7 for timestamp 1700566469131.
# No expression weights found for participant 7 for timestamp 1700566469172.
# No expression weights found for participant 7 for timestamp 1700566469199.
# No expression weights found for participant 7 for timestamp 1700566469227.
# No expression weights found for participant 7 for timestamp 1700566469269.
# No expression weights found for participant 7 for timestamp 1700566469297.
# No expression weights found for participant 7 for timestamp 1700566469339.
# No expression weights found for participant 7 for timestamp 1700566469366.
# No expression weights found for participant 7 for timestamp 1700566469395.
# No expression weights found for participant 7 for timestamp 1700566469435.
# No expression weights found for participant 7 for timestamp 1700566469477.
# No expression weights found for participant 7 for timestamp 1700566469503.
# No expression weights found for participant 7 for timestamp 1700566469532.
# No expression weights found for participant 7 for timestamp 1700566469560.
# No expression weights found for participant 7 for timestamp 1700566469601.
# No expression weights found for participant 7 for timestamp 1700566469629.
# No expression weights found for participant 7 for timestamp 1700566469672.
# No expression weights found for participant 7 for timestamp 1700566469701.
# No expression weights found for participant 7 for timestamp 1700566469729.
# No expression weights found for participant 7 for timestamp 1700566469770.
# No expression weights found for participant 7 for timestamp 1700566469797.
# No expression weights found for participant 7 for timestamp 1700566469839.
# No expression weights found for participant 7 for timestamp 1700566480238.
# No expression weights found for participant 7 for timestamp 1700566479278.
# No expression weights found for participant 7 for timestamp 1700566479306.
# No expression weights found for participant 7 for timestamp 1700566479334.
# No expression weights found for participant 7 for timestamp 1700566479376.
# No expression weights found for participant 7 for timestamp 1700566479403.
# No expression weights found for participant 7 for timestamp 1700566479432.
# No expression weights found for participant 7 for timestamp 1700566479479.
# No expression weights found for participant 7 for timestamp 1700566479502.
# No expression weights found for participant 7 for timestamp 1700566479543.
# No expression weights found for participant 7 for timestamp 1700566479571.
# No expression weights found for participant 7 for timestamp 1700566479598.
# No expression weights found for participant 7 for timestamp 1700566479640.
# No expression weights found for participant 7 for timestamp 1700566479667.
# No expression weights found for participant 7 for timestamp 1700566479709.
# No expression weights found for participant 7 for timestamp 1700566479738.
# No expression weights found for participant 7 for timestamp 1700566479776.
# No expression weights found for participant 7 for timestamp 1700566479804.
# No expression weights found for participant 7 for timestamp 1700566479831.
# No expression weights found for participant 7 for timestamp 1700566479874.
# No expression weights found for participant 7 for timestamp 1700566479900.
# No expression weights found for participant 7 for timestamp 1700566479942.
# No expression weights found for participant 7 for timestamp 1700566479969.
# No expression weights found for participant 7 for timestamp 1700566480010.
# No expression weights found for participant 7 for timestamp 1700566480037.
# No expression weights found for participant 7 for timestamp 1700566480065.
# No expression weights found for participant 7 for timestamp 1700566480104.
# No expression weights found for participant 7 for timestamp 1700566480144.
# No expression weights found for participant 7 for timestamp 1700566480170.
# No expression weights found for participant 7 for timestamp 1700566480197.
# No expression weights found for participant 7 for timestamp 1700566569894.
# No expression weights found for participant 7 for timestamp 1700566569316.
# No expression weights found for participant 7 for timestamp 1700566569352.
# No expression weights found for participant 7 for timestamp 1700566569394.
# No expression weights found for participant 7 for timestamp 1700566569421.
# No expression weights found for participant 7 for timestamp 1700566569449.
# No expression weights found for participant 7 for timestamp 1700566569490.
# No expression weights found for participant 7 for timestamp 1700566569518.
# No expression weights found for participant 7 for timestamp 1700566569560.
# No expression weights found for participant 7 for timestamp 1700566569588.
# No expression weights found for participant 7 for timestamp 1700566569629.
# No expression weights found for participant 7 for timestamp 1700566569657.
# No expression weights found for participant 7 for timestamp 1700566569685.
# No expression weights found for participant 7 for timestamp 1700566569726.
# No expression weights found for participant 7 for timestamp 1700566569754.
# No expression weights found for participant 7 for timestamp 1700566569796.
# No expression weights found for participant 7 for timestamp 1700566569824.
# No expression weights found for participant 7 for timestamp 1700566569851.
# No expression weights found for participant 7 for timestamp 1700566569921.
# No expression weights found for participant 7 for timestamp 1700566569963.
# No expression weights found for participant 7 for timestamp 1700566570000.
# No expression weights found for participant 7 for timestamp 1700566570019.
# No expression weights found for participant 7 for timestamp 1700566570060.
# No expression weights found for participant 7 for timestamp 1700566570089.
# No expression weights found for participant 7 for timestamp 1700566570144.
# No expression weights found for participant 7 for timestamp 1700566570200.
# No expression weights found for participant 7 for timestamp 1700566570256.
# No expression weights found for participant 7 for timestamp 1700566570354.
# No expression weights found for participant 7 for timestamp 1700566570375.
# No expression weights found for participant 7 for timestamp 1700566570396.
# No expression weights found for participant 7 for timestamp 1700566594120.
# No expression weights found for participant 7 for timestamp 1700566593522.
# No expression weights found for participant 7 for timestamp 1700566593549.
# No expression weights found for participant 7 for timestamp 1700566593591.
# No expression weights found for participant 7 for timestamp 1700566593618.
# No expression weights found for participant 7 for timestamp 1700566593646.
# No expression weights found for participant 7 for timestamp 1700566593688.
# No expression weights found for participant 7 for timestamp 1700566593717.
# No expression weights found for participant 7 for timestamp 1700566593744.
# No expression weights found for participant 7 for timestamp 1700566593786.
# No expression weights found for participant 7 for timestamp 1700566593814.
# No expression weights found for participant 7 for timestamp 1700566593856.
# No expression weights found for participant 7 for timestamp 1700566593884.
# No expression weights found for participant 7 for timestamp 1700566593912.
# No expression weights found for participant 7 for timestamp 1700566593953.
# No expression weights found for participant 7 for timestamp 1700566593981.
# No expression weights found for participant 7 for timestamp 1700566594024.
# No expression weights found for participant 7 for timestamp 1700566594051.
# No expression weights found for participant 7 for timestamp 1700566594078.
# No expression weights found for participant 7 for timestamp 1700566594147.
# No expression weights found for participant 7 for timestamp 1700566594190.
# No expression weights found for participant 7 for timestamp 1700566594218.
# No expression weights found for participant 7 for timestamp 1700566594245.
# No expression weights found for participant 7 for timestamp 1700566594287.
# No expression weights found for participant 7 for timestamp 1700566594315.
# No expression weights found for participant 7 for timestamp 1700566594348.
# No expression weights found for participant 7 for timestamp 1700566594383.
# No expression weights found for participant 7 for timestamp 1700566594411.
# No expression weights found for participant 7 for timestamp 1700566594453.
# No expression weights found for participant 7 for timestamp 1700566594481.
# No expression weights found for participant 7 for timestamp 1700566599215.
# No expression weights found for participant 7 for timestamp 1700566598256.
# No expression weights found for participant 7 for timestamp 1700566598284.
# No expression weights found for participant 7 for timestamp 1700566598312.
# No expression weights found for participant 7 for timestamp 1700566598355.
# No expression weights found for participant 7 for timestamp 1700566598380.
# No expression weights found for participant 7 for timestamp 1700566598422.
# No expression weights found for participant 7 for timestamp 1700566598450.
# No expression weights found for participant 7 for timestamp 1700566598478.
# No expression weights found for participant 7 for timestamp 1700566598520.
# No expression weights found for participant 7 for timestamp 1700566598548.
# No expression weights found for participant 7 for timestamp 1700566598575.
# No expression weights found for participant 7 for timestamp 1700566598617.
# No expression weights found for participant 7 for timestamp 1700566598656.
# No expression weights found for participant 7 for timestamp 1700566598678.
# No expression weights found for participant 7 for timestamp 1700566598713.
# No expression weights found for participant 7 for timestamp 1700566598753.
# No expression weights found for participant 7 for timestamp 1700566598779.
# No expression weights found for participant 7 for timestamp 1700566598821.
# No expression weights found for participant 7 for timestamp 1700566598847.
# No expression weights found for participant 7 for timestamp 1700566598887.
# No expression weights found for participant 7 for timestamp 1700566598913.
# No expression weights found for participant 7 for timestamp 1700566598955.
# No expression weights found for participant 7 for timestamp 1700566598982.
# No expression weights found for participant 7 for timestamp 1700566599009.
# No expression weights found for participant 7 for timestamp 1700566599049.
# No expression weights found for participant 7 for timestamp 1700566599077.
# No expression weights found for participant 7 for timestamp 1700566599118.
# No expression weights found for participant 7 for timestamp 1700566599145.
# No expression weights found for participant 7 for timestamp 1700566599187.
# No expression weights found for participant 7 for timestamp 1700566741767.
# No expression weights found for participant 7 for timestamp 1700566740800.
# No expression weights found for participant 7 for timestamp 1700566740828.
# No expression weights found for participant 7 for timestamp 1700566740869.
# No expression weights found for participant 7 for timestamp 1700566740898.
# No expression weights found for participant 7 for timestamp 1700566740926.
# No expression weights found for participant 7 for timestamp 1700566740967.
# No expression weights found for participant 7 for timestamp 1700566740996.
# No expression weights found for participant 7 for timestamp 1700566741037.
# No expression weights found for participant 7 for timestamp 1700566741065.
# No expression weights found for participant 7 for timestamp 1700566741093.
# No expression weights found for participant 7 for timestamp 1700566741126.
# No expression weights found for participant 7 for timestamp 1700566741161.
# No expression weights found for participant 7 for timestamp 1700566741203.
# No expression weights found for participant 7 for timestamp 1700566741231.
# No expression weights found for participant 7 for timestamp 1700566741258.
# No expression weights found for participant 7 for timestamp 1700566741300.
# No expression weights found for participant 7 for timestamp 1700566741328.
# No expression weights found for participant 7 for timestamp 1700566741357.
# Processing file 24500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1700566741767-0-7-4-2-4-0/1700566741414-0-7-4-2-4-0.png
# No expression weights found for participant 7 for timestamp 1700566741414.
# No expression weights found for participant 7 for timestamp 1700566741468.
# No expression weights found for participant 7 for timestamp 1700566741533.
# No expression weights found for participant 7 for timestamp 1700566741603.
# No expression weights found for participant 7 for timestamp 1700566741617.
# No expression weights found for participant 7 for timestamp 1700566741630.
# No expression weights found for participant 7 for timestamp 1700566741645.
# No expression weights found for participant 7 for timestamp 1700566741659.
# No expression weights found for participant 7 for timestamp 1700566741673.
# No expression weights found for participant 7 for timestamp 1700566741700.
# No expression weights found for participant 7 for timestamp 1700566741729.
# No expression weights found for participant 7 for timestamp 1700566745158.
# No expression weights found for participant 7 for timestamp 1700566744220.
# No expression weights found for participant 7 for timestamp 1700566744249.
# No expression weights found for participant 7 for timestamp 1700566744261.
# No expression weights found for participant 7 for timestamp 1700566744302.
# No expression weights found for participant 7 for timestamp 1700566744328.
# No expression weights found for participant 7 for timestamp 1700566744369.
# No expression weights found for participant 7 for timestamp 1700566744396.
# No expression weights found for participant 7 for timestamp 1700566744438.
# No expression weights found for participant 7 for timestamp 1700566744465.
# No expression weights found for participant 7 for timestamp 1700566744492.
# No expression weights found for participant 7 for timestamp 1700566744534.
# No expression weights found for participant 7 for timestamp 1700566744561.
# No expression weights found for participant 7 for timestamp 1700566744603.
# No expression weights found for participant 7 for timestamp 1700566744641.
# No expression weights found for participant 7 for timestamp 1700566744659.
# No expression weights found for participant 7 for timestamp 1700566744701.
# No expression weights found for participant 7 for timestamp 1700566744728.
# No expression weights found for participant 7 for timestamp 1700566744769.
# No expression weights found for participant 7 for timestamp 1700566744797.
# No expression weights found for participant 7 for timestamp 1700566744825.
# No expression weights found for participant 7 for timestamp 1700566744867.
# No expression weights found for participant 7 for timestamp 1700566744895.
# No expression weights found for participant 7 for timestamp 1700566744925.
# No expression weights found for participant 7 for timestamp 1700566744961.
# No expression weights found for participant 7 for timestamp 1700566745003.
# No expression weights found for participant 7 for timestamp 1700566745046.
# No expression weights found for participant 7 for timestamp 1700566745060.
# No expression weights found for participant 7 for timestamp 1700566745102.
# No expression weights found for participant 7 for timestamp 1700566745130.
# No expression weights found for participant 7 for timestamp 1700566747392.
# No expression weights found for participant 7 for timestamp 1700566746426.
# No expression weights found for participant 7 for timestamp 1700566746466.
# No expression weights found for participant 7 for timestamp 1700566746494.
# No expression weights found for participant 7 for timestamp 1700566746521.
# No expression weights found for participant 7 for timestamp 1700566746563.
# No expression weights found for participant 7 for timestamp 1700566746590.
# No expression weights found for participant 7 for timestamp 1700566746632.
# No expression weights found for participant 7 for timestamp 1700566746660.
# No expression weights found for participant 7 for timestamp 1700566746688.
# No expression weights found for participant 7 for timestamp 1700566746730.
# No expression weights found for participant 7 for timestamp 1700566746757.
# No expression weights found for participant 7 for timestamp 1700566746799.
# No expression weights found for participant 7 for timestamp 1700566746826.
# No expression weights found for participant 7 for timestamp 1700566746854.
# No expression weights found for participant 7 for timestamp 1700566746896.
# No expression weights found for participant 7 for timestamp 1700566746925.
# No expression weights found for participant 7 for timestamp 1700566746990.
# No expression weights found for participant 7 for timestamp 1700566747047.
# No expression weights found for participant 7 for timestamp 1700566747095.
# No expression weights found for participant 7 for timestamp 1700566747161.
# No expression weights found for participant 7 for timestamp 1700566747175.
# No expression weights found for participant 7 for timestamp 1700566747187.
# No expression weights found for participant 7 for timestamp 1700566747201.
# No expression weights found for participant 7 for timestamp 1700566747214.
# No expression weights found for participant 7 for timestamp 1700566747228.
# No expression weights found for participant 7 for timestamp 1700566747255.
# No expression weights found for participant 7 for timestamp 1700566747295.
# No expression weights found for participant 7 for timestamp 1700566747322.
# No expression weights found for participant 7 for timestamp 1700566747364.
# No expression weights found for participant 7 for timestamp 1700566769680.
# No expression weights found for participant 7 for timestamp 1700566768702.
# No expression weights found for participant 7 for timestamp 1700566768739.
# No expression weights found for participant 7 for timestamp 1700566768779.
# No expression weights found for participant 7 for timestamp 1700566768806.
# No expression weights found for participant 7 for timestamp 1700566768847.
# No expression weights found for participant 7 for timestamp 1700566768875.
# No expression weights found for participant 7 for timestamp 1700566768916.
# No expression weights found for participant 7 for timestamp 1700566768944.
# No expression weights found for participant 7 for timestamp 1700566768971.
# No expression weights found for participant 7 for timestamp 1700566769013.
# No expression weights found for participant 7 for timestamp 1700566769041.
# No expression weights found for participant 7 for timestamp 1700566769082.
# No expression weights found for participant 7 for timestamp 1700566769110.
# No expression weights found for participant 7 for timestamp 1700566769138.
# No expression weights found for participant 7 for timestamp 1700566769180.
# No expression weights found for participant 7 for timestamp 1700566769208.
# No expression weights found for participant 7 for timestamp 1700566769247.
# No expression weights found for participant 7 for timestamp 1700566769275.
# No expression weights found for participant 7 for timestamp 1700566769315.
# No expression weights found for participant 7 for timestamp 1700566769342.
# No expression weights found for participant 7 for timestamp 1700566769383.
# No expression weights found for participant 7 for timestamp 1700566769408.
# No expression weights found for participant 7 for timestamp 1700566769447.
# No expression weights found for participant 7 for timestamp 1700566769474.
# No expression weights found for participant 7 for timestamp 1700566769517.
# No expression weights found for participant 7 for timestamp 1700566769536.
# No expression weights found for participant 7 for timestamp 1700566769570.
# No expression weights found for participant 7 for timestamp 1700566769612.
# No expression weights found for participant 7 for timestamp 1700566769639.
# Processing file 25000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1700582183583-0-12-3-12-4-0/1700582182872-0-12-3-12-4-0.png
# Processing file 25500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1700753894954-0-17-2-0-4-0/1700753895154-0-17-2-0-4-0.png
# Processing file 26000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1700824746918-0-19-4-4-4-0/1700824746550-0-19-4-4-4-0.png
# Processing file 26500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1700827814313-0-21-3-12-4-0/1700827813614-0-21-3-12-4-0.png
# Processing file 27000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1701087284069-0-24-2-0-4-0/1701087284041-0-24-2-0-4-0.png
# Processing file 27500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1701091287847-0-25-4-4-4-0/1701091287618-0-25-4-4-4-0.png
# Found expression weights for participant 26 for timestamp 1701092950082 with difference >= 15 milliseconds.
# Processing file 28000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1701170627518-0-28-3-14-4-0/1701170626819-0-28-3-14-4-0.png
# Processing file 28500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1701188079711-0-31-2-7-4-0/1701188079666-0-31-2-7-4-0.png
# Processing file 29000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1701350606249-0-33-4-5-4-0/1701350605873-0-33-4-5-4-0.png
# Processing file 29500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Neutral/1701429614383-0-35-4-2-4-0/1701429613650-0-35-4-2-4-0.png
# Processing file 30000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Surprise/1700487975578-0-3-2-9-6-0/1700487975559-0-3-2-9-6-0.png
# Found expression weights for participant 4 for timestamp 1700489861837 with difference >= 15 milliseconds.
# Processing file 30500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Surprise/1700490090087-0-4-4-27-6-0/1700490089797-0-4-4-27-6-0.png
# No expression weights found for participant 7 for timestamp 1700566457312.
# No expression weights found for participant 7 for timestamp 1700566456340.
# No expression weights found for participant 7 for timestamp 1700566456368.
# No expression weights found for participant 7 for timestamp 1700566456411.
# No expression weights found for participant 7 for timestamp 1700566456438.
# No expression weights found for participant 7 for timestamp 1700566456480.
# No expression weights found for participant 7 for timestamp 1700566456508.
# No expression weights found for participant 7 for timestamp 1700566456535.
# No expression weights found for participant 7 for timestamp 1700566456578.
# No expression weights found for participant 7 for timestamp 1700566456605.
# No expression weights found for participant 7 for timestamp 1700566456646.
# No expression weights found for participant 7 for timestamp 1700566456674.
# No expression weights found for participant 7 for timestamp 1700566456701.
# No expression weights found for participant 7 for timestamp 1700566456744.
# No expression weights found for participant 7 for timestamp 1700566456771.
# No expression weights found for participant 7 for timestamp 1700566456813.
# No expression weights found for participant 7 for timestamp 1700566456840.
# No expression weights found for participant 7 for timestamp 1700566456868.
# No expression weights found for participant 7 for timestamp 1700566456909.
# No expression weights found for participant 7 for timestamp 1700566456936.
# No expression weights found for participant 7 for timestamp 1700566456979.
# No expression weights found for participant 7 for timestamp 1700566457006.
# No expression weights found for participant 7 for timestamp 1700566457034.
# No expression weights found for participant 7 for timestamp 1700566457076.
# No expression weights found for participant 7 for timestamp 1700566457104.
# No expression weights found for participant 7 for timestamp 1700566457146.
# No expression weights found for participant 7 for timestamp 1700566457177.
# No expression weights found for participant 7 for timestamp 1700566457200.
# No expression weights found for participant 7 for timestamp 1700566457243.
# No expression weights found for participant 7 for timestamp 1700566457270.
# No expression weights found for participant 7 for timestamp 1700566471449.
# No expression weights found for participant 7 for timestamp 1700566470940.
# No expression weights found for participant 7 for timestamp 1700566470978.
# No expression weights found for participant 7 for timestamp 1700566471019.
# No expression weights found for participant 7 for timestamp 1700566471045.
# No expression weights found for participant 7 for timestamp 1700566471074.
# No expression weights found for participant 7 for timestamp 1700566471116.
# No expression weights found for participant 7 for timestamp 1700566471143.
# No expression weights found for participant 7 for timestamp 1700566471185.
# No expression weights found for participant 7 for timestamp 1700566471214.
# No expression weights found for participant 7 for timestamp 1700566471241.
# No expression weights found for participant 7 for timestamp 1700566471282.
# No expression weights found for participant 7 for timestamp 1700566471311.
# No expression weights found for participant 7 for timestamp 1700566471352.
# No expression weights found for participant 7 for timestamp 1700566471380.
# No expression weights found for participant 7 for timestamp 1700566471408.
# No expression weights found for participant 7 for timestamp 1700566471478.
# No expression weights found for participant 7 for timestamp 1700566471519.
# No expression weights found for participant 7 for timestamp 1700566471547.
# No expression weights found for participant 7 for timestamp 1700566471576.
# No expression weights found for participant 7 for timestamp 1700566471621.
# No expression weights found for participant 7 for timestamp 1700566471645.
# No expression weights found for participant 7 for timestamp 1700566471686.
# No expression weights found for participant 7 for timestamp 1700566471714.
# No expression weights found for participant 7 for timestamp 1700566471741.
# No expression weights found for participant 7 for timestamp 1700566471783.
# No expression weights found for participant 7 for timestamp 1700566471810.
# No expression weights found for participant 7 for timestamp 1700566471852.
# No expression weights found for participant 7 for timestamp 1700566471880.
# No expression weights found for participant 7 for timestamp 1700566471909.
# No expression weights found for participant 7 for timestamp 1700566577455.
# No expression weights found for participant 7 for timestamp 1700566576484.
# No expression weights found for participant 7 for timestamp 1700566576526.
# No expression weights found for participant 7 for timestamp 1700566576554.
# No expression weights found for participant 7 for timestamp 1700566576582.
# No expression weights found for participant 7 for timestamp 1700566576630.
# No expression weights found for participant 7 for timestamp 1700566576651.
# No expression weights found for participant 7 for timestamp 1700566576692.
# No expression weights found for participant 7 for timestamp 1700566576720.
# No expression weights found for participant 7 for timestamp 1700566576748.
# No expression weights found for participant 7 for timestamp 1700566576790.
# No expression weights found for participant 7 for timestamp 1700566576816.
# No expression weights found for participant 7 for timestamp 1700566576869.
# No expression weights found for participant 7 for timestamp 1700566576925.
# No expression weights found for participant 7 for timestamp 1700566576979.
# No expression weights found for participant 7 for timestamp 1700566577034.
# No expression weights found for participant 7 for timestamp 1700566577047.
# No expression weights found for participant 7 for timestamp 1700566577061.
# No expression weights found for participant 7 for timestamp 1700566577073.
# No expression weights found for participant 7 for timestamp 1700566577084.
# No expression weights found for participant 7 for timestamp 1700566577126.
# No expression weights found for participant 7 for timestamp 1700566577152.
# No expression weights found for participant 7 for timestamp 1700566577195.
# No expression weights found for participant 7 for timestamp 1700566577221.
# No expression weights found for participant 7 for timestamp 1700566577261.
# No expression weights found for participant 7 for timestamp 1700566577289.
# No expression weights found for participant 7 for timestamp 1700566577317.
# No expression weights found for participant 7 for timestamp 1700566577358.
# No expression weights found for participant 7 for timestamp 1700566577386.
# No expression weights found for participant 7 for timestamp 1700566577427.
# No expression weights found for participant 7 for timestamp 1700566596617.
# No expression weights found for participant 7 for timestamp 1700566595646.
# No expression weights found for participant 7 for timestamp 1700566595687.
# No expression weights found for participant 7 for timestamp 1700566595715.
# No expression weights found for participant 7 for timestamp 1700566595757.
# No expression weights found for participant 7 for timestamp 1700566595799.
# No expression weights found for participant 7 for timestamp 1700566595824.
# No expression weights found for participant 7 for timestamp 1700566595851.
# No expression weights found for participant 7 for timestamp 1700566595877.
# No expression weights found for participant 7 for timestamp 1700566595918.
# No expression weights found for participant 7 for timestamp 1700566595943.
# No expression weights found for participant 7 for timestamp 1700566595983.
# No expression weights found for participant 7 for timestamp 1700566596025.
# No expression weights found for participant 7 for timestamp 1700566596050.
# No expression weights found for participant 7 for timestamp 1700566596076.
# No expression weights found for participant 7 for timestamp 1700566596117.
# No expression weights found for participant 7 for timestamp 1700566596145.
# No expression weights found for participant 7 for timestamp 1700566596186.
# No expression weights found for participant 7 for timestamp 1700566596214.
# No expression weights found for participant 7 for timestamp 1700566596256.
# No expression weights found for participant 7 for timestamp 1700566596283.
# No expression weights found for participant 7 for timestamp 1700566596311.
# No expression weights found for participant 7 for timestamp 1700566596358.
# No expression weights found for participant 7 for timestamp 1700566596380.
# No expression weights found for participant 7 for timestamp 1700566596422.
# No expression weights found for participant 7 for timestamp 1700566596449.
# No expression weights found for participant 7 for timestamp 1700566596478.
# No expression weights found for participant 7 for timestamp 1700566596520.
# No expression weights found for participant 7 for timestamp 1700566596547.
# No expression weights found for participant 7 for timestamp 1700566596588.
# No expression weights found for participant 7 for timestamp 1700566609011.
# No expression weights found for participant 7 for timestamp 1700566608045.
# No expression weights found for participant 7 for timestamp 1700566608074.
# No expression weights found for participant 7 for timestamp 1700566608113.
# No expression weights found for participant 7 for timestamp 1700566608141.
# No expression weights found for participant 7 for timestamp 1700566608183.
# No expression weights found for participant 7 for timestamp 1700566608210.
# No expression weights found for participant 7 for timestamp 1700566608250.
# No expression weights found for participant 7 for timestamp 1700566608277.
# No expression weights found for participant 7 for timestamp 1700566608318.
# No expression weights found for participant 7 for timestamp 1700566608345.
# No expression weights found for participant 7 for timestamp 1700566608386.
# No expression weights found for participant 7 for timestamp 1700566608412.
# No expression weights found for participant 7 for timestamp 1700566608467.
# No expression weights found for participant 7 for timestamp 1700566608481.
# No expression weights found for participant 7 for timestamp 1700566608519.
# No expression weights found for participant 7 for timestamp 1700566608546.
# No expression weights found for participant 7 for timestamp 1700566608574.
# No expression weights found for participant 7 for timestamp 1700566608615.
# No expression weights found for participant 7 for timestamp 1700566608643.
# No expression weights found for participant 7 for timestamp 1700566608685.
# No expression weights found for participant 7 for timestamp 1700566608711.
# No expression weights found for participant 7 for timestamp 1700566608750.
# No expression weights found for participant 7 for timestamp 1700566608777.
# No expression weights found for participant 7 for timestamp 1700566608818.
# No expression weights found for participant 7 for timestamp 1700566608843.
# No expression weights found for participant 7 for timestamp 1700566608882.
# No expression weights found for participant 7 for timestamp 1700566608910.
# No expression weights found for participant 7 for timestamp 1700566608950.
# No expression weights found for participant 7 for timestamp 1700566608992.
# No expression weights found for participant 7 for timestamp 1700566743230.
# No expression weights found for participant 7 for timestamp 1700566742388.
# No expression weights found for participant 7 for timestamp 1700566742425.
# No expression weights found for participant 7 for timestamp 1700566742467.
# No expression weights found for participant 7 for timestamp 1700566742494.
# No expression weights found for participant 7 for timestamp 1700566742522.
# No expression weights found for participant 7 for timestamp 1700566742564.
# No expression weights found for participant 7 for timestamp 1700566742591.
# No expression weights found for participant 7 for timestamp 1700566742634.
# No expression weights found for participant 7 for timestamp 1700566742661.
# No expression weights found for participant 7 for timestamp 1700566742689.
# No expression weights found for participant 7 for timestamp 1700566742731.
# No expression weights found for participant 7 for timestamp 1700566742758.
# No expression weights found for participant 7 for timestamp 1700566742800.
# No expression weights found for participant 7 for timestamp 1700566742828.
# No expression weights found for participant 7 for timestamp 1700566742858.
# No expression weights found for participant 7 for timestamp 1700566742898.
# No expression weights found for participant 7 for timestamp 1700566742926.
# No expression weights found for participant 7 for timestamp 1700566742967.
# No expression weights found for participant 7 for timestamp 1700566742995.
# No expression weights found for participant 7 for timestamp 1700566743022.
# No expression weights found for participant 7 for timestamp 1700566743064.
# No expression weights found for participant 7 for timestamp 1700566743091.
# No expression weights found for participant 7 for timestamp 1700566743133.
# No expression weights found for participant 7 for timestamp 1700566743177.
# No expression weights found for participant 7 for timestamp 1700566743189.
# No expression weights found for participant 7 for timestamp 1700566743258.
# No expression weights found for participant 7 for timestamp 1700566743300.
# No expression weights found for participant 7 for timestamp 1700566743327.
# No expression weights found for participant 7 for timestamp 1700566743355.
# No expression weights found for participant 7 for timestamp 1700566771764.
# No expression weights found for participant 7 for timestamp 1700566770791.
# No expression weights found for participant 7 for timestamp 1700566770833.
# No expression weights found for participant 7 for timestamp 1700566770861.
# No expression weights found for participant 7 for timestamp 1700566770902.
# No expression weights found for participant 7 for timestamp 1700566770930.
# No expression weights found for participant 7 for timestamp 1700566770958.
# No expression weights found for participant 7 for timestamp 1700566771005.
# No expression weights found for participant 7 for timestamp 1700566771024.
# No expression weights found for participant 7 for timestamp 1700566771066.
# No expression weights found for participant 7 for timestamp 1700566771094.
# No expression weights found for participant 7 for timestamp 1700566771137.
# No expression weights found for participant 7 for timestamp 1700566771165.
# No expression weights found for participant 7 for timestamp 1700566771193.
# No expression weights found for participant 7 for timestamp 1700566771235.
# No expression weights found for participant 7 for timestamp 1700566771264.
# No expression weights found for participant 7 for timestamp 1700566771291.
# No expression weights found for participant 7 for timestamp 1700566771332.
# No expression weights found for participant 7 for timestamp 1700566771360.
# No expression weights found for participant 7 for timestamp 1700566771402.
# No expression weights found for participant 7 for timestamp 1700566771430.
# No expression weights found for participant 7 for timestamp 1700566771458.
# No expression weights found for participant 7 for timestamp 1700566771500.
# No expression weights found for participant 7 for timestamp 1700566771528.
# No expression weights found for participant 7 for timestamp 1700566771570.
# No expression weights found for participant 7 for timestamp 1700566771598.
# No expression weights found for participant 7 for timestamp 1700566771626.
# No expression weights found for participant 7 for timestamp 1700566771667.
# No expression weights found for participant 7 for timestamp 1700566771695.
# No expression weights found for participant 7 for timestamp 1700566771737.
# No expression weights found for participant 7 for timestamp 1700566785956.
# No expression weights found for participant 7 for timestamp 1700566784998.
# No expression weights found for participant 7 for timestamp 1700566785026.
# No expression weights found for participant 7 for timestamp 1700566785069.
# No expression weights found for participant 7 for timestamp 1700566785098.
# No expression weights found for participant 7 for timestamp 1700566785124.
# No expression weights found for participant 7 for timestamp 1700566785166.
# No expression weights found for participant 7 for timestamp 1700566785193.
# No expression weights found for participant 7 for timestamp 1700566785235.
# No expression weights found for participant 7 for timestamp 1700566785263.
# No expression weights found for participant 7 for timestamp 1700566785290.
# No expression weights found for participant 7 for timestamp 1700566785332.
# No expression weights found for participant 7 for timestamp 1700566785360.
# No expression weights found for participant 7 for timestamp 1700566785397.
# No expression weights found for participant 7 for timestamp 1700566785430.
# No expression weights found for participant 7 for timestamp 1700566785457.
# No expression weights found for participant 7 for timestamp 1700566785498.
# No expression weights found for participant 7 for timestamp 1700566785526.
# No expression weights found for participant 7 for timestamp 1700566785568.
# No expression weights found for participant 7 for timestamp 1700566785595.
# No expression weights found for participant 7 for timestamp 1700566785624.
# No expression weights found for participant 7 for timestamp 1700566785665.
# No expression weights found for participant 7 for timestamp 1700566785692.
# No expression weights found for participant 7 for timestamp 1700566785734.
# No expression weights found for participant 7 for timestamp 1700566785761.
# No expression weights found for participant 7 for timestamp 1700566785789.
# No expression weights found for participant 7 for timestamp 1700566785831.
# No expression weights found for participant 7 for timestamp 1700566785859.
# No expression weights found for participant 7 for timestamp 1700566785901.
# No expression weights found for participant 7 for timestamp 1700566785928.
# Processing file 31000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Surprise/1700580704337-0-11-4-21-6-0/1700580703641-0-11-4-21-6-0.png
# Processing file 31500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Surprise/1700749005486-0-16-4-19-6-0/1700749005947-0-16-4-19-6-0.png
# Processing file 32000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Surprise/1700824772745-0-19-4-19-6-0/1700824772385-0-19-4-19-6-0.png
# Processing file 32500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Surprise/1700828000810-0-21-4-19-6-0/1700828000375-0-21-4-19-6-0.png
# Processing file 33000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Surprise/1701087642989-0-24-4-27-6-0/1701087642962-0-24-4-27-6-0.png
# Processing file 33500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Surprise/1701092995220-0-26-4-27-6-0/1701092994857-0-26-4-27-6-0.png
# Processing file 34000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Surprise/1701188066425-0-31-2-2-6-0/1701188065723-0-31-2-2-6-0.png
# Processing file 34500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Surprise/1701350634052-0-33-4-21-6-0/1701350634011-0-33-4-21-6-0.png
# Processing file 35000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Surprise/1701429615895-0-35-4-3-6-0/1701429615538-0-35-4-3-6-0.png
# Processing file 35500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Fear/1700489747611-0-4-2-10-2-0/1700489746945-0-4-2-10-2-0.png
# No expression weights found for participant 7 for timestamp 1700566460103.
# No expression weights found for participant 7 for timestamp 1700566459132.
# No expression weights found for participant 7 for timestamp 1700566459173.
# No expression weights found for participant 7 for timestamp 1700566459201.
# No expression weights found for participant 7 for timestamp 1700566459243.
# No expression weights found for participant 7 for timestamp 1700566459271.
# No expression weights found for participant 7 for timestamp 1700566459298.
# No expression weights found for participant 7 for timestamp 1700566459339.
# No expression weights found for participant 7 for timestamp 1700566459367.
# No expression weights found for participant 7 for timestamp 1700566459410.
# No expression weights found for participant 7 for timestamp 1700566459437.
# No expression weights found for participant 7 for timestamp 1700566459465.
# No expression weights found for participant 7 for timestamp 1700566459506.
# No expression weights found for participant 7 for timestamp 1700566459535.
# No expression weights found for participant 7 for timestamp 1700566459576.
# No expression weights found for participant 7 for timestamp 1700566459603.
# No expression weights found for participant 7 for timestamp 1700566459631.
# No expression weights found for participant 7 for timestamp 1700566459674.
# No expression weights found for participant 7 for timestamp 1700566459715.
# No expression weights found for participant 7 for timestamp 1700566459733.
# No expression weights found for participant 7 for timestamp 1700566459769.
# No expression weights found for participant 7 for timestamp 1700566459812.
# No expression weights found for participant 7 for timestamp 1700566459839.
# No expression weights found for participant 7 for timestamp 1700566459867.
# No expression weights found for participant 7 for timestamp 1700566459909.
# No expression weights found for participant 7 for timestamp 1700566459937.
# No expression weights found for participant 7 for timestamp 1700566459979.
# No expression weights found for participant 7 for timestamp 1700566460007.
# No expression weights found for participant 7 for timestamp 1700566460035.
# No expression weights found for participant 7 for timestamp 1700566460075.
# No expression weights found for participant 7 for timestamp 1700566468011.
# No expression weights found for participant 7 for timestamp 1700566466979.
# No expression weights found for participant 7 for timestamp 1700566467020.
# No expression weights found for participant 7 for timestamp 1700566467049.
# No expression weights found for participant 7 for timestamp 1700566467089.
# No expression weights found for participant 7 for timestamp 1700566467117.
# No expression weights found for participant 7 for timestamp 1700566467145.
# No expression weights found for participant 7 for timestamp 1700566467201.
# No expression weights found for participant 7 for timestamp 1700566467221.
# No expression weights found for participant 7 for timestamp 1700566467243.
# No expression weights found for participant 7 for timestamp 1700566467284.
# No expression weights found for participant 7 for timestamp 1700566467311.
# No expression weights found for participant 7 for timestamp 1700566467352.
# No expression weights found for participant 7 for timestamp 1700566467379.
# No expression weights found for participant 7 for timestamp 1700566467421.
# No expression weights found for participant 7 for timestamp 1700566467450.
# No expression weights found for participant 7 for timestamp 1700566467477.
# No expression weights found for participant 7 for timestamp 1700566467510.
# No expression weights found for participant 7 for timestamp 1700566467547.
# No expression weights found for participant 7 for timestamp 1700566467576.
# No expression weights found for participant 7 for timestamp 1700566467616.
# No expression weights found for participant 7 for timestamp 1700566467644.
# No expression weights found for participant 7 for timestamp 1700566467685.
# No expression weights found for participant 7 for timestamp 1700566467713.
# No expression weights found for participant 7 for timestamp 1700566467755.
# No expression weights found for participant 7 for timestamp 1700566467784.
# No expression weights found for participant 7 for timestamp 1700566467812.
# No expression weights found for participant 7 for timestamp 1700566467864.
# No expression weights found for participant 7 for timestamp 1700566467918.
# No expression weights found for participant 7 for timestamp 1700566467960.
# No expression weights found for participant 7 for timestamp 1700566603144.
# No expression weights found for participant 7 for timestamp 1700566602178.
# No expression weights found for participant 7 for timestamp 1700566602218.
# No expression weights found for participant 7 for timestamp 1700566602245.
# No expression weights found for participant 7 for timestamp 1700566602286.
# No expression weights found for participant 7 for timestamp 1700566602313.
# No expression weights found for participant 7 for timestamp 1700566602354.
# No expression weights found for participant 7 for timestamp 1700566602382.
# No expression weights found for participant 7 for timestamp 1700566602412.
# No expression weights found for participant 7 for timestamp 1700566602451.
# No expression weights found for participant 7 for timestamp 1700566602478.
# No expression weights found for participant 7 for timestamp 1700566602521.
# No expression weights found for participant 7 for timestamp 1700566602548.
# No expression weights found for participant 7 for timestamp 1700566602575.
# No expression weights found for participant 7 for timestamp 1700566602617.
# No expression weights found for participant 7 for timestamp 1700566602645.
# No expression weights found for participant 7 for timestamp 1700566602677.
# No expression weights found for participant 7 for timestamp 1700566602716.
# No expression weights found for participant 7 for timestamp 1700566602743.
# No expression weights found for participant 7 for timestamp 1700566602784.
# No expression weights found for participant 7 for timestamp 1700566602812.
# No expression weights found for participant 7 for timestamp 1700566602853.
# No expression weights found for participant 7 for timestamp 1700566602881.
# No expression weights found for participant 7 for timestamp 1700566602909.
# No expression weights found for participant 7 for timestamp 1700566602950.
# No expression weights found for participant 7 for timestamp 1700566602978.
# No expression weights found for participant 7 for timestamp 1700566603018.
# No expression weights found for participant 7 for timestamp 1700566603046.
# No expression weights found for participant 7 for timestamp 1700566603088.
# No expression weights found for participant 7 for timestamp 1700566603116.
# No expression weights found for participant 7 for timestamp 1700566754162.
# No expression weights found for participant 7 for timestamp 1700566753103.
# No expression weights found for participant 7 for timestamp 1700566753145.
# No expression weights found for participant 7 for timestamp 1700566753172.
# No expression weights found for participant 7 for timestamp 1700566753200.
# No expression weights found for participant 7 for timestamp 1700566753242.
# No expression weights found for participant 7 for timestamp 1700566753269.
# No expression weights found for participant 7 for timestamp 1700566753298.
# No expression weights found for participant 7 for timestamp 1700566753339.
# No expression weights found for participant 7 for timestamp 1700566753367.
# No expression weights found for participant 7 for timestamp 1700566753409.
# No expression weights found for participant 7 for timestamp 1700566753437.
# No expression weights found for participant 7 for timestamp 1700566753477.
# No expression weights found for participant 7 for timestamp 1700566753505.
# No expression weights found for participant 7 for timestamp 1700566753533.
# No expression weights found for participant 7 for timestamp 1700566753575.
# No expression weights found for participant 7 for timestamp 1700566753603.
# No expression weights found for participant 7 for timestamp 1700566753631.
# No expression weights found for participant 7 for timestamp 1700566753672.
# No expression weights found for participant 7 for timestamp 1700566753701.
# No expression weights found for participant 7 for timestamp 1700566753731.
# No expression weights found for participant 7 for timestamp 1700566753771.
# No expression weights found for participant 7 for timestamp 1700566753798.
# No expression weights found for participant 7 for timestamp 1700566753839.
# No expression weights found for participant 7 for timestamp 1700566753867.
# No expression weights found for participant 7 for timestamp 1700566753908.
# No expression weights found for participant 7 for timestamp 1700566753937.
# No expression weights found for participant 7 for timestamp 1700566753993.
# No expression weights found for participant 7 for timestamp 1700566754059.
# No expression weights found for participant 7 for timestamp 1700566754112.
# No expression weights found for participant 7 for timestamp 1700566782497.
# No expression weights found for participant 7 for timestamp 1700566781527.
# No expression weights found for participant 7 for timestamp 1700566781568.
# No expression weights found for participant 7 for timestamp 1700566781596.
# No expression weights found for participant 7 for timestamp 1700566781636.
# No expression weights found for participant 7 for timestamp 1700566781664.
# No expression weights found for participant 7 for timestamp 1700566781692.
# No expression weights found for participant 7 for timestamp 1700566781733.
# No expression weights found for participant 7 for timestamp 1700566781761.
# No expression weights found for participant 7 for timestamp 1700566781803.
# No expression weights found for participant 7 for timestamp 1700566781830.
# No expression weights found for participant 7 for timestamp 1700566781858.
# No expression weights found for participant 7 for timestamp 1700566781899.
# No expression weights found for participant 7 for timestamp 1700566781925.
# No expression weights found for participant 7 for timestamp 1700566781968.
# No expression weights found for participant 7 for timestamp 1700566781996.
# No expression weights found for participant 7 for timestamp 1700566782038.
# No expression weights found for participant 7 for timestamp 1700566782066.
# No expression weights found for participant 7 for timestamp 1700566782094.
# No expression weights found for participant 7 for timestamp 1700566782136.
# No expression weights found for participant 7 for timestamp 1700566782166.
# No expression weights found for participant 7 for timestamp 1700566782203.
# No expression weights found for participant 7 for timestamp 1700566782231.
# No expression weights found for participant 7 for timestamp 1700566782272.
# No expression weights found for participant 7 for timestamp 1700566782299.
# No expression weights found for participant 7 for timestamp 1700566782337.
# No expression weights found for participant 7 for timestamp 1700566782363.
# No expression weights found for participant 7 for timestamp 1700566782403.
# No expression weights found for participant 7 for timestamp 1700566782430.
# No expression weights found for participant 7 for timestamp 1700566782471.
# Processing file 36000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Fear/1700580524093-0-11-3-20-2-0/1700580524066-0-11-3-20-2-0.png
# Processing file 36500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Fear/1700754218629-0-17-4-23-2-0/1700754218253-0-17-4-23-2-0.png
# Processing file 37000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Fear/1701087638925-0-24-4-25-2-0/1701087638699-0-24-4-25-2-0.png
# Processing file 37500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Fear/1701170511673-0-28-2-10-2-0/1701170511647-0-28-2-10-2-0.png
# Processing file 38000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Fear/1701188393051-0-31-4-23-2-0/1701188392686-0-31-4-23-2-0.png
# Processing file 38500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Fear/1701429639116-0-35-4-16-2-0/1701429638413-0-35-4-16-2-0.png
# Found expression weights for participant 3 for timestamp 1700488092556 with difference >= 15 milliseconds.
# Processing file 39000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Disgust/1700490088390-0-4-4-26-1-0/1700490088362-0-4-4-26-1-0.png
# No expression weights found for participant 7 for timestamp 1700566462521.
# No expression weights found for participant 7 for timestamp 1700566461562.
# No expression weights found for participant 7 for timestamp 1700566461588.
# No expression weights found for participant 7 for timestamp 1700566461615.
# No expression weights found for participant 7 for timestamp 1700566461656.
# No expression weights found for participant 7 for timestamp 1700566461684.
# No expression weights found for participant 7 for timestamp 1700566461726.
# No expression weights found for participant 7 for timestamp 1700566461755.
# No expression weights found for participant 7 for timestamp 1700566461783.
# No expression weights found for participant 7 for timestamp 1700566461825.
# No expression weights found for participant 7 for timestamp 1700566461853.
# No expression weights found for participant 7 for timestamp 1700566461894.
# No expression weights found for participant 7 for timestamp 1700566461921.
# No expression weights found for participant 7 for timestamp 1700566461949.
# No expression weights found for participant 7 for timestamp 1700566461990.
# No expression weights found for participant 7 for timestamp 1700566462019.
# No expression weights found for participant 7 for timestamp 1700566462061.
# No expression weights found for participant 7 for timestamp 1700566462088.
# No expression weights found for participant 7 for timestamp 1700566462116.
# No expression weights found for participant 7 for timestamp 1700566462159.
# No expression weights found for participant 7 for timestamp 1700566462189.
# No expression weights found for participant 7 for timestamp 1700566462215.
# No expression weights found for participant 7 for timestamp 1700566462255.
# No expression weights found for participant 7 for timestamp 1700566462283.
# No expression weights found for participant 7 for timestamp 1700566462325.
# No expression weights found for participant 7 for timestamp 1700566462353.
# No expression weights found for participant 7 for timestamp 1700566462395.
# No expression weights found for participant 7 for timestamp 1700566462423.
# No expression weights found for participant 7 for timestamp 1700566462451.
# No expression weights found for participant 7 for timestamp 1700566462494.
# No expression weights found for participant 7 for timestamp 1700566589454.
# No expression weights found for participant 7 for timestamp 1700566588482.
# No expression weights found for participant 7 for timestamp 1700566588523.
# No expression weights found for participant 7 for timestamp 1700566588551.
# No expression weights found for participant 7 for timestamp 1700566588579.
# No expression weights found for participant 7 for timestamp 1700566588620.
# No expression weights found for participant 7 for timestamp 1700566588649.
# No expression weights found for participant 7 for timestamp 1700566588690.
# No expression weights found for participant 7 for timestamp 1700566588717.
# No expression weights found for participant 7 for timestamp 1700566588745.
# No expression weights found for participant 7 for timestamp 1700566588787.
# No expression weights found for participant 7 for timestamp 1700566588815.
# No expression weights found for participant 7 for timestamp 1700566588857.
# No expression weights found for participant 7 for timestamp 1700566588884.
# No expression weights found for participant 7 for timestamp 1700566588912.
# No expression weights found for participant 7 for timestamp 1700566588954.
# No expression weights found for participant 7 for timestamp 1700566588983.
# No expression weights found for participant 7 for timestamp 1700566589023.
# No expression weights found for participant 7 for timestamp 1700566589051.
# No expression weights found for participant 7 for timestamp 1700566589079.
# No expression weights found for participant 7 for timestamp 1700566589120.
# No expression weights found for participant 7 for timestamp 1700566589150.
# No expression weights found for participant 7 for timestamp 1700566589189.
# No expression weights found for participant 7 for timestamp 1700566589217.
# No expression weights found for participant 7 for timestamp 1700566589247.
# No expression weights found for participant 7 for timestamp 1700566589286.
# No expression weights found for participant 7 for timestamp 1700566589314.
# No expression weights found for participant 7 for timestamp 1700566589356.
# No expression weights found for participant 7 for timestamp 1700566589384.
# No expression weights found for participant 7 for timestamp 1700566589412.
# No expression weights found for participant 7 for timestamp 1700566738359.
# No expression weights found for participant 7 for timestamp 1700566737390.
# No expression weights found for participant 7 for timestamp 1700566737418.
# No expression weights found for participant 7 for timestamp 1700566737461.
# No expression weights found for participant 7 for timestamp 1700566737488.
# No expression weights found for participant 7 for timestamp 1700566737529.
# No expression weights found for participant 7 for timestamp 1700566737557.
# No expression weights found for participant 7 for timestamp 1700566737584.
# No expression weights found for participant 7 for timestamp 1700566737625.
# No expression weights found for participant 7 for timestamp 1700566737653.
# No expression weights found for participant 7 for timestamp 1700566737693.
# No expression weights found for participant 7 for timestamp 1700566737721.
# No expression weights found for participant 7 for timestamp 1700566737763.
# No expression weights found for participant 7 for timestamp 1700566737791.
# No expression weights found for participant 7 for timestamp 1700566737818.
# No expression weights found for participant 7 for timestamp 1700566737860.
# No expression weights found for participant 7 for timestamp 1700566737886.
# No expression weights found for participant 7 for timestamp 1700566737930.
# No expression weights found for participant 7 for timestamp 1700566737951.
# No expression weights found for participant 7 for timestamp 1700566737985.
# No expression weights found for participant 7 for timestamp 1700566738026.
# No expression weights found for participant 7 for timestamp 1700566738054.
# No expression weights found for participant 7 for timestamp 1700566738096.
# No expression weights found for participant 7 for timestamp 1700566738123.
# No expression weights found for participant 7 for timestamp 1700566738151.
# No expression weights found for participant 7 for timestamp 1700566738207.
# No expression weights found for participant 7 for timestamp 1700566738234.
# No expression weights found for participant 7 for timestamp 1700566738263.
# No expression weights found for participant 7 for timestamp 1700566738289.
# No expression weights found for participant 7 for timestamp 1700566738317.
# Processing file 39500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Disgust/1700753907881-0-17-2-5-1-0/1700753907519-0-17-2-5-1-0.png
# Processing file 40000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Disgust/1701087622004-0-24-4-15-1-0/1701087621311-0-24-4-15-1-0.png
# Processing file 40500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Disgust/1701177695486-0-30-2-4-1-0/1701177695472-0-30-2-4-1-0.png
# Found expression weights for participant 31 for timestamp 1701188073794 with difference >= 20 milliseconds.
# Processing file 41000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Disgust/1701357445964-0-34-2-5-1-0/1701357445590-0-34-2-5-1-0.png
# Processing file 41500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/training_set/Disgust/1701440282185-0-37-2-1-1-0/1701440281479-0-37-2-1-1-0.png
# Processing file 42000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Sadness/1700486376407-1-2-4-8-5-0/1700486376381-1-2-4-8-5-0.png
# Processing file 42500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Sadness/1700571361673-1-9-4-8-5-0/1700571361507-1-9-4-8-5-0.png
# Processing file 43000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Sadness/1701176244544-1-29-4-1-5-0/1701176244015-1-29-4-1-5-0.png
# Processing file 43500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Happiness/1700486224796-1-2-3-17-3-0/1700486224755-1-2-3-17-3-0.png
# Processing file 44000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Happiness/1700497109218-1-6-4-11-3-0/1700497109148-1-6-4-11-3-0.png
# Processing file 44500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Happiness/1701175866954-1-29-1-6-3-0/1701175866252-1-29-1-6-3-0.png
# Processing file 45000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Happiness/1701438243088-1-36-3-4-3-0/1701438243061-1-36-3-4-3-0.png
# Processing file 45500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Anger/1700491807581-1-5-4-10-0-0/1700491807454-1-5-4-10-0-0.png
# Processing file 46000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Anger/1700571365685-1-9-4-10-0-0/1700571364977-1-9-4-10-0-0.png
# Processing file 46500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Anger/1701346917938-1-32-3-2-0-0/1701346917918-1-32-3-2-0-0.png
# Processing file 47000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Neutral/1700491518328-1-5-2-7-4-0/1700491517970-1-5-2-7-4-0.png
# Processing file 47500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Neutral/1700571355274-1-9-4-4-4-0/1700571354576-1-9-4-4-4-0.png
# Processing file 48000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Neutral/1701346809545-1-32-2-7-4-0/1701346809493-1-32-2-7-4-0.png
# Processing file 48500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Disgust/1700486192396-1-2-3-1-1-0/1700486192087-1-2-3-1-1-0.png
# Processing file 49000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Disgust/1700496952599-1-6-3-18-1-0/1700496951901-1-6-3-18-1-0.png
# Processing file 49500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Disgust/1700745420373-1-14-4-15-1-0/1700745420331-1-14-4-15-1-0.png
# Processing file 50000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Disgust/1701438424827-1-36-4-0-1-0/1701438424896-1-36-4-0-1-0.png
# Processing file 50500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Surprise/1700496922484-1-6-3-3-6-0/1700496921776-1-6-3-3-6-0.png
# Processing file 51000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Surprise/1700745228376-1-14-3-3-6-0/1700745228351-1-14-3-3-6-0.png
# Processing file 51500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Surprise/1701438136355-1-36-2-8-6-0/1701438135990-1-36-2-8-6-0.png
# Processing file 52000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Fear/1700491655095-1-5-3-20-2-0/1700491654398-1-5-3-20-2-0.png
# Processing file 52500 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Fear/1700745115681-1-14-2-3-2-0/1700745115639-1-14-2-3-2-0.png
# Found expression weights for participant 29 for timestamp 1701176258907 with difference >= 15 milliseconds.
# Processing file 53000 : /media/thor/PortableSSD/mydata/emojihero/dataset/emoji-hero-vr-image-sequences-original-resolution/validation_set/Fear/1701347188648-1-32-4-16-2-0/1701347188272-1-32-4-16-2-0.png
#
# Time Difference Categories:
#   <= 5 ms: 51824 files
#   <= 10 ms: 8 files
#   <= 15 ms: 7 files
#   <= 20 ms: 1 files
# No expression weights found for 1500 timestamps of participant 7: [1700566360473, 1700566359501, 1700566359542, 1700566359571, 1700566359624, 1700566359653, 1700566359666, 1700566359708, 1700566359736, 1700566359778, 1700566359805, 1700566359833, 1700566359876, 1700566359903, 1700566359955, 1700566359974, 1700566359999, 1700566360041, 1700566360068, 1700566360110, 1700566360139, 1700566360195, 1700566360261, 1700566360318, 1700566360370, 1700566360397, 1700566360408, 1700566360420, 1700566360433, 1700566360446, 1700566368554, 1700566367595, 1700566367623, 1700566367650, 1700566367692, 1700566367722, 1700566367748, 1700566367789, 1700566367816, 1700566367858, 1700566367886, 1700566367927, 1700566367956, 1700566367983, 1700566368027, 1700566368054, 1700566368094, 1700566368122, 1700566368148, 1700566368201, 1700566368255, 1700566368310, 1700566368380, 1700566368401, 1700566368421, 1700566368435, 1700566368449, 1700566368462, 1700566368489, 1700566368515, 1700566370537, 1700566369566, 1700566369593, 1700566369635, 1700566369660, 1700566369704, 1700566369732, 1700566369760, 1700566369800, 1700566369827, 1700566369869, 1700566369897, 1700566369938, 1700566369966, 1700566369993, 1700566370035, 1700566370063, 1700566370106, 1700566370134, 1700566370161, 1700566370204, 1700566370234, 1700566370261, 1700566370301, 1700566370329, 1700566370370, 1700566370399, 1700566370426, 1700566370468, 1700566370496, 1700566575385, 1700566574480, 1700566574534, 1700566574546, 1700566574560, 1700566574573, 1700566574600, 1700566574620, 1700566574654, 1700566574694, 1700566574721, 1700566574749, 1700566574790, 1700566574818, 1700566574859, 1700566574886, 1700566574930, 1700566574956, 1700566574983, 1700566575025, 1700566575053, 1700566575095, 1700566575122, 1700566575150, 1700566575193, 1700566575218, 1700566575259, 1700566575287, 1700566575315, 1700566575358, 1700566591118, 1700566590150, 1700566590191, 1700566590219, 1700566590246, 1700566590288, 1700566590329, 1700566590345, 1700566590384, 1700566590412, 1700566590454, 1700566590482, 1700566590511, 1700566590555, 1700566590598, 1700566590650, 1700566590721, 1700566590732, 1700566590746, 1700566590760, 1700566590786, 1700566590814, 1700566590855, 1700566590883, 1700566590911, 1700566590954, 1700566590979, 1700566591021, 1700566591048, 1700566591090, 1700566750284, 1700566749385, 1700566749423, 1700566749464, 1700566749492, 1700566749520, 1700566749562, 1700566749589, 1700566749631, 1700566749659, 1700566749687, 1700566749728, 1700566749756, 1700566749798, 1700566749826, 1700566749854, 1700566749897, 1700566749923, 1700566749965, 1700566749992, 1700566750020, 1700566750062, 1700566750090, 1700566750131, 1700566750159, 1700566750187, 1700566750227, 1700566750336, 1700566750390, 1700566750456, 1700566756199, 1700566755241, 1700566755268, 1700566755296, 1700566755338, 1700566755366, 1700566755407, 1700566755433, 1700566755476, 1700566755505, 1700566755531, 1700566755574, 1700566755601, 1700566755629, 1700566755670, 1700566755698, 1700566755741, 1700566755770, 1700566755797, 1700566755837, 1700566755865, 1700566755907, 1700566755935, 1700566755963, 1700566756004, 1700566756032, 1700566756060, 1700566756103, 1700566756129, 1700566756171, 1700566763172, 1700566762199, 1700566762226, 1700566762267, 1700566762296, 1700566762323, 1700566762365, 1700566762393, 1700566762435, 1700566762463, 1700566762490, 1700566762531, 1700566762559, 1700566762601, 1700566762628, 1700566762657, 1700566762698, 1700566762726, 1700566762767, 1700566762798, 1700566762823, 1700566762865, 1700566762894, 1700566762950, 1700566762994, 1700566763038, 1700566763119, 1700566763136, 1700566763144, 1700566763158, 1700566776707, 1700566775769, 1700566775806, 1700566775848, 1700566775876, 1700566775904, 1700566775945, 1700566775973, 1700566776015, 1700566776043, 1700566776070, 1700566776112, 1700566776140, 1700566776182, 1700566776209, 1700566776237, 1700566776289, 1700566776307, 1700566776347, 1700566776376, 1700566776403, 1700566776445, 1700566776473, 1700566776514, 1700566776542, 1700566776570, 1700566776610, 1700566776637, 1700566776679, 1700566776749, 1700566378592, 1700566377634, 1700566377662, 1700566377689, 1700566377731, 1700566377759, 1700566377800, 1700566377828, 1700566377856, 1700566377898, 1700566377925, 1700566377967, 1700566377995, 1700566378023, 1700566378067, 1700566378092, 1700566378134, 1700566378162, 1700566378189, 1700566378231, 1700566378259, 1700566378301, 1700566378329, 1700566378356, 1700566378398, 1700566378425, 1700566378467, 1700566378495, 1700566378522, 1700566378564, 1700566582653, 1700566581692, 1700566581720, 1700566581747, 1700566581789, 1700566581816, 1700566581858, 1700566581886, 1700566581915, 1700566581956, 1700566581984, 1700566582014, 1700566582054, 1700566582080, 1700566582122, 1700566582151, 1700566582192, 1700566582220, 1700566582248, 1700566582290, 1700566582332, 1700566582355, 1700566582387, 1700566582415, 1700566582456, 1700566582484, 1700566582526, 1700566582553, 1700566582581, 1700566582624, 1700566584746, 1700566583788, 1700566583816, 1700566583857, 1700566583885, 1700566583913, 1700566583955, 1700566583983, 1700566584029, 1700566584049, 1700566584091, 1700566584119, 1700566584147, 1700566584190, 1700566584218, 1700566584245, 1700566584288, 1700566584318, 1700566584357, 1700566584385, 1700566584413, 1700566584455, 1700566584482, 1700566584524, 1700566584552, 1700566584580, 1700566584623, 1700566584652, 1700566584692, 1700566584720, 1700566601149, 1700566600186, 1700566600214, 1700566600256, 1700566600283, 1700566600311, 1700566600355, 1700566600382, 1700566600439, 1700566600489, 1700566600543, 1700566600596, 1700566600623, 1700566600636, 1700566600662, 1700566600679, 1700566600689, 1700566600717, 1700566600743, 1700566600784, 1700566600812, 1700566600852, 1700566600880, 1700566600922, 1700566600952, 1700566600975, 1700566601015, 1700566601042, 1700566601082, 1700566601110, 1700566739900, 1700566738942, 1700566738969, 1700566738998, 1700566739039, 1700566739066, 1700566739108, 1700566739161, 1700566739213, 1700566739269, 1700566739323, 1700566739337, 1700566739364, 1700566739377, 1700566739405, 1700566739418, 1700566739431, 1700566739470, 1700566739497, 1700566739538, 1700566739565, 1700566739606, 1700566739634, 1700566739662, 1700566739699, 1700566739742, 1700566739768, 1700566739796, 1700566739834, 1700566739875, 1700566768553, 1700566767569, 1700566767597, 1700566767640, 1700566767667, 1700566767709, 1700566767737, 1700566767764, 1700566767812, 1700566767833, 1700566767875, 1700566767903, 1700566767930, 1700566767972, 1700566768000, 1700566768043, 1700566768070, 1700566768098, 1700566768139, 1700566768166, 1700566768209, 1700566768238, 1700566768294, 1700566768346, 1700566768401, 1700566768484, 1700566768497, 1700566768511, 1700566768525, 1700566768539, 1700566365489, 1700566364525, 1700566364554, 1700566364581, 1700566364628, 1700566364653, 1700566364681, 1700566364721, 1700566364748, 1700566364790, 1700566364818, 1700566364860, 1700566364887, 1700566364918, 1700566364958, 1700566364986, 1700566365026, 1700566365054, 1700566365082, 1700566365123, 1700566365151, 1700566365193, 1700566365248, 1700566365302, 1700566365351, 1700566365408, 1700566365421, 1700566365436, 1700566365449, 1700566365463, 1700566375750, 1700566374733, 1700566374761, 1700566374802, 1700566374830, 1700566374858, 1700566374900, 1700566374928, 1700566374961, 1700566374996, 1700566375024, 1700566375066, 1700566375094, 1700566375136, 1700566375163, 1700566375192, 1700566375233, 1700566375261, 1700566375303, 1700566375331, 1700566375358, 1700566375400, 1700566375427, 1700566375468, 1700566375495, 1700566375550, 1700566375604, 1700566375655, 1700566375710, 1700566375738, 1700566380398, 1700566379427, 1700566379455, 1700566379497, 1700566379524, 1700566379566, 1700566379594, 1700566379622, 1700566379668, 1700566379693, 1700566379734, 1700566379761, 1700566379788, 1700566379830, 1700566379858, 1700566379900, 1700566379927, 1700566379971, 1700566380029, 1700566380083, 1700566380127, 1700566380181, 1700566380209, 1700566380222, 1700566380235, 1700566380248, 1700566380276, 1700566380298, 1700566380330, 1700566380357, 1700566578554, 1700566577594, 1700566577622, 1700566577650, 1700566577692, 1700566577720, 1700566577747, 1700566577789, 1700566577817, 1700566577859, 1700566577886, 1700566577915, 1700566577956, 1700566577984, 1700566578028, 1700566578051, 1700566578094, 1700566578122, 1700566578150, 1700566578193, 1700566578221, 1700566578248, 1700566578290, 1700566578320, 1700566578360, 1700566578388, 1700566578416, 1700566578457, 1700566578484, 1700566578526, 1700566593020, 1700566592050, 1700566592091, 1700566592115, 1700566592143, 1700566592184, 1700566592211, 1700566592252, 1700566592279, 1700566592318, 1700566592358, 1700566592398, 1700566592411, 1700566592453, 1700566592480, 1700566592522, 1700566592549, 1700566592577, 1700566592619, 1700566592649, 1700566592688, 1700566592716, 1700566592743, 1700566592785, 1700566592813, 1700566592855, 1700566592883, 1700566592910, 1700566592953, 1700566592978, 1700566604908, 1700566603951, 1700566603978, 1700566604020, 1700566604048, 1700566604077, 1700566604116, 1700566604143, 1700566604185, 1700566604214, 1700566604255, 1700566604282, 1700566604311, 1700566604352, 1700566604382, 1700566604419, 1700566604447, 1700566604475, 1700566604515, 1700566604542, 1700566604583, 1700566604608, 1700566604648, 1700566604675, 1700566604717, 1700566604742, 1700566604784, 1700566604811, 1700566604853, 1700566604881, 1700566748186, 1700566747648, 1700566747686, 1700566747727, 1700566747755, 1700566747783, 1700566747825, 1700566747853, 1700566747895, 1700566747922, 1700566747950, 1700566747991, 1700566748020, 1700566748062, 1700566748089, 1700566748131, 1700566748159, 1700566748227, 1700566748256, 1700566748283, 1700566748326, 1700566748353, 1700566748395, 1700566748423, 1700566748450, 1700566748485, 1700566748519, 1700566748561, 1700566748589, 1700566748617, 1700566757865, 1700566756894, 1700566756941, 1700566756964, 1700566756992, 1700566757033, 1700566757060, 1700566757102, 1700566757129, 1700566757171, 1700566757199, 1700566757227, 1700566757267, 1700566757296, 1700566757337, 1700566757365, 1700566757393, 1700566757435, 1700566757463, 1700566757504, 1700566757532, 1700566757561, 1700566757601, 1700566757629, 1700566757670, 1700566757698, 1700566757726, 1700566757768, 1700566757796, 1700566757838, 1700566780730, 1700566779764, 1700566779806, 1700566779829, 1700566779875, 1700566779903, 1700566779930, 1700566779972, 1700566780000, 1700566780042, 1700566780069, 1700566780098, 1700566780140, 1700566780167, 1700566780208, 1700566780236, 1700566780263, 1700566780305, 1700566780333, 1700566780375, 1700566780402, 1700566780430, 1700566780469, 1700566780497, 1700566780540, 1700566780568, 1700566780596, 1700566780638, 1700566780666, 1700566780709, 1700566451956, 1700566450988, 1700566451016, 1700566451057, 1700566451085, 1700566451127, 1700566451155, 1700566451183, 1700566451224, 1700566451252, 1700566451294, 1700566451321, 1700566451349, 1700566451391, 1700566451419, 1700566451460, 1700566451488, 1700566451516, 1700566451557, 1700566451588, 1700566451620, 1700566451659, 1700566451687, 1700566451717, 1700566451760, 1700566451789, 1700566451817, 1700566451859, 1700566451888, 1700566451929, 1700566469866, 1700566468894, 1700566468936, 1700566468964, 1700566469005, 1700566469034, 1700566469061, 1700566469103, 1700566469131, 1700566469172, 1700566469199, 1700566469227, 1700566469269, 1700566469297, 1700566469339, 1700566469366, 1700566469395, 1700566469435, 1700566469477, 1700566469503, 1700566469532, 1700566469560, 1700566469601, 1700566469629, 1700566469672, 1700566469701, 1700566469729, 1700566469770, 1700566469797, 1700566469839, 1700566480238, 1700566479278, 1700566479306, 1700566479334, 1700566479376, 1700566479403, 1700566479432, 1700566479479, 1700566479502, 1700566479543, 1700566479571, 1700566479598, 1700566479640, 1700566479667, 1700566479709, 1700566479738, 1700566479776, 1700566479804, 1700566479831, 1700566479874, 1700566479900, 1700566479942, 1700566479969, 1700566480010, 1700566480037, 1700566480065, 1700566480104, 1700566480144, 1700566480170, 1700566480197, 1700566569894, 1700566569316, 1700566569352, 1700566569394, 1700566569421, 1700566569449, 1700566569490, 1700566569518, 1700566569560, 1700566569588, 1700566569629, 1700566569657, 1700566569685, 1700566569726, 1700566569754, 1700566569796, 1700566569824, 1700566569851, 1700566569921, 1700566569963, 1700566570000, 1700566570019, 1700566570060, 1700566570089, 1700566570144, 1700566570200, 1700566570256, 1700566570354, 1700566570375, 1700566570396, 1700566594120, 1700566593522, 1700566593549, 1700566593591, 1700566593618, 1700566593646, 1700566593688, 1700566593717, 1700566593744, 1700566593786, 1700566593814, 1700566593856, 1700566593884, 1700566593912, 1700566593953, 1700566593981, 1700566594024, 1700566594051, 1700566594078, 1700566594147, 1700566594190, 1700566594218, 1700566594245, 1700566594287, 1700566594315, 1700566594348, 1700566594383, 1700566594411, 1700566594453, 1700566594481, 1700566599215, 1700566598256, 1700566598284, 1700566598312, 1700566598355, 1700566598380, 1700566598422, 1700566598450, 1700566598478, 1700566598520, 1700566598548, 1700566598575, 1700566598617, 1700566598656, 1700566598678, 1700566598713, 1700566598753, 1700566598779, 1700566598821, 1700566598847, 1700566598887, 1700566598913, 1700566598955, 1700566598982, 1700566599009, 1700566599049, 1700566599077, 1700566599118, 1700566599145, 1700566599187, 1700566741767, 1700566740800, 1700566740828, 1700566740869, 1700566740898, 1700566740926, 1700566740967, 1700566740996, 1700566741037, 1700566741065, 1700566741093, 1700566741126, 1700566741161, 1700566741203, 1700566741231, 1700566741258, 1700566741300, 1700566741328, 1700566741357, 1700566741414, 1700566741468, 1700566741533, 1700566741603, 1700566741617, 1700566741630, 1700566741645, 1700566741659, 1700566741673, 1700566741700, 1700566741729, 1700566745158, 1700566744220, 1700566744249, 1700566744261, 1700566744302, 1700566744328, 1700566744369, 1700566744396, 1700566744438, 1700566744465, 1700566744492, 1700566744534, 1700566744561, 1700566744603, 1700566744641, 1700566744659, 1700566744701, 1700566744728, 1700566744769, 1700566744797, 1700566744825, 1700566744867, 1700566744895, 1700566744925, 1700566744961, 1700566745003, 1700566745046, 1700566745060, 1700566745102, 1700566745130, 1700566747392, 1700566746426, 1700566746466, 1700566746494, 1700566746521, 1700566746563, 1700566746590, 1700566746632, 1700566746660, 1700566746688, 1700566746730, 1700566746757, 1700566746799, 1700566746826, 1700566746854, 1700566746896, 1700566746925, 1700566746990, 1700566747047, 1700566747095, 1700566747161, 1700566747175, 1700566747187, 1700566747201, 1700566747214, 1700566747228, 1700566747255, 1700566747295, 1700566747322, 1700566747364, 1700566769680, 1700566768702, 1700566768739, 1700566768779, 1700566768806, 1700566768847, 1700566768875, 1700566768916, 1700566768944, 1700566768971, 1700566769013, 1700566769041, 1700566769082, 1700566769110, 1700566769138, 1700566769180, 1700566769208, 1700566769247, 1700566769275, 1700566769315, 1700566769342, 1700566769383, 1700566769408, 1700566769447, 1700566769474, 1700566769517, 1700566769536, 1700566769570, 1700566769612, 1700566769639, 1700566457312, 1700566456340, 1700566456368, 1700566456411, 1700566456438, 1700566456480, 1700566456508, 1700566456535, 1700566456578, 1700566456605, 1700566456646, 1700566456674, 1700566456701, 1700566456744, 1700566456771, 1700566456813, 1700566456840, 1700566456868, 1700566456909, 1700566456936, 1700566456979, 1700566457006, 1700566457034, 1700566457076, 1700566457104, 1700566457146, 1700566457177, 1700566457200, 1700566457243, 1700566457270, 1700566471449, 1700566470940, 1700566470978, 1700566471019, 1700566471045, 1700566471074, 1700566471116, 1700566471143, 1700566471185, 1700566471214, 1700566471241, 1700566471282, 1700566471311, 1700566471352, 1700566471380, 1700566471408, 1700566471478, 1700566471519, 1700566471547, 1700566471576, 1700566471621, 1700566471645, 1700566471686, 1700566471714, 1700566471741, 1700566471783, 1700566471810, 1700566471852, 1700566471880, 1700566471909, 1700566577455, 1700566576484, 1700566576526, 1700566576554, 1700566576582, 1700566576630, 1700566576651, 1700566576692, 1700566576720, 1700566576748, 1700566576790, 1700566576816, 1700566576869, 1700566576925, 1700566576979, 1700566577034, 1700566577047, 1700566577061, 1700566577073, 1700566577084, 1700566577126, 1700566577152, 1700566577195, 1700566577221, 1700566577261, 1700566577289, 1700566577317, 1700566577358, 1700566577386, 1700566577427, 1700566596617, 1700566595646, 1700566595687, 1700566595715, 1700566595757, 1700566595799, 1700566595824, 1700566595851, 1700566595877, 1700566595918, 1700566595943, 1700566595983, 1700566596025, 1700566596050, 1700566596076, 1700566596117, 1700566596145, 1700566596186, 1700566596214, 1700566596256, 1700566596283, 1700566596311, 1700566596358, 1700566596380, 1700566596422, 1700566596449, 1700566596478, 1700566596520, 1700566596547, 1700566596588, 1700566609011, 1700566608045, 1700566608074, 1700566608113, 1700566608141, 1700566608183, 1700566608210, 1700566608250, 1700566608277, 1700566608318, 1700566608345, 1700566608386, 1700566608412, 1700566608467, 1700566608481, 1700566608519, 1700566608546, 1700566608574, 1700566608615, 1700566608643, 1700566608685, 1700566608711, 1700566608750, 1700566608777, 1700566608818, 1700566608843, 1700566608882, 1700566608910, 1700566608950, 1700566608992, 1700566743230, 1700566742388, 1700566742425, 1700566742467, 1700566742494, 1700566742522, 1700566742564, 1700566742591, 1700566742634, 1700566742661, 1700566742689, 1700566742731, 1700566742758, 1700566742800, 1700566742828, 1700566742858, 1700566742898, 1700566742926, 1700566742967, 1700566742995, 1700566743022, 1700566743064, 1700566743091, 1700566743133, 1700566743177, 1700566743189, 1700566743258, 1700566743300, 1700566743327, 1700566743355, 1700566771764, 1700566770791, 1700566770833, 1700566770861, 1700566770902, 1700566770930, 1700566770958, 1700566771005, 1700566771024, 1700566771066, 1700566771094, 1700566771137, 1700566771165, 1700566771193, 1700566771235, 1700566771264, 1700566771291, 1700566771332, 1700566771360, 1700566771402, 1700566771430, 1700566771458, 1700566771500, 1700566771528, 1700566771570, 1700566771598, 1700566771626, 1700566771667, 1700566771695, 1700566771737, 1700566785956, 1700566784998, 1700566785026, 1700566785069, 1700566785098, 1700566785124, 1700566785166, 1700566785193, 1700566785235, 1700566785263, 1700566785290, 1700566785332, 1700566785360, 1700566785397, 1700566785430, 1700566785457, 1700566785498, 1700566785526, 1700566785568, 1700566785595, 1700566785624, 1700566785665, 1700566785692, 1700566785734, 1700566785761, 1700566785789, 1700566785831, 1700566785859, 1700566785901, 1700566785928, 1700566460103, 1700566459132, 1700566459173, 1700566459201, 1700566459243, 1700566459271, 1700566459298, 1700566459339, 1700566459367, 1700566459410, 1700566459437, 1700566459465, 1700566459506, 1700566459535, 1700566459576, 1700566459603, 1700566459631, 1700566459674, 1700566459715, 1700566459733, 1700566459769, 1700566459812, 1700566459839, 1700566459867, 1700566459909, 1700566459937, 1700566459979, 1700566460007, 1700566460035, 1700566460075, 1700566468011, 1700566466979, 1700566467020, 1700566467049, 1700566467089, 1700566467117, 1700566467145, 1700566467201, 1700566467221, 1700566467243, 1700566467284, 1700566467311, 1700566467352, 1700566467379, 1700566467421, 1700566467450, 1700566467477, 1700566467510, 1700566467547, 1700566467576, 1700566467616, 1700566467644, 1700566467685, 1700566467713, 1700566467755, 1700566467784, 1700566467812, 1700566467864, 1700566467918, 1700566467960, 1700566603144, 1700566602178, 1700566602218, 1700566602245, 1700566602286, 1700566602313, 1700566602354, 1700566602382, 1700566602412, 1700566602451, 1700566602478, 1700566602521, 1700566602548, 1700566602575, 1700566602617, 1700566602645, 1700566602677, 1700566602716, 1700566602743, 1700566602784, 1700566602812, 1700566602853, 1700566602881, 1700566602909, 1700566602950, 1700566602978, 1700566603018, 1700566603046, 1700566603088, 1700566603116, 1700566754162, 1700566753103, 1700566753145, 1700566753172, 1700566753200, 1700566753242, 1700566753269, 1700566753298, 1700566753339, 1700566753367, 1700566753409, 1700566753437, 1700566753477, 1700566753505, 1700566753533, 1700566753575, 1700566753603, 1700566753631, 1700566753672, 1700566753701, 1700566753731, 1700566753771, 1700566753798, 1700566753839, 1700566753867, 1700566753908, 1700566753937, 1700566753993, 1700566754059, 1700566754112, 1700566782497, 1700566781527, 1700566781568, 1700566781596, 1700566781636, 1700566781664, 1700566781692, 1700566781733, 1700566781761, 1700566781803, 1700566781830, 1700566781858, 1700566781899, 1700566781925, 1700566781968, 1700566781996, 1700566782038, 1700566782066, 1700566782094, 1700566782136, 1700566782166, 1700566782203, 1700566782231, 1700566782272, 1700566782299, 1700566782337, 1700566782363, 1700566782403, 1700566782430, 1700566782471, 1700566462521, 1700566461562, 1700566461588, 1700566461615, 1700566461656, 1700566461684, 1700566461726, 1700566461755, 1700566461783, 1700566461825, 1700566461853, 1700566461894, 1700566461921, 1700566461949, 1700566461990, 1700566462019, 1700566462061, 1700566462088, 1700566462116, 1700566462159, 1700566462189, 1700566462215, 1700566462255, 1700566462283, 1700566462325, 1700566462353, 1700566462395, 1700566462423, 1700566462451, 1700566462494, 1700566589454, 1700566588482, 1700566588523, 1700566588551, 1700566588579, 1700566588620, 1700566588649, 1700566588690, 1700566588717, 1700566588745, 1700566588787, 1700566588815, 1700566588857, 1700566588884, 1700566588912, 1700566588954, 1700566588983, 1700566589023, 1700566589051, 1700566589079, 1700566589120, 1700566589150, 1700566589189, 1700566589217, 1700566589247, 1700566589286, 1700566589314, 1700566589356, 1700566589384, 1700566589412, 1700566738359, 1700566737390, 1700566737418, 1700566737461, 1700566737488, 1700566737529, 1700566737557, 1700566737584, 1700566737625, 1700566737653, 1700566737693, 1700566737721, 1700566737763, 1700566737791, 1700566737818, 1700566737860, 1700566737886, 1700566737930, 1700566737951, 1700566737985, 1700566738026, 1700566738054, 1700566738096, 1700566738123, 1700566738151, 1700566738207, 1700566738234, 1700566738263, 1700566738289, 1700566738317]
