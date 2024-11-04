import unittest
import numpy as np
from lidaEnvironment import CompostingEnv


class TestUpdateNaturalAction(unittest.TestCase):
    def setUp(self):
        # Initialize the environment
        self.env = CompostingEnv()
        
        # Set up expected natural changes for verification
        self.expected_temp_change = -0.1
        self.expected_moisture_change = -0.05
        self.expected_methane_increase = 0.02
        self.expected_oxygen_decrease = -0.03
        self.expected_co2_increase = 0.04

        # Get initial chamber values to compute expected results
        self.initial_active_values = {
            "temperature": self.env.active_chamber.get_temperature().copy(),
            "moisture": self.env.active_chamber.get_moisture().copy(),
            "methane": self.env.active_chamber.get_methane().copy(),
            "oxygen": self.env.active_chamber.get_oxygen().copy(),
            "co2": self.env.active_chamber.get_co2().copy()
        }
        self.initial_curing_values = {
            "temperature": self.env.curing_chamber.get_temperature().copy(),
            "moisture": self.env.curing_chamber.get_moisture().copy(),
            "methane": self.env.curing_chamber.get_methane().copy(),
            "oxygen": self.env.curing_chamber.get_oxygen().copy(),
            "co2": self.env.curing_chamber.get_co2().copy()
        }

    def test_update_natural_action_active_chamber(self):
        """Test natural action updates for the active chamber."""
        # Apply natural action
        self.env.update_natural_action(self.env.active_chamber)
        
        # Check temperature
        updated_temperature = self.env.active_chamber.get_temperature()
        expected_temperature = self.initial_active_values["temperature"] + self.expected_temp_change
        np.testing.assert_array_almost_equal(updated_temperature, expected_temperature, decimal=2)

        # Check moisture
        updated_moisture = self.env.active_chamber.get_moisture()
        expected_moisture = self.initial_active_values["moisture"] + self.expected_moisture_change
        np.testing.assert_array_almost_equal(updated_moisture, expected_moisture, decimal=2)

        # Check methane
        updated_methane = self.env.active_chamber.get_methane()
        expected_methane = self.initial_active_values["methane"] + self.expected_methane_increase
        np.testing.assert_array_almost_equal(updated_methane, expected_methane, decimal=2)

        # Check oxygen
        updated_oxygen = self.env.active_chamber.get_oxygen()
        expected_oxygen = self.initial_active_values["oxygen"] + self.expected_oxygen_decrease
        np.testing.assert_array_almost_equal(updated_oxygen, expected_oxygen, decimal=2)

        # Check CO2
        updated_co2 = self.env.active_chamber.get_co2()
        expected_co2 = self.initial_active_values["co2"] + self.expected_co2_increase
        np.testing.assert_array_almost_equal(updated_co2, expected_co2, decimal=2)

    def test_update_natural_action_curing_chamber(self):
        """Test natural action updates for the curing chamber."""
        # Apply natural action
        self.env.update_natural_action(self.env.curing_chamber)
        
        # Check temperature
        updated_temperature = self.env.curing_chamber.get_temperature()
        expected_temperature = self.initial_curing_values["temperature"] + self.expected_temp_change
        np.testing.assert_array_almost_equal(updated_temperature, expected_temperature, decimal=2)

        # Check moisture
        updated_moisture = self.env.curing_chamber.get_moisture()
        expected_moisture = self.initial_curing_values["moisture"] + self.expected_moisture_change
        np.testing.assert_array_almost_equal(updated_moisture, expected_moisture, decimal=2)

        # Check methane
        updated_methane = self.env.curing_chamber.get_methane()
        expected_methane = self.initial_curing_values["methane"] + self.expected_methane_increase
        np.testing.assert_array_almost_equal(updated_methane, expected_methane, decimal=2)

        # Check oxygen
        updated_oxygen = self.env.curing_chamber.get_oxygen()
        expected_oxygen = self.initial_curing_values["oxygen"] + self.expected_oxygen_decrease
        np.testing.assert_array_almost_equal(updated_oxygen, expected_oxygen, decimal=2)

        # Check CO2
        updated_co2 = self.env.curing_chamber.get_co2()
        expected_co2 = self.initial_curing_values["co2"] + self.expected_co2_increase
        np.testing.assert_array_almost_equal(updated_co2, expected_co2, decimal=2)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)