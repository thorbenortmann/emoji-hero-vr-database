from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def create_dataframe(base_directory):
    """Creates a DataFrame with the samples per emotion and set."""
    records = []

    # Iterate through the directory structure and count the files
    for set_name in ['training_set', 'validation_set', 'test_set']:
        for emotion_name in ['Neutral', 'Happiness', 'Sadness', 'Surprise', 'Fear', 'Disgust', 'Anger']:
            emotion_path = base_directory / set_name / emotion_name
            file_count = sum(1 for p in emotion_path.iterdir() if p.is_file() and p.stem.endswith('-0'))
            records.append((emotion_name, set_name, file_count))

    return pd.DataFrame(records, columns=['Emotion', 'Set', 'Samples'])


def plot_stacked_barchart(data):
    """Creates a stacked bar chart from the DataFrame."""
    # Pivot the DataFrame to prepare it for plotting
    data_pivoted = data.pivot(index='Emotion', columns='Set', values='Samples').fillna(0)

    # Adjust the order of the sets for plotting
    data_pivoted = data_pivoted[['training_set', 'validation_set', 'test_set']]

    # Define the color scheme, reverse the order so dark blue is at the bottom
    color_palette = sns.color_palette("Blues_d", n_colors=len(data_pivoted.columns))[::-1]

    # Create the bar chart
    ax = data_pivoted.plot(kind='bar', stacked=True, figsize=(8, 4), width=0.6, color=color_palette)

    # Annotate each bar with its value
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        if height > 0:  # Only annotate if the bar is visible
            ax.text(x + width / 2,
                    y + height / 2,
                    str(int(height)),
                    ha='center',
                    va='center',
                    fontweight='bold',
                    color='white',
                    fontsize=11)

    # Write the total sum of segments per emotion above the bars
    for i, (index, row) in enumerate(data_pivoted.iterrows()):
        total_height = row.sum()
        ax.text(i, total_height + 8, f'{int(total_height)}',
                ha='center', va='bottom', fontsize=12)

    plt.xlabel('Emotion Label', fontsize=12,
               fontweight='bold'
               )
    plt.ylabel('Number of Samples', fontsize=12,
               fontweight='bold'
               )
    plt.xticks(fontsize=13, rotation=0)
    plt.yticks(fontsize=13)

    # Set Y-axis labels in steps of 200
    ax.set_yticks(range(0, max(data_pivoted.sum(axis=1)) + 1, 100))

    plt.legend(title='', labels=['Training', 'Validation', 'Test'], fontsize=11,
               bbox_to_anchor=(0.0, 1.1), loc='upper left')

    # Remove Y-axis gridlines to further clean up the chart
    ax.yaxis.grid(False)

    # Only remove the top and right frame
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    # plt.show()
    plt.savefig('stacked_bar_chart.png', dpi=400)


if __name__ == '__main__':
    base_directory = Path(r'dataset')
    data = create_dataframe(base_directory)
    plot_stacked_barchart(data)
