import numpy as np

class Chamber:
    def __init__(self, temperature, moisture, oxygen, co2, methane, paddle_direction=1, lid_status=False, air_pump_status=False, isEmpty=True):
        # Sensor Data as arrays for multiple sensors, truncating to 2 decimal places
        self.temperature = self.truncate_to_2_decimals(np.array(temperature, dtype=float))
        self.moisture = self.truncate_to_2_decimals(np.array(moisture, dtype=float))
        self.oxygen = self.truncate_to_2_decimals(np.array(oxygen, dtype=float))
        self.co2 = self.truncate_to_2_decimals(np.array(co2, dtype=float))
        self.methane = self.truncate_to_2_decimals(np.array(methane, dtype=float))
        
        # Equipment Status
        self.paddle_status = False
        self.paddle_direction = paddle_direction
        self.lid_status = lid_status
        self.air_pump_status = air_pump_status
        self.isEmpty = isEmpty


    def truncate_to_2_decimals(self, value):
        """Truncate a float or array to 2 decimal places without rounding."""
        factor = 10 ** 2
        if isinstance(value, np.ndarray):  # Handle array input
            return np.floor(value * factor) / factor
        else:  # Handle single float input
            return float(np.floor(value * factor) / factor)


    # Getter and Setter
    def get_isEmpty_status(self):
        return self.isEmpty
    
    def get_paddle_status(self):
        return self.paddle_status

    def get_paddle_direction(self):
        return self.paddle_direction

    def get_air_pump_status(self):
        return self.air_pump_status
    
    def get_isEmpty(self):
        return self.isEmpty

    # Getter with optional index parameter
    def get_temperature(self, index=None):
        """Get temperature values. If index is provided, return the specific sensor's value."""
        if index is not None:
            if 0 <= index < len(self.temperature):
                return self.temperature[index]
            else:
                raise IndexError(f"Temperature sensor index {index} out of range")
        return self.temperature

    def get_moisture(self, index=None):
        """Get moisture values. If index is provided, return the specific sensor's value."""
        if index is not None:
            if 0 <= index < len(self.moisture):
                return self.moisture[index]
            else:
                raise IndexError(f"Moisture sensor index {index} out of range")
        return self.moisture

    def get_oxygen(self, index=None):
        """Get oxygen values. If index is provided, return the specific sensor's value."""
        if index is not None:
            if 0 <= index < len(self.oxygen):
                return self.oxygen[index]
            else:
                raise IndexError(f"Oxygen sensor index {index} out of range")
        return self.oxygen

    def get_co2(self, index=None):
        """Get CO2 values. If index is provided, return the specific sensor's value."""
        if index is not None:
            if 0 <= index < len(self.co2):
                return self.co2[index]
            else:
                raise IndexError(f"CO2 sensor index {index} out of range")
        return self.co2

    def get_methane(self, index=None):
        """Get methane values. If index is provided, return the specific sensor's value."""
        if index is not None:
            if 0 <= index < len(self.methane):
                return self.methane[index]
            else:
                raise IndexError(f"Methane sensor index {index} out of range")
        return self.methane

    # Set status for the chamber
    def set_isEmpty_status(self, new_isEmpty: bool):
        """Sets whether the chamber capacity is empty"""
        if isinstance(new_isEmpty, bool):
            self.isEmpty = new_isEmpty
        else:
            raise ValueError("isEmpty status must be a boolean (True or False)")

    # Setters with truncation for each attribute
    def set_temperature(self, new_temp):
        """Set temperature values, ensuring each element is truncated to 2 decimal places."""
        self.temperature = self.truncate_to_2_decimals(np.array(new_temp, dtype=float))
    
    def set_moisture(self, new_moisture):
        """Set moisture values, ensuring each element is truncated to 2 decimal places."""
        self.moisture = self.truncate_to_2_decimals(np.array(new_moisture, dtype=float))
    
    def set_oxygen(self, new_oxygen):
        """Set oxygen values, ensuring each element is truncated to 2 decimal places."""
        self.oxygen = self.truncate_to_2_decimals(np.array(new_oxygen, dtype=float))
    
    def set_co2(self, new_co2):
        """Set CO2 values, ensuring each element is truncated to 2 decimal places."""
        self.co2 = self.truncate_to_2_decimals(np.array(new_co2, dtype=float))
    
    def set_methane(self, new_methane):
        """Set methane values, ensuring each element is truncated to 2 decimal places."""
        self.methane = self.truncate_to_2_decimals(np.array(new_methane, dtype=float))


    # Equipment operation
    def operate_paddle(self, paddle_status: bool):
        """Operate the paddle, True is on, False is off"""
        if isinstance(paddle_status, bool):
            self.paddle_status = paddle_status
        else:
            raise ValueError("Paddle status must be True (operating) or False (stopped)")

    def change_paddle_direction(self, direction):
        """Set the paddle direction, 1 is clockwise, -1 is counterclockwise"""
        if direction in [1, -1]:
            self.paddle_direction = direction
        else:
            raise ValueError("Paddle direction must be 1 (clockwise) or -1 (counterclockwise)")

    def simulate_air_pump(self, status):
        """Operate the air pump, True is on, False is off"""
        if isinstance(status, bool):
            self.air_pump_status = status
        else:
            raise ValueError("Air pump status must be a boolean (True or False)")

    def open_lid(self):
        """Open the lid"""
        self.lid_status = True

    def close_lid(self):
        """Close the lid"""
        self.lid_status = False

    # Update temperature function with single or all sensor options
    # Update functions with rounding for each attribute
    # Update functions with truncation for each attribute
  # Update temperature function with truncation for single or all sensor options
    def update_temperature(self, delta, index=None):
        """Adjust temperature sensor readings with truncation."""
        if index is not None:
            if 0 <= index < len(self.temperature):
                updated_value = self.temperature[index] + delta
                self.temperature[index] = self.truncate_to_2_decimals(np.clip(updated_value, -100, 100))
            else:
                raise IndexError(f"Temperature sensor index {index} out of range")
        else:
            updated_values = self.temperature + delta
            self.temperature = self.truncate_to_2_decimals(np.clip(updated_values, -100, 100))

    def update_moisture(self, delta, index=None):
        """Adjust moisture sensor readings with truncation."""
        if index is not None:
            if 0 <= index < len(self.moisture):
                updated_value = self.moisture[index] + delta
                self.moisture[index] = self.truncate_to_2_decimals(np.clip(updated_value, -100, 100))
            else:
                raise IndexError(f"Moisture sensor index {index} out of range")
        else:
            updated_values = self.moisture + delta
            self.moisture = self.truncate_to_2_decimals(np.clip(updated_values, -100, 100))

    def update_oxygen(self, delta, index=None):
        """Update oxygen sensor readings with truncation."""
        if index is not None:
            if 0 <= index < len(self.oxygen):
                updated_value = self.oxygen[index] + delta
                self.oxygen[index] = self.truncate_to_2_decimals(np.clip(updated_value, -100, 100))
            else:
                raise IndexError(f"Oxygen sensor index {index} out of range")
        else:
            updated_values = self.oxygen + delta
            self.oxygen = self.truncate_to_2_decimals(np.clip(updated_values, -100, 100))

    def update_co2(self, delta, index=None):
        """Update CO2 sensor readings with truncation."""
        if index is not None:
            if 0 <= index < len(self.co2):
                updated_value = self.co2[index] + delta
                self.co2[index] = self.truncate_to_2_decimals(updated_value)
            else:
                raise IndexError(f"CO2 sensor index {index} out of range")
        else:
            updated_values = self.co2 + delta
            self.co2 = self.truncate_to_2_decimals(updated_values)
    
    def update_methane(self, delta, index=None):
        """Update methane sensor readings with truncation."""
        if index is not None:
            if 0 <= index < len(self.methane):
                updated_value = self.methane[index] + delta
                self.methane[index] = self.truncate_to_2_decimals(updated_value)
            else:
                raise IndexError(f"Methane sensor index {index} out of range")
        else:
            updated_values = self.methane + delta
            self.methane = self.truncate_to_2_decimals(updated_values)


    def get_status(self):
        """Returns the current chamber status, including all sensor values and device status"""
        return {
            "temperature": self.temperature,
            "moisture": self.moisture,
            "oxygen": self.oxygen,
            "methane": self.methane,
            "co2": self.co2,
            "paddle_status": self.paddle_status,
            "paddle_direction": self.paddle_direction,
            "lid_status": self.lid_status,
            "air_pump_status": self.air_pump_status
        }
