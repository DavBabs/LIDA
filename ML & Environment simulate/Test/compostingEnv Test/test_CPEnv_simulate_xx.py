import unittest
from lidaEnvironment import CompostingEnv
from chamber import Chamber
import numpy as np

class TestCompostingEnvSimulateActions(unittest.TestCase):
    def setUp(self):
        # Create an instance of CompostingEnv
        self.env = CompostingEnv()

    def test_simulate_paddle(self):
        """Test that simulate_paddle correctly operates the paddle."""
        # Test paddle on, clockwise
        self.env.simulate_paddle(self.env.active_chamber, (1, 1))
        self.assertTrue(self.env.active_chamber.get_paddle_status(), "Expected paddle to be on.")
        self.assertEqual(self.env.active_chamber.get_paddle_direction(), 1, "Expected paddle direction to be clockwise.")

        # Test paddle on, counterclockwise
        self.env.simulate_paddle(self.env.active_chamber, (1, 0))
        self.assertTrue(self.env.active_chamber.get_paddle_status(), "Expected paddle to be on.")
        self.assertEqual(self.env.active_chamber.get_paddle_direction(), -1, "Expected paddle direction to be counterclockwise.")

        # Test paddle off
        self.env.simulate_paddle(self.env.active_chamber, (0, 1))
        self.assertFalse(self.env.active_chamber.get_paddle_status(), "Expected paddle to be off.")

    def test_simulate_air_pump(self):
        """Test that simulate_air_pump correctly operates the air pump."""
        # Test air pump on
        self.env.simulate_air_pump(self.env.active_chamber, 1)
        self.assertTrue(self.env.active_chamber.get_air_pump_status(), "Expected air pump to be on.")

        # Test air pump off
        self.env.simulate_air_pump(self.env.active_chamber, 0)
        self.assertFalse(self.env.active_chamber.get_air_pump_status(), "Expected air pump to be off.")

    def test_simulate_lid(self):
        """Test that simulate_lid correctly operates the lid."""
        # Test lid open
        self.env.simulate_lid(self.env.curing_chamber, 1)
        self.assertTrue(self.env.curing_chamber.lid_status, "Expected lid to be open.")

        # Test lid closed
        self.env.simulate_lid(self.env.curing_chamber, 0)
        self.assertFalse(self.env.curing_chamber.lid_status, "Expected lid to be closed.")

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
