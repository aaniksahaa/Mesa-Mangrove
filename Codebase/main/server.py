import mesa
from model import MangroveModel  # Make sure to import the necessary model
from mesa.visualization.modules import TextElement
import datetime
import pandas as pd
import re

from utils.writer import run_log

class MyTextElement(TextElement):
    def __init__(self):
        super().__init__()
        run_log('here')
        self.saved_warnings = set()

    def sanitize_filename(self, filename):
        # Remove any characters that are not alphanumeric, underscore, or hyphen
        return re.sub(r'[^a-zA-Z0-9_\-]', '', filename)
    
    def get_table_html(self,type,params):
        table_body = ""
        cnt = 1
        for key, value in params.items():
            color = "green"
            ch = "▲"
            if value < 0:
                color = "red"
                ch = "▼"
            value = abs(round(value,2))
            table_body += f"""
                <tr>
                    <th scope="row">{cnt}</th>
                    <td><b>{key}</b></td>
                    <td><b><font color="{color}">{value}% {ch}</font></b></td>
                </tr>
            """
            cnt += 1
    
        table_html = f"""
                <div class="container mt-5">
                    <table class="table table-striped" style="font-size: 16px;">
                        <thead>
                            <tr>
                            <th scope="col">#</th>
                            <th scope="col">{type}</th>
                            <th scope="col">Change</th>
                            </tr>
                        </thead>
                        <tbody>
                        {table_body}
                        </tbody>
                    </table>
                </div>
            """
        return table_html
    
    def get_warning_messages(self,data):
        # Define threshold values 
        threshold_golpata_extraction = 100
        threshold_fishermen_in_loan = 40
        threshold_household_fishers_in_loan = 175
        threshold_farmers_in_loan = 75
        threshold_crop_production = 8
        threshold_golpata_stock = 0

        warning_messages = []

        # Golpata Extraction Capacity
        golpata_extraction = float(data["Golpata Extraction Capacity"].iloc[-1])
        if golpata_extraction > threshold_golpata_extraction:
            warning_messages.append("WARNING: Over-extraction of Golpata! Implement stricter harvesting quotas.")

        # Mangrove Fishers in Loan
        fishermen_in_loan = int(data["Mangrove Fishers in Loan"].iloc[-1]) + int(data["Household Fishers in Loan"].iloc[-1])
        if fishermen_in_loan > threshold_fishermen_in_loan:
            warning_messages.append("WARNING: High Fishermen Debt! Provide financial aid and alternative livelihood training.")
        
        # Household Fishers in Loan
        if data["Household Fishers in Loan"].iloc[-1] > threshold_household_fishers_in_loan:
            warning_messages.append("WARNING: High Household Fisher Debt! Promote sustainable fishing practices and diversify income sources.")

        # Farmers in Loan
        if data["Farmers in Loan"].iloc[-1] > threshold_farmers_in_loan:
            warning_messages.append("WARNING: High Farmer Debt! Implement crop insurance, improve market access, and promote sustainable agriculture.")

        # Crop Production Capacity
        if data["Crop Production Capacity"].iloc[-1] < threshold_crop_production:
            warning_messages.append("WARNING: Low Crop Production! Invest in agricultural infrastructure and technology, improve soil health, and support farmers with resources.")

        # Golpata Stock
        # if data["Golpata Stock"].iloc[-1] < threshold_golpata_stock:
        #     warning_messages.append("WARNING: Low Golpata Stock! Enforce stricter conservation measures, reforestation efforts, and regulate extraction activities.")

        return warning_messages

    def save_warnings_as_csv(self,model,data,warning_messages):
        # Save parameters each time a new warning appears
        for warning in warning_messages:
            warning_prefix = warning.split("!")[0]  # Extract warning prefix up to "!"
            sanitized_warning_prefix = self.sanitize_filename(warning_prefix)
            if warning_prefix not in self.saved_warnings:
                self.saved_warnings.add(warning_prefix)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"statistics/current_run/warnings/{sanitized_warning_prefix}_{timestamp}.csv"

                # Get the latest data and model parameters
                latest_data = data.iloc[-1:].transpose()  # Get the latest row of data and transpose it
                latest_data.columns = ['Value']  # Rename the column for clarity
                params_df = pd.DataFrame.from_dict(model.params, orient='index', columns=['Value'])

                # Combine both DataFrames
                combined_df = pd.concat([latest_data, params_df])

                # Save to CSV
                combined_df.to_csv(filename)
                run_log(f"Saved warning parameters to {filename}")

    def render(self, model):
        current_step = model.step_count

        # current output metrics
        data = model.datacollector.get_model_vars_dataframe()

        # if len(data)>0 and (len(model.previous_output_values) > current_step - 1):
        #     top_k = 5

        #     current_values = data.iloc[-1]
        #     previous_values = model.previous_output_values.loc[current_step-1]

        #     # Transpose the DataFrames to have parameters as columns
        #     current_values = current_values.transpose().reset_index()
        #     previous_values = previous_values.transpose().reset_index()

        #     # Rename columns for clarity
        #     current_values.columns = ['parameter', 'value_current']
        #     previous_values.columns = ['parameter', 'value_previous']

        #     # Merge the two DataFrames on 'Parameter'
        #     merged_df = pd.merge(previous_values, current_values, on='parameter')

        #     merged_df['value_difference_pct'] = 100*(merged_df['value_current'] - merged_df['value_previous'])/merged_df['value_previous']

        #     merged_df['absolute_difference_pct'] = merged_df['value_difference_pct'].abs()

        #     filtered_df = merged_df[merged_df['absolute_difference_pct'] > 0]

        #     sorted_df = filtered_df.sort_values(by='absolute_difference_pct', ascending=False)

        #     top_k_parameters = sorted_df.head(top_k)

        #     top_k_dict = top_k_parameters.set_index('parameter')['value_difference_pct'].to_dict()

        #     run_log(f"output diff calc at step {current_step}")
        #     run_log(top_k_dict)

        warning_messages = []

        if not data.empty:
            warning_messages = self.get_warning_messages(data)
            self.save_warnings_as_csv(model,data,warning_messages)
            
        if warning_messages:
            restrict_forest_message = "<br>".join(warning_messages)
        else:
            restrict_forest_message = ""  # Clear the message if no warnings

        # Regal HTML Output
        return f"""
        {self.get_table_html("Input Parameter",model.parameter_differences)}
        {self.get_table_html("Output Metric",model.output_differences)}
        <div style="
            border: 3px double #800000;  
            padding: 15px;
            background-color: #fffdf0;  
            font-family: Georgia, serif;  
            text-align: center; 
        ">
            <h2 style="font-size: 1.4em; margin-bottom: 10px; color: #800000;">PRAGMATIC MEASURE</h2>
            <div style="background-color: #fff5ee; padding: 10px; border: 1px solid #deb887; border-radius: 8px;">
                <h3 style="font-size: 1.1em; color: #a0522d;">Warnings for the concerned authority:</h3>
                <ul style="list-style: none; padding: 0; font-size: 0.9em;">
                    {restrict_forest_message}  
                </ul>
            </div>
        </div>
        """
       

# Create text element to display model data
text = MyTextElement()

# chart0 = mesa.visualization.ChartModule(
#     [
#         {"Label": "Golpata Stock", "Color": "#0000FF"},
#     ],162
# )

chart1 = mesa.visualization.ChartModule(
    [
        {"Label": "Golpata Extraction Capacity", "Color": "#0000FF"},
    ],162
)


chart2 = mesa.visualization.ChartModule(
    [
        #{"Label": "Extraction Capacity", "Color": "#FF0000"},
        {"Label": "Catching Capacity Mangrove", "Color": "#00FF00"},
        {"Label": "Catching Capacity Household", "Color": "#FF0000"},
    ],162
)

chart6 = mesa.visualization.ChartModule(
    [
        {"Label": "Crop Production Capacity", "Color": "#0FF0FF"},
    ]
)

chart3 = mesa.visualization.ChartModule(
    [
        {"Label": "Mangrove Fishers in Loan", "Color": "#0F000F"},
    ]
)

chart4 = mesa.visualization.ChartModule(
    [
        {"Label": "Household Fishers in Loan", "Color": "#F000FF"},
    ]
)

chart5 = mesa.visualization.ChartModule(
    [
        {"Label": "Farmers in Loan", "Color": "#0F000F"},
    ]
)



# model_params = {
#     "n_bawali": mesa.visualization.Slider(
#         "Number of Bawalis",
#         300,
#         1,
#         500,
#         1,
#         description="Choose the number of Bawalis",
#     ),
#     "n_mangrove_fisher": mesa.visualization.Slider(
#         "Number of Mangrove Fishermen",
#         300,
#         1,
#         500,
#         1,
#         description="Choose the number of Mangrove Fishermen",
#     ),
#     "n_household_fisher": mesa.visualization.Slider(
#         "Number of Household Fishermen",
#         300,
#         1,
#         500,
#         1,
#         description="Choose the number of Household Fishermen",
#     ),
#     "n_farmer": mesa.visualization.Slider(
#         "Number of Farmers",
#         300,
#         1,
#         500,
#         1,
#         description="Choose the number of Farmers",
#     ),
#     "covariance": mesa.visualization.Slider(
#         "Covariance(%)",
#         0.1,
#         0.01,
#         1,
#         0.01,
#         description="Choose how much agents differ from each other",
#     ),
#     "chosen_natural_hazard_loss": mesa.visualization.Slider(
#         "Natural Hazard Loss of Golpata",
#         75,
#         1,
#         300,
#         1,
#     ),
#     "chosen_fertilizer_cost": mesa.visualization.Slider(
#         "Fertilizer Cost",
#         0.625,
#         0,
#         1.5,
#         0.125,
#     ),
#     "chosen_land_crop_productivity": mesa.visualization.Slider(
#         "Land Crop Productivity",
#         20,
#         5,
#         30,
#         1,
#     ),
#     "chosen_golpata_natural_growth_rate": mesa.visualization.Slider(
#         "Golpata Natural Growth Rate",
#         62.5,
#         50,
#         300,
#         1,
#     ),
#     "chosen_golpata_conservation_growth_rate": mesa.visualization.Slider(
#         "Golpata Conservation Growth Rate",
#         137.5,
#         50,
#         300,
#         1,
#     ),

# }


# server = mesa.visualization.ModularServer(
#     MangroveModel,
#     [text,chart0,chart1,chart2,chart3,chart4,chart5,chart6],
#     "Mangrove Model",
#     model_params
# )



params = [
    {
        "variable_name": "n_bawali",
        "name": "Number of Bawalis",
        "initial_value": 300,
        "min_value": 1,
        "max_value": 500,
        "step_size": 1,
        "description": "Initial count of Bawali"
    },
    {
        "variable_name": "n_mangrove_fisher",
        "name": "Number of Mangrove Fishermen",
        "initial_value": 300,
        "min_value": 1,
        "max_value": 500,
        "step_size": 1,
        "description": "Initial count of Mangrove Fishermen"
    },
    {
        "variable_name": "n_household_fisher",
        "name": "Number of Household Fishermen",
        "initial_value": 300,
        "min_value": 1,
        "max_value": 500,
        "step_size": 1,
        "description": "Initial count of Household Fishermen"
    },
    {
        "variable_name": "n_farmer",
        "name": "Number of Farmers",
        "initial_value": 300,
        "min_value": 1,
        "max_value": 500,
        "step_size": 1,
        "description": "Initial count of Farmers"
    },
    {
        "variable_name": "covariance",
        "name": "Covariance(%)",
        "initial_value": 0.1,
        "min_value": 0.01,
        "max_value": 1,
        "step_size": 0.01,
        "description": "Covariance"
    },
    {
        "variable_name": "chosen_natural_hazard_loss",
        "name": "Natural Hazard Loss of Golpata",
        "initial_value": 75,
        "min_value": 1,
        "max_value": 300,
        "step_size": 1,
        "description": "Impact of Natural Hazard"
    },
    {
        "variable_name": "chosen_fertilizer_cost",
        "name": "Fertilizer Cost",
        "initial_value": 0.625,
        "min_value": 0,
        "max_value": 1.5,
        "step_size": 0.125,
        "description": "Fertilizer Cost"
    },
    {
        "variable_name": "chosen_land_crop_productivity",
        "name": "Land Crop Productivity",
        "initial_value": 20,
        "min_value": 5,
        "max_value": 30,
        "step_size": 1,
        "description": "Land Crop Productivity"
    },
    {
        "variable_name": "chosen_golpata_natural_growth_rate",
        "name": "Golpata Natural Growth Rate",
        "initial_value": 62.5,
        "min_value": 50,
        "max_value": 300,
        "step_size": 1,
        "description": "Natural growth rate of Golpata"
    },
    {
        "variable_name": "chosen_golpata_conservation_growth_rate",
        "name": "Golpata Conservation Growth Rate",
        "initial_value": 137.5,
        "min_value": 50,
        "max_value": 300,
        "step_size": 1,
        "description": "Conservation growth rate of Golpata"
    }
]

rotation_colors = ['green','red']
model_params = {}

for index, param in enumerate(params):
    color = rotation_colors[index % len(rotation_colors)]
    model_params[param["variable_name"]] = mesa.visualization.Slider(
        param["name"],
        param["initial_value"],
        param["min_value"],
        param["max_value"],
        param["step_size"],
        description=param["description"]+";"+color
    )


server = mesa.visualization.ModularServer(
    MangroveModel,
    [text,chart1,chart2,chart3,chart4,chart5,chart6],
    "Mangrove Model",
    model_params
)



server.port = 8524
