import unittest
import numpy as np
from lidaEnvironment import CompostingEnv
import config  # config.py including max_duration
from gym import spaces

class TestCompostingEnvInitialization(unittest.TestCase):
    def setUp(self):
        # Create an instance of CompostingEnv
        self.env = CompostingEnv()

    def test_max_duration(self):
        """Test that max_duration is loaded from config.py"""
        self.assertEqual(self.env.max_duration, config.max_duration)

    def test_thresholds_and_weights(self):
        """Test that weights, optimal_ranges, and extreme_limits are initialized correctly"""
        # Expected weights, optimal ranges, and extreme limits
        expected_weights = {
            "co2": 0.35,
            "methane": 0.23,
            "oxygen": 0.18,
            "temperature": 0.14,
            "moisture": 0.1
        }
        expected_optimal_ranges = {
            "temperature": (0, 40),
            "moisture": (10, 20),
            "oxygen": (10, 25),
            "co2": (15, 30),
            "methane": (0, 5)
        }
        expected_extreme_limits = {
            "temperature": (0, 100),
            "moisture": (10, 100),
            "oxygen": (5, 70),
            "co2": (0, 70),
            "methane": (0, 30)
        }

        self.assertEqual(self.env.weights, expected_weights)
        self.assertEqual(self.env.optimal_ranges, expected_optimal_ranges)
        self.assertEqual(self.env.extreme_limits, expected_extreme_limits)

    def test_initial_state(self):
        """Test that the initial state time is set to 0"""
        self.assertEqual(self.env.state["time"], 0)

    def test_chamber_initialization(self):
        """Test that active_chamber and curing_chamber are initialized with correct sensor values"""
        # Expected sensor values for active and curing chambers
        expected_active_chamber_values = {
            "temperature": np.array([50.0, 52.0, 51.0, 50.0]),
            "moisture": np.array([60.0, 62.0]),
            "oxygen": np.array([15.0]),
            "co2": np.array([5.0]),
            "methane": np.array([1.0])
        }
        expected_curing_chamber_values = {
            "temperature": np.array([60.0, 61.0]),
            "moisture": np.array([70.0, 72.0]),
            "oxygen": np.array([18.0]),
            "co2": np.array([6.0]),
            "methane": np.array([2.0])
        }

        # Validate active_chamber values
        np.testing.assert_array_equal(self.env.active_chamber.get_temperature(), expected_active_chamber_values["temperature"])
        np.testing.assert_array_equal(self.env.active_chamber.get_moisture(), expected_active_chamber_values["moisture"])
        np.testing.assert_array_equal(self.env.active_chamber.get_oxygen(), expected_active_chamber_values["oxygen"])
        np.testing.assert_array_equal(self.env.active_chamber.get_co2(), expected_active_chamber_values["co2"])
        np.testing.assert_array_equal(self.env.active_chamber.get_methane(), expected_active_chamber_values["methane"])

        # Validate curing_chamber values
        np.testing.assert_array_equal(self.env.curing_chamber.get_temperature(), expected_curing_chamber_values["temperature"])
        np.testing.assert_array_equal(self.env.curing_chamber.get_moisture(), expected_curing_chamber_values["moisture"])
        np.testing.assert_array_equal(self.env.curing_chamber.get_oxygen(), expected_curing_chamber_values["oxygen"])
        np.testing.assert_array_equal(self.env.curing_chamber.get_co2(), expected_curing_chamber_values["co2"])
        np.testing.assert_array_equal(self.env.curing_chamber.get_methane(), expected_curing_chamber_values["methane"])

    def test_observation_and_action_spaces(self):
        """Test that observation_space and action_space are initialized correctly"""
        # Check observation_space
        self.assertIsInstance(self.env.observation_space, spaces.Dict)
        self.assertIn("active_chamber", self.env.observation_space.spaces)
        self.assertIn("curing_chamber", self.env.observation_space.spaces)

        # Check action_space
        self.assertIsInstance(self.env.action_space, spaces.Dict)
        self.assertIn("active_chamber", self.env.action_space.spaces)
        self.assertIn("curing_chamber", self.env.action_space.spaces)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
