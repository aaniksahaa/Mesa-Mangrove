import random

INFINITY = 9999

class Occupation:
    def __init__(self, name, agent, duration):
        self.name = name
        self.agent = agent
        self.start_step = agent.model.step_count
        self.duration = duration 

    def step(self):
        raise NotImplementedError("Subclasses should implement this method.")

class Bawali(Occupation):
    def __init__(self, agent, duration=INFINITY):
        super().__init__('Bawali', agent, duration)

    def step(self):
        agent = self.agent
        model = self.agent.model

        if((agent.golpata_permit <= 0  and not agent.is_rouge ) or model.golpata_stock<=0 ):
            # no permission or no golpata, so no extraction performed
            # has enough extraction capacity
            if(agent.extraction_capacity >= model.bawali_minimum_capacity):
                agent.extraction_capacity -= 10 # due to off permission
        # if they do not have the minimum capacity
        elif(agent.extraction_capacity < model.bawali_minimum_capacity):
            # not enough extraction_capacity, so no extraction performed

            # swicth occupation for one year
            agent.switch_to_occupation(Farmer(agent, 1))
            
            agent.extraction_capacity += 2 # by fishing or farming during the next year
        else:
            # extraction performed
            actual_extraction_amount = min(agent.golpata_permit , agent.extraction_capacity)

            # taking into account the movement cost 
            new_actual_extraction_amount = actual_extraction_amount - model.movement_cost_bawali
            agent.extraction_capacity += 0.01*new_actual_extraction_amount

            # modifying total golpata_stock
            model.golpata_stock -= actual_extraction_amount

class Mangrove_Fisher(Occupation):
    def __init__(self, agent, duration=INFINITY):
        super().__init__('Mangrove_Fisher', agent, duration)

    def step(self):
        agent = self.agent
        model = self.agent.model

        # taking into account the cost
        actual_catching_capacity = agent.catching_capacity - model.movement_cost_fishermen_M - model.ice_cost
        
        if(actual_catching_capacity <= 0):
            agent.in_loan = 1
            agent.catching_capacity += 0.1  # takes loan
            return
        
        # Randomly generate the approx relative catching in 12 months
        # with Imagined probability of catching a certain amount of fish

        # data may be incorporated in this, if exact month-wise fishing data is available

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
            agent.catching_capacity += 0.05*actual_catching_capacity
        else:
            agent.catching_capacity -= 0.075
        
        if(moderate >= 2):
            agent.catching_capacity += 0.075
        else:
            agent.catching_capacity -= 0.1

        if(small <= 2):
            agent.catching_capacity += 0.05
        else:
            agent.catching_capacity -= 0.03

        # during jobless month
        agent.catching_capacity -= 0.125

        now_capacity = agent.catching_capacity

        if(now_capacity > 2.5):
            agent.in_loan = False
            agent.catching_capacity -= 0.25 # increased expenses
        if(now_capacity < 2):
            agent.in_loan = True
            agent.catching_capacity += 0.1
        
        # due to slight household fishing(minor, so not switching)
        agent.catching_capacity += 0.005

class Household_Fisher(Occupation):
    def __init__(self, agent, duration=INFINITY):
        super().__init__('Household_Fisher', agent, duration)

    def step(self):
        agent = self.agent
        model = self.agent.model

        actual_catching_capacity = agent.catching_capacity - model.production_cost_fish
        if(actual_catching_capacity <= 0):
            agent.in_loan = 1
            agent.catching_capacity += 0.2  # takes loan # 0.1
            return
        
        # randomly generate fishing relative fishing condition

        chance_good = 60  # 40
        chance_moderate = 25  # 25
        chance_low = 10
        chance_very_low = 100-chance_good-chance_moderate-chance_low

        catches = random.randint(1,100)

        if(catches <= chance_good): # good for most of the year
            agent.catching_capacity += 0.1*actual_catching_capacity   # 0.1
        elif(catches <= chance_good+chance_moderate): # moderate
            agent.catching_capacity += 0.075*actual_catching_capacity  # 0.075
        elif(catches <= chance_good+chance_moderate+chance_low): # moderate
            agent.catching_capacity += 0  
        else: # very low
            agent.catching_capacity -= 0.5

        now_capacity = agent.catching_capacity

        if(now_capacity >= 2.7):
            agent.in_loan = False
            agent.catching_capacity -= 0.25 # other expenditure
        elif(agent.in_loan == True and now_capacity > 2):  # 2
            agent.in_loan = False
            agent.catching_capacity -= 0.2 # pay back loan
        elif(now_capacity < 1): # 2
            agent.in_loan = True
            agent.catching_capacity += 0.2 # taking loan

class Farmer(Occupation):
    def __init__(self, agent, duration=INFINITY):
        super().__init__('Farmer', agent, duration)

    def step(self):
        agent = self.agent
        model = self.agent.model

        if(agent.crop_production_capacity >= model.crop_production_capacity_minimum):
            actual_crop_productivity = model.land_crop_productivity - model.natural_hazard_loss_crops

            actual_crop_production = 0

            if(agent.crop_production_capacity > 0.5*actual_crop_productivity):
                actual_crop_production = 0.5*actual_crop_productivity
            else:
                actual_crop_production = agent.crop_production_capacity
            
            if(actual_crop_productivity > 15):
                agent.crop_production_capacity += 0.1*(actual_crop_production - model.fertilizer_cost)
            elif(actual_crop_productivity < 10):
                agent.crop_production_capacity = actual_crop_production - model.fertilizer_cost
            else:
                agent.crop_production_capacity += 0.05*(actual_crop_production - model.fertilizer_cost)
            
        now_capacity = agent.crop_production_capacity

        if(now_capacity <= 2): # 2.5
            # takes loan
            agent.in_loan = 1
            agent.crop_production_capacity += 1
        elif(now_capacity > 3): # 4
            # pay back loan
            agent.in_loan = 0
            agent.crop_production_capacity -= 1.25