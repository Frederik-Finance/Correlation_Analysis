import pandas as pd
import numpy as np
import seaborn as sns
import os
import pickle
import glob
import matplotlib.pyplot as plt


N_CORRELATION_PAIRS = 20


def _unpickle(filename):
    abs_path = os.path.abspath(os.curdir)

    file_paths = glob.glob(os.path.join(
        abs_path, '**', '*' + filename), recursive=True)

    if not file_paths:
        return None

    file_path = min(file_paths, key=len)
    with open(file_path, 'rb') as fp:
        return pickle.load(fp)


corr_df = _unpickle('corr_df')
relevant = _unpickle('relevant')

exlcude = ['UP', 'DOWN', 'BEAR', 'BULL']

non_lev = [symbol for symbol in relevant if all(
    excludes not in symbol for excludes in exlcude)]

stacked = corr_df.filter(non_lev, axis=1).filter(non_lev, axis=0)
stacked = stacked.dropna()

unstacked = stacked.unstack()
unstacked = unstacked[unstacked < 1]


highest_corr = unstacked[unstacked > 0].nlargest(N_CORRELATION_PAIRS)
print(highest_corr)

lowest_corr = unstacked[unstacked < 0].nsmallest(5)

vis_dir = 'visualizations'
if not os.path.exists(vis_dir):
    os.makedirs(vis_dir)


highest_corr = highest_corr.reset_index()
highest_corr = highest_corr.pivot(index='level_1', columns='level_0', values=0)


f, ax = plt.subplots(figsize=(11, 9))

cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(highest_corr, cmap='viridis', annot=True,
            fmt='.2f', cbar=True)

plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.savefig(os.path.join(vis_dir, 'highest_corr.png'))


lowest_corr = lowest_corr.reset_index()
lowest_corr = lowest_corr.pivot(index='level_1', columns='level_0', values=0)


sns.heatmap(lowest_corr, cmap='viridis', annot=True,
            fmt='.2f', cbar=True)
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.savefig(os.path.join(vis_dir, 'lowest_corr.png'))
