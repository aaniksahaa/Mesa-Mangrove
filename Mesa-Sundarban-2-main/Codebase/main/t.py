import pandas as pd 
import numpy as np 


def get_time_dependent_params():
    df = pd.read_csv('dataset/input_data/parameters.csv')

    input_csv_data = {}

    columns = df.columns.tolist()

    for c in columns:
        data = df[c].tolist()
        # value for default usage
        mean_value = np.mean(np.array(data))
        input_csv_data[c] = [data, mean_value]

    return input_csv_data

print(get_time_dependent_params())