import unittest
from lidaEnvironment import CompostingEnv

class TestCompostingEnvCalculations(unittest.TestCase):
    def setUp(self):
        self.env = CompostingEnv()

    def test_calculate_temperature_with_paddle(self):
        # Paddle action should increase temperature
        duration = 10
        expected_adjustment = duration * 0.5  # Paddle increases temperature by 0.5 per second
        result = self.env.calculate_temperature("paddle", duration)
        self.assertEqual(result, expected_adjustment, "Paddle action did not increase temperature as expected")

    def test_calculate_temperature_with_air_pump(self):
        # Air pump action should decrease temperature
        duration = 10
        expected_adjustment = duration * -0.6  # Air pump decreases temperature by 0.6 per second
        result = self.env.calculate_temperature("air_pump", duration)
        self.assertEqual(result, expected_adjustment, "Air pump action did not decrease temperature as expected")

    def test_calculate_moisture_with_paddle(self):
        # Paddle action should decrease moisture more than air pump
        duration = 10
        expected_adjustment = duration * -0.1  # Paddle decreases moisture by 0.1 per second
        result = self.env.calculate_moisture("paddle", duration)
        self.assertEqual(result, expected_adjustment, "Paddle action did not decrease moisture as expected")

    def test_calculate_moisture_with_air_pump(self):
        # Air pump action should decrease moisture, but less than paddle
        duration = 10
        expected_adjustment = duration * -0.02  # Air pump decreases moisture by 0.02 per second
        result = self.env.calculate_moisture("air_pump", duration)
        self.assertEqual(result, expected_adjustment, "Air pump action did not decrease moisture as expected")

    def test_calculate_oxygen_increase(self):
        # Both actions should increase oxygen equally
        duration = 10
        expected_adjustment = duration * 0.1  # Both paddle and air pump increase oxygen by 0.1 per second
        result_paddle = self.env.calculate_oxygen("paddle", duration)
        result_air_pump = self.env.calculate_oxygen("air_pump", duration)
        self.assertEqual(result_paddle, expected_adjustment, "Paddle action did not increase oxygen as expected")
        self.assertEqual(result_air_pump, expected_adjustment, "Air pump action did not increase oxygen as expected")

    def test_calculate_co2_with_paddle(self):
        # Paddle action should increase CO2
        duration = 10
        expected_adjustment = duration * 0.08  # Paddle increases CO2 by 0.08 per second
        result = self.env.calculate_co2("paddle", duration)
        self.assertEqual(result, expected_adjustment, "Paddle action did not increase CO2 as expected")

    def test_calculate_co2_with_air_pump(self):
        # Air pump action should decrease CO2
        duration = 10
        expected_adjustment = duration * -0.2  # Air pump decreases CO2 by 0.2 per second
        result = self.env.calculate_co2("air_pump", duration)
        self.assertEqual(result, expected_adjustment, "Air pump action did not decrease CO2 as expected")

    def test_calculate_methane_with_paddle(self):
        # Paddle action should decrease methane more than air pump
        duration = 10
        expected_adjustment = duration * -0.2  # Paddle decreases methane by 0.2 per second
        result = self.env.calculate_methane("paddle", duration)
        self.assertEqual(result, expected_adjustment, "Paddle action did not decrease methane as expected")

    def test_calculate_methane_with_air_pump(self):
        # Air pump action should decrease methane, but less than paddle
        duration = 10
        expected_adjustment = duration * -0.1  # Air pump decreases methane by 0.1 per second
        result = self.env.calculate_methane("air_pump", duration)
        self.assertEqual(result, expected_adjustment, "Air pump action did not decrease methane as expected")


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
