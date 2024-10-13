# V.A. Data Annotation Procedure

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
using the facial expression recognition model described in section `III.B`.
You can find it on Google Drive:
https://drive.google.com/file/d/1Niww_GBbVBq2nx9ZCuHOe75FT2grgZaX/view?usp=sharing.

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

The `details.csv` files enabled us to associate the labels with the original files.
It's instance for participant 1 can be found here: [details.csv](details.csv).

All details of the image selection step can be found in [select_best_guesses.py](select_best_guesses.py).
Note that it relies on the
[PosterV2Recognizer class](https://github.com/thorbenortmann/facial-expression-recognition-microservice/blob/study-setup/fer/posterv2/posterv2_recognizer.py)
and other code from the
[facial-expression-recognition-microservice repository](https://github.com/thorbenortmann/facial-expression-recognition-microservice/tree/study-setup).
You can clone the
[facial-expression-recognition-microservice repository](https://github.com/thorbenortmann/facial-expression-recognition-microservice/tree/study-setup),
checkout the
[study-setup branch](https://github.com/thorbenortmann/facial-expression-recognition-microservice/tree/study-setup)
and copy the
[select_best_guesses.py file](select_best_guesses.py)
to the repositories root directory to execute it.

## Image Annotation

The images were given to three annotators who labeled each image in random order.
For labeling, we developed a minimalistic web service using the Python Flask framework.
The labeling service's code is available on GitHub:
https://github.com/thorbenortmann/facial-expression-labeling-service.
