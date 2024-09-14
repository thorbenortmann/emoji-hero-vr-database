from pathlib import Path

import cv2


def save_as_jpg_with_high_quality(image_path, output_path, quality=95):
    """
    Lädt ein Bild, entfernt den Alphakanal falls vorhanden, und speichert es als JPG mit gegebener Qualität.
    """
    # Bild laden, dabei den Alphakanal ignorieren
    img = cv2.imread(str(image_path), cv2.IMREAD_COLOR)  # Lädt das Bild im RGB-Format

    # Stelle sicher, dass der Zielordner existiert
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Bild als JPG mit spezifizierter Qualität speichern
    cv2.imwrite(str(output_path).replace('.png', '.jpg'), img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])


def process_images(input_folder):
    """
    Durchsucht rekursiv den Eingabeordner nach PNG-Dateien, entfernt den Alphakanal und speichert sie als JPG in einer Parallelstruktur.
    """
    input_path = Path(input_folder)
    output_folder = input_path.parent / f'{input_path.name}_jpg_95'

    for img_path in input_path.rglob('*.png'):
        relative_path = img_path.relative_to(input_path)
        # Ändere die Dateiendung von .png zu .jpg im Ausgabepfad
        output_path = output_folder / relative_path.with_suffix('.jpg')

        save_as_jpg_with_high_quality(img_path, output_path)

    print(f"Finished processing images from {input_folder}. Saved to {output_folder}")


if __name__ == "__main__":
    input_folder = r'E:\mydata\emoijhero\dataset\dataset-cropped-face18400_resized'  # Aktualisiere diesen Pfad entsprechend
    process_images(input_folder)
