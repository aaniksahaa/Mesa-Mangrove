import mesa
from occupations import *
from config.global_variables import *

import random

class LivelihoodAgent(mesa.Agent):
    def __init__(
            self, id, model,
            init_extraction_capacity,
            init_catching_capacity,
            init_crop_production_capacity,
            init_occupation: Occupation,
            ):
        super().__init__(id, model)

        self.extraction_capacity = init_extraction_capacity
        self.catching_capacity = init_catching_capacity
        self.crop_production_capacity = init_crop_production_capacity
        
        # TODO change this
        self.is_rouge = random.random() < 0.05

        self.occupations = [init_occupation]

        self.in_loan = False 
        # self.loan_amount = 0

    def switch_to_occupation(self, occupation):
        if not isinstance(occupation, Occupation):
            raise TypeError("Only objects of type Occupation can be passed as a parameter.")
        self.occupations.append(occupation)

    def __switch_back_if_needed(self):
        # switch back while needed but keep at least one occupation, the initial one
        while len(self.occupations) > 1:
            current_occupation = self.current_occupation()
            current_step = self.model.step_count
            if(current_step - current_occupation.start_step >= current_occupation.duration):
                self.occupations.pop()

    def current_occupation(self):
        if not self.occupations:
            return None
        return self.occupations[-1]

    def step(self):
        self.current_occupation().step()
        # check if occupations needs to be switched back
        self.__switch_back_if_needed()


class Fisherman(Occupation):
    def __init__(self, name, boat):
        super().__init__(name)
        self.boat = boat

    def work(self):
        return f"{self.name} fishes using {self.boat}."

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

