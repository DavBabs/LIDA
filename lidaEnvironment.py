import gym
from gym import spaces
import numpy as np
import config  # Import config.py file directly
import json
import optimal_conditions_sample
import random

class CompostingEnv(gym.Env):
    def __init__(self):
        super(CompostingEnv, self).__init__()

        # 1. Load optimal conditions from the JSON file
        with open('optimal_conditions.json') as f:
            self.optimal_conditions = json.load(f)

        # 1.1 Load configuration for max_duration from config.py
        self.max_duration = config.max_duration  # Use the max_duration from config.py

        #Track paddle direction: 1=clockwise, -1 = counterclockwise
        self.paddle_direction = 1 #Start with clockwise direction

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
         # Assign the action to self.current_action
        self.current_action = action

        # 1. Apply action if provided, otherwise simulate natural changes
        self._apply_action(action)

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

        # Check if the action is for the paddle (motor ID: 0)
        if motor_action['id'] == 0:
            self.simulate_paddle(motor_action['duration_sec'][0])  # Simulate paddle movement

        # Check if the action is for the air pump (motor ID: 1)
        elif motor_action['id'] == 1:
            self.simulate_air_pump(motor_action['duration_sec'][0])  # Simulate air pump

        else:
            # No action taken, so apply natural changes to the environment
            self._apply_natural_changes()
        
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
    

    def _update_state(self):
        """
        Update the current environmental state based on independent actions of the paddle and air pump.
        Natural changes are applied if no action is taken.
        """
        motor_action = self.current_action['motor'] if self.current_action else None
        pump_action = self.current_action['actions'] if self.current_action else None

        # Check paddle (motor) action
        paddle_running = motor_action and motor_action['id'] == 0
        paddle_duration = motor_action['duration_sec'][0] if paddle_running else 0

        # Check air pump action
        air_pump_running = any([pump['id'] == 1 for pump in pump_action]) if pump_action else False
        pump_duration = pump_action[0]['duration_ms'][0] if air_pump_running else 0

        # Independent paddle control: Update temperature and moisture if paddle is running
        if paddle_running:
            self.update_temperature(paddle_duration)
            self.update_moisture(paddle_duration)
        else:
            # Apply natural changes to temperature and moisture
            self.update_temperature()  # Natural changes
            self.update_moisture()     # Natural changes

        # Independent air pump control: Update gases if air pump is running
        if air_pump_running:
            for pump in pump_action:
                if pump['id'] == 1:
                    self.update_methane(pump_duration)
                    self.update_oxygen_co2(pump_duration)
        else:
            # Apply natural changes to gases
            self.update_methane()      # Natural changes
            self.update_oxygen_co2()   # Natural changes


    
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
        Check if the episode has reached its end condition, which could be due to:
        - Composting completion (environment variables in optimal range after a certain time)
        - Composting failure (extreme environment values or time limit exceeded)
        """
        # Check elapsed time (e.g., if episode has run for more than 14 days)
        if self.state['time'] >= 14 * 24 * 60 * 60:  # Assuming time is in seconds
            # Check if environment variables are within the optimal range for compost completion
            temperature_active = np.mean(self.state['temperature_active'])
            moisture_active = np.mean(self.state['moisture_active'])
            co2_level = self.state['gases']['co2'][0]
            oxygen_level = self.state['gases']['oxygen'][0]
            methane_level = self.state['gases']['methane'][0]
            
            # Check if all variables are within the completion thresholds
            if (45 <= temperature_active <= 60 and 50 <= moisture_active <= 70 and
                15 <= co2_level <= 30 and 10 <= oxygen_level <= 25 and methane_level < 5):
                return True  # Composting successfully completed
            
            # If time has exceeded 14 days but conditions not met, it may fail soon
            if self.state['time'] >= 20 * 24 * 60 * 60:  # Time exceeds 20 days
                return True  # Episode terminates due to failure

        # Check for extreme values indicating compost failure (even before the time limit)
        temperature_active = np.mean(self.state['temperature_active'])
        if temperature_active > 100 or temperature_active < 0:
            return True  # Extreme temperature values
        
        moisture_active = np.mean(self.state['moisture_active'])
        if moisture_active < 10 or moisture_active > 90:
            return True  # Extreme moisture values
        
        co2_level = self.state['gases']['co2'][0]
        oxygen_level = self.state['gases']['oxygen'][0]
        methane_level = self.state['gases']['methane'][0]
        if co2_level > 70 or oxygen_level < 5 or methane_level > 30:
            return True  # Gas levels indicate failure
        
        # If no termination condition is met, continue the episode
        return False

    
    def _get_dynamic_duration(self, current_value, category, variable, scaling_factor=None):
        """
        Get dynamic action duration based on the current state and optimal conditions.
        Optionally allows passing in a custom scaling factor.
        """
        if scaling_factor is None:
            scaling_factor = config.scaling_factor  # Default to config if not provided

        optimal_min = self.optimal_conditions[category][variable]['min']
        optimal_max = self.optimal_conditions[category][variable]['max']

        # Calculate duration as a function of deviation from optimal conditions
        if current_value < optimal_min:
            duration = (optimal_min - current_value) * scaling_factor
        elif current_value > optimal_max:
            duration = (current_value - optimal_max) * scaling_factor
        else:
            duration = 500  # Default duration if within the optimal range

        # Ensure duration stays within a valid range
        return np.clip(duration, 0, self.max_duration)

    def simulate_air_pump(self, duration_sec):
        oxygen_increase_rate = 0.1  # % per second
        methane_decrease_rate = 0.2  # ppm per second
        temp_decrease_rate = 0.05 # degrees per second
        co2_decrease_rate = 0
        
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
            # Call the function to switch paddle direction if needed
            self.switch_paddle_direction(sec)

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
    
    def switch_paddle_direction(self, sec):
        """
        Switch paddle direction at regular intervals.
        Alternates direction every 60 seconds (just an example, discussion needed)

        """
        if sec % 60 == 0: # Adjust this interval as needed
            self.paddle_direction *= -1 # Toggle direction (1 for clockwise,  -1 for counterclockwise)

    def update_temperature(self):
        """
        Handles temperature changes, including random spikes and natural progression.
        """
        # Probability of a temperature spike happening at any given time
        temperature_spike_chance = 0.01  # 1% chance per time step
        spike_duration = 5  # Spike lasts for 5 time steps
        spike_intensity = 5.0  # Spike increases temperature by 5 degrees

        # Track the duration of the spike
        if not hasattr(self, 'spike_counter'):
            self.spike_counter = 0

        if self.spike_counter > 0:
            # If we're in the middle of a temperature spike, apply the spike increase
            for i in range(len(self.state['temperature_active'])):
                self.state['temperature_active'][i] += spike_intensity
            self.spike_counter -= 1  # Decrease spike counter
        else:
            # Chance to trigger a temperature spike
            if random.random() < temperature_spike_chance:
                self.spike_counter = spike_duration  # Start the spike

        # Apply natural temperature changes if no spike is active
        temp_natural_change_rate = 0.01  # Temperature naturally rises/falls slightly
        for i in range(len(self.state['temperature_active'])):
            self.state['temperature_active'][i] += temp_natural_change_rate
            
    def update_methane(self):
        """
        Handles methane changes based on natural decomposition and air pump action.
        """
        methane_increase_rate = 0.01  # Natural methane increase
        methane_decrease_rate = 0.02  # Decrease rate when air pump is running

        # Apply natural methane increase
        self.state['gases']['methane'][0] = min(100, self.state['gases']['methane'][0] + methane_increase_rate)

        # Check if the air pump is running to decrease methane
        if self.current_action and self.current_action['motor']['id'] == 1:
            pump_duration = self.current_action['motor']['duration_sec'][0]
            methane_reduction = pump_duration * methane_decrease_rate
            self.state['gases']['methane'][0] = max(0, self.state['gases']['methane'][0] - methane_reduction)
    
            return self.state
        
    def update_oxygen_co2(self, pump_duration=None):
        """
        Updates both oxygen and CO2 levels. If the air pump is running, 
        it will affect the levels more significantly. If no air pump is running, 
        natural changes are applied.

        """
        oxygen_increase_rate = 0.015  # Air pump effect on oxygen
        co2_decrease_rate = 0.01      # Air pump effect on CO2
        
        if pump_duration:  # If air pump is running
            self.state['gases']['oxygen'][0] = min(100, self.state['gases']['oxygen'][0] + pump_duration * oxygen_increase_rate)
            self.state['gases']['co2'][0] = max(0, self.state['gases']['co2'][0] - pump_duration * co2_decrease_rate)
        else:  # Natural changes if no air pump
            oxygen_natural_decrease_rate = 0.01
            co2_natural_increase_rate = 0.02
            
            self.state['gases']['oxygen'][0] = max(0, self.state['gases']['oxygen'][0] - oxygen_natural_decrease_rate)
            self.state['gases']['co2'][0] = min(100, self.state['gases']['co2'][0] + co2_natural_increase_rate)
    
    def update_moisture(self, paddle_duration=None):
        """
        Updates moisture levels in the compost based on whether the paddles are running.
        If paddles are running, moisture is evenly distributed. Otherwise, natural evaporation is applied.

        Moisture's dependence on paddles: Moisture is primarily affected by the operation of the paddles, as stirring can even out moisture levels and prevent pockets of overly dry or wet compost.

        Natural moisture loss: When the paddles aren’t running, moisture will naturally decrease due to evaporation.
        Optimal conditions: Ensure the moisture levels are within optimal ranges.

        Paddle operation: When the paddles are running, the function ensures that moisture levels are evened out across the moisture_active array, simulating the mixing effect of the paddles. It also applies slight natural moisture loss.

        Natural changes: If the paddles aren’t running, only natural evaporation is applied to both moisture_active and moisture_curing.
        Boundaries: The moisture levels are capped at 0 to avoid negative values, as moisture can't go below 0%.

        """
        moisture_evening_rate = 0.01  # Rate at which moisture evens out when paddles are running
        natural_evaporation_rate = 0.005  # Rate of moisture loss due to natural evaporation

        # Determine whether to apply paddle effects or natural changes
        if paddle_duration:  # If paddles are running
            moisture_diff = max(self.state['moisture_active']) - min(self.state['moisture_active'])
            if moisture_diff > 0:
                for i in range(len(self.state['moisture_active'])):
                    # Evening out moisture differences
                    self.state['moisture_active'][i] -= moisture_diff * moisture_evening_rate
            
            # Also apply a slight moisture reduction due to paddle mixing
            for i in range(len(self.state['moisture_active'])):
                self.state['moisture_active'][i] = max(0, self.state['moisture_active'][i] - natural_evaporation_rate)

        else:  # Natural evaporation
            for i in range(len(self.state['moisture_active'])):
                self.state['moisture_active'][i] = max(0, self.state['moisture_active'][i] - natural_evaporation_rate)
        
        # Optionally adjust curing moisture if needed
        for i in range(len(self.state['moisture_curing'])):
            self.state['moisture_curing'][i] = max(0, self.state['moisture_curing'][i] - natural_evaporation_rate)



    

