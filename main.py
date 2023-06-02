import os
from functools import reduce

import pandas as pd

times_scores = pd.read_csv("times_university_scores.csv")
CWUR_scores = pd.read_csv("CWUR_university_scores.csv")
QS_scores = pd.read_csv("QS_university_scores.csv")
ARWU_scores = pd.read_csv("ARWU_university_scores.csv")
webometrics_scores = pd.read_csv("webometrics_university_scores.csv")

# Merge the dataframes
merged_df = reduce(lambda x, y: pd.merge(x, y, on='University Name', how='outer'),
                   [times_scores, CWUR_scores, QS_scores, ARWU_scores, webometrics_scores])


# Save the merged dataframe
merged_df.to_csv("university_scores.csv", index=False)
