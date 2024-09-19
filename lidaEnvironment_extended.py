import gym
from gym import spaces
import numpy as np
import config  # Import config.py file directly
import json


class CompostingEnv(gym.Env):
    def __init__(self):
        super(CompostingEnv, self).__init__()

        # 1. Load optimal conditions from the JSON file
        with open('optimal_conditions.json') as f:
            self.optimal_conditions = json.load(f)

        # 1.1 Load configuration for max_duration from config.py
        self.max_duration = config.max_duration  # Use the max_duration from config.py

        # 2. Define the observation space
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

        # 3. Define the action space
        self.action_space = spaces.Dict({
            "motor": spaces.Dict({
                "id": spaces.Discrete(2),  # Motor ID: 0 for paddle, 1 for air pump
                "duration_sec": spaces.Box(low=1, high=self.max_duration, shape=(1,), dtype=np.float32)  # Duration in seconds, configurable
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
        Reset the environment state to the initial values.
        This is called at the beginning of each training episode.
        """
        self.state = {
            "temperature_active": np.array([50.0, 50.0, 50.0, 50.0], dtype=np.float32),  # Initial temperatures
            "temperature_curing": np.array([60.0, 60.0], dtype=np.float32),  # Initial curing temperatures
            "moisture_active": np.array([60.0, 60.0], dtype=np.float32),  # Initial moisture levels
            "moisture_curing": np.array([70.0, 70.0], dtype=np.float32),  # Initial curing moisture
            "gases": {
                "co2": np.array([5.0], dtype=np.float32),  # Initial CO2 level
                "oxygen": np.array([15.0], dtype=np.float32),  # Initial oxygen level
                "methane": np.array([1.0], dtype=np.float32)  # Initial methane level
            },
            "time": 0  # Reset time to 0
        }
        return self.state

    def step(self, action):
        """
        Execute an action, update the state, calculate reward, and return the results.
        """
        # 1. Apply action if provided, otherwise simulate natural changes
        if action:
            if action['motor']['id'] == 0:  # Paddle action
                self.simulate_paddle(action['motor']['duration_sec'][0])  # Duration is in seconds now
            elif action['motor']['id'] == 1:  # Air pump action
                self.simulate_air_pump(action['motor']['duration_sec'][0])  # Duration in seconds
        else:
            # No action taken, so apply natural changes to the environment
            self._apply_natural_changes()

        # 2. Update the environment state
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
        
        # Dynamically adjust action timing based on optimal conditions
        motor_duration = self._get_dynamic_duration(self.state['temperature_active'][0], 'temperature', 'active')
        motor_action['duration_ms'][0] = motor_duration

        # Adjust air pump action duration based on optimal gas levels
        for pump in pump_action:
            pump_duration = self._get_dynamic_duration(self.state['gases']['co2'][0], 'gases', 'co2')
            pump['duration_ms'][0] = pump_duration

        # Assume longer air pump run time reduces CO2 and methane, increases oxygen
        co2_reduction = pump_duration * 0.01
        methane_reduction = pump_duration * 0.005
        oxygen_increase = pump_duration * 0.015

        self.state['gases']['co2'][0] = max(0, self.state['gases']['co2'][0] - co2_reduction)
        self.state['gases']['methane'][0] = max(0, self.state['gases']['methane'][0] - methane_reduction)
        self.state['gases']['oxygen'][0] = min(100, self.state['gases']['oxygen'][0] + oxygen_increase)

    def _get_dynamic_duration(self, current_value, category, variable):
        """
        Get dynamic action duration based on the current state and optimal conditions
        """
        optimal_min = self.optimal_conditions[category][variable]['min']
        optimal_max = self.optimal_conditions[category][variable]['max']

        # Calculate duration as a function of deviation from optimal conditions
        if current_value < optimal_min:
            duration = (optimal_min - current_value) * 100  # Example scaling factor
        elif current_value > optimal_max:
            duration = (current_value - optimal_max) * 100
        else:
            duration = 500  # Default duration if within optimal range

        return np.clip(duration, 0, 10000)  # Ensure duration stays within valid range

    def _update_state(self):
        """
        Update the current environmental state based on motor and air pump actions,
        and compare it to the optimal conditions to adjust accordingly.
        """
        # Simulate how motor affects temperature
        motor_id = self.current_action['motor']['id']
        motor_duration = self.current_action['motor']['duration_ms'][0]

        # Adjust temperature based on motor operation, referencing optimal conditions
        optimal_temp_active_min = self.optimal_conditions['temperature']['active']['min']
        optimal_temp_active_max = self.optimal_conditions['temperature']['active']['max']
        
        if motor_id == 0:  # Affect active stage temperature
            if self.state['temperature_active'][0] < optimal_temp_active_min:
                self.state['temperature_active'][0] += motor_duration * 0.01
            elif self.state['temperature_active'][0] > optimal_temp_active_max:
                self.state['temperature_active'][0] -= motor_duration * 0.01

        optimal_temp_curing_min = self.optimal_conditions['temperature']['curing']['min']
        optimal_temp_curing_max = self.optimal_conditions['temperature']['curing']['max']
        
        if motor_id == 1:  # Affect curing stage temperature
            if self.state['temperature_curing'][0] < optimal_temp_curing_min:
                self.state['temperature_curing'][0] += motor_duration * 0.01
            elif self.state['temperature_curing'][0] > optimal_temp_curing_max:
                self.state['temperature_curing'][0] -= motor_duration * 0.01

        # Update gas concentrations based on air pump actions, referencing optimal conditions
        optimal_co2_min = self.optimal_conditions['gases']['co2']['min']
        optimal_co2_max = self.optimal_conditions['gases']['co2']['max']
        optimal_methane_min = self.optimal_conditions['gases']['methane']['min']
        optimal_methane_max = self.optimal_conditions['gases']['methane']['max']
        optimal_oxygen_min = self.optimal_conditions['gases']['oxygen']['min']
        optimal_oxygen_max = self.optimal_conditions['gases']['oxygen']['max']

        for pump in self.current_action['actions']:
            pump_duration = pump['duration_ms'][0]

            # CO2 adjustment based on optimal conditions
            if self.state['gases']['co2'][0] > optimal_co2_max:
                self.state['gases']['co2'][0] -= pump_duration * 0.01
            elif self.state['gases']['co2'][0] < optimal_co2_min:
                self.state['gases']['co2'][0] += pump_duration * 0.01

            # Methane adjustment
            if self.state['gases']['methane'][0] > optimal_methane_max:
                self.state['gases']['methane'][0] -= pump_duration * 0.005
            elif self.state['gases']['methane'][0] < optimal_methane_min:
                self.state['gases']['methane'][0] += pump_duration * 0.005

            # Oxygen adjustment
            if self.state['gases']['oxygen'][0] < optimal_oxygen_min:
                self.state['gases']['oxygen'][0] += pump_duration * 0.015
            elif self.state['gases']['oxygen'][0] > optimal_oxygen_max:
                self.state['gases']['oxygen'][0] -= pump_duration * 0.015

        # Ensure all gas values remain within realistic bounds
        self.state['gases']['co2'][0] = max(0, self.state['gases']['co2'][0])
        self.state['gases']['methane'][0] = max(0, self.state['gases']['methane'][0])
        self.state['gases']['oxygen'][0] = min(100, self.state['gases']['oxygen'][0])

        # Optionally update moisture based on motor or pump actions, using optimal moisture values
        optimal_moisture_active_min = self.optimal_conditions['moisture']['active']['min']
        optimal_moisture_active_max = self.optimal_conditions['moisture']['active']['max']
        
        if self.state['moisture_active'][0] < optimal_moisture_active_min:
            self.state['moisture_active'][0] += motor_duration * 0.01
        elif self.state['moisture_active'][0] > optimal_moisture_active_max:
            self.state['moisture_active'][0] -= motor_duration * 0.01

        optimal_moisture_curing_min = self.optimal_conditions['moisture']['curing']['min']
        optimal_moisture_curing_max = self.optimal_conditions['moisture']['curing']['max']
        
        if self.state['moisture_curing'][0] < optimal_moisture_curing_min:
            self.state['moisture_curing'][0] += motor_duration * 0.01
        elif self.state['moisture_curing'][0] > optimal_moisture_curing_max:
            self.state['moisture_curing'][0] -= motor_duration * 0.01

    def _apply_natural_changes(self):
    """
    This function applies the natural changes to the environment when no actions are taken.
    For example, oxygen decreases, methane increases, temperature and moisture might change slowly.
    """
    # Define natural change rates per time step (e.g., per second)
    oxygen_decrease_rate = 0.01  # Oxygen decreases due to decomposition
    methane_increase_rate = 0.01  # Methane increases due to anaerobic activity
    co2_increase_rate = 0.02  # CO2 naturally increases due to composting
    temp_natural_change_rate = 0.01  # Temperature naturally rises/falls slightly due to microbial activity
    moisture_decrease_rate = 0.005  # Moisture slowly evaporates

    # Apply natural changes to gases
    self.state['gases']['oxygen'][0] = max(0, self.state['gases']['oxygen'][0] - oxygen_decrease_rate)
    self.state['gases']['methane'][0] = min(100, self.state['gases']['methane'][0] + methane_increase_rate)
    self.state['gases']['co2'][0] = min(100, self.state['gases']['co2'][0] + co2_increase_rate)

    # Apply natural changes to temperature (active stage)
    for i in range(len(self.state['temperature_active'])):
        self.state['temperature_active'][i] += temp_natural_change_rate

    # Apply natural changes to moisture (active stage)
    for i in range(len(self.state['moisture_active'])):
        self.state['moisture_active'][i] = max(0, self.state['moisture_active'][i] - moisture_decrease_rate)

    # Ensure values stay within realistic bounds
    self.state['gases']['oxygen'][0] = min(100, self.state['gases']['oxygen'][0])
    self.state['gases']['methane'][0] = max(0, self.state['gases']['methane'][0])
    self.state['gases']['co2'][0] = min(100, self.state['gases']['co2'][0])


    def calculate_reward(current, minvalue, maxvalue):
        # If the current value is less than the minimum, calculate reward as current / minvalue
        if (current / minvalue) < 1:
            return (current / minvalue)
        # If the current value is within the optimal range, return full reward (1)
        elif minvalue <= current <= maxvalue:
            return 1
        # If the current value is greater than the maximum, scale the reward as maxvalue / current
        else:
            return (maxvalue / current)

    def _calculate_reward(self):
        # Get current environmental state values
        temperature = np.mean(self.state['temperature_active'])
        methane = self.state['gases']['methane']
        co2 = self.state['gases']['co2']
        o2 = self.state['gasses']['oxygen']

        # Calculate rewards for each variable
        temp_reward = calculate_reward(temperature, optimal.active_min, optimal.active_max)
        methane_reward = calculate_reward(methane, optimal.moisture_min, optimal.moisture_max)
        co2_reward = calculate_reward(co2, optimal.co2_min, optimal.co2_max)
        o2_reward = calculate_reward(o2, optimal.o2_min, optimal.o2_max)
        
        # Define weights for each variable
        temp_weight = 0.4
        methane_weight = 0.3
        o2_weight = 0.2
        co2_weight = 0.1
        
        # Calculate total weighted reward
        total_reward = (
            temp_reward * temp_weight + 
            methane_reward * methane_weight + 
            o2_reward * o2_weight + 
            co2_reward * co2_weight
        )

        return total_reward

    def _check_done(self):
        """
        Check if the episode has reached its end condition
        """
        temperature = self.state['temperature_active'][0]
        if temperature > 100 or temperature < 0:
            return True
        return False

    def simulate_air_pump(self, duration_sec):
        oxygen_increase_rate = 0.1  # % per second
        methane_decrease_rate = 0.2  # ppm per second
        temp_decrease_rate = 0.05 # degrees per second
        
        for sec in range(int(duration_sec)):
            self.state['oxygen'] = min(25.0, self.state['oxygen'] + oxygen_increase_rate)
            self.state['methane'] = max(0.0, self.state['methane'] - methane_decrease_rate)
            self.state['co2'] = max(0.0, self.state['co2'] - co2_decrease_rate)
            self.state['time'] += 1  # Increment time by 1 second

    def simulate_paddle(self, duration_sec):
    """
    Simulates the paddle stirring the compost for a specific duration in seconds.
    The paddle affects temperature distribution and moisture by mixing the compost.
    """
    # Define the effect rates per second of paddle operation
    temp_evening_rate = 0.02  # Helps equalize temperature (reduce extremes)
    moisture_evening_rate = 0.01  # Helps equalize moisture (reduce extremes)
    
    for sec in range(int(duration_sec)):
        # Evening out temperature differences across the active compost
        temp_diff = max(self.state['temperature_active']) - min(self.state['temperature_active'])
        if temp_diff > 0:
            for i in range(len(self.state['temperature_active'])):
                self.state['temperature_active'][i] -= temp_diff * temp_evening_rate
        
        # Evening out moisture differences across the active compost
        moisture_diff = max(self.state['moisture_active']) - min(self.state['moisture_active'])
        if moisture_diff > 0:
            for i in range(len(self.state['moisture_active'])):
                self.state['moisture_active'][i] -= moisture_diff * moisture_evening_rate
        
        # Increase gas mixing by slightly reducing methane and increasing oxygen
        self.state['gases']['oxygen'][0] = min(25.0, self.state['gases']['oxygen'][0] + 0.02)
        self.state['gases']['methane'][0] = max(0.0, self.state['gases']['methane'][0] - 0.01)

        self.state['time'] += 1  # Increment time by 1 second
    
    return self.state

