import unittest
import numpy as np
from chamber import Chamber

class TestChamberGetters(unittest.TestCase):
    def setUp(self):
        # Initialize the Chamber with sample data
        self.temp = [20, 21, 19]
        self.moisture = [50, 52, 49]
        self.oxygen = [18, 17, 19]
        self.co2 = [0.04, 0.05, 0.03]
        self.methane = [0.01, 0.02, 0.015]
        
        # Create Chamber instance
        self.chamber = Chamber(
            temperature=self.temp,
            moisture=self.moisture,
            oxygen=self.oxygen,
            co2=self.co2,
            methane=self.methane
        )

    def test_get_isEmpty_status(self):
        """Test get_isEmpty_status method returns correct value"""
        self.assertTrue(self.chamber.get_isEmpty_status())

    def test_get_paddle_status(self):
        """Test get_paddle_status method returns correct value"""
        self.assertFalse(self.chamber.get_paddle_status())

    def test_get_paddle_direction(self):
        """Test get_paddle_direction method returns correct value"""
        self.assertEqual(self.chamber.get_paddle_direction(), 1)

    def test_get_air_pump_status(self):
        """Test get_air_pump_status method returns correct value"""
        self.assertFalse(self.chamber.get_air_pump_status())

    def test_get_temperature(self):
        """Test get_temperature method returns correct values and handles index correctly"""
        # Check full array
        np.testing.assert_array_equal(self.chamber.get_temperature(), np.array(self.temp))
        # Check individual indexes
        self.assertEqual(self.chamber.get_temperature(0), self.temp[0])
        self.assertEqual(self.chamber.get_temperature(1), self.temp[1])
        self.assertEqual(self.chamber.get_temperature(2), self.temp[2])
        # Check out of bounds
        with self.assertRaises(IndexError):
            self.chamber.get_temperature(3)

    def test_get_moisture(self):
        """Test get_moisture method returns correct values and handles index correctly"""
        # Check full array
        np.testing.assert_array_equal(self.chamber.get_moisture(), np.array(self.moisture))
        # Check individual indexes
        self.assertEqual(self.chamber.get_moisture(0), self.moisture[0])
        self.assertEqual(self.chamber.get_moisture(1), self.moisture[1])
        self.assertEqual(self.chamber.get_moisture(2), self.moisture[2])
        # Check out of bounds
        with self.assertRaises(IndexError):
            self.chamber.get_moisture(3)

    def test_get_oxygen(self):
        """Test get_oxygen method returns correct values and handles index correctly"""
        # Check full array
        np.testing.assert_array_equal(self.chamber.get_oxygen(), np.array(self.oxygen))
        # Check individual indexes
        self.assertEqual(self.chamber.get_oxygen(0), self.oxygen[0])
        self.assertEqual(self.chamber.get_oxygen(1), self.oxygen[1])
        self.assertEqual(self.chamber.get_oxygen(2), self.oxygen[2])
        # Check out of bounds
        with self.assertRaises(IndexError):
            self.chamber.get_oxygen(3)

    def test_get_co2(self):
        """Test get_co2 method returns correct values and handles index correctly"""
        # Check full array
        np.testing.assert_array_equal(self.chamber.get_co2(), np.array(self.co2))
        # Check individual indexes
        self.assertEqual(self.chamber.get_co2(0), self.co2[0])
        self.assertEqual(self.chamber.get_co2(1), self.co2[1])
        self.assertEqual(self.chamber.get_co2(2), self.co2[2])
        # Check out of bounds
        with self.assertRaises(IndexError):
            self.chamber.get_co2(3)

    def test_get_methane(self):
        """Test get_methane method returns correct values and handles index correctly"""
        # Check full array
        np.testing.assert_array_equal(self.chamber.get_methane(), np.array(self.methane))
        # Check individual indexes
        self.assertEqual(self.chamber.get_methane(0), self.methane[0])
        self.assertEqual(self.chamber.get_methane(1), self.methane[1])
        self.assertEqual(self.chamber.get_methane(2), self.methane[2])
        # Check out of bounds
        with self.assertRaises(IndexError):
            self.chamber.get_methane(3)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
