import mesa

from config.global_variables import *

import random

class Bawali(mesa.Agent):
    def __init__(
            self, id, model,
            init_extraction_capacity,
            ):
        super().__init__(id, model)
        self.extraction_capacity = init_extraction_capacity
        self.type = Type.BAWALI
        self.is_rouge = random.random() < 0.05
    def step(self):

        # print(self.extraction_capacity)
        
        # parameters that may need global change
        # golpata_stock, golpata_permit

        # needed parameters
        bawali_minimum_capacity = self.model.bawali_minimum_capacity
        movement_cost_bawali = self.model.movement_cost_bawali
        golpata_permit = self.model.golpata_permit


        if((self.model.golpata_permit <= 0  and not self.is_rouge ) or self.model.golpata_stock<=0 ):
            # no permission or no golpata, so no extraction performed
            if(self.extraction_capacity >= bawali_minimum_capacity):
                self.extraction_capacity -= 10 # due to off permission
        elif(self.extraction_capacity < bawali_minimum_capacity):
            # not enough extraction_capacity, so no extraction performed
            self.extraction_capacity += 2 # by fishing or farming
        else:
            # extraction performed
            actual_extraction_amount = min(golpata_permit , self.extraction_capacity)
            new_actual_extraction_amount = actual_extraction_amount - movement_cost_bawali
            self.extraction_capacity += 0.01*new_actual_extraction_amount
            # modifying total golpata_stock
            self.model.golpata_stock -= actual_extraction_amount

class Mangrove_Fisher(mesa.Agent):
    def __init__(self, id, model, init_catching_capacity):
        super().__init__(id, model)
        self.catching_capacity = init_catching_capacity
        self.type = Type.MANGROVE_FISHER
        self.inLoan = 0
    def step(self):
        # needed parameters
        movement_cost_fishermen_M = self.model.movement_cost_fishermen_M
        ice_cost = self.model.ice_cost

        actual_catching_capacity = self.catching_capacity - movement_cost_fishermen_M - ice_cost
        if(actual_catching_capacity <= 0):
            self.inLoan = 1
            self.catching_capacity += 0.1  # takes loan
            return
        # Randomly generate the approx relative catching in 12 months

        # Imagined probability of catching a certain amount of fish

        chance_good = 65
        chance_moderate = 25
        chance_small = 100-chance_good-chance_moderate

        catches = [0]*12
        for i in range(12):
            catches[i] = random.randint(1,100)
        good = 0
        moderate = 0
        small = 0
        for x in catches:
            if(x <= chance_good):
                good += 1
            elif(x <= chance_good+chance_moderate):
                moderate += 1
            else:
                small += 1

        # year-basis calculation

        if(good >= 7):
            self.catching_capacity += 0.05*actual_catching_capacity
        else:
            self.catching_capacity -= 0.075
        
        if(moderate >= 2):
            self.catching_capacity += 0.075
        else:
            self.catching_capacity -= 0.1

        if(small <= 2):
            self.catching_capacity += 0.05
        else:
            self.catching_capacity -= 0.03

        # during jobless month

        self.catching_capacity -= 0.125

        now_capacity = self.catching_capacity

        if(now_capacity > 2.5):
            self.inLoan = 0
            self.catching_capacity -= 0.25 # increased expenses
        if(now_capacity < 2):
            self.inLoan = 1
            self.catching_capacity += 0.1
        
        # due to slight household fishing

        self.catching_capacity += 0.005

class Household_Fisher(mesa.Agent):
    def __init__(self, id, model, init_catching_capacity):
        super().__init__(id, model)
        self.catching_capacity = init_catching_capacity
        self.type = Type.HOUSEHOLD_FISHER
        self.inLoan = 0
    def step(self):
        # needed parameters
        production_cost_fish = self.model.production_cost_fish

        actual_catching_capacity = self.catching_capacity - production_cost_fish
        if(actual_catching_capacity <= 0):
            self.inLoan = 1
            self.catching_capacity += 0.2  # takes loan # 0.1
            return
        #randomly generate fishing relative fishing condition

        chance_good = 60  # 40
        chance_moderate = 25  # 25
        chance_low = 10
        chance_very_low = 100-chance_good-chance_moderate-chance_low

        catches = random.randint(1,100)
        if(catches <= chance_good): # good for most of the year
            self.catching_capacity += 0.1*actual_catching_capacity   # 0.1
        elif(catches <= chance_good+chance_moderate): # moderate
            self.catching_capacity += 0.075*actual_catching_capacity  # 0.075
        elif(catches >= chance_very_low): # very low
            self.catching_capacity -= 0.5

        now_capacity = self.catching_capacity
        if(now_capacity >= 2.7):
            self.inLoan = 0
            self.catching_capacity -= 0.25 # other expenditure
        elif(self.inLoan == 1 and now_capacity > 2):  # 2
            self.inLoan = 0
            self.catching_capacity -= 0.2 # pay back loan
        elif(now_capacity < 1): # 2
            self.inLoan = 1
            self.catching_capacity += 0.2 # taking loan

class Farmer(mesa.Agent):
    def __init__(self, id, model, init_crop_production_capacity):
        super().__init__( id, model )
        self.crop_production_capacity = init_crop_production_capacity
        self.type = Type.FARMER
        self.inLoan = 0
    def step(self):
        # needed parameters
        crop_production_capacity_minimum = self.model.crop_production_capacity_minimum
        land_crop_productivity = self.model.land_crop_productivity
        natural_hazard_loss_crops = self.model.natural_hazard_loss_crops
        fertilizer_cost = self.model.fertilizer_cost

        if(self.crop_production_capacity >= crop_production_capacity_minimum):
            actual_crop_productivity = land_crop_productivity - natural_hazard_loss_crops
            actual_crop_production = 0
            if(self.crop_production_capacity > 0.5*actual_crop_productivity):
                actual_crop_production = 0.5*actual_crop_productivity
            else:
                actual_crop_production = self.crop_production_capacity
            
            if(actual_crop_productivity > 15):
                self.crop_production_capacity += 0.1*(actual_crop_production - fertilizer_cost)
            elif(actual_crop_productivity < 10):
                self.crop_production_capacity = actual_crop_production - fertilizer_cost
            else:
                self.crop_production_capacity += 0.05*(actual_crop_production - fertilizer_cost)
            
        now_capacity = self.crop_production_capacity

        if(now_capacity <= 2): # 2.5
            self.inLoan = 1
            self.crop_production_capacity += 1
        elif(now_capacity > 3): # 4
            self.inLoan = 0
            self.crop_production_capacity -= 1.25