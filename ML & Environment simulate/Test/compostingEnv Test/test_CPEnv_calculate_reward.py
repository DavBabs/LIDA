import unittest
from lidaEnvironment import CompostingEnv

class TestCalculateReward(unittest.TestCase):
    def setUp(self):
        # Initialize the environment
        self.env = CompostingEnv()

    def test_calculate_reward_all_optimal(self):
        """Test calculate_reward when all factors are within optimal ranges with float values."""
        # Set sensor values within optimal ranges using floats
        self.env.active_chamber.set_temperature([30.5, 35.2, 28.9, 32.7])  # Avg within range (0, 40)
        self.env.active_chamber.set_moisture([15.5, 18.3])  # Within range (10, 20)
        self.env.active_chamber.set_oxygen([20.5])  # Within range (10, 25)
        self.env.active_chamber.set_co2([20.7])  # Within range (15, 30)
        self.env.active_chamber.set_methane([3.4])  # Within range (0, 5)

        reward = self.env.calculate_reward()
        
        # Expected reward is the sum of weights since all scores should be 1
        expected_reward = sum(self.env.weights.values())
        self.assertAlmostEqual(reward, expected_reward, places=2)

    def test_calculate_reward_some_optimal_some_not(self):
        """Test calculate_reward when some factors are within optimal ranges and others are not, with floats."""
        # Set values with some factors out of optimal ranges
        self.env.active_chamber.set_temperature([45.3, 50.1, 48.6, 47.4])  # Avg above optimal range (0, 40)
        self.env.active_chamber.set_moisture([12.7, 18.2])  # Within range (10, 20)
        self.env.active_chamber.set_oxygen([26.5])  # Above range (10, 25)
        self.env.active_chamber.set_co2([25.4])  # Within range (15, 30)
        self.env.active_chamber.set_methane([10.5])  # Above range (0, 5)

        reward = self.env.calculate_reward()

        # Expected reward is the weighted sum where only in-range factors contribute
        expected_reward = (
            self.env.weights["co2"] +
            self.env.weights["moisture"]
        )
        self.assertAlmostEqual(reward, expected_reward, places=2)

    def test_calculate_reward_all_outside(self):
        """Test calculate_reward when all factors are outside the optimal ranges using float values."""
        # Set sensor values outside optimal ranges
        self.env.active_chamber.set_temperature([50.2, 55.7, 52.8, 51.3])  # Avg above optimal range (0, 40)
        self.env.active_chamber.set_moisture([5.3, 9.9])  # Below range (10, 20)
        self.env.active_chamber.set_oxygen([30.7])  # Above range (10, 25)
        self.env.active_chamber.set_co2([35.2])  # Above range (15, 30)
        self.env.active_chamber.set_methane([10.1])  # Above range (0, 5)

        reward = self.env.calculate_reward()

        # Expected reward should be 0, as all factors are out of optimal ranges
        self.assertAlmostEqual(reward, 0.0, places=2)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
