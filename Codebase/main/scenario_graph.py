import pandas as pd
import matplotlib.pyplot as plt
import os 
from scipy.stats import skew, kurtosis, mode
import numpy as np 
from collections import defaultdict

NUM_STEPS = 100

common_path = './statistics/saved/sceneario_wise'

def get_filename(ind):
    return f"scenario_{ind}.csv"

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

data = []

columns_to_plot = [
    "Golpata Stock",
    "Catching Capacity Mangrove",
    "Catching Capacity Household",
    "Crop Production Capacity",
    "Mangrove Fishers in Loan",
    "Household Fishers in Loan",
    "Farmers in Loan"
]

scenarios = ['Favorable', 'Moderate', 'Critical']

for i in range(3):
    ind = i+1
    filename = get_filename(ind)
    df = pd.read_csv(os.path.join(common_path, filename))
    df = df[:NUM_STEPS]
    df = df[columns_to_plot]
    data.append(df)

COLORS = ['#2ca02c', '#1f77b4', '#d62728']

all_metrics = defaultdict(list)

# Plotting with enhanced style
for column in columns_to_plot:
    plt.figure(figsize=(12, 8))

    for i in range(3):
        ind = i+1
        df = data[i]
        df = df[[column]]
        metrics = calculate_metrics(df)
        all_metrics[column].append(metrics)
        plt.plot(df.index, df[column], label=f"{scenarios[ind-1]} Scenario", color=COLORS[i], linewidth=2)

    # Setting title and labels with a sophisticated font
    plt.title(f'{column} vs Time', fontsize=20, fontweight='bold', fontname='serif')
    plt.xlabel('Time', fontsize=16, fontname='serif')
    plt.ylabel(column, fontsize=16, fontname='serif')

    # Adding a grid and legend
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.legend(fontsize=14, frameon=True, shadow=True)

    # Formatting the plot with a "regal" look
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_color('#6E6E6E')
    plt.gca().spines['bottom'].set_color('#6E6E6E')
    plt.gca().spines['left'].set_linewidth(1.5)
    plt.gca().spines['bottom'].set_linewidth(1.5)
    plt.xticks(fontsize=14, fontname='serif')
    plt.yticks(fontsize=14, fontname='serif')

    # Save the plot as an image
    output_filename = f'./plots/scenario/{column.replace(" ", "_").lower()}_vs_time.png'
    plt.savefig(output_filename, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()  # Close the figure after saving

print("Plots have been saved successfully as images.")

stat_keys = []

for column in columns_to_plot:
    vals = defaultdict(list)
    print(column)
    for metrics in all_metrics[column]:
        stat_keys = metrics.keys()
        for k in stat_keys:
            vals[k].append(metrics[k].iloc[0])

    s = ''

    for k in stat_keys:
        vals_str = ''.join([f" & {round(v,4)}" for v in vals[k]])
        s += f"{k}{vals_str}\\\\\n"

    print(f'\n\nGenerated Latex for {column}\n\n')
    print(s)
