import os
import random
import mesa
import csv

import numpy as np 
import pandas as pd 

from config.global_variables import *
from config.initial_parameters import *
from config.settings import *

from model_helpers import *

from agents import LivelihoodAgent

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
                 chosen_natural_hazard_loss=natural_hazard_loss,
                 chosen_fertilizer_cost=fertilizer_cost,
                 chosen_land_crop_productivity=20,
                 chosen_golpata_natural_growth_rate=golpata_natural_growth_rate,
                 chosen_golpata_conservation_growth_rate=golpata_conservation_growth_rate,
                 chosen_rogue_percentage=0.05,
                 policy = 'Policy 1',
                 start_date="2005-01-01"):
        
        self.policy = policy 

        self.step_count = 0
        self.parameter_differences = {}
        self.output_differences = {}

        self.time_dependent_params = self.get_time_dependent_params()

        # initializations
        self.agent_count = 0

        occupation_names = ['Bawali', 'Mangrove_Fisher', 'Household_Fisher', 'Farmer']

        self.occupation_counts = {}

        for occupation_name in occupation_names:
            self.occupation_counts[occupation_name] = 0

        # self.n_bawali = 0
        # self.n_mangrove_fisher = 0
        # self.n_household_fisher = 0
        # self.n_farmer = 0

        self.days_from_start = 0

        # setting user-chosen parameters
        self.covariance = covariance

        self.fertilizer_cost = chosen_fertilizer_cost
        self.natural_hazard_loss = chosen_natural_hazard_loss
        self.land_crop_productivity = chosen_land_crop_productivity
        self.golpata_conservation_growth_rate = chosen_golpata_conservation_growth_rate
        self.golpata_natural_growth_rate = chosen_golpata_natural_growth_rate
        self.rogue_percentage = chosen_rogue_percentage

        self.now = datetime.strptime(start_date,"%Y-%m-%d")

        self.schedule = mesa.time.RandomActivation(self)

        # setting global parameters
        self.span = span 

        self.golpata_stock = init_golpata_stock
        self.golpata_minimum = golpata_minimum

        self.bawali_minimum_capacity = bawali_minimum_capacity
        self.movement_cost_bawali = movement_cost_bawali
        self.ice_cost = ice_cost
        self.movement_cost_fishermen_M = movement_cost_fishermen_M
        self.production_cost_fish = production_cost_fish
        self.natural_hazard_loss_crops = natural_hazard_loss_crops
        self.extraction_control_efficiency = extraction_control_efficiency
        self.regulatory_efficiency = regulatory_efficiency
        self.init_golpata_permit = init_golpata_permit
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
                "Current Bawali Count": get_current_bawali_count
            }
        )

        self.params = {
            "n_bawali": self.occupation_counts['Bawali'],
            "n_mangrove_fisher": self.occupation_counts['Mangrove_Fisher'],
            "n_household_fisher": self.occupation_counts['Household_Fisher'],
            "n_farmer": self.occupation_counts['Farmer'],
            "covariance": self.covariance,
            "chosen_natural_hazard_loss": self.natural_hazard_loss,
            "chosen_fertilizer_cost": self.fertilizer_cost,
            "chosen_land_crop_productivity": self.land_crop_productivity,
            "chosen_golpata_natural_growth_rate": self.golpata_natural_growth_rate,
            "chosen_golpata_conservation_growth_rate":self.golpata_conservation_growth_rate,
            "chosen_rogue_percentage":self.rogue_percentage,
        }    
    
    # Add bawalis with beta-distributed characteristics
    def add_bawali(self,n_bawali):
        bawali_capacities = get_beta_distributed_data(init_extraction_capacity, self.covariance, n_bawali)
        for i in range(n_bawali):
            self.agent_count += 1
            self.occupation_counts['Bawali'] += 1
            b = LivelihoodAgent(self.agent_count,self)
            b.init_bawali(bawali_capacities[i])
            self.schedule.add(b)

    def add_mangrove_fisher(self,n_mangrove_fisher):
        mangrove_fisher_capacities = get_beta_distributed_data(init_catching_capacity_M, self.covariance, n_mangrove_fisher)
        for i in range(n_mangrove_fisher):
            self.agent_count += 1
            self.occupation_counts['Mangrove_Fisher'] += 1
            mf = LivelihoodAgent(self.agent_count,self)
            mf.init_mangrove_fisher(mangrove_fisher_capacities[i])
            self.schedule.add(mf)

    def add_household_fisher(self,n_household_fisher):
        household_fisher_capacities = get_beta_distributed_data(init_catching_capacity_H,self.covariance,n_household_fisher)
        for i in range(n_household_fisher):
            self.agent_count += 1
            self.occupation_counts['Household_Fisher'] += 1
            hf = LivelihoodAgent(self.agent_count,self)
            hf.init_household_fisher(household_fisher_capacities[i])
            self.schedule.add(hf)
    
    def add_farmer(self,n_farmer):
        farmer_capacities = get_beta_distributed_data(init_crop_production_capacity,self.covariance,n_farmer)
        for i in range(n_farmer):
            self.agent_count += 1
            self.occupation_counts['Farmer'] += 1
            f = LivelihoodAgent(self.agent_count,self)
            f.init_farmer(farmer_capacities[i])
            self.schedule.add(f)

    def get_time_dependent_params(self):
        input_csv_data = {}

        parameters_path = 'dataset/input_data/parameters.csv'

        if not os.path.exists(parameters_path):
            return input_csv_data
        
        df = pd.read_csv(parameters_path)

        columns = df.columns.tolist()

        for c in columns:
            data = df[c].tolist()
            # value for default usage
            mean_value = np.mean(np.array(data))
            input_csv_data[c] = [data, mean_value]

        return input_csv_data

    def generate_parameters_csv(self, filename):
        data = [
            ("Number of Bawalis", self.occupation_counts['Bawali']),
            ("Number of Mangrove Fishers", self.occupation_counts['Mangrove_Fisher']),
            ("Number of Household Fishers", self.occupation_counts['Household_Fisher']),
            ("Number of Farmers", self.occupation_counts['Farmer']),
            ("Covariance", self.covariance),
            ("Natural Hazard Loss", self.natural_hazard_loss),
            ("Fertilizer Cost", self.fertilizer_cost),
            ("Land Crop Productivity", self.land_crop_productivity),
            ("Golpata Natural Growth Rate", self.golpata_natural_growth_rate),
            ("Golpata Conservation Growth Rate", self.golpata_conservation_growth_rate),
            ("Rogue Percentage", self.rogue_percentage),
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
        #clear_folder('statistics/current_run/warnings')
        copy_files('statistics/current_run', 'statistics/previous_run')
        clear_folder('statistics/current_run')

        self.generate_parameters_csv("statistics/current_run/input_parameters.csv")

        run_log('input parameters saved')

        self.calculate_parameter_differences()

        run_log('parameter differences calculated')
        run_log(str(self.parameter_differences))

        self.previous_output_values = pd.read_csv("statistics/previous_run/output_values.csv")
        run_log("\n\n" + str(len(self.previous_output_values)) + "\n\n")

    def step(self):
        # print(f'at step {self.step_count}')

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

        # print('steps run for all agents')

        self.datacollector.collect(self)
        self.now += timedelta(days=span)
        self.days_from_start += span

        critical_situation = False

        POLICY = self.policy

        if POLICY == 'Policy 1':
            num_stages = 1
            threshold_fractions = [0.25]
            zero_permission_percentages = [0.2]
            rest_permission_fractions = [0.2]

        if POLICY == 'Policy 2':
            num_stages = 2
            threshold_fractions = [0.25, 0.5]
            zero_permission_percentages = [0.5, 0.1]
            rest_permission_fractions = [0.1, 0.8]

        if POLICY == 'Policy 3':
            num_stages = 3
            threshold_fractions = [0.25, 0.33, 0.5]
            zero_permission_percentages = [0.5, 0.3, 0.1]
            rest_permission_fractions = [0.1, 0.5, 0.8]

        for i in range(num_stages):
            if(self.golpata_stock < threshold_fractions[i]*init_golpata_stock):
                for agent in self.schedule.agents:
                    if(agent.original_occupation().name == 'Bawali'):
                        random_indicator = random.random()  # from 0 to 1
                        if random.random() < zero_permission_percentages[i]:
                            agent.golpata_permit = 0
                        else:
                            agent.golpata_permit = self.max_golpata_permit*rest_permission_fractions[i]
                self.golpata_stock += (self.golpata_natural_growth_rate + self.golpata_conservation_growth_rate - self.natural_hazard_loss)*golpata_rate_multiplier
                critical_situation = True 
                break

        if not critical_situation:
            for agent in self.schedule.agents:
                if(agent.original_occupation().name == 'Bawali'):
                    agent.golpata_permit = self.max_golpata_permit

            self.golpata_stock += (self.golpata_natural_growth_rate - self.natural_hazard_loss)*golpata_rate_multiplier
            
        
        if self.golpata_stock < 0:
            self.golpata_stock = 0

        data = self.datacollector.get_model_vars_dataframe()
        
        # calculating output differences
        if len(self.parameter_differences)>0 and len(data)>0 and (len(self.previous_output_values) > self.step_count ):
            self.calculate_output_differences(data)

        # saving output values for future comparison
        if(self.step_count % 10 == 0):
            data.to_csv("statistics/current_run/output_values.csv", index=False)
            run_log(f"Output values saved at step {self.step_count}")

        self.step_count += 1