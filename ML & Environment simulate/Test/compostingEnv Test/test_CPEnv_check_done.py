import unittest
import numpy as np
from lidaEnvironment import CompostingEnv

class TestCheckDone(unittest.TestCase):
    def setUp(self):
        self.env = CompostingEnv()

    def test_check_done_successful_completion(self):
        """Test if check_done() returns True when optimal conditions are met after 14 days."""
        # Set the time to 14 days in seconds
        self.env.state['time'] = 14 * 24 * 60 * 60
        
        # Mock optimal conditions in both chambers
        self.env.active_chamber.set_temperature(np.array([25.0, 25.0, 25.0, 25.0]))
        self.env.active_chamber.set_moisture(np.array([15.0, 15.0]))
        self.env.active_chamber.set_oxygen(np.array([20.0]))
        self.env.active_chamber.set_co2(np.array([20.0]))
        self.env.active_chamber.set_methane(np.array([2.5]))

        self.env.curing_chamber.set_temperature(np.array([25.0, 25.0]))
        self.env.curing_chamber.set_moisture(np.array([15.0, 15.0]))
        self.env.curing_chamber.set_oxygen(np.array([20.0]))
        self.env.curing_chamber.set_co2(np.array([20.0]))
        self.env.curing_chamber.set_methane(np.array([2.5]))

        # Test if check_done returns True
        self.assertTrue(self.env.check_done())

    def test_check_done_excessive_duration(self):
        """Test if check_done() returns True when time exceeds 20 days without optimal conditions."""
        # Set time to 20 days in seconds
        self.env.state['time'] = 20 * 24 * 60 * 60

        # Test if check_done returns True
        self.assertTrue(self.env.check_done())

    def test_check_done_extreme_values(self):
        """Test if check_done() returns True when extreme values are detected in the chambers."""
        # Set time to less than 14 days
        self.env.state['time'] = 10 * 24 * 60 * 60

        # Mock extreme values in active chamber
        self.env.active_chamber.set_temperature(np.array([120.0]))  # exceeds the extreme limit for temperature

        # Test if check_done returns True
        self.assertTrue(self.env.check_done())

    def test_check_done_not_done(self):
        """Test if check_done() returns False when neither duration, extreme values, nor optimal conditions are met."""
        # Set time to less than 14 days
        self.env.state['time'] = 10 * 24 * 60 * 60

        # Set conditions within normal but non-optimal range
        self.env.active_chamber.set_temperature(np.array([35.0, 35.0, 35.0, 35.0]))
        self.env.active_chamber.set_moisture(np.array([25.0, 25.0]))
        self.env.active_chamber.set_oxygen(np.array([18.0]))
        self.env.active_chamber.set_co2(np.array([10.0]))
        self.env.active_chamber.set_methane(np.array([8.0]))

        self.env.curing_chamber.set_temperature(np.array([35.0, 35.0]))
        self.env.curing_chamber.set_moisture(np.array([25.0, 25.0]))
        self.env.curing_chamber.set_oxygen(np.array([18.0]))
        self.env.curing_chamber.set_co2(np.array([10.0]))
        self.env.curing_chamber.set_methane(np.array([8.0]))

        # Test if check_done returns False
        self.assertFalse(self.env.check_done())

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
