from pathlib import Path

import cv2


def resize_image_lanczos(image_path, output_path, output_size=(224, 224)):
    """
    Lädt ein Bild, resized es mit Lanczos-Interpolation und speichert es im Zielordner.
    """
    # Bild laden
    img = cv2.imread(str(image_path))

    # Bild auf die gewünschte Größe mit Lanczos-Interpolation resizen
    resized_img = cv2.resize(img, output_size, interpolation=cv2.INTER_LANCZOS4)

    # Stelle sicher, dass der Zielordner existiert
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Gespeichertes Bild
    cv2.imwrite(str(output_path), resized_img)


def process_images(input_folder, output_suffix='_resized'):
    """
    Durchsucht rekursiv den Eingabeordner nach PNG-Dateien, resized sie und speichert sie in einer Parallelstruktur.
    """
    input_path = Path(input_folder)
    output_folder = input_path.parent / f'{input_path.name}{output_suffix}'

    for img_path in input_path.rglob('*.png'):
        relative_path = img_path.relative_to(input_path)
        output_path = output_folder / relative_path

        resize_image_lanczos(img_path, output_path)

    print(f"Finished resizing images from {input_folder} to {output_folder}")


if __name__ == "__main__":
    input_folder = r'E:\mydata\emoijhero\dataset\dataset-cropped-face18400'  # Aktualisiere diesen Pfad
    process_images(input_folder)
