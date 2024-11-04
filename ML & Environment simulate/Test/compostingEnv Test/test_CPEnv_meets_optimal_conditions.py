import unittest
import numpy as np
from lidaEnvironment import CompostingEnv
from chamber import Chamber

class TestMeetsOptimalConditions(unittest.TestCase):
    def setUp(self):
        # Initialize the environment
        self.env = CompostingEnv()

    def test_meets_optimal_conditions_all_optimal(self):
        """Test that the chamber meets optimal conditions when all factors are within optimal ranges."""
        # Set all values within the optimal range
        self.env.active_chamber.set_temperature(np.array([20.0, 25.0, 30.0]))
        self.env.active_chamber.set_moisture(np.array([15.0, 18.0]))
        self.env.active_chamber.set_oxygen(np.array([20.0]))
        self.env.active_chamber.set_co2(np.array([20.0]))
        self.env.active_chamber.set_methane(np.array([3.0]))
        
        # Check if the environment identifies these values as optimal
        self.assertTrue(self.env.meets_optimal_conditions(self.env.active_chamber))

    def test_meets_optimal_conditions_some_non_optimal(self):
        """Test that the chamber does not meet optimal conditions when one factor is outside the optimal range."""
        # Set values within the optimal range, except temperature
        self.env.active_chamber.set_temperature(np.array([45.0]))  # Outside optimal range (0-40)
        self.env.active_chamber.set_moisture(np.array([15.0, 18.0]))
        self.env.active_chamber.set_oxygen(np.array([20.0]))
        self.env.active_chamber.set_co2(np.array([20.0]))
        self.env.active_chamber.set_methane(np.array([3.0]))

        # Check if the environment correctly identifies these values as non-optimal
        self.assertFalse(self.env.meets_optimal_conditions(self.env.active_chamber))

    def test_meets_optimal_conditions_all_non_optimal(self):
        """Test that the chamber does not meet optimal conditions when all factors are outside the optimal range."""
        # Set all values outside the optimal range
        self.env.active_chamber.set_temperature(np.array([50.0]))  # Above optimal
        self.env.active_chamber.set_moisture(np.array([30.0]))     # Above optimal
        self.env.active_chamber.set_oxygen(np.array([5.0]))        # Below optimal
        self.env.active_chamber.set_co2(np.array([35.0]))          # Above optimal
        self.env.active_chamber.set_methane(np.array([10.0]))      # Above optimal

        # Check if the environment correctly identifies these values as non-optimal
        self.assertFalse(self.env.meets_optimal_conditions(self.env.active_chamber))

    def test_meets_optimal_conditions_edge_cases(self):
        """Test edge values at the boundary of the optimal range to verify they are considered optimal."""
        # Set values at the boundary of optimal ranges
        self.env.active_chamber.set_temperature(np.array([0.0, 40.0]))  # Lower and upper bounds
        self.env.active_chamber.set_moisture(np.array([10.0, 20.0]))    # Lower and upper bounds
        self.env.active_chamber.set_oxygen(np.array([10.0, 25.0]))      # Lower and upper bounds
        self.env.active_chamber.set_co2(np.array([15.0, 30.0]))         # Lower and upper bounds
        self.env.active_chamber.set_methane(np.array([0.0, 5.0]))       # Lower and upper bounds

        # Check if the environment identifies these boundary values as optimal
        self.assertTrue(self.env.meets_optimal_conditions(self.env.active_chamber))

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
