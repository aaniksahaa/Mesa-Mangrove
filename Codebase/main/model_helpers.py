from config.global_variables import *
from config.initial_parameters import *

def get_golpata_stock(model):
    return max(model.golpata_stock,0)

def get_extraction_capacity(model):
    intended_occupation_name = 'Bawali'
    ans = 0
    for agent in model.schedule.agents:
        current_occupation_name = agent.current_occupation().name
        if(current_occupation_name == intended_occupation_name):
            ans += agent.extraction_capacity
    return ans/model.occupation_counts[intended_occupation_name]

def get_catching_capacity_M(model):
    intended_occupation_name = 'Mangrove_Fisher'
    ans = 0
    for agent in model.schedule.agents:
        current_occupation_name = agent.current_occupation().name
        if(current_occupation_name == intended_occupation_name):
            ans += agent.catching_capacity
    return ans/model.occupation_counts[intended_occupation_name]

def get_catching_capacity_H(model):
    intended_occupation_name = 'Household_Fisher'
    ans = 0
    for agent in model.schedule.agents:
        current_occupation_name = agent.current_occupation().name
        if(current_occupation_name == intended_occupation_name):
            ans += agent.catching_capacity
    return ans/model.occupation_counts[intended_occupation_name]

def get_crop_production_capacity(model):
    intended_occupation_name = 'Farmer'
    ans = 0
    for agent in model.schedule.agents:
        current_occupation_name = agent.current_occupation().name
        if(current_occupation_name == intended_occupation_name):
            ans += agent.crop_production_capacity
    return ans/model.occupation_counts[intended_occupation_name]

def get_loan_fishermen_M(model):
    intended_occupation_name = 'Mangrove_Fisher'
    ans = 0
    for agent in model.schedule.agents:
        current_occupation_name = agent.current_occupation().name
        if(current_occupation_name == intended_occupation_name):
            if agent.in_loan:
                ans += 1
    return ans

def get_loan_fishermen_H(model):
    intended_occupation_name = 'Household_Fisher'
    ans = 0
    for agent in model.schedule.agents:
        current_occupation_name = agent.current_occupation().name
        if(current_occupation_name == intended_occupation_name):
            if agent.in_loan:
                ans += 1
    return ans

def get_loan_farmer(model):
    intended_occupation_name = 'Farmer'
    ans = 0
    for agent in model.schedule.agents:
        current_occupation_name = agent.current_occupation().name
        if(current_occupation_name == intended_occupation_name):
            if agent.in_loan:
                ans += 1
    return ans
