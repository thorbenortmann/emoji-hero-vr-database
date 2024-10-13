from statistics import mean

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import cohen_kappa_score
from statsmodels.stats.inter_rater import fleiss_kappa


def calculate_accuracy(data, true_labels_col, predicted_labels_col):
    """
    Calculate the accuracy of predictions against true labels.

    Parameters:
    - data: pandas DataFrame containing the labels
    - true_labels_col: string, name of the column with the true labels
    - predicted_labels_col: string, name of the column with the predicted labels

    Returns:
    - accuracy: float, the accuracy of the predictions
    """
    true_labels = data[true_labels_col]
    predicted_labels = data[predicted_labels_col]
    accuracy = accuracy_score(true_labels, predicted_labels)
    return accuracy


def calculate_cohens_kappa(data, label_col1, label_col2):
    """
    Calculate Cohen's Kappa Score between two sets of labels.

    Parameters:
    - data: pandas DataFrame containing the labels
    - label_col1: string, name of the first column of labels
    - label_col2: string, name of the second column of labels

    Returns:
    - kappa: float, Cohen's Kappa Score
    """
    label_1 = data[label_col1]
    label_2 = data[label_col2]
    kappa = cohen_kappa_score(label_1, label_2)
    return kappa


def calculate_fleiss_kappa(data, label_cols):
    """
    Calculate Fleiss' Kappa for a set of label columns.

    Parameters:
    - data: pandas DataFrame containing the labels
    - label_cols: list of strings, names of the columns with labels from different raters

    Returns:
    - kappa: float, Fleiss' Kappa score
    """
    # Convert the label columns into a format suitable for Fleiss' Kappa computation
    # Count the frequency of each category in each row (image)
    category_counts = data[label_cols].apply(lambda x: x.value_counts(), axis=1).fillna(0)

    # Compute Fleiss' Kappa
    kappa = fleiss_kappa(category_counts)

    return kappa


def compute_confusion_matrix(df, label_cols):
    predicted_labels = df[label_cols].values.flatten()
    expected_labels = np.repeat(df['target_emotion'], 3)
    labels = sorted(df['target_emotion'].unique())

    report = classification_report(expected_labels, predicted_labels, labels=labels, target_names=labels, digits=4)
    print(report)

    cm = confusion_matrix(expected_labels, predicted_labels, labels=labels)

    plt.figure(figsize=(7, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels, cbar=False,
                annot_kws={'size': 11, 'weight': 'bold'})
    plt.xlabel('Labeled Emotion', fontsize=12, fontweight='bold')
    plt.ylabel('Emotion to Reenact', fontsize=12, fontweight='bold')
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.tight_layout()
    plt.savefig('confusion_matrix.eps', dpi=400)


if __name__ == '__main__':
    # Load the dataset
    FILE_PATH = r'labels-master-table-analysis_irr.csv'
    ONLY_INCLUDED = False
    df = pd.read_csv(FILE_PATH, delimiter=';')

    if ONLY_INCLUDED:
        df = df[df['agreement'] >= 2]

    # Calculate Accuracy Score for each labeler
    accuracy_1 = calculate_accuracy(df, 'target_emotion', 'label_1')
    accuracy_2 = calculate_accuracy(df, 'target_emotion', 'label_2')
    accuracy_3 = calculate_accuracy(df, 'target_emotion', 'label_3')

    # Calculate Cohen's Kappa Score for each pair of labelers
    kappa_1 = calculate_cohens_kappa(df, 'target_emotion', 'label_1')
    kappa_2 = calculate_cohens_kappa(df, 'target_emotion', 'label_2')
    kappa_3 = calculate_cohens_kappa(df, 'target_emotion', 'label_3')
    kappa_12 = calculate_cohens_kappa(df, 'label_1', 'label_2')
    kappa_13 = calculate_cohens_kappa(df, 'label_1', 'label_3')
    kappa_23 = calculate_cohens_kappa(df, 'label_2', 'label_3')

    fleiss_kappa_score = calculate_fleiss_kappa(df, ['label_1', 'label_2', 'label_3'])

    compute_confusion_matrix(df, ['label_1', 'label_2', 'label_3'])

    # Output the results
    print(f"Accuracy Scores:")
    print(f"Labeler 1: {accuracy_1:.4f}")
    print(f"Labeler 2: {accuracy_2:.4f}")
    print(f"Labeler 3: {accuracy_3:.4f}")
    print(f"Average: {mean([accuracy_1, accuracy_2, accuracy_3]):.4f}")

    print(f"\nCohen's Kappa Scores:")
    print(f"Labeler 1: {kappa_1:.4f}")
    print(f"Labeler 2: {kappa_2:.4f}")
    print(f"Labeler 3: {kappa_3:.4f}")
    print(f"Average: {mean([kappa_1, kappa_2, kappa_3]):.4f}")

    print(f"\nLabeler 1 vs Labeler 2: {kappa_12:.4f}")
    print(f"Labeler 1 vs Labeler 3: {kappa_13:.4f}")
    print(f"Labeler 2 vs Labeler 3: {kappa_23:.4f}")
    print(f"Average: {mean([kappa_12, kappa_13, kappa_23]):.4f}")

    print(f"\nFleiss' Kappa Score: {fleiss_kappa_score:.4f}")

# OUTPUT
#               precision    recall  f1-score   support
#
#        Anger     0.7237    0.5144    0.6014      1110
#      Disgust     0.7084    0.5712    0.6324      1110
#         Fear     0.6364    0.5423    0.5856      1110
#    Happiness     0.8880    0.9640    0.9244      1110
#      Neutral     0.6616    0.9405    0.7768      1110
#      Sadness     0.6295    0.6721    0.6501      1110
#     Surprise     0.7824    0.8261    0.8037      1110
#
#     accuracy                         0.7187      7770
#    macro avg     0.7186    0.7187    0.7106      7770
# weighted avg     0.7186    0.7187    0.7106      7770
#
# Accuracy Scores:
# Labeler 1: 0.6687
# Labeler 2: 0.7413
# Labeler 3: 0.7459
# Average: 0.7187
#
# Cohen's Kappa Scores:
# Labeler 1: 0.6135
# Labeler 2: 0.6982
# Labeler 3: 0.7036
# Average: 0.6718
#
# Labeler 1 vs Labeler 2: 0.6732
# Labeler 1 vs Labeler 3: 0.6333
# Labeler 2 vs Labeler 3: 0.7282
# Average: 0.6782
#
# Fleiss' Kappa Score: 0.6776
