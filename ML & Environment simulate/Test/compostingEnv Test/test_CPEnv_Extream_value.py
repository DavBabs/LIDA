import unittest
import numpy as np
from lidaEnvironment import CompostingEnv

class TestHasExtremeValues(unittest.TestCase):
    def setUp(self):
        # Initialize the environment
        self.env = CompostingEnv()

    def test_no_extreme_values(self):
        """Test that has_extreme_values returns False when all values are within safe limits."""
        self.env.active_chamber.set_temperature(np.array([30.0, 35.0]))
        self.env.active_chamber.set_moisture(np.array([50.0]))
        self.env.active_chamber.set_oxygen(np.array([20.0]))
        self.env.active_chamber.set_co2(np.array([25.0]))
        self.env.active_chamber.set_methane(np.array([2.0]))
        self.assertFalse(self.env.has_extreme_values(self.env.active_chamber))

    def test_temperature_extreme_high(self):
        """Test that has_extreme_values returns True for high temperature exceeding limit."""
        self.env.active_chamber.set_temperature(np.array([105.0]))  # Exceeds max limit
        self.assertTrue(self.env.has_extreme_values(self.env.active_chamber))

    def test_temperature_extreme_low(self):
        """Test that has_extreme_values returns True for low temperature below limit."""
        self.env.active_chamber.set_temperature(np.array([-5.0]))  # Below min limit
        self.assertTrue(self.env.has_extreme_values(self.env.active_chamber))

    def test_moisture_extreme_low(self):
        """Test that has_extreme_values returns True for low moisture below limit."""
        self.env.active_chamber.set_moisture(np.array([5.0]))  # Below min limit
        self.assertTrue(self.env.has_extreme_values(self.env.active_chamber))

    def test_oxygen_extreme_high(self):
        """Test that has_extreme_values returns True for high oxygen exceeding limit."""
        self.env.active_chamber.set_oxygen(np.array([75.0]))  # Exceeds max limit
        self.assertTrue(self.env.has_extreme_values(self.env.active_chamber))

    def test_co2_extreme_high(self):
        """Test that has_extreme_values returns True for high CO2 exceeding limit."""
        self.env.active_chamber.set_co2(np.array([75.0]))  # Exceeds max limit
        self.assertTrue(self.env.has_extreme_values(self.env.active_chamber))

    def test_methane_extreme_high(self):
        """Test that has_extreme_values returns True for high methane exceeding limit."""
        self.env.active_chamber.set_methane(np.array([35.0]))  # Exceeds max limit
        self.assertTrue(self.env.has_extreme_values(self.env.active_chamber))

    def test_multiple_extreme_values(self):
        """Test that has_extreme_values returns True when multiple parameters exceed limits."""
        self.env.active_chamber.set_temperature(np.array([105.0]))  # High temperature
        self.env.active_chamber.set_methane(np.array([35.0]))       # High methane
        self.assertTrue(self.env.has_extreme_values(self.env.active_chamber))

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
