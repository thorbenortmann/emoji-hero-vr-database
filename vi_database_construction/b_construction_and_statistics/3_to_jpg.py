from pathlib import Path

import cv2


def save_as_jpg_with_high_quality(image_path, new_path, quality):
    img = cv2.imread(str(image_path), cv2.IMREAD_COLOR)  # Load PNG as RGB
    new_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(new_path).replace('.png', '.jpg'), img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])


def process_images(input_path, output_path, quality=95):
    for img_path in input_path.rglob('*.png'):
        relative_path = img_path.relative_to(input_path)
        new_path = output_path / relative_path.with_suffix('.jpg')
        save_as_jpg_with_high_quality(img_path, new_path, quality)
        print(f'Converted {img_path} to JPG as {new_path}.')

    print(f'Finished processing images from {input_path}. Saved to {output_path}')


if __name__ == '__main__':
    input_path = Path(r'/media/thor/PortableSSD/emoji-hero-vr-db/intermediate_versions/emoji-hero-vr-db-images-224-png')
    output_path = input_path.parent.parent / 'emoji-hero-vr-db-images-224'
    process_images(input_path, output_path)
