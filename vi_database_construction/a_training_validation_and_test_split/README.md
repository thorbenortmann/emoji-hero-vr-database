# VI.A. Training, Validation and Test Split

At the beginning of this step, we have labels for 1,921 images (see [labels.csv](label.csv)).
These labels resulted from the agreement between three annotators,
each labeling 2,590 images (one per reenactment process).
Also, we have the facial recordings in a directory structure like this:

```
facial-recordings
├── <participant-id>
    ├── Level <level-id>
        ├── <emoji-id>-<emotion-name>
            ├── <timestamp>.png
            ├── <timestamp>-1.png
```

In this step, we split the 1,921 labels into training, validation and test sets,
and copy the corresponding images in a new directory structure that looks like this:

```
dataset
├── <set-name>
    ├── <emotion-name>
        ├── <timestamp>-<participant-id>-<camera-index>.png
```
Additionally, we balanced the validation and test sets by iteratively discarding images.
As a result, we have 3,556 images (1,778 * 2 (camera angles)) divided into three set directories.

The details are defined in [select_balanced_labeled_images.py](select_balanced_labeled_images.py).
