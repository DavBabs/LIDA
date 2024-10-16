#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 25  // Pin where the data line is connected

// Create a OneWire instance
OneWire oneWire(ONE_WIRE_BUS);

// Pass the OneWire reference to DallasTemperature
DallasTemperature sensors(&oneWire);

void setup() {
    Serial.begin(9600);
    sensors.begin();  // Start the DallasTemperature library
}

void loop() {
    // Request temperature readings from all sensors
    sensors.requestTemperatures();  

    // Print the temperature of each sensor
    Serial.println("Temperatures:");

    // Loop through all connected sensors
    for (int i = 0; i < sensors.getDeviceCount(); i++) {
        float temperature = sensors.getTempCByIndex(i);  // Get temperature in Celsius
        Serial.print("Sensor ");
        Serial.print(i);
        Serial.print(": ");
        Serial.print(temperature);
        Serial.println(" °C");
    }

    Serial.println();
    delay(2000);  // Wait for 2 seconds before the next reading
}
