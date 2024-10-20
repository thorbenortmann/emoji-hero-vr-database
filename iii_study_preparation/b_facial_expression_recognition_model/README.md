# III.B. Facial Expression Recognition Model

## Artificial Occlusion

We simulated the facial occlusion caused by Virtual Reality Headset by adding black rectangles to images of existing
Facial Expression Recognition databases. For details, see: [occlude_images.py](./occlude_images.py).

## Model Architecture and Training

To train the models described in subsection `III.B. Facial Expression Recognition Model`,
we relied on the Poster++ model architecture.
Accompanying their publication
[POSTER V2: A simpler and stronger facial expression recognition network](https://doi.org/10.48550/arXiv.2301.12149):

```
@article{mao2023poster,
  title={POSTER V2: A simpler and stronger facial expression recognition network},
  author={Mao, Jiawei and Xu, Rui and Yin, Xuesong and Chang, Yuanqi and Nie, Binling and Huang, Aibin},
  journal={arXiv preprint arXiv:2301.12149},
  year={2023},
  doi={10.48550/arXiv.2301.12149}
}
```

Mao et al. published their code in the
[POSTER_V2 repository](https://github.com/Talented-Q/POSTER_V2/tree/18de5591c3fa0b7b22bb9fe2d61e7f813e6e3b08)
under the
[MIT License](https://github.com/Talented-Q/POSTER_V2/blob/18de5591c3fa0b7b22bb9fe2d61e7f813e6e3b08/LICENSE)
on GitHub.

For our training, we created a
[fork](https://github.com/thorbenortmann/POSTER_V2/tree/88986ffd0b12cd4386613e5128c9eaa8a5db05ca)
of the
[POSTER_V2 repository](https://github.com/Talented-Q/POSTER_V2/tree/18de5591c3fa0b7b22bb9fe2d61e7f813e6e3b08).
We only made minor adjustments to the original code for simpler usage and more reproducible environments.

You may find the model for which we reported 81% accuracy on unseen artificially occluded images of the
[KDEF](https://doi.org/10.1080/02699930701626582)
dataset on Google Drive:
https://drive.google.com/file/d/11Joon36cD6onMLS_3vyoqqb9mPj8MpoX/view?usp=sharing

The more detailed evaluation metrics are as follows:

| Emotion       | Precision     | Recall (Class-wise Accuracy)     | F1-Score         |
|---------------|---------------|----------------------------------|------------------|
| Anger         | 0.61          | 0.58                             | 0.60             |
| Disgust       | 0.79          | 0.94                             | 0.86             |
| Fear          | 0.66          | 0.94                             | 0.78             |
| Happy         | 0.96          | 0.98                             | 0.97             |
| Sad           | 0.94          | 0.67                             | 0.78             |
| Surprise      | 1.00          | 0.71                             | 0.83             |
| Neutral       | 0.87          | 0.87                             | 0.87             |
| ------------- | ------------- | -------------------------------- | ---------------- |
| **Average**   | **0.83**      | **0.81**                         | **0.81**         |
