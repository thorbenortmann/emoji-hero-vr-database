from pathlib import Path

import cv2


def resize_image_lanczos(image_path, new_path, output_size):
    img = cv2.imread(str(image_path))
    resized_img = cv2.resize(img, output_size, interpolation=cv2.INTER_LANCZOS4)
    new_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(new_path), resized_img)


def process_images(input_path, output_path, output_size=(224, 224)):
    for img_path in input_path.rglob('*.png'):
        relative_path = img_path.relative_to(input_path)
        new_path = output_path / relative_path
        resize_image_lanczos(img_path, new_path, output_size)
        print(f'Resized {img_path} to a resolution of {output_size} as {new_path}.')

    print(f'Finished resizing images from {input_path} to {output_path}')


if __name__ == "__main__":
    input_path = Path(r'/media/thor/PortableSSD/emoji-hero-vr-db/intermediate_versions/emoji-hero-vr-db-images-faces-png')
    output_path = input_path.parent / 'emoji-hero-vr-db-images-224-png'
    process_images(input_path, output_path)
