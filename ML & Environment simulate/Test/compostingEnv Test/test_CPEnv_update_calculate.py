import unittest
from chamber import Chamber
from lidaEnvironment import CompostingEnv

class TestCalculateAndUpdateFunctions(unittest.TestCase):
    def setUp(self):
        # Initialize the environment and chamber for testing
        self.env = CompostingEnv()
        self.chamber = self.env.active_chamber
        self.duration = 10  # Define a standard duration for testing

    def test_calculate_and_update_temperature(self):
        # Calculate adjustment
        temp_adjustment = self.env.calculate_temperature("paddle", self.duration)
        
        # Record initial temperature
        initial_temp = self.chamber.get_temperature().mean()
        
        # Apply update with the calculated adjustment
        self.env.update_temperature(self.chamber, temp_adjustment)
        
        # Calculate expected new temperature
        expected_temp = initial_temp + temp_adjustment
        
        # Verify the temperature was updated correctly
        updated_temp = self.chamber.get_temperature().mean()
        self.assertAlmostEqual(updated_temp, expected_temp, places=2)

    def test_calculate_and_update_methane(self):
        # Calculate adjustment
        methane_adjustment = self.env.calculate_methane("paddle", self.duration)
        
        # Record initial methane level
        initial_methane = self.chamber.get_methane()[0]
        
        # Apply update with the calculated adjustment
        self.env.update_methane(self.chamber, methane_adjustment)
        
        # Calculate expected new methane level
        expected_methane = initial_methane + methane_adjustment
        
        # Verify the methane level was updated correctly
        updated_methane = self.chamber.get_methane()[0]
        self.assertAlmostEqual(updated_methane, expected_methane, places=2)

    def test_calculate_and_update_oxygen(self):
        # Calculate adjustment
        oxygen_adjustment = self.env.calculate_oxygen("paddle", self.duration)
        
        # Record initial oxygen level
        initial_oxygen = self.chamber.get_oxygen()[0]
        
        # Apply update with the calculated adjustment
        self.env.update_oxygen(self.chamber, oxygen_adjustment)
        
        # Calculate expected new oxygen level
        expected_oxygen = initial_oxygen + oxygen_adjustment
        
        # Verify the oxygen level was updated correctly
        updated_oxygen = self.chamber.get_oxygen()[0]
        self.assertAlmostEqual(updated_oxygen, expected_oxygen, places=2)

    def test_calculate_and_update_co2(self):
        # Calculate adjustment
        co2_adjustment = self.env.calculate_co2("paddle", self.duration)
        
        # Record initial CO2 level
        initial_co2 = self.chamber.get_co2()[0]
        
        # Apply update with the calculated adjustment
        self.env.update_co2(self.chamber, co2_adjustment)
        
        # Calculate expected new CO2 level
        expected_co2 = initial_co2 + co2_adjustment
        
        # Verify the CO2 level was updated correctly
        updated_co2 = self.chamber.get_co2()[0]
        self.assertAlmostEqual(updated_co2, expected_co2, places=2)

    def test_calculate_and_update_moisture(self):
        # Calculate adjustment
        moisture_adjustment = self.env.calculate_moisture("paddle", self.duration)
        
        # Record initial moisture level
        initial_moisture = self.chamber.get_moisture().mean()
        
        # Apply update with the calculated adjustment
        self.env.update_moisture(self.chamber, moisture_adjustment)
        
        # Calculate expected new moisture level
        expected_moisture = initial_moisture + moisture_adjustment
        
        # Verify the moisture level was updated correctly
        updated_moisture = self.chamber.get_moisture().mean()
        self.assertAlmostEqual(updated_moisture, expected_moisture, places=2)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
