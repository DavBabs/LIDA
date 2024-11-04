import unittest
import numpy as np
from chamber import Chamber

class TestChamberUpdates(unittest.TestCase):
    def setUp(self):
        # Initialize the Chamber with sample data
        self.temp = [20.0, 21.44, 19.9]
        self.moisture = [50.17, 52.5, 49.26]
        self.oxygen = [18.35, 17.8, 19.28]
        self.co2 = [0.04, 0.05, 0.78]
        self.methane = [0.65, 0.12, 0.38]
        
        # Create Chamber instance
        self.chamber = Chamber(
            temperature=self.temp,
            moisture=self.moisture,
            oxygen=self.oxygen,
            co2=self.co2,
            methane=self.methane
        )

    def test_update_temperature(self):
        """Test update_temperature method for single and all sensor updates"""
        # Update single sensor
        self.chamber.update_temperature(5, index=1)
        self.assertAlmostEqual(self.chamber.temperature[1], 26.44, places=2)
        
        # Update all sensors
        self.chamber.update_temperature(-5)
        np.testing.assert_array_almost_equal(self.chamber.temperature, np.array([15.0, 21.44, 14.9]), decimal=2)
        
        # Check out of bounds
        with self.assertRaises(IndexError):
            self.chamber.update_temperature(5, index=3)

    def test_update_moisture(self):
        """Test update_moisture method for single and all sensor updates"""
        # Update single sensor
        self.chamber.update_moisture(3, index=0)
        self.assertAlmostEqual(self.chamber.moisture[0], 53.17, places=2)
        
        # Update all sensors
        self.chamber.update_moisture(-10)
        np.testing.assert_array_almost_equal(self.chamber.moisture, np.array([43.17, 42.5, 39.26]), decimal=2)
        
        # Check out of bounds
        with self.assertRaises(IndexError):
            self.chamber.update_moisture(5, index=3)

    def test_update_oxygen(self):
        """Test update_oxygen method for single and all sensor updates"""
        # Update single sensor
        self.chamber.update_oxygen(2, index=2)
        self.assertAlmostEqual(self.chamber.oxygen[2], 21.28, places=2)
        
        # Update all sensors
        self.chamber.update_oxygen(-3)
        np.testing.assert_array_almost_equal(self.chamber.oxygen, np.array([15.35, 14.8, 18.28]), decimal=2)
        
        # Check out of bounds
        with self.assertRaises(IndexError):
            self.chamber.update_oxygen(5, index=3)

    def test_update_co2(self):
        """Test update_co2 method for single and all sensor updates"""
        # Update single sensor
        self.chamber.update_co2(0.01, index=1)
        self.assertAlmostEqual(self.chamber.co2[1], 0.06, places=2)
        
        # Update all sensors
        self.chamber.update_co2(-0.02)
        np.testing.assert_array_almost_equal(self.chamber.co2, np.array([0.02, 0.04, 0.76]), decimal=2)
        
        # Check out of bounds
        with self.assertRaises(IndexError):
            self.chamber.update_co2(0.01, index=3)

    def test_update_methane(self):
        """Test update_methane method for single and all sensor updates"""
        # Update single sensor
        self.chamber.update_methane(0.005, index=0)
        self.assertAlmostEqual(self.chamber.methane[0], 0.65, places=2)
        
        # Update all sensors
        self.chamber.update_methane(-0.01)
        np.testing.assert_array_almost_equal(self.chamber.methane, np.array([0.645, 0.11, 0.37]), decimal=2)
        
        # Check out of bounds
        with self.assertRaises(IndexError):
            self.chamber.update_methane(0.005, index=3)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
