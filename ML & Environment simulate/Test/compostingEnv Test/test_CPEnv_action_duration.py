import unittest
from lidaEnvironment import CompostingEnv

class TestCompostingEnvGetActionDuration(unittest.TestCase):
    def setUp(self):
        # Create an instance of CompostingEnv
        self.env = CompostingEnv()

    def test_get_action_duration_with_duration_specified(self):
        """Test get_action_duration returns the specified duration from action dictionary."""
        chamber_action = {"duration": 5}
        result = self.env.get_action_duration(chamber_action)
        self.assertEqual(result, 5, "Expected specified duration of 5 to be returned.")

    def test_get_action_duration_with_no_duration_specified(self):
        """Test get_action_duration returns max_duration when no duration is specified."""
        chamber_action = {}  # No duration specified
        result = self.env.get_action_duration(chamber_action)
        self.assertEqual(result, self.env.max_duration, f"Expected max_duration {self.env.max_duration} to be returned.")

    def test_get_action_duration_with_invalid_action_type(self):
        """Test get_action_duration raises TypeError when action is not a dictionary."""
        invalid_action = "invalid_action_type"  # Not a dictionary
        with self.assertRaises(TypeError, msg="Expected TypeError for non-dictionary input."):
            self.env.get_action_duration(invalid_action)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)
