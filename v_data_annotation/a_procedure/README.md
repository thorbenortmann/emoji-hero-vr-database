# Data Annotation Procedure

## Image Selection

First, we selected one image per participant and reenacted emoji to label.
Each of the 37 participants reenacted 70 emojis.
Thus, we wanted to select 2,590 images.
During study execution, we had saved the images in a structure like this:

```
facial-recordings
├── <participant-id>
    ├── <level-id>
        ├── <emoji-id>-<emotion-name>
            ├── <timestamp>.png
            ├── <timestamp>-1.png
```

For every central-view image, we made a prediction
using the facial expression recognition model described in section III.B.
<!--
For the exact model see: /media/thor/Windows/Users/thorb/Desktop/repos/facial-expression-recognition-microservice
-->
As a result, for each of the 2,590 reenactments,
we selected the image with the highest probability for the correct emotion.

The resulting directory structure looks like this:

```
facial-recordings
├── <participant-id>-for-labeling
    ├── images
    │   ├── <timestamp>.png
    │
    └── details.csv
```

The `detail.csv` files later enabled us to associate the labels with the original files.
It's instance for participant 1 can be found here: [details.csv](details.csv).

All details of the image selection step can be found in [find_best_guesses.py](find_best_guesses.py).

## Annotation

The images were given to three annotators who labeled each image in random order. 
