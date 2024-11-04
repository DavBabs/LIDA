import unittest
import numpy as np
from chamber import Chamber
from lidaEnvironment import CompostingEnv

class TestUpdateFunctions(unittest.TestCase):

    def setUp(self):
        # Initialize environment and chambers for testing
        self.env = CompostingEnv()
        self.test_chamber = Chamber(
            temperature=np.array([50.0, 52.0, 51.0, 50.0]),
            moisture=np.array([60.0, 62.0]),
            oxygen=np.array([15.0]),
            co2=np.array([5.0]),
            methane=np.array([1.0]),
            isEmpty=False
        )

    def test_update_temperature(self):
        # Test temperature update
        initial_temp = np.mean(self.test_chamber.get_temperature())
        adjust_value = 5.0
        self.env.update_temperature(self.test_chamber, adjust_value)
        updated_temp = np.mean(self.test_chamber.get_temperature())
        self.assertAlmostEqual(updated_temp, initial_temp + adjust_value, places=2)

    def test_update_methane(self):
        # Test methane update
        initial_methane = self.test_chamber.get_methane()[0]
        adjust_value = 0.5
        self.env.update_methane(self.test_chamber, adjust_value)
        updated_methane = self.test_chamber.get_methane()[0]
        self.assertAlmostEqual(updated_methane, initial_methane + adjust_value, places=2)

    def test_update_oxygen(self):
        # Test oxygen update
        initial_oxygen = self.test_chamber.get_oxygen()[0]
        adjust_value = 1.0
        self.env.update_oxygen(self.test_chamber, adjust_value)
        updated_oxygen = self.test_chamber.get_oxygen()[0]
        self.assertAlmostEqual(updated_oxygen, initial_oxygen + adjust_value, places=2)

    def test_update_co2(self):
        # Test CO2 update
        initial_co2 = self.test_chamber.get_co2()[0]
        adjust_value = -0.8
        self.env.update_co2(self.test_chamber, adjust_value)
        updated_co2 = self.test_chamber.get_co2()[0]
        self.assertAlmostEqual(updated_co2, initial_co2 + adjust_value, places=2)

    def test_update_moisture(self):
        # Test moisture update
        initial_moisture = np.mean(self.test_chamber.get_moisture())
        adjust_value = -2.0
        self.env.update_moisture(self.test_chamber, adjust_value)
        updated_moisture = np.mean(self.test_chamber.get_moisture())
        self.assertAlmostEqual(updated_moisture, initial_moisture + adjust_value, places=2)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)