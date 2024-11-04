import unittest
from lidaEnvironment import CompostingEnv

class TestProximityScore(unittest.TestCase):
    def setUp(self):
        # Initialize the environment
        self.env = CompostingEnv()

    def test_proximity_score_within_range(self):
        """Test proximity score for values within the optimal range, including decimal values."""
        self.assertEqual(self.env.proximity_score(25.5, (10.0, 30.0)), 1)  # In range
        self.assertEqual(self.env.proximity_score(10.0, (10.0, 30.0)), 1)  # Edge case (lower bound)
        self.assertEqual(self.env.proximity_score(30.0, (10.0, 30.0)), 1)  # Edge case (upper bound)
        self.assertEqual(self.env.proximity_score(15.75, (10.5, 20.5)), 1)  # In range

    def test_proximity_score_outside_range(self):
        """Test proximity score for values outside the optimal range with decimals."""
        self.assertEqual(self.env.proximity_score(5.5, (10.0, 30.0)), 0)   # Below range
        self.assertEqual(self.env.proximity_score(30.5, (10.0, 30.0)), 0)  # Above range
        self.assertEqual(self.env.proximity_score(9.99, (10.0, 20.0)), 0)  # Just below lower bound

    def test_proximity_score_single_threshold(self):
        """Test proximity score when a single threshold is used, including decimal values."""
        threshold_range = {"threshold": 10.5}
        self.assertEqual(self.env.proximity_score(5.25, threshold_range), 1)   # Below threshold
        self.assertEqual(self.env.proximity_score(10.5, threshold_range), 1)   # Edge case (threshold value)
        self.assertEqual(self.env.proximity_score(10.51, threshold_range), 0)  # Just above threshold

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)