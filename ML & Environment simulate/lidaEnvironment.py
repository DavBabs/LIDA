import gym
from gym import spaces
import numpy as np
import config  # Import config.py file directly
import json
import random
from chamber import Chamber

class CompostingEnv(gym.Env):
    def __init__(self):
        super(CompostingEnv, self).__init__()

        # 0.1 Load configuration for max_duration from config.py
        self.max_duration = config.max_duration  # Use the max_duration from config.py

        # 1.Define thresholds
         # Initialize weights and thresholds
        self.weights = {
            "co2": 0.35,
            "methane": 0.23,
            "oxygen": 0.18,
            "temperature": 0.14,
            "moisture": 0.1
        }
        self.optimal_ranges = {
            "temperature": (0, 40),
            "moisture": (10, 20),
            "oxygen": (10, 25),
            "co2": (15, 30),
            "methane": (0, 5)
        }
        self.extreme_limits = {
            "temperature": (0, 100),
            "moisture": (10, 100),
            "oxygen": (5, 70),
            "co2": (0, 70),
            "methane": (0, 30)
        }
        # 1.1 Initialize state with time as 0, time increase in step() function
        self.state = {"time": 0}

        # 2. Create two Chamber instances with initial sensor values
        self.active_chamber = Chamber(
            temperature=np.array([50.0, 52.0, 51.0, 50.0]),
            moisture=np.array([60.0, 62.0]),
            oxygen=np.array([15.0]),
            co2=np.array([5.0]),
            methane=np.array([1.0]),
            isEmpty=False
        )

        self.curing_chamber = Chamber(
            temperature=np.array([60.0, 61.0]),
            moisture=np.array([70.0, 72.0]),
            oxygen=np.array([18.0]),
            co2=np.array([6.0]),
            methane=np.array([2.0]),
            isEmpty=True
        )

        # Define observation and action spaces (assuming similar structure as provided)
        self.observation_space = spaces.Dict({
            "active_chamber": spaces.Dict({
                "temperature": spaces.Box(low=0, high=100, shape=(len(self.active_chamber.temperature),), dtype=np.float32),
                "moisture": spaces.Box(low=0, high=100, shape=(len(self.active_chamber.moisture),), dtype=np.float32),
                "oxygen": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32),
                "co2": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32),
                "methane": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32)
            }),
            "curing_chamber": spaces.Dict({
                "temperature": spaces.Box(low=0, high=100, shape=(len(self.curing_chamber.temperature),), dtype=np.float32),
                "moisture": spaces.Box(low=0, high=100, shape=(len(self.curing_chamber.moisture),), dtype=np.float32),
                "oxygen": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32),
                "co2": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32),
                "methane": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32)
            })
        })

        self.action_space = spaces.Dict({
            "active_chamber": spaces.Dict({
                "paddle": spaces.Tuple((
                    spaces.Discrete(2),  # Paddle status: 0 for off, 1 for on
                    spaces.Discrete(2)   # Paddle direction: 0 for counterclockwise, 1 for clockwise
                )),
                "air_pump": spaces.Discrete(2),  # 0 for off, 1 for on
                "lid": spaces.Discrete(2),  # 0 for closed, 1 for open
                "duration": spaces.Discrete(self.max_duration)  # Duration of the action
            }),
            "curing_chamber": spaces.Dict({
                "paddle": spaces.Tuple((
                    spaces.Discrete(2),  # Paddle status: 0 for off, 1 for on
                    spaces.Discrete(2)   # Paddle direction: 0 for counterclockwise, 1 for clockwise
                )),
                "air_pump": spaces.Discrete(2),  # 0 for off, 1 for on
                "lid": spaces.Discrete(2),  # 0 for closed, 1 for open
                "duration": spaces.Discrete(self.max_duration)  # Duration of the action
            })
        })

    def reset(self):
        """
        Reset the environment by resetting both chambers' states.
        """
        self.active_chamber.set_temperature(np.array([50.0, 52.0, 51.0, 50.0], dtype=float))
        self.active_chamber.set_moisture(np.array([60.0, 62.0], dtype=float))
        self.active_chamber.set_oxygen(np.array([15.0], dtype=float))
        self.active_chamber.set_co2(np.array([5.0], dtype=float))
        self.active_chamber.set_methane(np.array([1.0], dtype=float))
        self.active_chamber.set_isEmpty_status(False)
        
        self.curing_chamber.set_temperature(np.array([60.0, 61.0], dtype=float))
        self.curing_chamber.set_moisture(np.array([70.0, 72.0], dtype=float))
        self.curing_chamber.set_oxygen(np.array([18.0], dtype=float))
        self.curing_chamber.set_co2(np.array([6.0], dtype=float))
        self.curing_chamber.set_methane(np.array([2.0], dtype=float))
        self.curing_chamber.set_isEmpty_status(True)
        
        return self.get_observation()


    
    def get_observation(self):
        """
        Return the observation for both active and curing chambers.
        """
        observation = {
            "active_chamber": {
                "temperature": self.active_chamber.get_temperature(),
                "moisture": self.active_chamber.get_moisture(),
                "oxygen": self.active_chamber.get_oxygen(),
                "co2": self.active_chamber.get_co2(),
                "methane": self.active_chamber.get_methane(),
                "isEmpty": self.active_chamber.get_isEmpty()
            },
            "curing_chamber": {
                "temperature": self.curing_chamber.get_temperature(),
                "moisture": self.curing_chamber.get_moisture(),
                "oxygen": self.curing_chamber.get_oxygen(),
                "co2": self.curing_chamber.get_co2(),
                "methane": self.curing_chamber.get_methane(),
                "isEmpty": self.curing_chamber.get_isEmpty()
            }
        }
        return observation

    def step(self, action):
        """
        Execute an action, update the state, calculate reward, and return the results.
        """
        # Increment the time by a simulated amount (Assuming each step represents one hour)
        time_increment = 360  
        self.state['time'] += time_increment

        # Step 1: Apply actions to both chambers
        self.apply_action(self.active_chamber, action['active_chamber'])
        self.apply_action(self.curing_chamber, action['curing_chamber'])

        # Step 2: Update the environment state for both chambers
        self.update_state(action)

        # Step 3: Calculate the reward based on current state
        reward = self.calculate_reward()

        # Step 4: Check if the episode is finished
        done = self.check_done()

        # Step 5: Return the new state, reward, completion status, and any debug information
        return self.get_observation(), reward, done, {}

    def apply_action(self, chamber, chamber_action):
        """
        Apply the action to the specific chamber based on the given action dictionary.
        """
        # Handle paddle action only if specified in the action
        if 'paddle' in chamber_action:
            self.simulate_paddle(chamber, chamber_action['paddle'])
            
        # Handle air pump action only if specified in the action
        if 'air_pump' in chamber_action:
            self.simulate_air_pump(chamber, chamber_action['air_pump'])

        # Handle lid action only if specified in the action
        if 'lid' in chamber_action:
            self.simulate_lid(chamber, chamber_action['lid'])


    def update_state(self, action):
        """
        Update the environmental state based on the action's specified durations.
        """
        for chamber_key, chamber in zip(['active_chamber', 'curing_chamber'], [self.active_chamber, self.curing_chamber]):
            chamber_action = action[chamber_key]
            duration = self.get_action_duration(chamber_action)

            # Check paddle status
            if chamber.get_paddle_status() == 1:
                # Apply paddle-specific updates
                temp_adjustment = self.calculate_temperature("paddle", duration)
                self.update_temperature(chamber, temp_adjustment)

                moisture_adjustment = self.calculate_moisture("paddle", duration)
                self.update_moisture(chamber, moisture_adjustment)

                co2_adjustment = self.calculate_co2("paddle", duration)
                self.update_co2(chamber, co2_adjustment)

            # Check air pump status
            if chamber.get_air_pump_status() == 1:
                # Apply air pump-specific updates
                methane_adjustment = self.calculate_methane("air_pump", duration)
                self.update_methane(chamber, methane_adjustment)

                oxygen_adjustment = self.calculate_oxygen("air_pump", duration)
                self.update_oxygen(chamber, oxygen_adjustment)

                temp_adjustment = self.calculate_temperature("air_pump", duration)
                self.update_temperature(chamber, temp_adjustment)

            # Apply natural changes if no components are active
            if chamber.get_paddle_status() == 0 and chamber.get_air_pump_status() == 0:
                self.update_natural_action(chamber)


    def update_natural_action(self, chamber):
        """
        Simulate natural environmental changes when no components are active.

        """
        # Natural decay or fluctuation rates (placeholders)
        natural_temp_change = -0.1  # Natural cooling
        natural_moisture_change = -0.05  # Gradual drying
        natural_methane_increase = 0.02  # Methane builds up slowly
        natural_oxygen_decrease = -0.03  # Oxygen gradually depletes
        natural_co2_increase = 0.04  # CO2 increases due to decomposition

        # Apply natural changes to the chamber
        self.update_temperature(chamber, natural_temp_change)
        self.update_moisture(chamber, natural_moisture_change)
        self.update_methane(chamber, natural_methane_increase)
        self.update_oxygen(chamber, natural_oxygen_decrease)
        self.update_co2(chamber, natural_co2_increase)

    # Placeholder functions for environmental updates
    def update_temperature(self, chamber:Chamber, adjust_value):
        chamber.update_temperature(adjust_value)

    def update_methane(self, chamber:Chamber, adjust_value):
        chamber.update_methane(adjust_value)

    def update_oxygen(self, chamber:Chamber, adjust_value):
        chamber.update_oxygen(adjust_value)

    def update_co2(self, chamber:Chamber, adjust_value):
        chamber.update_co2(adjust_value)

    def update_moisture(self, chamber:Chamber, adjust_value):
        chamber.update_moisture(adjust_value)


    def calculate_temperature(self, action, duration):
        adjustment = 0.15 if action == "paddle" else -0.2  # 增大paddle和air pump的温度调整幅度
        return duration * adjustment
    
    def calculate_oxygen(self, action, duration):
        adjustment = 0.3 if action == "air_pump" else 0.1  # 增大空气泵的氧气调整幅度
        return duration * adjustment

    
    def calculate_moisture(self, action, duration):
        adjustment = -0.1 if action == "paddle" else -0.02  # Both actions decrease moisture, paddle decreases more
        return duration * adjustment

    def calculate_co2(self, action, duration):
        adjustment = 0.08 if action == "paddle" else -0.2  # Paddle increases, air pump decreases
        return duration * adjustment

    def calculate_methane(self, action, duration):
        adjustment = -0.2 if action == "paddle" else -0.1  # Both actions decrease methane, paddle decreases more
        return duration * adjustment



    def get_action_duration(self, chamber_action):
        """
        Extract the duration from the action dictionary if available, else return max_duration.
        """
        #Make sure chamber_action is a dictionary or contains a duration attribute
        if isinstance(chamber_action, dict):
            return chamber_action.get("duration", self.max_duration)
        else:
            raise TypeError("Expected chamber_action to be a dictionary containing 'duration'.")


    def calculate_reward(self):
        """
        Calculate the reward based on proximity of factors to optimal conditions.
        """
        current_values = {
            "co2": self.active_chamber.get_co2()[0],
            "methane": self.active_chamber.get_methane()[0],
            "oxygen": self.active_chamber.get_oxygen()[0],
            "temperature": np.mean(self.active_chamber.get_temperature()),
            "moisture": np.mean(self.active_chamber.get_moisture())
        }
        
        scores = {factor: self.proximity_score(current_values[factor], self.optimal_ranges[factor])
                  for factor in current_values}

        total_reward = sum(scores[factor] * self.weights[factor] for factor in scores)
        return total_reward

    def proximity_score(self, value, optimal_range):
        """
        Calculate score based on proximity of value to optimal condition.
        """
        if isinstance(optimal_range, tuple):
            min_val, max_val = optimal_range
            return 1 if min_val <= value <= max_val else 0
        elif isinstance(optimal_range, dict) and "threshold" in optimal_range:
            return 1 if value <= optimal_range["threshold"] else 0
        else:
            # Handle unexpected format
            raise ValueError("Invalid format for optimal_range.")


    def meets_optimal_conditions(self, chamber: Chamber):
        temp = np.mean(chamber.get_temperature())
        moist = np.mean(chamber.get_moisture())
        oxy = chamber.get_oxygen()[0]
        co2 = chamber.get_co2()[0]
        meth = chamber.get_methane()[0]

        return (self.optimal_ranges["temperature"][0] <= temp <= self.optimal_ranges["temperature"][1] and
                self.optimal_ranges["moisture"][0] <= moist <= self.optimal_ranges["moisture"][1] and
                self.optimal_ranges["oxygen"][0] <= oxy <= self.optimal_ranges["oxygen"][1] and
                self.optimal_ranges["co2"][0] <= co2 <= self.optimal_ranges["co2"][1] and
                self.optimal_ranges["methane"][0] <= meth <= self.optimal_ranges["methane"][1])

    def has_extreme_values(self, chamber: Chamber):
        temp = np.mean(chamber.get_temperature())
        moist = np.mean(chamber.get_moisture())
        oxy = chamber.get_oxygen()[0]
        co2 = chamber.get_co2()[0]
        meth = chamber.get_methane()[0]
        
        # Debug statements
        print(f"Checking extreme values for chamber: temp={temp}, moisture={moist}, oxygen={oxy}, co2={co2}, methane={meth}")
        print(f"Thresholds: temperature={self.extreme_limits['temperature']}, moisture={self.extreme_limits['moisture']}, "
              f"oxygen={self.extreme_limits['oxygen']}, co2={self.extreme_limits['co2']}, methane={self.extreme_limits['methane']}")
    
        # Evaluate extreme conditions based on defined limits
        return (temp < self.extreme_limits["temperature"][0] or temp > self.extreme_limits["temperature"][1] or
                moist < self.extreme_limits["moisture"][0] or moist > self.extreme_limits["moisture"][1] or
                oxy < self.extreme_limits["oxygen"][0] or oxy > self.extreme_limits["oxygen"][1] or
                co2 < self.extreme_limits["co2"][0] or co2 > self.extreme_limits["co2"][1] or
                meth > self.extreme_limits["methane"][1])

    def check_done(self):
        """
        Check if the episode has reached its end condition.
        """
        if self.state['time'] >= 14 * 24 * 60 * 60:
            if self.meets_optimal_conditions(self.active_chamber) and self.meets_optimal_conditions(self.curing_chamber):
                return True  # Successful completion
    
            if self.state['time'] >= 20 * 24 * 60 * 60:
                return True  # Episode ends due to excessive duration
    
        # Critical check for extreme values
        if self.has_extreme_values(self.active_chamber) or self.has_extreme_values(self.curing_chamber):
            return True  # Episode ends due to extreme values
    
        return False

    

    def simulate_paddle(self, chamber: Chamber, paddle_action):
        """
        Simulate the paddle action based on RL action.
        paddle_action: (status, direction) where
            - status: 0 = off, 1 = on
            - direction: 0 = counterclockwise, 1 = clockwise
        """
        if paddle_action[0] == 1:  # If paddle is turned on
            chamber.operate_paddle(True)
            direction = 1 if paddle_action[1] == 1 else -1  # 1 for clockwise, -1 for counterclockwise
            chamber.change_paddle_direction(direction)
        else:
            chamber.operate_paddle(False)  # Turn paddle off


    def simulate_air_pump(self, chamber: Chamber, air_pump_action):
        """
        Simulate the air pump action based on RL action.
        air_pump_action: 0 = off, 1 = on
        """
        chamber.simulate_air_pump(bool(air_pump_action))

    def simulate_lid(self, chamber: Chamber, lid_action):
        """
        Simulate the lid action based on RL action.
        lid_action: 0 = closed, 1 = open
        """
        if lid_action == 1:
            chamber.open_lid()
        else:
            chamber.close_lid()

    
    def switch_paddle_direction(self, chamber:Chamber, sec):
        """
        Switch paddle direction at regular intervals.
        Alternates direction every 60 seconds (just an example, discussion needed)
        """
        if sec % 60 == 0: # Adjust this interval as needed
            chamber.paddle_direction *= -1 # Toggle direction (1 for clockwise,  -1 for counterclockwise)