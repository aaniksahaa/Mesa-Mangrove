
from config.global_variables import *
from config.settings import *

span = 365
if(time_mode == Type.DAY):
    span = 1
elif(time_mode == Type.MONTH):
    span = 30

multiplier = span/365

golpata_rate_multiplier = 100  # not sure

# Independent of Time Mode
init_golpata_stock = 113888
golpata_minimum = init_golpata_stock * 0.4

# Dependent on Time Mode

# environment defining parameters
bawali_minimum_capacity = 40*multiplier

scenarios = ['Favorable', 'Moderate', 'Critical']

current_scenario = scenarios[2]

# Favorable

if current_scenario == 'Favorable':
    movement_cost_bawali = 10*multiplier

    golpata_conservation_growth_rate = 150*multiplier
    golpata_natural_growth_rate = 75*multiplier
    natural_hazard_loss = 50*multiplier

    ice_cost = 0.25*multiplier 
    movement_cost_fishermen_M = 0.25*multiplier 
    production_cost_fish = 0.25*multiplier 
    natural_hazard_loss_crops = 0.5*multiplier 
    fertilizer_cost = 0.5*multiplier 
    extraction_control_efficiency = 4
    regulatory_efficiency = 2 

# Moderate
if current_scenario == 'Moderate':
    movement_cost_bawali = 14.75*multiplier

    golpata_conservation_growth_rate = 125*multiplier
    golpata_natural_growth_rate = 62.5*multiplier
    natural_hazard_loss = 75*multiplier

    ice_cost = 0.375*multiplier 
    movement_cost_fishermen_M = 0.375*multiplier 
    production_cost_fish = 0.5*multiplier 
    natural_hazard_loss_crops = 0.75*multiplier 
    fertilizer_cost = 0.75*multiplier 
    extraction_control_efficiency = 3 
    regulatory_efficiency = 1.5 

# Critical
if current_scenario == 'Critical':
    movement_cost_bawali = 20*multiplier

    golpata_conservation_growth_rate = 100*multiplier
    golpata_natural_growth_rate = 50*multiplier
    natural_hazard_loss = 100*multiplier

    ice_cost = 0.5*multiplier 
    movement_cost_fishermen_M = 0.5*multiplier 
    production_cost_fish = 0.75*multiplier 
    natural_hazard_loss_crops = 1*multiplier 
    fertilizer_cost = 1*multiplier 
    extraction_control_efficiency = 2 
    regulatory_efficiency = 1

crop_production_capacity_minimum = 1*multiplier
land_crop_productivity = 20*multiplier 

# Case 2

max_golpata_permit = 125*multiplier
init_golpata_permit = max_golpata_permit
init_catching_capacity_M = 2.3*multiplier  
init_catching_capacity_H = 2.3*multiplier  
init_crop_production_capacity = 5*multiplier 

# agent initialization parameters
init_extraction_capacity = 40*multiplier  # 50
