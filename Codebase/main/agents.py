import mesa
from config.initial_parameters import *
from occupations import *
import random

class LivelihoodAgent(mesa.Agent):
    INFINITY = 9999
    def __init__(
            self, id, model,
            # init_extraction_capacity,
            # init_catching_capacity,
            # init_crop_production_capacity,
            # init_occupation,
            ):
        super().__init__(id, model)

        self.extraction_capacity = 0
        self.catching_capacity = 0
        self.crop_production_capacity = 0

        self.golpata_permit = model.init_golpata_permit

        self.occupations = []
        
        # TODO change this
        self.is_rouge = random.random() < model.rogue_percentage

        self.in_loan = False 
        # self.loan_amount = 0

    def init_bawali(self,init_extraction_capacity):
        self.extraction_capacity = init_extraction_capacity
        self.catching_capacity = 0
        self.crop_production_capacity = 0

        # initial occupation
        self.occupations.append(Bawali(self))

    def init_mangrove_fisher(self,init_catching_capacity):
        self.extraction_capacity = 0
        self.catching_capacity = init_catching_capacity
        self.crop_production_capacity = 0

        # initial occupation
        self.occupations.append(Mangrove_Fisher(self))

    def init_household_fisher(self,init_catching_capacity):
        self.extraction_capacity = 0
        self.catching_capacity = init_catching_capacity
        self.crop_production_capacity = 0

        # initial occupation
        self.occupations.append(Household_Fisher(self))

    def init_farmer(self,init_crop_production_capacity):
        self.extraction_capacity = 0
        self.catching_capacity = 0
        self.crop_production_capacity = init_crop_production_capacity

        # initial occupation
        self.occupations.append(Farmer(self))

    def switch_to_occupation(self, occupation):
        model = self.model 

        current_occupation = self.current_occupation()
        model.occupation_counts[current_occupation.name] -= 1
        model.occupation_counts[occupation.name] += 1

        self.occupations.append(occupation)

        # giving the needed capacity
        if(occupation.name == 'Bawali'):
            self.extraction_capacity = init_extraction_capacity
        elif(occupation.name == 'Mangrove_Fisher'):
            self.catching_capacity = init_catching_capacity_M
        elif(occupation.name == 'Household_Fisher'):
            self.catching_capacity = init_catching_capacity_H
        elif(occupation.name == 'Farmer'):
            self.crop_production_capacity = init_crop_production_capacity

        #print(f'\nOne {current_occupation.name} switched to {occupation.name}\n')

    def __switch_back_if_needed(self):
        current_occupation = self.current_occupation()

        # switch back while needed but keep at least one occupation, the initial one
        while len(self.occupations) > 1:
            current_occupation = self.current_occupation()
            current_step = self.model.step_count
            if(current_step - current_occupation.start_step >= current_occupation.duration):
                self.occupations.pop()
            else:
                break

        final_occupation = self.current_occupation()

        #print(f'\nOne {current_occupation.name} switched back to {final_occupation.name}\n')

    def current_occupation(self):
        if not self.occupations:
            return None
        return self.occupations[-1]
    
    def original_occupation(self):
        if not self.occupations:
            return None
        return self.occupations[0]

    def step(self):
        self.current_occupation().step()

        # check if occupations needs to be switched back
        self.__switch_back_if_needed()
