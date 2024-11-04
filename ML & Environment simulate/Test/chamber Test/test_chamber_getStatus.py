import unittest
import numpy as np
from chamber import Chamber

class TestChamberGetStatus(unittest.TestCase):
    def setUp(self):
        # Initialize the Chamber with sample data
        self.temp = [20, 21, 19]
        self.moisture = [50, 52, 49]
        self.oxygen = [18, 17, 19]
        self.co2 = [0.04, 0.05, 0.03]
        self.methane = [0.01, 0.02, 0.015]
        
        # Create Chamber instance
        self.chamber = Chamber(
            temperature=self.temp,
            moisture=self.moisture,
            oxygen=self.oxygen,
            co2=self.co2,
            methane=self.methane
        )

    def test_get_status(self):
        """Test get_status method returns the correct status of the chamber"""
        # Manually set the status for each component
        self.chamber.operate_paddle(True)
        self.chamber.change_paddle_direction(-1)
        self.chamber.simulate_air_pump(True)
        self.chamber.open_lid()

        # Expected status dictionary
        expected_status = {
            "temperature": np.array(self.temp),
            "moisture": np.array(self.moisture),
            "oxygen": np.array(self.oxygen),
            "methane": np.array(self.methane),
            "co2": np.array(self.co2),
            "paddle_status": True,
            "paddle_direction": -1,
            "lid_status": True,
            "air_pump_status": True
        }

        # Get the actual status from the method
        actual_status = self.chamber.get_status()

        # Check sensor arrays
        np.testing.assert_array_equal(actual_status["temperature"], expected_status["temperature"])
        np.testing.assert_array_equal(actual_status["moisture"], expected_status["moisture"])
        np.testing.assert_array_equal(actual_status["oxygen"], expected_status["oxygen"])
        np.testing.assert_array_equal(actual_status["methane"], expected_status["methane"])
        np.testing.assert_array_equal(actual_status["co2"], expected_status["co2"])

        # Check equipment statuses
        self.assertEqual(actual_status["paddle_status"], expected_status["paddle_status"])
        self.assertEqual(actual_status["paddle_direction"], expected_status["paddle_direction"])
        self.assertEqual(actual_status["lid_status"], expected_status["lid_status"])
        self.assertEqual(actual_status["air_pump_status"], expected_status["air_pump_status"])

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
