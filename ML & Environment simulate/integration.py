from lidaEnvironment import CompostingEnv
import numpy as np
import random

# Initialize the environment
env = CompostingEnv()
obs = env.reset()

# Define a function to simulate a single step with given action
def simulate_step(action):
    obs, reward, done, _ = env.step(action)
    print(f"Observation: {obs}")
    print(f"Reward: {reward}")
    print(f"Done: {done}")
    return obs, reward, done

# Test Scenario 1: Simulate a composting cycle with formatted output and optimized actions
def test_compost_cycle():
    # Actions are chosen to align with optimal conditions for reward increase
    actions = [
        {"paddle": (1, 1), "air_pump": 1, "lid": 1, "duration": 100},  # Optimized initial stage
        {"paddle": (1, 1), "air_pump": 1, "lid": 1, "duration": 200},  # Continue optimal action
        {"paddle": (1, 1), "air_pump": 1, "lid": 1, "duration": 150}   # Maintaining optimal actions
    ]

    # Execute each action in the sequence
    for i, action in enumerate(actions):
        print(f"\nRunning Step {i+1} with Action: {action}")
        # Apply the action to both active and curing chambers
        full_action = {
            "active_chamber": action,
            "curing_chamber": action  # Setting same action for curing chamber
        }
        obs, reward, done = simulate_step(full_action)
        
        # Format the output with dividers for clarity
        print(f"Observation: {obs}")
        print(f"Reward: {reward:.2f}")  # Print reward with two decimal precision
        print(f"Done: {done}\n{'='*30}")  # Print divider for each step

        # Extra check for high reward notification
        if reward >= 0.8:  # Threshold for a high reward
            print("High reward achieved, actions are aligned with optimal conditions!")


# Test Scenario 2: Simulate environmental response
def test_environment_response():
    # Set random environmental changes for temperature, CO2, and moisture
    random_adjustments = [
        {"temperature": random.uniform(-1, 1), "co2": random.uniform(-0.5, 0.5), "moisture": random.uniform(-0.2, 0.2)}
        for _ in range(5)
    ]

    # Apply each environmental adjustment
    for i, adjustment in enumerate(random_adjustments):
        print(f"\nEnvironment Adjustment Step {i+1}: {adjustment}")
        env.active_chamber.update_temperature(adjustment["temperature"])
        env.active_chamber.update_co2(adjustment["co2"])
        env.active_chamber.update_moisture(adjustment["moisture"])

        # Simulate environment's natural state changes without actions
        obs, reward, done = simulate_step({"active_chamber": {}, "curing_chamber": {}})
        print(f"Post-adjustment Observation: {obs}")

# Run the tests
print("Testing Compost Cycle")
test_compost_cycle()

print("\nTesting Environment Response")
test_environment_response()
