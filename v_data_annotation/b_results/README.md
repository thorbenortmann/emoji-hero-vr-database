# V.B. Data Annotation Results

Each annotator delivered a csv file with their labels for the 2,590 selected reenactments.
Based on the `details.csv` files we created during the image selection,
we connected the labels with the original files and target emotions.

We combined all labels into one csv file ([labels-master-table.csv](labels-master-table.csv)),
and computed several metrics ([cohens_kappa.py](cohens_kappa.py)).
Additionally, we computed some extra columns via excel including the inclusion criterion for the dataset,
i.e. two or more annotators agree on the correct target emotion ([labels-master-table-analysis_irr.csv](labels-master-table-analysis_irr.csv)).

