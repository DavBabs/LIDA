import gym
from gym import spaces
import numpy as np

class CompostingEnv(gym.Env):
    def __init__(self):
        super(CompostingEnv, self).__init__()

        # 1. Define the observation space
        self.observation_space = spaces.Dict({
            "temperature_active": spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32),
            "temperature_curing": spaces.Box(low=0, high=100, shape=(2,), dtype=np.float32),
            "moisture_active": spaces.Box(low=0, high=100, shape=(2,), dtype=np.float32),
            "moisture_curing": spaces.Box(low=0, high=100, shape=(2,), dtype=np.float32),
            "gases": spaces.Dict({
                "co2": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32),
                "oxygen": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32),
                "methane": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32)
            }),
        })

        # 2. Define the action space
        self.action_space = spaces.Dict({
            "motor": spaces.Dict({
                "id": spaces.Discrete(2),  # Motor ID: 0, 1
                "duration_ms": spaces.Box(low=0, high=10000, shape=(1,), dtype=np.float32)
            }),
            "actions": spaces.Tuple([
                spaces.Dict({
                    "type": spaces.Discrete(1),  # Only 1 type here for air_pump
                    "id": spaces.Discrete(2),  # Air pump ID: 0, 1
                    "duration_ms": spaces.Box(low=0, high=10000, shape=(1,), dtype=np.float32)
                }),
                spaces.Dict({
                    "type": spaces.Discrete(1),  # Only 1 type here for air_pump
                    "id": spaces.Discrete(2),  # Air pump ID: 0, 1
                    "duration_ms": spaces.Box(low=0, high=10000, shape=(1,), dtype=np.float32)
                })
            ])
        })

        # Initialize the state of the compost environment
        self.state = self.reset()

    def reset(self):
        """
        Initialize the environment state
        """
        self.state = {
            "temperature_active": np.array([50.0, 50.0, 50.0, 50.0], dtype=np.float32),
            "temperature_curing": np.array([60.0, 60.0], dtype=np.float32),
            "moisture_active": np.array([60.0, 60.0], dtype=np.float32),
            "moisture_curing": np.array([70.0, 70.0], dtype=np.float32),
            "gases": {
                "co2": np.array([5.0], dtype=np.float32),
                "oxygen": np.array([15.0], dtype=np.float32),
                "methane": np.array([1.0], dtype=np.float32)
            }
        }
        return self.state

    def step(self, action):
        """
        Execute an action, update the state, calculate reward, and return the results
        """
        # 1. Apply action: this can define how motors and air pumps affect temperature and humidity
        self._apply_action(action)

        # 2. Update state: update temperature, humidity, and gas concentrations
        self._update_state()

        # 3. Calculate the reward
        reward = self._calculate_reward()

        # 4. Check if the episode is finished
        done = self._check_done()

        # 5. Return the new state, reward, completion status, and any debug information
        return self.state, reward, done, {}

    def _apply_action(self, action):
        """
        Apply the input action to update the motor or air pump control parameters
        """
        motor_action = action['motor']
        pump_action = action['actions']
        
        # Motor action: adjust temperature or other variables based on motor ID and duration
        motor_id = motor_action['id']
        motor_duration = motor_action['duration_ms']

        # Air pump action: adjust CO2, methane, and oxygen based on the duration of the air pumps
        for pump in pump_action:
            pump_duration = pump['duration_ms'][0]  # Get the running time of the air pump

            # Assume longer air pump run time reduces CO2 and methane, increases oxygen
            co2_reduction = pump_duration * 0.01  # Each 100ms reduces CO2 by 0.01%
            methane_reduction = pump_duration * 0.005  # Each 100ms reduces methane by 0.005%
            oxygen_increase = pump_duration * 0.015  # Each 100ms increases oxygen by 0.015%

            # Update gas concentrations, ensuring they remain within a reasonable range
            self.state['gases']['co2'][0] = max(0, self.state['gases']['co2'][0] - co2_reduction)
            self.state['gases']['methane'][0] = max(0, self.state['gases']['methane'][0] - methane_reduction)
            self.state['gases']['oxygen'][0] = min(100, self.state['gases']['oxygen'][0] + oxygen_increase)


    def _update_state(self):
    """
    Update the current environmental state based on motor and air pump actions.
    Simulate changes in temperature, humidity, CO2, and methane.
    """

    # Simulate how running the motor impacts temperature
    if self.current_action['motor']['id'] == 0:  # Example motor ID
        motor_duration = self.current_action['motor']['duration_ms'][0]
        self.state['temperature_active'][0] += motor_duration * 0.01  # Example: motor raises temperature
    
    # Simulate how air pump actions affect CO2, methane, and oxygen
    for pump in self.current_action['actions']:
        pump_duration = pump['duration_ms'][0]
        # Air pump reduces CO2, methane and increases oxygen
        self.state['gases']['co2'][0] -= pump_duration * 0.01
        self.state['gases']['methane'][0] -= pump_duration * 0.005
        self.state['gases']['oxygen'][0] += pump_duration * 0.015

    # Make sure all values stay within their limits
    self.state['gases']['co2'][0] = max(0, self.state['gases']['co2'][0])
    self.state['gases']['methane'][0] = max(0, self.state['gases']['methane'][0])
    self.state['gases']['oxygen'][0] = min(100, self.state['gases']['oxygen'][0])


    def _calculate_reward(self):
        """
        Calculate the reward based on the current state
        """
        temperature = self.state['temperature_active'][0]  # Example: read the current temperature
        humidity = self.state['moisture_active'][0]  # Read the current humidity
        co2 = self.state['gases']['co2'][0]
        methane = self.state['gases']['methane'][0]
        
        # Reward function: positive reward if temperature, humidity, CO2, methane are within ideal ranges
        if 50 <= temperature <= 60 and 50 <= humidity <= 70 and 5 <= co2 <= 10 and 1 <= methane <= 5:
            return 1  # Positive reward
        else:
            return -1  # Negative reward

    def _check_done(self):
        """
        Check if the episode has reached its end condition
        """
        # For example, end the episode if the temperature or humidity is too high or too low
        temperature = self.state['temperature_active'][0]
        if temperature > 100 or temperature < 0:
            return True  # Environment state unacceptable, end the episode
        return False  # Conditions not met for ending
