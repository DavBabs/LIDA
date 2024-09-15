import gym
from gym import spaces
import numpy as np
import json

class CompostingEnv(gym.Env):
    def __init__(self):
        super(CompostingEnv, self).__init__()

        # 1. Load optimal conditions from the JSON file
        with open('optimal_conditions.json') as f:
            self.optimal_conditions = json.load(f)

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


    def _calculate_reward(self):
        """
        Calculate the reward based on the current state
        """
        temperature = self.state['temperature_active'][0]
        humidity = self.state['moisture_active'][0]
        co2 = self.state['gases']['co2'][0]
        methane = self.state['gases']['methane'][0]
        
        if 55 <= temperature <= 65 and 40 <= humidity <= 50 and 10 <= co2 <= 20 and 5 <= methane <= 10:
            return 1  # Positive reward
        else:
            return -1  # Negative reward

    def _check_done(self):
        """
        Check if the episode has reached its end condition
        """
        temperature = self.state['temperature_active'][0]
        if temperature > 100 or temperature < 0:
            return True
        return False
