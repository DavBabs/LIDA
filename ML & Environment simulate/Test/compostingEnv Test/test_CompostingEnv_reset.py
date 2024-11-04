import unittest
import numpy as np
from lidaEnvironment import CompostingEnv  # Assuming this is the correct import path

class TestCompostingEnvReset(unittest.TestCase):
    def setUp(self):
        # Create an instance of CompostingEnv
        self.env = CompostingEnv()

    def test_reset_initial_values(self):
        """Test that reset correctly reinitializes the environment."""
        # Call reset and get the observation
        observation = self.env.reset()

        # Define expected sensor values for active and curing chambers
        expected_active_chamber_values = {
            "temperature": np.array([50.0, 52.0, 51.0, 50.0]),
            "moisture": np.array([60.0, 62.0]),
            "oxygen": np.array([15.0]),
            "co2": np.array([5.0]),
            "methane": np.array([1.0]),
            "isEmpty": False  # active_chamber is not empty after reset
        }
        
        expected_curing_chamber_values = {
            "temperature": np.array([60.0, 61.0]),
            "moisture": np.array([70.0, 72.0]),
            "oxygen": np.array([18.0]),
            "co2": np.array([6.0]),
            "methane": np.array([2.0]),
            "isEmpty": True  # curing_chamber should be empty after reset
        }

        # Validate active_chamber values after reset
        np.testing.assert_array_equal(self.env.active_chamber.get_temperature(), expected_active_chamber_values["temperature"])
        np.testing.assert_array_equal(self.env.active_chamber.get_moisture(), expected_active_chamber_values["moisture"])
        np.testing.assert_array_equal(self.env.active_chamber.get_oxygen(), expected_active_chamber_values["oxygen"])
        np.testing.assert_array_equal(self.env.active_chamber.get_co2(), expected_active_chamber_values["co2"])
        np.testing.assert_array_equal(self.env.active_chamber.get_methane(), expected_active_chamber_values["methane"])
        self.assertEqual(self.env.active_chamber.get_isEmpty(), expected_active_chamber_values["isEmpty"])

        # Validate curing_chamber values after reset
        np.testing.assert_array_equal(self.env.curing_chamber.get_temperature(), expected_curing_chamber_values["temperature"])
        np.testing.assert_array_equal(self.env.curing_chamber.get_moisture(), expected_curing_chamber_values["moisture"])
        np.testing.assert_array_equal(self.env.curing_chamber.get_oxygen(), expected_curing_chamber_values["oxygen"])
        np.testing.assert_array_equal(self.env.curing_chamber.get_co2(), expected_curing_chamber_values["co2"])
        np.testing.assert_array_equal(self.env.curing_chamber.get_methane(), expected_curing_chamber_values["methane"])
        self.assertEqual(self.env.curing_chamber.get_isEmpty(), expected_curing_chamber_values["isEmpty"])

        # Additional check: observation output matches expected values
        self.assertEqual(observation["active_chamber"]["isEmpty"], expected_active_chamber_values["isEmpty"])
        self.assertEqual(observation["curing_chamber"]["isEmpty"], expected_curing_chamber_values["isEmpty"])
        np.testing.assert_array_equal(observation["active_chamber"]["temperature"], expected_active_chamber_values["temperature"])
        np.testing.assert_array_equal(observation["curing_chamber"]["temperature"], expected_curing_chamber_values["temperature"])

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)