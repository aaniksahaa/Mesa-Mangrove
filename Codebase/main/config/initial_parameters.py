
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
crop_production_capacity_minimum = 1*multiplier
land_crop_productivity = 20*multiplier # 8
max_golpata_permit = 150*multiplier
init_golpata_permit = 150*multiplier

# agent initialization parameters
init_extraction_capacity = 40*multiplier  # 50
init_catching_capacity_M = 3.5*multiplier  # 2.3
init_catching_capacity_H = 2.7*multiplier  # 2.3
init_crop_production_capacity = 2.5*multiplier # 5
