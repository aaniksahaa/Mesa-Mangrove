import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis, mode

# Sample DataFrame
data = {
    'Column1': [2.489809285, 2.49111, 2.38423, 2.51722],
    'Column2': [2.487280881, 2.48847, 2.45019, 2.51102],
    'Column3': [2.487386642, 2.48499, 2.46128, 2.54016]
}

df = pd.DataFrame(data)

# Function to calculate metrics
def calculate_metrics(df):
    metrics = {}
    metrics['Mean'] = df.mean()
    metrics['Median'] = df.median()
    metrics['Min'] = df.min()
    metrics['Max'] = df.max()
    metrics['Range'] = df.max() - df.min()
    metrics['Standard Deviation'] = df.std()
    metrics['Variance'] = df.var()
    metrics['Interquartile Range (IQR)'] = df.quantile(0.75) - df.quantile(0.25)
    metrics['Skewness'] = df.apply(skew)
    metrics['Kurtosis'] = df.apply(kurtosis)
    metrics['First Quartile'] = df.quantile(0.25)
    metrics['Third Quartile'] = df.quantile(0.75)
    metrics['MAD (Mean Absolute Deviation)'] = df.apply(lambda x: np.mean(np.abs(x - np.mean(x))))
    metrics['Coefficient of Variation'] = df.std() / df.mean()

    return pd.DataFrame(metrics)

# Calculate and print metrics
metrics_df = calculate_metrics(df)
print(metrics_df)
