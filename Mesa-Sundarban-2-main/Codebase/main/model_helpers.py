import mesa

from config.global_variables import *
from config.initial_parameters import *

def get_golpata_stock(model):
    return model.golpata_stock

def get_extraction_capacity(model):
    ans = 0
    for agent in model.schedule.agents:
        if(agent.type == Type.BAWALI):
            ans += agent.extraction_capacity
    return ans/model.n_bawali

def get_catching_capacity_M(model):
    ans = 0
    for agent in model.schedule.agents:
        if(agent.type == Type.MANGROVE_FISHER):
            ans += agent.catching_capacity
    return ans/model.n_mangrove_fisher

def get_catching_capacity_H(model):
    ans = 0
    for agent in model.schedule.agents:
        if(agent.type == Type.HOUSEHOLD_FISHER):
            ans += agent.catching_capacity
    return ans/model.n_household_fisher

def get_crop_production_capacity(model):
    ans = 0
    for agent in model.schedule.agents:
        if(agent.type == Type.FARMER):
            ans += agent.crop_production_capacity
    return ans/model.n_farmer

def get_loan_fishermen_M(model):
    ans = 0
    for agent in model.schedule.agents:
        if(agent.type == Type.MANGROVE_FISHER):
            ans += agent.inLoan
    return ans

def get_loan_fishermen_H(model):
    ans = 0
    for agent in model.schedule.agents:
        if(agent.type == Type.HOUSEHOLD_FISHER):
            ans += agent.inLoan
    return ans

def get_loan_farmer(model):
    ans = 0
    for agent in model.schedule.agents:
        if(agent.type == Type.FARMER):
            ans += agent.inLoan
    return ans
