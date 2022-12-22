# Correlation_Analysis

Introduction
This project is a tool for analyzing the correlations between different cryptocurrency pairs using historical data from the Binance exchange. The tool uses the log returns of the closing prices of each pair to calculate the correlations and visualize the results in the form of heatmaps.

Dependencies
The following Python libraries are required to run this project:

Pandas
NumPy
Seaborn
Matplotlib
Pickle
Glob
Usage
To use this tool, follow these steps:

Download the historical data for the cryptocurrency pairs you want to analyze from the Binance exchange and save the data as CSV files in the data directory.
Run the preprocess.py script to preprocess the data and create pickled versions of the log returns dataframe (logretdf), closing prices dataframe (closesdf), and merged dataframe (mergeddf).
Run the correlation.py script to calculate the correlations between the pairs and create heatmaps of the highest and lowest correlated pairs. The heatmaps will be saved in the visualizations directory.
License
This project is licensed under the MIT License. See the LICENSE file for details.
