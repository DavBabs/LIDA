import unittest
import numpy as np
from lidaEnvironment import CompostingEnv

class TestUpdateState(unittest.TestCase):
    def setUp(self):
        # Initialize the CompostingEnv instance
        self.env = CompostingEnv()
        self.env.reset()
        self.tolerance = 0.3  # Set tolerance level to accept errors within 0.3 or below

    def test_update_state_with_paddle_on(self):
        # Set the action with the paddle turned on
        action = {
            'active_chamber': {'paddle': (1, 1), 'air_pump': 0, 'lid': 0, 'duration': 3},
            'curing_chamber': {'paddle': (0, 0), 'air_pump': 0, 'lid': 0, 'duration': 0}
        }
        
        # Save initial state values
        initial_temp = np.mean(self.env.active_chamber.get_temperature())
        initial_moisture = np.mean(self.env.active_chamber.get_moisture())
        initial_co2 = self.env.active_chamber.get_co2()[0]

        # Update the state based on the action
        self.env.update_state(action)

        # Check if temperature, moisture, and CO2 changes are within tolerance
        self.assertGreaterEqual(np.mean(self.env.active_chamber.get_temperature()), initial_temp - self.tolerance)
        self.assertLessEqual(np.mean(self.env.active_chamber.get_moisture()), initial_moisture + self.tolerance)
        self.assertGreaterEqual(self.env.active_chamber.get_co2()[0], initial_co2 - self.tolerance)

    def test_update_state_with_air_pump_on(self):
        # Set the action with the air pump turned on
        action = {
            'active_chamber': {'paddle': (0, 0), 'air_pump': 1, 'lid': 0, 'duration': 3},
            'curing_chamber': {'paddle': (0, 0), 'air_pump': 0, 'lid': 0, 'duration': 0}
        }
        
        # Save initial state values
        initial_oxygen = self.env.active_chamber.get_oxygen()[0]
        initial_methane = self.env.active_chamber.get_methane()[0]

        # Update the state based on the action
        self.env.update_state(action)

        # Check if oxygen and methane changes are within tolerance
        self.assertGreaterEqual(self.env.active_chamber.get_oxygen()[0], initial_oxygen - self.tolerance)
        self.assertLessEqual(self.env.active_chamber.get_methane()[0], initial_methane + self.tolerance)

    def test_update_state_with_natural_changes_only(self):
        # Set the action with all components turned off
        action = {
            'active_chamber': {'paddle': (0, 0), 'air_pump': 0, 'lid': 0, 'duration': 0},
            'curing_chamber': {'paddle': (0, 0), 'air_pump': 0, 'lid': 0, 'duration': 0}
        }
        
        # Save initial state values
        initial_temp = np.mean(self.env.active_chamber.get_temperature())
        initial_moisture = np.mean(self.env.active_chamber.get_moisture())
        initial_co2 = self.env.active_chamber.get_co2()[0]
        initial_methane = self.env.active_chamber.get_methane()[0]
        initial_oxygen = self.env.active_chamber.get_oxygen()[0]

        # Update the state based on the action
        self.env.update_state(action)

        # Check if natural changes are within tolerance
        self.assertLessEqual(np.mean(self.env.active_chamber.get_temperature()), initial_temp + self.tolerance)
        self.assertLessEqual(np.mean(self.env.active_chamber.get_moisture()), initial_moisture + self.tolerance)
        self.assertGreaterEqual(self.env.active_chamber.get_co2()[0], initial_co2 - self.tolerance)
        self.assertGreaterEqual(self.env.active_chamber.get_methane()[0], initial_methane - self.tolerance)
        self.assertLessEqual(self.env.active_chamber.get_oxygen()[0], initial_oxygen + self.tolerance)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
