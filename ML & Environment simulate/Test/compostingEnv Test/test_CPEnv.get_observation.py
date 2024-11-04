import unittest
import numpy as np
from lidaEnvironment import CompostingEnv

class TestCompostingEnvObservation(unittest.TestCase):
    def setUp(self):
        # Create a CompostingEnv instance
        self.env = CompostingEnv()

    def test_get_observation(self):
        """Test whether the observation data returned by the get_observation method meets expectations"""
        # Call the get_observation method to get the actual observation value
        observation = self.env.get_observation()

        # Define the expected observation value
        expected_observation = {
            "active_chamber": {
                "temperature": np.array([50.0, 52.0, 51.0, 50.0]),
                "moisture": np.array([60.0, 62.0]),
                "oxygen": np.array([15.0]),
                "co2": np.array([5.0]),
                "methane": np.array([1.0]),
                "isEmpty": False
            },
            "curing_chamber": {
                "temperature": np.array([60.0, 61.0]),
                "moisture": np.array([70.0, 72.0]),
                "oxygen": np.array([18.0]),
                "co2": np.array([6.0]),
                "methane": np.array([2.0]),
                "isEmpty": True
            }
        }

        # Verify each attribute of active_chamber 
        np.testing.assert_array_equal(
            observation["active_chamber"]["temperature"],
            expected_observation["active_chamber"]["temperature"]
        )
        np.testing.assert_array_equal(
            observation["active_chamber"]["moisture"],
            expected_observation["active_chamber"]["moisture"]
        )
        np.testing.assert_array_equal(
            observation["active_chamber"]["oxygen"],
            expected_observation["active_chamber"]["oxygen"]
        )
        np.testing.assert_array_equal(
            observation["active_chamber"]["co2"],
            expected_observation["active_chamber"]["co2"]
        )
        np.testing.assert_array_equal(
            observation["active_chamber"]["methane"],
            expected_observation["active_chamber"]["methane"]
        )
        self.assertEqual(
            observation["active_chamber"]["isEmpty"],
            expected_observation["active_chamber"]["isEmpty"]
        )

        # Verify each attribute of curing_chamber 
        np.testing.assert_array_equal(
            observation["curing_chamber"]["temperature"],
            expected_observation["curing_chamber"]["temperature"]
        )
        np.testing.assert_array_equal(
            observation["curing_chamber"]["moisture"],
            expected_observation["curing_chamber"]["moisture"]
        )
        np.testing.assert_array_equal(
            observation["curing_chamber"]["oxygen"],
            expected_observation["curing_chamber"]["oxygen"]
        )
        np.testing.assert_array_equal(
            observation["curing_chamber"]["co2"],
            expected_observation["curing_chamber"]["co2"]
        )
        np.testing.assert_array_equal(
            observation["curing_chamber"]["methane"],
            expected_observation["curing_chamber"]["methane"]
        )
        self.assertEqual(
            observation["curing_chamber"]["isEmpty"],
            expected_observation["curing_chamber"]["isEmpty"]
        )

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
