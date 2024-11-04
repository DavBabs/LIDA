import unittest
from chamber import Chamber

class TestChamberEquipmentOperations(unittest.TestCase):
    def setUp(self):
        # Initialize the Chamber with default data
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

    def test_operate_paddle(self):
        """Test operate_paddle method sets paddle status correctly"""
        # Turn paddle on
        self.chamber.operate_paddle(True)
        self.assertTrue(self.chamber.paddle_status)
        
        # Turn paddle off
        self.chamber.operate_paddle(False)
        self.assertFalse(self.chamber.paddle_status)
        
        # Check invalid input
        with self.assertRaises(ValueError):
            self.chamber.operate_paddle("invalid")

    def test_change_paddle_direction(self):
        """Test change_paddle_direction method sets paddle direction correctly"""
        # Set direction to clockwise
        self.chamber.change_paddle_direction(1)
        self.assertEqual(self.chamber.paddle_direction, 1)
        
        # Set direction to counterclockwise
        self.chamber.change_paddle_direction(-1)
        self.assertEqual(self.chamber.paddle_direction, -1)
        
        # Check invalid input
        with self.assertRaises(ValueError):
            self.chamber.change_paddle_direction(0)

    def test_simulate_air_pump(self):
        """Test simulate_air_pump method sets air pump status correctly"""
        # Turn air pump on
        self.chamber.simulate_air_pump(True)
        self.assertTrue(self.chamber.air_pump_status)
        
        # Turn air pump off
        self.chamber.simulate_air_pump(False)
        self.assertFalse(self.chamber.air_pump_status)
        
        # Check invalid input
        with self.assertRaises(ValueError):
            self.chamber.simulate_air_pump("invalid")

    def test_open_lid(self):
        """Test open_lid method sets lid status to True"""
        self.chamber.open_lid()
        self.assertTrue(self.chamber.lid_status)

    def test_close_lid(self):
        """Test close_lid method sets lid status to False"""
        # Open the lid first
        self.chamber.open_lid()
        self.assertTrue(self.chamber.lid_status)

        # Close the lid
        self.chamber.close_lid()
        self.assertFalse(self.chamber.lid_status)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
