import os
import mesa
import csv

import numpy as np
import pandas as pd 

from config.global_variables import *
from config.initial_parameters import *
from config.settings import *

from model_helpers import *

from agents import Bawali, Mangrove_Fisher, Household_Fisher, Farmer

from utils.normal_dist import get_normally_distributed_data
from utils.beta_dist import get_beta_distributed_data

from datetime import datetime, timedelta

from utils.writer import run_log

from utils.writer import clear_logs
from utils.misc import copy_files, clear_folder

class MangroveModel(mesa.Model):
    description = """
        Usage: Please click 'Reset' after any change in the sliders
"""
    def __init__(self,n_bawali=50,
                 n_mangrove_fisher=50,
                 n_household_fisher=50,
                 n_farmer=50,
                 covariance=0.1,
                 chosen_natural_hazard_loss=75,
                 chosen_fertilizer_cost=0.625,
                 chosen_land_crop_productivity=20,
                 chosen_golpata_natural_growth_rate=62.5,
                 
                 chosen_golpata_conservation_growth_rate=137.5,
                 start_date="2005-01-01"):

        self.step_count = 0
        self.ui_message = ""
        self.parameter_differences = {}
        self.output_differences = {}

        self.time_dependent_params = self.get_time_dependent_params()

        # initializations
        self.agent_count = 0
        self.n_bawali = 0
        self.n_mangrove_fisher = 0
        self.n_household_fisher = 0
        self.n_farmer = 0
        self.days_from_start = 0

        # setting user-chosen parameters
        self.covariance = covariance

        self.fertilizer_cost = chosen_fertilizer_cost
        self.natural_hazard_loss = chosen_natural_hazard_loss
        self.land_crop_productivity = chosen_land_crop_productivity
        self.golpata_conservation_growth_rate = chosen_golpata_conservation_growth_rate
        self.golpata_natural_growth_rate = chosen_golpata_natural_growth_rate

        self.now = datetime.strptime(start_date,"%Y-%m-%d")

        self.schedule = mesa.time.RandomActivation(self)

        # setting global parameters
        self.span = span 

        self.golpata_stock = golpata_stock
        self.golpata_minimum = golpata_minimum

        self.bawali_minimum_capacity = bawali_minimum_capacity
        self.movement_cost_bawali = movement_cost_bawali
        self.ice_cost = ice_cost
        self.movement_cost_fishermen_M = movement_cost_fishermen_M
        self.production_cost_fish = production_cost_fish
        self.natural_hazard_loss_crops = natural_hazard_loss_crops
        self.extraction_control_efficiency = extraction_control_efficiency
        self.regulatory_efficiency = regulatory_efficiency
        self.golpata_permit = golpata_permit
        self.crop_production_capacity_minimum = crop_production_capacity_minimum
        self.max_golpata_permit = max_golpata_permit
        
        # adding agents to the model
        self.add_bawali(n_bawali)
        self.add_mangrove_fisher(n_mangrove_fisher)
        self.add_household_fisher(n_household_fisher)
        self.add_farmer(n_farmer)

        # data collectors 
        self.datacollector = mesa.DataCollector(
            {
                "Golpata Extraction Capacity": get_extraction_capacity,
                "Catching Capacity Mangrove": get_catching_capacity_M,
                "Catching Capacity Household": get_catching_capacity_H,
                "Crop Production Capacity": get_crop_production_capacity,
                "Mangrove Fishers in Loan": get_loan_fishermen_M,
                "Household Fishers in Loan": get_loan_fishermen_H,
                "Farmers in Loan": get_loan_farmer,
                "Golpata Stock": get_golpata_stock,
                "Fishermen": lambda m: m.count_mangrove_fishermen(),
                "Bawali": lambda m: m.count_bawali(),
                "Farmers": lambda m: m.count_farmers(),
            }
        )
        self.params = {
            "n_bawali": self.n_bawali,
            "n_mangrove_fisher": self.n_mangrove_fisher,
            "n_household_fisher": self.n_household_fisher,
            "n_farmer": self.n_farmer,
            "covariance": self.covariance,
            "chosen_natural_hazard_loss": self.natural_hazard_loss,
            "chosen_fertilizer_cost": self.fertilizer_cost,
            "chosen_land_crop_productivity": self.land_crop_productivity,
            "chosen_golpata_natural_growth_rate": self.golpata_natural_growth_rate,
            "chosen_golpata_conservation_growth_rate":self.golpata_conservation_growth_rate
        }
    def count_mangrove_fishermen(self):
        return sum(1 for agent in self.schedule.agents if isinstance(agent, Mangrove_Fisher) and agent.type == Type.MANGROVE_FISHER)

    def count_bawali(self):
        return sum(1 for agent in self.schedule.agents if isinstance(agent, Bawali))

    def count_farmers(self):
        return sum(1 for agent in self.schedule.agents if isinstance(agent, Farmer))        
        
    
    # Add bawalis with beta-distributed characteristics
    def add_bawali(self,n_bawali):
        bawali_capacities = get_beta_distributed_data(init_extraction_capacity, self.covariance, n_bawali)
        for i in range(n_bawali):
            self.agent_count += 1
            self.n_bawali += 1
            b = Bawali(self.agent_count,self,bawali_capacities[i])
            self.schedule.add(b)

    def add_mangrove_fisher(self,n_mangrove_fisher):
        mangrove_fisher_capacities = get_beta_distributed_data(init_catching_capacity_M, self.covariance, n_mangrove_fisher)
        for i in range(n_mangrove_fisher):
            self.agent_count += 1
            mf = Mangrove_Fisher(self.agent_count,self,mangrove_fisher_capacities[i])
            self.schedule.add(mf)
        self.n_mangrove_fisher += n_mangrove_fisher

    def add_household_fisher(self,n_household_fisher):
        household_fisher_capacities = get_beta_distributed_data(init_catching_capacity_H,self.covariance,n_household_fisher)
        for i in range(n_household_fisher):
            self.agent_count += 1
            hf = Household_Fisher(self.agent_count,self,household_fisher_capacities[i])
            self.schedule.add(hf)
        self.n_household_fisher += n_household_fisher
    
    def add_farmer(self,n_farmer):
        farmer_capacities = get_beta_distributed_data(init_crop_production_capacity,self.covariance,n_farmer)
        for i in range(n_farmer):
            self.agent_count += 1
            f = Farmer(self.agent_count,self,farmer_capacities[i])
            self.schedule.add(f)
        self.n_farmer += n_farmer

    def get_time_dependent_params(self):
        df = pd.read_csv('dataset/input_data/parameters.csv')

        input_csv_data = {}

        columns = df.columns.tolist()

        for c in columns:
            data = df[c].tolist()
            # value for default usage
            mean_value = np.mean(np.array(data))
            input_csv_data[c] = [data, mean_value]

        return input_csv_data

    def generate_parameters_csv(self, filename):
        data = [
            ("Number of Bawalis", self.n_bawali),
            ("Number of Mangrove Fishers", self.n_mangrove_fisher),
            ("Number of Household Fishers", self.n_household_fisher),
            ("Number of Farmers", self.n_farmer),
            ("Covariance", self.covariance),
            ("Natural Hazard Loss", self.natural_hazard_loss),
            ("Fertilizer Cost", self.fertilizer_cost),
            ("Land Crop Productivity", self.land_crop_productivity),
            ("Golpata Natural Growth Rate", self.golpata_natural_growth_rate),
            ("Golpata Conservation Growth Rate", self.golpata_conservation_growth_rate)
        ]

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['parameter', 'value'])
            writer.writerows(data)
    
    def calculate_parameter_differences(self):
        top_k = 3

        current_parameters_path = 'statistics/current_run/input_parameters.csv'
        previous_parameters_path = 'statistics/previous_run/input_parameters.csv'

        if not os.path.exists(current_parameters_path):
            run_log(f"File not found: {current_parameters_path}")
            return 
        elif not os.path.exists(previous_parameters_path):
            run_log(f"File not found: {previous_parameters_path}")
            return 

        current_df = pd.read_csv('statistics/current_run/input_parameters.csv')
        previous_df = pd.read_csv('statistics/previous_run/input_parameters.csv')

        merged_df = pd.merge(current_df, previous_df, on='parameter', suffixes=('_current', '_previous'))

        merged_df['value_difference_pct'] = 100*(merged_df['value_current'] - merged_df['value_previous'])/merged_df['value_previous']

        merged_df['absolute_difference_pct'] = merged_df['value_difference_pct'].abs()

        filtered_df = merged_df[merged_df['absolute_difference_pct'] > 0]

        sorted_df = filtered_df.sort_values(by='absolute_difference_pct', ascending=False)

        top_k_parameters = sorted_df.head(top_k)

        top_k_dict = top_k_parameters.set_index('parameter')['value_difference_pct'].to_dict()

        self.parameter_differences = top_k_dict

    def calculate_output_differences(self,data):
        top_k = 3

        current_values = data.iloc[-1]
        previous_values = self.previous_output_values.loc[self.step_count]

        # Transpose the DataFrames to have parameters as columns
        current_values = current_values.transpose().reset_index()
        previous_values = previous_values.transpose().reset_index()

        # Rename columns for clarity
        current_values.columns = ['parameter', 'value_current']
        previous_values.columns = ['parameter', 'value_previous']

        # Merge the two DataFrames on 'Parameter'
        merged_df = pd.merge(previous_values, current_values, on='parameter')

        merged_df['value_difference_pct'] = 100*(merged_df['value_current'] - merged_df['value_previous'])/merged_df['value_previous']

        merged_df['absolute_difference_pct'] = merged_df['value_difference_pct'].abs()

        filtered_df = merged_df[merged_df['absolute_difference_pct'] > 0]

        sorted_df = filtered_df.sort_values(by='absolute_difference_pct', ascending=False)

        top_k_parameters = sorted_df.head(top_k)

        top_k_dict = top_k_parameters.set_index('parameter')['value_difference_pct'].to_dict()

        self.output_differences = top_k_dict

    def get_current_time_dependent_params(self, param_names):
        values = {}
        for param_name in param_names:
            if param_name in self.time_dependent_params:
                data = self.time_dependent_params[param_name]
                if(self.step_count < len(data[0])):
                    values[param_name] = data[0][self.step_count]
                else:
                    values[param_name] = data[1]
            else:
                values[param_name] = None
        return values

    def initiate(self):
        run_log("\n\nModel constructor called\n\n")

        clear_logs()
        copy_files('statistics/current_run', 'statistics/previous_run')
        clear_folder('statistics/current_run/warnings')
        clear_folder('statistics/current_run')

        self.generate_parameters_csv("statistics/current_run/input_parameters.csv")

        run_log('input parameters saved')

        self.calculate_parameter_differences()

        run_log('parameter differences calculated')
        run_log(str(self.parameter_differences))

        self.previous_output_values = pd.read_csv("statistics/previous_run/output_values.csv")
        run_log("\n\n" + str(len(self.previous_output_values)) + "\n\n")

    def step(self):
        if(self.step_count == 0):
            self.initiate()

        # update time dependent params

        time_dependent_param_names = ['Natural Hazard Loss of Golpata', 'Fertilizer Cost', 'Land Crop Productivity', 'Golpata Natural Growth Rate', 'Golpata Conservation Growth Rate']

        params = self.get_current_time_dependent_params(time_dependent_param_names)

        if(params['Natural Hazard Loss of Golpata'] is not None):
            self.natural_hazard_loss = params['Natural Hazard Loss of Golpata']
        if(params['Fertilizer Cost'] is not None):
            self.fertilizer_cost = params['Fertilizer Cost']
        if(params['Land Crop Productivity'] is not None):
            self.land_crop_productivity = params['Land Crop Productivity']
        if(params['Golpata Natural Growth Rate'] is not None):
            self.golpata_natural_growth_rate = params['Golpata Natural Growth Rate']
        if(params['Golpata Conservation Growth Rate'] is not None):
            self.golpata_conservation_growth_rate = params['Golpata Conservation Growth Rate']

        self.schedule.step()
        self.datacollector.collect(self)
        self.now += timedelta(days=span)
        self.days_from_start += span

        # Change in Golpata Stock
        if(self.golpata_stock < self.golpata_minimum):
            self.golpata_permit = 0
            self.golpata_stock += self.golpata_natural_growth_rate + self.golpata_conservation_growth_rate - self.natural_hazard_loss
        else:
            # here we may apply policy
            self.golpata_permit = self.max_golpata_permit
            self.golpata_stock += self.golpata_natural_growth_rate - self.natural_hazard_loss
        
        if self.golpata_stock < 0:
            self.golpata_stock = 0

        data = self.datacollector.get_model_vars_dataframe()

        if len(self.parameter_differences)>0 and len(data)>0 and (len(self.previous_output_values) > self.step_count ):
            self.calculate_output_differences(data)

        if(self.step_count % 10 == 0):
            data.to_csv("statistics/current_run/output_values.csv", index=False)
            run_log(f"Output values saved at step {self.step_count}")

        self.step_count += 1

    def handle_fishermen_debt(self):
        fishermen = [a for a in self.schedule.agents if isinstance(a, Mangrove_Fisher)]
        n = len(fishermen)
        farmers_to_convert = n // 4  # 25%
        bawalis_to_convert = n // 4  # 25%

        selected_for_farming = self.random.sample(fishermen, farmers_to_convert)
        remaining_fishermen = [f for f in fishermen if f not in selected_for_farming]
        selected_for_bawalis = self.random.sample(remaining_fishermen, bawalis_to_convert)

        for fisherman in selected_for_farming:
            fisherman.switch_to_farmer()

        for fisherman in selected_for_bawalis:
            fisherman.switch_to_bawali()

        # UI Message Update
        self.ui_message = f"Converted {farmers_to_convert} fishermen to farmers and {bawalis_to_convert} to bawali."
    