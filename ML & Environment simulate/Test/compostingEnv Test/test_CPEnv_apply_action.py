import unittest
from lidaEnvironment import CompostingEnv
import numpy as np

class TestCompostingEnvApplyAction(unittest.TestCase):
    def setUp(self):
        # Initialize the environment
        self.env = CompostingEnv()
        self.env.reset()

    def test_apply_action_paddle_on_clockwise(self):
        """Test applying action to turn paddle on with clockwise direction in active chamber."""
        action = {
            "active_chamber": {"paddle": (1, 1), "air_pump": 0, "lid": 0, "duration": 10},
            "curing_chamber": {"paddle": (0, 0), "air_pump": 0, "lid": 0, "duration": 0}
        }
        self.env.apply_action(self.env.active_chamber, action['active_chamber'])
        
        # Check paddle status and direction
        self.assertTrue(self.env.active_chamber.get_paddle_status(), "Paddle should be on")
        self.assertEqual(self.env.active_chamber.get_paddle_direction(), 1, "Paddle direction should be clockwise")

    def test_apply_action_paddle_on_counterclockwise(self):
        """Test applying action to turn paddle on with counterclockwise direction in curing chamber."""
        action = {
            "active_chamber": {"paddle": (0, 0), "air_pump": 0, "lid": 0, "duration": 0},
            "curing_chamber": {"paddle": (1, 0), "air_pump": 0, "lid": 0, "duration": 10}
        }
        self.env.apply_action(self.env.curing_chamber, action['curing_chamber'])
        
        # Check paddle status and direction
        self.assertTrue(self.env.curing_chamber.get_paddle_status(), "Paddle should be on")
        self.assertEqual(self.env.curing_chamber.get_paddle_direction(), -1, "Paddle direction should be counterclockwise")

    def test_apply_action_air_pump_on(self):
        """Test applying action to turn air pump on in active chamber."""
        action = {
            "active_chamber": {"paddle": (0, 0), "air_pump": 1, "lid": 0, "duration": 10},
            "curing_chamber": {"paddle": (0, 0), "air_pump": 0, "lid": 0, "duration": 0}
        }
        self.env.apply_action(self.env.active_chamber, action['active_chamber'])
        
        # Check air pump status
        self.assertTrue(self.env.active_chamber.get_air_pump_status(), "Air pump should be on")

    def test_apply_action_lid_open(self):
        """Test applying action to open the lid in curing chamber."""
        action = {
            "active_chamber": {"paddle": (0, 0), "air_pump": 0, "lid": 0, "duration": 0},
            "curing_chamber": {"paddle": (0, 0), "air_pump": 0, "lid": 1, "duration": 10}
        }
        self.env.apply_action(self.env.curing_chamber, action['curing_chamber'])
        
        # Check lid status
        self.assertTrue(self.env.curing_chamber.lid_status, "Lid should be open")

    def test_apply_action_all_off(self):
        """Test applying action to turn off all components in active chamber."""
        action = {
            "active_chamber": {"paddle": (0, 0), "air_pump": 0, "lid": 0, "duration": 10},
            "curing_chamber": {"paddle": (0, 0), "air_pump": 0, "lid": 0, "duration": 0}
        }
        # Apply the action
        self.env.apply_action(self.env.active_chamber, action['active_chamber'])
        
        # Check that all components are off
        self.assertFalse(self.env.active_chamber.get_paddle_status(), "Paddle should be off")
        self.assertFalse(self.env.active_chamber.get_air_pump_status(), "Air pump should be off")
        self.assertFalse(self.env.active_chamber.lid_status, "Lid should be closed")

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
