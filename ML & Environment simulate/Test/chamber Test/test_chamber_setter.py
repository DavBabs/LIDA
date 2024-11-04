import unittest
from chamber import Chamber

class TestChamberSetters(unittest.TestCase):
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

    def test_set_temperature(self):
        """Test set_temperature method sets the correct value"""
        self.chamber.set_temperature(25.5)
        self.assertEqual(self.chamber.temperature, 25.5)
        
        # Check invalid input
        with self.assertRaises(ValueError):
            self.chamber.set_temperature("invalid")

    def test_set_moisture(self):
        """Test set_moisture method sets the correct value"""
        self.chamber.set_moisture(55.5)
        self.assertEqual(self.chamber.moisture, 55.5)
        
        # Check invalid input
        with self.assertRaises(ValueError):
            self.chamber.set_moisture("invalid")

    def test_set_oxygen(self):
        """Test set_oxygen method sets the correct value"""
        self.chamber.set_oxygen(20.0)
        self.assertEqual(self.chamber.oxygen, 20.0)
        
        # Check invalid input
        with self.assertRaises(ValueError):
            self.chamber.set_oxygen("invalid")

    def test_set_co2(self):
        """Test set_co2 method sets the correct value"""
        self.chamber.set_co2(0.06)
        self.assertEqual(self.chamber.co2, 0.06)
        
        # Check invalid input
        with self.assertRaises(ValueError):
            self.chamber.set_co2("invalid")

    def test_set_methane(self):
        """Test set_methane method sets the correct value"""
        self.chamber.set_methane(0.03)
        self.assertEqual(self.chamber.methane, 0.03)
        
        # Check invalid input
        with self.assertRaises(ValueError):
            self.chamber.set_methane("invalid")

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
