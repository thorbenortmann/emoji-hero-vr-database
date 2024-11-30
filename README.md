# EmojiHeroVR Database (EmoHeVRDB)

This repository provides all accompanying information for the paper
[EmojiHeroVR: A Study on Facial Expression Recognition under Partial Occlusion from Head-Mounted Displays](https://doi.org/10.48550/arXiv.2410.03331)
which will be published in IEEE Explore as part of the proceedings of the
[12th International Conference on Affective Computing and Intelligent Interaction (ACII 2024)](https://acii-conf.net/2024/).
This repository is structured mirroring the paper's structure.

Related repositories are:

- https://github.com/MirCore/EmojiHeroVR
- https://github.com/thorbenortmann/POSTER_V2
- https://github.com/thorbenortmann/facial-expression-recognition-microservice
- https://github.com/thorbenortmann/facial-expression-labeling-service

## Request Access to EmoHeVRDB

To request access to EmoHeVRDB, please email `thorben.ortmann@haw-hamburg.de`
with the subject: `EmoHeVRDB Access Request.`
In your email, please include the following information:

**1. Confirmation of Identity**:
Provide a link to your academic profile (e.g., institutional webpage or Google Scholar) to confirm your status as a
researcher.

**2. Requested Subsets**:
Specify which subsets of EmoHeVRDB you wish to access:

- [ ] EmoHeVRDB-SI (one 224x224 image per label)
- [ ] EmoHeVRDB-SFEA (one 63x1 vector per label)
- [ ] EmoHeVRDB-DI (thirty 224x224 images per label)
- [ ] EmoHeVRDB-DFEA (thirty 63x1 vectors per label)

**3. Purpose of Use**:
Clearly describe the intended purpose of using EmoHeVRDB.
Please note that access is provided for research purposes only.

---

If your request is valid,
we will send you an End User License Agreement (EULA) detailing the terms of use for EmoHeVRDB.
After receiving the signed EULA, we will provide a link to download the requested data and a password to decrypt it.

## EmoHeVRDB Subsets and Structure

We use some placeholders to describe EmoHeVRDB's structure. These have the following meanings:

- `<set-name>` is one of `training_set`, `validation_set`, `test_set`.
- `<emotion-name>` ist one of `Anger`, `Disgust`, `Fear`, `Happiness`, `Neutral`, `Sadness` and `Surprise`.
- `<timestamp>` is a Unix timestamp specifying the number of milliseconds since January 1, 1970, midnight UTC.
- `<participant-id>` is a whole number between `1` and `37`.
- `<level-id>` is a whole number between `1` and `4`.
- `<emoji-id>` is a whole number between `0` and `8` for `<level-id>=1`, between `0` and `11` for `<level-id>=2`,
  between `0` and `20` for `<level-id>=3` and between `0` and `27` for `<level-id>=4`.
- `<emotion-id>` is a whole number between `0` and `6`:
  `0=Anger`, `1=Disgust`, `2=Fear`, `3=Happiness`, `4=Neutral`, `5=Sadness`, `6=Surprise`.
- `<camera-index>` is either `0` or `1`: `0=central-view`, `1=side-view`.

### 1. EmoHeVRDB-SI

EmoHeVRDB-SI (EmoHeVRDB-static-images)
contains 3,556 labeled facial images
recorded from central view and 45° side view
with a resolution of 224x224 pixels in jpg format.

EmoHeVRDB-SI has the following directory structure:

```
emoji-hero-vr-db-si
├── <set-name>
... ├── <emotion-name>
    ... ├── <timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>-<camera-index>.jpg`
        ...
```

### 2. EmoHeVRDB-SFEA

EmoHeVRDB-SFEA (EmoHeVRDB-static-facial-expression-activations)
contains 1,727 labeled JSON files, 
each containing a 63-dimensional vector of floating pointing numbers between 0 and 1.

EmoHeVRDB-SFEA has the following directory structure:

```
emoji-hero-vr-db-sfea
├── <set-name>
... ├── <emotion-name>
    ... ├── <timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>.json`
        ...
```


Each JSON file corresponds to exactly one central-view image and one side-view image from EmoHeVRDB-SI.
You can identify the corresponding images by using the file names:

`emoji-hero-vr-db-sfea/<set-name>/<emotion-name>/<timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>.json`  

corresponds to  

`emoji-hero-vr-db-si/<set-name>/<emotion-name>/<timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>-0.jpg`  
and  
`emoji-hero-vr-db-si/<set-name>/<emotion-name>/<timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>-1.jpg`.

### 3. EmoHeVRDB-DI

EmoHeVRDB-DI (EmoHeVRDB-dynamic-image-sequences)
contains 3,556 labeled facial image sequences
recorded from central view and 45° side view.
Each sequence consists of exactly 30 jpg files with a resolution of 224x224 pixels.

EmoHeVRDB-DI has the following directory structure:

```
emoji-hero-vr-db-di
├── <set-name>
... ├── <emotion-name>
    ... ├── <sequence-id>
        ... ├── <timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>-<camera-index>.jpg`
            ...
```

Each sequence in EmoHeVRDB-DI was constructed around one image from EmoHeVRDB-SI.
`<sequence-id>` specifies the corresponding image file from EmoHeVRDB-SI by using its name without the file extension.


### 4. EmoHeVRDB-DFEA

EmoHeVRDB-DFEA (EmoHeVRDB-dynamic-facial-expression-activation-sequences)
contains 1,727 labeled facial expression activation sequences.
Each sequence consists of 30 JSON files.
Each JSON file contains a 63-dimensional vector of floating pointing numbers between 0 and 1.  

EmoHeVRDB-DFEA has the following directory structure:

```
emoji-hero-vr-db-dfea
├── <set-name>
... ├── <emotion-name>
    ... ├── <sequence-id>
        ... ├── <timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>.json`
            ...
```
Each JSON file corresponds to exactly one central-view image and one side-view image from EmoHeVRDB-DI.
You can identify the corresponding images by using the file names:

`emoji-hero-vr-db-dfea/<set-name>/<emotion-name>/<sequence-id>/<timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>.json`

corresponds to

`emoji-hero-vr-db-di/<set-name>/<emotion-name>/<sequence-id>-0/<timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>-0.jpg`  
and  
`emoji-hero-vr-db-di/<set-name>/<emotion-name>/<sequence-id>-1/<timestamp>-<set-id>-<participant-id>-<level-id>-<emoji-id>-<emotion-id>-1.jpg`.
