import unittest
import numpy as np
from lidaEnvironment import CompostingEnv

class TestUpdateStateFunction(unittest.TestCase):

    def setUp(self):
        # Initialize the environment and reset for a known baseline state
        self.env = CompostingEnv()
        self.env.reset()

    def test_update_state_with_paddle_action(self):
        # Action with paddle active for active_chamber
        action = {
            "active_chamber": {
                "paddle": (1, 1),  # Paddle on, clockwise
                "air_pump": 0,
                "lid": 0,
                "duration": 30
            },
            "curing_chamber": {
                "paddle": (0, 0),
                "air_pump": 0,
                "lid": 0,
                "duration": 0
            }
        }
        
        # Get initial temperatures and calculate expected change
        initial_temperatures = np.array(self.env.active_chamber.get_temperature())
        expected_adjustment = self.env.calculate_temperature("paddle", action["active_chamber"]["duration"])
        expected_temperatures = initial_temperatures + expected_adjustment

        # Apply action
        self.env.update_state(action)

        # Verify temperatures increased as expected
        updated_temperatures = np.array(self.env.active_chamber.get_temperature())
        np.testing.assert_array_almost_equal(
            updated_temperatures, expected_temperatures, decimal=2,
            err_msg="Temperature did not update correctly with paddle active"
        )

    def test_update_state_with_air_pump_action(self):
        # Action with air pump active for active_chamber
        action = {
            "active_chamber": {
                "paddle": (0, 0),
                "air_pump": 1,  # Air pump on
                "lid": 0,
                "duration": 30
            },
            "curing_chamber": {
                "paddle": (0, 0),
                "air_pump": 0,
                "lid": 0,
                "duration": 0
            }
        }

        # Get initial values and calculate expected changes
        initial_methane = np.array(self.env.active_chamber.get_methane())
        initial_oxygen = np.array(self.env.active_chamber.get_oxygen())
        initial_co2 = np.array(self.env.active_chamber.get_co2())

        expected_methane_change = self.env.calculate_methane("air_pump", action["active_chamber"]["duration"])
        expected_oxygen_change = self.env.calculate_oxygen("air_pump", action["active_chamber"]["duration"])
        expected_co2_change = self.env.calculate_co2("air_pump", action["active_chamber"]["duration"])

        expected_methane = initial_methane + expected_methane_change
        expected_oxygen = initial_oxygen + expected_oxygen_change
        expected_co2 = initial_co2 + expected_co2_change

        # Apply action
        self.env.update_state(action)

        # Verify methane, oxygen, and CO2 changed as expected
        updated_methane = np.array(self.env.active_chamber.get_methane())
        updated_oxygen = np.array(self.env.active_chamber.get_oxygen())
        updated_co2 = np.array(self.env.active_chamber.get_co2())

        np.testing.assert_array_almost_equal(
            updated_methane, expected_methane, decimal=2,
            err_msg="Methane did not update correctly with air pump active"
        )
        np.testing.assert_array_almost_equal(
            updated_oxygen, expected_oxygen, decimal=2,
            err_msg="Oxygen did not update correctly with air pump active"
        )
        np.testing.assert_array_almost_equal(
            updated_co2, expected_co2, decimal=2,
            err_msg="CO2 did not update correctly with air pump active"
        )

    def test_update_state_with_no_action(self):
        # Action with no components active
        action = {
            "active_chamber": {
                "paddle": (0, 0),
                "air_pump": 0,
                "lid": 0,
                "duration": 0
            },
            "curing_chamber": {
                "paddle": (0, 0),
                "air_pump": 0,
                "lid": 0,
                "duration": 0
            }
        }

        # Capture initial values
        initial_temperatures = np.array(self.env.active_chamber.get_temperature())
        initial_moisture = np.array(self.env.active_chamber.get_moisture())
        initial_oxygen = np.array(self.env.active_chamber.get_oxygen())
        initial_co2 = np.array(self.env.active_chamber.get_co2())

        # Calculate expected natural changes
        natural_temp_change = -0.1
        natural_moisture_change = -0.05
        natural_oxygen_change = -0.03
        natural_co2_change = 0.04

        expected_temperatures = initial_temperatures + natural_temp_change
        expected_moisture = initial_moisture + natural_moisture_change
        expected_oxygen = initial_oxygen + natural_oxygen_change
        expected_co2 = initial_co2 + natural_co2_change

        # Apply no-action update (natural state change)
        self.env.update_state(action)

        # Verify natural decay or changes
        updated_temperatures = np.array(self.env.active_chamber.get_temperature())
        updated_moisture = np.array(self.env.active_chamber.get_moisture())
        updated_oxygen = np.array(self.env.active_chamber.get_oxygen())
        updated_co2 = np.array(self.env.active_chamber.get_co2())

        np.testing.assert_array_almost_equal(
            updated_temperatures, expected_temperatures, decimal=2,
            err_msg="Temperature did not decrease correctly with no action"
        )
        np.testing.assert_array_almost_equal(
            updated_moisture, expected_moisture, decimal=2,
            err_msg="Moisture did not decrease correctly with no action"
        )
        np.testing.assert_array_almost_equal(
            updated_oxygen, expected_oxygen, decimal=2,
            err_msg="Oxygen did not decrease correctly with no action"
        )
        np.testing.assert_array_almost_equal(
            updated_co2, expected_co2, decimal=2,
            err_msg="CO2 did not increase correctly with no action"
        )

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)