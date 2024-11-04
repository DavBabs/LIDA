import numpy as np
from lidaEnvironment import CompostingEnv  # Adjust the import path if necessary

# Instantiate the environment
env = CompostingEnv()

# Call reset and observe output
observation = env.reset()

# Print outputs to verify reset behavior
print("Observation after reset:")
print("Active Chamber:", observation["active_chamber"])
print("Curing Chamber:", observation["curing_chamber"])
print("Expected Active Chamber isEmpty:", env.active_chamber.get_isEmpty())  # Expected to be False
print("Expected Curing Chamber isEmpty:", env.curing_chamber.get_isEmpty())  # Expected to be True
