from model import MangroveModel
from mesa.batchrunner import BatchRunner

# Define a function to get the final model value
def get_final_model_value(model, num_steps):
    data = model.datacollector.get_model_vars_dataframe().iloc[num_steps - 1]
    return data["Extraction Capacity"]

# Define a function to write a value from the data collector to a file
def write_value_to_file(final_value):
    with open('output_file.txt', 'w') as f:
        f.write(str(final_value))

# Set up the BatchRunner with parameters and model reporters
parameters = {"num_bawali": [100, 200, 300], "num_farmer": [100, 200, 300]}
num_steps = 100
model_reporter = lambda m: get_final_model_value(m, num_steps)

batch_runner = BatchRunner(MangroveModel, parameters, iterations=1, max_steps=num_steps,
                           model_reporters={"MyValue": model_reporter})

# Run the model
batch_runner.run_all()

# After running, get the final model value and write it to a file
final_value = get_final_model_value(batch_runner.model, num_steps)
write_value_to_file(batch_runner.model, final_value)