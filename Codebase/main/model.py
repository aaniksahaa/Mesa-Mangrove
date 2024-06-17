import os
import mesa
import csv

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
        self.parameter_differences = {}
        self.output_differences = {}

        # initializations
        self.agent_count = 0
        self.n_bawali = 0
        self.n_mangrove_fisher = 0
        self.n_household_fisher = 0
        self.n_farmer = 0
        self.days_from_start = 0

        # setting user-chosen parameters
        self.fertilizer_cost = chosen_fertilizer_cost
        self.natural_hazard_loss = chosen_natural_hazard_loss
        self.land_crop_productivity = chosen_land_crop_productivity
        self.golpata_conservation_growth_rate = chosen_golpata_conservation_growth_rate
        self.golpata_natural_growth_rate = chosen_golpata_natural_growth_rate
        self.covariance = covariance

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
                #"Golpata Stock": get_golpata_stock,
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

        data = self.datacollector.get_model_vars_dataframe()

        if len(self.parameter_differences)>0 and len(data)>0 and (len(self.previous_output_values) > self.step_count ):
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

        if(self.step_count % 10 == 0):
            data.to_csv("statistics/current_run/output_values.csv", index=False)
            run_log(f"Output values saved at step {self.step_count}")

        self.step_count += 1