"""
Soil Moisture Sensor Driver
Capacitive soil moisture sensor interface

Usage:
    sensor = SoilMoistureSensor(pin=34, dry_value=1800, wet_value=700)
    moisture = sensor.get_moisture()
"""

class SoilMoistureSensor:
    """Interface for capacitive soil moisture sensor"""
    
    def __init__(self, pin, dry_value=1800, wet_value=700, samples=10):
        """
        Initialize soil moisture sensor
        
        Args:
            pin: ADC pin number
            dry_value: Raw ADC value for completely dry soil
            wet_value: Raw ADC value for completely wet soil
            samples: Number of samples for averaging
        """
        self.pin = pin
        self.dry_value = dry_value
        self.wet_value = wet_value
        self.samples = samples
    
    def read_raw(self):
        """Read raw ADC value"""
        # In actual implementation, use Arduino analogRead()
        pass
    
    def get_raw_average(self):
        """Get averaged raw reading"""
        readings = [self.read_raw() for _ in range(self.samples)]
        return sum(readings) / len(readings)
    
    def get_moisture(self):
        """
        Get soil moisture percentage (0-100%)
        
        Returns:
            float: Moisture percentage
        """
        raw = self.get_raw_average()
        
        # Clamp to dry/wet range
        if raw > self.dry_value:
            return 0.0
        if raw < self.wet_value:
            return 100.0
        
        # Linear interpolation
        percentage = ((self.dry_value - raw) / 
                     (self.dry_value - self.wet_value)) * 100
        
        return max(0, min(100, percentage))
    
    def calibrate_dry(self):
        """Calibrate sensor in dry soil"""
        self.dry_value = self.get_raw_average()
        return self.dry_value
    
    def calibrate_wet(self):
        """Calibrate sensor in wet soil"""
        self.wet_value = self.get_raw_average()
        return self.wet_value


class RainSensor:
    """Interface for rain sensor module"""
    
    def __init__(self, pin, sensitivity=300):
        """
        Initialize rain sensor
        
        Args:
            pin: Digital input pin
            sensitivity: ADC threshold (0-4095)
        """
        self.pin = pin
        self.sensitivity = sensitivity
    
    def read_raw(self):
        """Read raw sensor value"""
        pass
    
    def is_raining(self):
        """
        Detect if it's raining
        
        Returns:
            bool: True if rain detected
        """
        # Digital output: LOW when rain detected
        return self.read_raw() == 0
    
    def get_rain_intensity(self):
        """
        Get rain intensity (0-100%)
        
        Returns:
            float: Rain intensity percentage
        """
        raw = self.read_raw()
        return (raw / 4095.0) * 100


class WaterLevelSensor:
    """Interface for water tank level sensor"""
    
    def __init__(self, pin, min_raw=200, max_raw=4000):
        """
        Initialize water level sensor
        
        Args:
            pin: ADC pin
            min_raw: Raw value at minimum level
            max_raw: Raw value at maximum level
        """
        self.pin = pin
        self.min_raw = min_raw
        self.max_raw = max_raw
    
    def read_raw(self):
        """Read raw ADC value"""
        pass
    
    def get_level_percentage(self):
        """
        Get tank water level percentage
        
        Returns:
            float: Level percentage (0-100%)
        """
        raw = self.read_raw()
        
        # Clamp to sensor range
        if raw < self.min_raw:
            return 0.0
        if raw > self.max_raw:
            return 100.0
        
        # Linear interpolation
        percentage = ((raw - self.min_raw) / 
                     (self.max_raw - self.min_raw)) * 100
        
        return max(0, min(100, percentage))
    
    def is_low(self, threshold=20):
        """
        Check if water level is below threshold
        
        Args:
            threshold: Level percentage threshold
            
        Returns:
            bool: True if level is below threshold
        """
        return self.get_level_percentage() < threshold


class TemperatureHumiditySensor:
    """Interface for DHT11 temperature/humidity sensor"""
    
    def __init__(self, pin):
        """
        Initialize DHT11 sensor
        
        Args:
            pin: Digital input pin
        """
        self.pin = pin
        self.last_temperature = None
        self.last_humidity = None
    
    def read(self):
        """
        Read temperature and humidity
        
        Returns:
            tuple: (temperature_celsius, humidity_percentage)
        """
        # TODO: Implement DHT11 protocol
        # This requires precise timing for DHT11 communication
        pass
    
    def get_temperature(self):
        """Get temperature in Celsius"""
        return self.last_temperature
    
    def get_humidity(self):
        """Get humidity in percentage"""
        return self.last_humidity


# Example usage
if __name__ == "__main__":
    # Initialize sensors
    moisture_sensor = SoilMoistureSensor(pin=34, dry_value=1800, wet_value=700)
    rain_sensor = RainSensor(pin=32)
    water_level = WaterLevelSensor(pin=35, min_raw=200, max_raw=4000)
    
    # Read values
    moisture = moisture_sensor.get_moisture()
    rain = rain_sensor.is_raining()
    tank_level = water_level.get_level_percentage()
    
    print(f"Soil Moisture: {moisture:.1f}%")
    print(f"Rain: {'Yes' if rain else 'No'}")
    print(f"Tank Level: {tank_level:.1f}%")
