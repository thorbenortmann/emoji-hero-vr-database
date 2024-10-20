# VI.B. Construction and Statistics

## Sequence Construction

In the previous step
([a_training_validation_and_test_split](../a_training_validation_and_test_split/README.md)),
we selected 3,556 images as the basis for the rest of EmoHeVRDB.

Next, we include 29 additional images per image to cover about one second of facial movement per 30 image sequence.
Thus, based on the selected images:

```
dataset
├── <set-name>
    ├── <emotion-name>
        ├── <timestamp>-<participant-id>-<camera-index>.png
```

We search the original image structure

```
facial-recordings
├── <participant-id>
    ├── Level <level-id>
        ├── <emoji-id>-<emotion-name>
            ├── <timestamp>.png
            ├── <timestamp>-1.png
```

to find the additional images.

In the new structure, we can find an image's origin in the original structure using its path.
First, we extract the `<participant-id>` in the image's name to navigate to the `<participant-id>`'s directory.
Next, we need to go into each `<level-id>`'s directory until we find our match.
In each `<level-id>`'s directory, we navigate into each `<emoji-id>-<emotion-name>`'s directory
where `<emotion-name>` matches the `<emotion-name>` of the new image's path.
In each of these directories, we iterate through all `.png` files until we find match.
To find the match we use the `<timestamp>` and `<camera-index>` information of the image name.
A `<camera-index>` value of `0` in the new structure corresponds to no value in the original structure,
a `<camera-index>` value of `1` corresponds to the `1` in half of the images names'.

We save the data in a structure analog to the new structure.
However, this time we include all information in each image's name:
`<timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>-<camera-index>.png`.
`<set-id>` is `0`, `1` and `2`for `training_set`, `validation_set` and `test_set`, respectively.
`<emotion-id>` is derived from `<emotion-name>` as follows:
`Anger : 0,
Disgust : 1,
Fear : 2,
Happiness : 3,
Neutral: 4,
Sadness : 5,
Surprise : 6,
`

You can find all details of this processing step in [organize_images.py](./organize_images.py) for static images
and in [organize_image_sequences.py](./organize_image_sequences.py), respectively.

## Image Processing

For static images and image sequences, we applied the same processing steps:

1. [1_crop_images2face.py](./1_crop_images2face.py): We detected a face on each original image (resolution 1280x720)
   and cropped the image accordingly.
   Each face's bounding box or cropped image is at least 400x400 pixels in size.
2. [2_resize_images.py](./2_resize_images.py): We resized the images to a uniform size of 224x224 pixels.
3. [3_to_jpg.py](./3_to_jpg.py): We converted the files from `PNG` to `JPG`.
