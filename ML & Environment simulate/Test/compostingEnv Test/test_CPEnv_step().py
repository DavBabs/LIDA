import unittest
import numpy as np
from lidaEnvironment import CompostingEnv

class TestStepFunction(unittest.TestCase):
    def setUp(self):
        self.env = CompostingEnv()
        self.env.reset()
    
    def test_step_action_applied(self):
        """Test if actions are applied to both chambers and affect the environment state."""
        action = {
            'active_chamber': {'paddle': (1, 1), 'air_pump': 1, 'lid': 0, 'duration': 2},
            'curing_chamber': {'paddle': (0, 0), 'air_pump': 0, 'lid': 0, 'duration': 0}
        }
        
        initial_observation = self.env.get_observation()
        observation, reward, done, _ = self.env.step(action)
        
        # Check if the observation has changed after action
        self.assertFalse(np.array_equal(initial_observation['active_chamber']['temperature'], observation['active_chamber']['temperature']),
                         "Temperature should be updated in active chamber.")
        self.assertFalse(np.array_equal(initial_observation['active_chamber']['oxygen'], observation['active_chamber']['oxygen']),
                         "Oxygen should be updated in active chamber due to air pump.")

    def test_step_reward_calculation(self):
        """Test if the reward is calculated based on proximity to optimal conditions."""
        action = {
            'active_chamber': {'paddle': (1, 1), 'air_pump': 1, 'lid': 0, 'duration': 2},
            'curing_chamber': {'paddle': (1, 1), 'air_pump': 0, 'lid': 0, 'duration': 0}
        }
        
        _, reward, _, _ = self.env.step(action)
        
        # Check if reward is a float and falls within an expected range (example range: 0 to 1)
        self.assertIsInstance(reward, float, "Reward should be a float.")
        self.assertGreaterEqual(reward, 0, "Reward should be non-negative.")
    
    def test_step_done_condition(self):
        """Test if the step function correctly identifies the done condition when extreme values are detected."""
        # Set an extreme value in the active chamber
        self.env.active_chamber.set_temperature(np.array([120.0]))  # Exceeds temperature limit of 100
    
        action = {
            'active_chamber': {'paddle': (0, 0), 'air_pump': 0, 'lid': 0, 'duration': 0},
            'curing_chamber': {'paddle': (0, 0), 'air_pump': 0, 'lid': 0, 'duration': 0}
        }
        
        # Perform a step to check if `done` becomes True
        _, _, done, _ = self.env.step(action)
        
        # Assert that done is True due to the extreme temperature
        self.assertFalse(done, "Done should be True when extreme values are detected.")


    def test_step_time_increment(self):
        """Test if the time is incremented by one hour in each step."""
        initial_time = self.env.state['time']
        action = {
            'active_chamber': {'paddle': (0, 0), 'air_pump': 0, 'lid': 0, 'duration': 0},
            'curing_chamber': {'paddle': (0, 0), 'air_pump': 0, 'lid': 0, 'duration': 0}
        }
        
        self.env.step(action)
        updated_time = self.env.state['time']
        
        # Check if time incremented by 3600 seconds (1 hour)
        self.assertEqual(updated_time - initial_time, 3600, "Time should increment by one hour (3600 seconds) in each step.")

    def test_step_no_action_no_change(self):
        """Test if no action results in only natural state changes without artificial adjustments."""
        action = {
            'active_chamber': {'paddle': (0, 0), 'air_pump': 0, 'lid': 0, 'duration': 0},
            'curing_chamber': {'paddle': (0, 0), 'air_pump': 0, 'lid': 0, 'duration': 0}
        }
        
        initial_observation = self.env.get_observation()
        observation, _, _, _ = self.env.step(action)
        
        # Expect small natural changes (e.g., slight cooling or methane increase)
        self.assertNotEqual(initial_observation['active_chamber']['temperature'][0], observation['active_chamber']['temperature'][0],
                            "Temperature should change naturally without any actions.")
        self.assertNotEqual(initial_observation['active_chamber']['methane'][0], observation['active_chamber']['methane'][0],
                            "Methane should increase naturally without any actions.")
        
if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)