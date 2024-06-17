import csv

class Parameters:
    def __init__(self):
        self.n_bawali = 50
        self.n_mangrove_fisher = 50
        self.n_household_fisher = 50
        self.n_farmer = 50
        self.covariance = 0.1
        self.chosen_natural_hazard_loss = 75
        self.chosen_fertilizer_cost = 0.625
        self.chosen_land_crop_productivity = 20
        self.chosen_golpata_natural_growth_rate = 62.5
        self.chosen_golpata_conservation_growth_rate = 137.5
    
    def generate_parameters_csv(self, filename):
        data = [
            ("n_bawali", self.n_bawali),
            ("n_mangrove_fisher", self.n_mangrove_fisher),
            ("n_household_fisher", self.n_household_fisher),
            ("n_farmer", self.n_farmer),
            ("covariance", self.covariance),
            ("chosen_natural_hazard_loss", self.chosen_natural_hazard_loss),
            ("chosen_fertilizer_cost", self.chosen_fertilizer_cost),
            ("chosen_land_crop_productivity", self.chosen_land_crop_productivity),
            ("chosen_golpata_natural_growth_rate", self.chosen_golpata_natural_growth_rate),
            ("chosen_golpata_conservation_growth_rate", self.chosen_golpata_conservation_growth_rate)
        ]

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['parameter', 'value'])
            writer.writerows(data)

# Usage example:
if __name__ == "__main__":
    parameters = Parameters()
    parameters.generate_parameters_csv('parameters.csv')
