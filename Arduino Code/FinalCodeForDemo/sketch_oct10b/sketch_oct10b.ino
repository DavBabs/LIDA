#include <Arduino.h>
#include <esp_check.h>
#include "secrets.h"
#include <freertos/FreeRTOS.h>
#include <esp_task_wdt.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <WiFiProv.h>
#include <WiFi.h>
#include <DFRobot_OxygenSensor.h>
#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 25  // Pin where the data line is connected
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

#define SETUP_PIN 0

// Automation active
bool automation_active = false;
String automation_phase = "active";
int automation_compartment = 1;

// motor automation
bool automation_motor_status = false;
int automation_motor_time = 0;

// airpump automation
bool automation_airpump_status = false;
int automation_airpump_time = 0;

const int AIR_VALUE = 3000;   // reading at air
const int WATER_VALUE = 1000; // reading at when soaked

const float MOISTURE_PINS[4] = {32, 33, 34, 35}; //
const int METHANE_PIN = 36; //
const int CO2_PIN = 39; //
const int DOOR_PIN = 27; //

// Oxygen
#define Oxygen_IICAddress ADDRESS_0
#define COLLECT_NUMBER 10
DFRobot_OxygenSensor oxygenSensor;

// Motor
#define MOTOR_PUL1_PIN 23 //
#define MOTOR_DIR1_PIN 26 //

#define MOTOR_PUL2_PIN 5 //
#define MOTOR_DIR2_PIN 19 //

// Air pump relay
#define AIRPUMP_ACTIVE1_PIN 4 //
#define AIRPUMP_ACTIVE2_PIN 16 //
#define AIRPUMP_CURING1_PIN 17 //
#define AIRPUMP_CURING2_PIN 18 //

// Linear Actuator
#define LINEARACTUATOR_LEFT_LEFT_EXTEND 6
#define LINEARACTUATOR_LEFT_LEFT_RETRACT 7

// MQTT Prefix
#define AWS_IOT_PREFIX "device/" DEVICE_ID

// MQTT Publish topic
#define AWS_IOT_PUBLISH_TOPIC_DATA AWS_IOT_PREFIX "/data"

// MQTT Subribe topic
#define AWS_IOT_SUBSCRIBE_TOPIC_CONTROL_MOTOR AWS_IOT_PREFIX "/motor"
#define AWS_IOT_SUBSCRIBE_TOPIC_CONTROL_AIRPUMP AWS_IOT_PREFIX "/airpump"
#define AWS_IOT_SUBSCRIBE_TOPIC_AUTOMATION AWS_IOT_PREFIX "/automation"
#define AWS_IOT_SUBSCRIBE_TOPIC_LINEARACTUATOR AWS_IOT_PREFIX "/linearactuator"

// Sensors
// Temperature
int temperatures[6];

// Moisture
int moistures[4];

// Oxygen
float oxygen = 0;

// Carbon Dioxide
int co2 = 0;

// Methane
int methane = 0;

// lib magnetic sensor
String lidState;

// Actuator
// Motor
bool motorOnActive = false;
bool motorOnCuring = false;

bool isWifiConnected = false;
bool isAwsIotSetup = false;
bool isAwsIotConnected = false;

WiFiClientSecure net = WiFiClientSecure();
PubSubClient client(net);

void airPumpActive(bool status, int compartment)
{
  // Turn machine on/off with status
  if (status)
  {
    if (compartment == 1)
    {

      // Turn on airpump compartment 1
      digitalWrite(AIRPUMP_ACTIVE1_PIN, LOW);

      Serial.println("AirPump Active Compartment 1 On");
    }
    else if (compartment == 2)
    {
      // Turn on airpump compartment 2
      digitalWrite(AIRPUMP_ACTIVE2_PIN, LOW);

      Serial.println("AirPump Active Compartment 2 On");
    }
  }
  else
  {
    if (compartment == 1)
    {
      // Turn off airpump compartment 1
      digitalWrite(AIRPUMP_ACTIVE1_PIN, HIGH);

      Serial.println("AirPump Active Compartment 1 Off");
    }
    else if (compartment == 2)
    {
      // Turn off airpump compartment 2
      digitalWrite(AIRPUMP_ACTIVE2_PIN, HIGH);

      Serial.println("AirPump Active Compartment 2 Off");
    }
  }
}

void airPumpCuring(bool status, int compartment)
{
  // Turn machine on/off with status
  if (status)
  {
    if (compartment == 1)
    {
      // Turn on airpump compartment 1
      digitalWrite(AIRPUMP_CURING1_PIN, LOW);

      Serial.println("AirPump Curing Compartment 1 On");
    }
    else if (compartment == 2)
    {
      // Turn on airpump compartment 2
      digitalWrite(AIRPUMP_CURING2_PIN, LOW);

      Serial.println("AirPump Curing Compartment 2 On");
    }
  }
  else
  {
    if (compartment == 1)
    {
      // Turn off airpump compartment 1
      digitalWrite(AIRPUMP_CURING1_PIN, HIGH);

      Serial.println("AirPump Curing Compartment 1 Off");
    }
    else if (compartment == 2)
    {
      // Turn off airpump compartment 2
      digitalWrite(AIRPUMP_CURING2_PIN, HIGH);

      Serial.println("AirPump Curing Compartment 2 Off");
    }
  }
}

void linear_actuator(int front, int back, int action) {
    if (action == 0) {
        digitalWrite(front, LOW); //EXTEND
        digitalWrite(back, HIGH); //EXTEND
        delay(5000);
        digitalWrite(front, HIGH); //STOP
        digitalWrite(back, LOW); //STOP
        }
    else if (action == 1) {
        digitalWrite(front, HIGH); //RETRACT
        digitalWrite(back, LOW); //RETRACT
        delay(25000);
        digitalWrite(front, HIGH); //STOP
        digitalWrite(back, HIGH); // STOP
        }
    }


void mqttMessageHandler(char *topic, byte *payload, unsigned int length)
{
  Serial.println("\n[MQTT]: incoming ");
  Serial.println(topic);

  StaticJsonDocument<200> doc;

  // Motor
  if (strstr(topic, AWS_IOT_SUBSCRIBE_TOPIC_CONTROL_MOTOR))
  {

    deserializeJson(doc, payload);
    String phaseStr = doc["phase"];
    String activeStr = doc["active"];

    // convert to int
    int active = activeStr.toInt();

    if (phaseStr == "active")
    {
      if (active == 1)
      {
        motorOnActive = true;
        Serial.println("Motor Active phase is ON");
      }
      else if (active == 0)
      {
        motorOnActive = false;
        digitalWrite(MOTOR_PUL1_PIN, LOW);
        Serial.println("Motor Active phase is OFF");
      }
    }
    else if (phaseStr == "curing")
    {
      if (active == 1)
      {
        motorOnCuring = true;
        Serial.println("Motor Curing phase is ON");
      }
      else if (active == 0)
      {
        motorOnCuring = false;
        digitalWrite(MOTOR_PUL2_PIN, LOW);
        Serial.println("Motor Curing phase is OFF");
      }
    }
  }

  // AirPump
  if (strstr(topic, AWS_IOT_SUBSCRIBE_TOPIC_CONTROL_AIRPUMP))
  {
    deserializeJson(doc, payload);
    String phaseStr = doc["phase"];
    String compartmentStr = doc["compartment"];
    String activeStr = doc["active"];
    int compartment = compartmentStr.toInt();
    int active = activeStr.toInt();

    if (phaseStr == "active")
    {
      airPumpActive(active, compartment);
    }
    else if (phaseStr == "curing")
    {
      airPumpCuring(active, compartment);
    }
  }

  // LinearActuator
  if (strstr(topic, AWS_IOT_SUBSCRIBE_TOPIC_LINEARACTUATOR))
  {
    deserializeJson(doc, payload);
    String compartmentStr = doc["compartment"];
    String actionStr = doc["action"];
    int compartment = compartmentStr.toInt();
    int action = actionStr.toInt();

    if (compartment == 1 && action == 0)
    {
      Serial.println("Activating Actuator Left");
      linear_actuator(1,3,action);
    }
  }

  // Automation
  if (strstr(topic, AWS_IOT_SUBSCRIBE_TOPIC_AUTOMATION))
  {
    deserializeJson(doc, payload);

    String phase = doc["phase"];
    String compartmentStr = doc["compartment"];
    int compartment = compartmentStr.toInt();
    JsonArray actions = doc["actions"].as<JsonArray>();

    // set automation
    automation_active = true;
    automation_phase = phase;
    automation_compartment = compartment;

    for (JsonVariant action : actions)
    {
      String type = action["type"];
      int time = action["time"].as<int>();
      Serial.println(type);
      Serial.println(time);

      if (type == "motor")
      {
        automation_motor_status = true;

        // Convert second to millisecond
        automation_motor_time = time * 1000;
      }
      else if (type == "airpump")
      {
        automation_airpump_status = true;

        // Convert second to millisecond
        automation_airpump_time = time * 1000;
      }
    }
  }
}

void connectAWS()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin("TPW4G-e3jWsZ", "8747435191");
 
  Serial.println("Connecting to Wi-Fi");
 
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
 
  // Configure WiFiClientSecure to ue the AWS IOT device credentials
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);

  // connect to MQTT Server
  client.setServer(AWS_IOT_ENDPOINT, 8883);

  client.setCallback(mqttMessageHandler);

  Serial.println("Connecting to AWS IOT");

  while (!client.connect(DEVICE_ID))
  {
    Serial.println(".");
    vTaskDelay(100 / portTICK_PERIOD_MS);
  }

  if (!client.connected())
  {
    Serial.println("AWS IOT Timeout");
    return;
  }

  // Subscribe to topic
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC_CONTROL_MOTOR);
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC_CONTROL_AIRPUMP);
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC_AUTOMATION);
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC_LINEARACTUATOR);

  Serial.println("AWS IOT Connected");
  isAwsIotConnected = true;
  isAwsIotSetup = true;
}

void reconnectAws()
{
  while (!client.connected())
  {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(DEVICE_ID))
    {
      Serial.println("AWS IOT Connected");
      // Subscribe to topic
      client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC_CONTROL_MOTOR);
      client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC_CONTROL_AIRPUMP);
      client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC_LINEARACTUATOR);
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      vTaskDelay(5000 / portTICK_PERIOD_MS);
    }
  }
}

void keepAwsAliveTask(void *parameters)
{
  // esp_task_wdt_add(nullptr);
  for (;;)
  {
    if (isWifiConnected)
    {
      if (client.connected())
      {
        vTaskDelay(10000 / portTICK_PERIOD_MS);
        continue;
      }
      else if (isAwsIotSetup)
      {
        reconnectAws();
      }
    }
  }
}

void readTemperatures()
{
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
}

void readMoistures()
{
  //   read moisture 1
  int val = analogRead(MOISTURE_PINS[0]);
  moistures[0] = map(val, AIR_VALUE, WATER_VALUE, 0, 100);

  // read moisture 2
  val = analogRead(MOISTURE_PINS[1]);
  moistures[1] = map(val, AIR_VALUE, WATER_VALUE, 0, 100);

  // read moisture 3
  val = analogRead(MOISTURE_PINS[2]);
  moistures[2] = map(val, AIR_VALUE, WATER_VALUE, 0, 100);

  // read moisture 4
  val = analogRead(MOISTURE_PINS[3]);
  moistures[3] = map(val, AIR_VALUE, WATER_VALUE, 0, 100);
}

void readMethanes()
{
  // read methane 1
  int val = analogRead(METHANE_PIN);
  // Serial.println("Methane");
  // Serial.println(val);
  methane = map(val, 0, 4095, 0, 5000);
}

void readCO2()
{
  int val = analogRead(CO2_PIN);
  co2 = map(val, 0, 4095, 0, 10000);
}

void readOxygen()
{
  oxygen = (float)oxygenSensor.getOxygenData(COLLECT_NUMBER);
  Serial.println("Oxygen at readOxygen");
  Serial.println(oxygen);
}

void readLid()
{
  int state = digitalRead(DOOR_PIN);
  if (state == HIGH)
  {
    lidState = "open";
  }
  else
  {
    lidState = "close";
  }
}

void publishDataTask(void *parameters)
{

  esp_task_wdt_add(nullptr);
  for (;;)
  {
    if (isAwsIotConnected)
    {
      readTemperatures();
      readMoistures();
      readMethanes();
      readCO2();
      readOxygen();
      readLid();

      StaticJsonDocument<400> doc;

      // temperature
      doc["temperature"]["active_phase"][0] = temperatures[0];
      doc["temperature"]["active_phase"][1] = temperatures[1];
      doc["temperature"]["active_phase"][2] = temperatures[2];
      doc["temperature"]["active_phase"][3] = temperatures[3];

      doc["temperature"]["curing_phase"][0] = temperatures[4];
      doc["temperature"]["curing_phase"][1] = temperatures[5];

      // moisture
      doc["moisture"]["active_phase"][0] = moistures[0];
      doc["moisture"]["active_phase"][1] = moistures[1];
      doc["moisture"]["curing_phase"][0] = moistures[2];
      doc["moisture"]["curing_phase"][1] = moistures[3];

      // methane
      doc["methane"] = methane;

      // oxygen
      doc["oxygen"] = oxygen;

      // co2
      doc["co2"] = co2;

      // lid
      doc["lid"] = lidState;

      doc["automation_active"] = automation_active;

      Serial.println("-----------------------------------");
      Serial.println(temperatures[0]);
      Serial.println(temperatures[1]);
      Serial.println(temperatures[2]);
      Serial.println(temperatures[3]);
      Serial.println(temperatures[4]);
      Serial.println(temperatures[5]);

      Serial.println(moistures[0]);
      Serial.println(moistures[1]);
      Serial.println(moistures[2]);
      Serial.println(moistures[3]);

      Serial.println(methane);
      Serial.println(oxygen);
      Serial.println(co2);
      Serial.println(lidState);

      Serial.println("-----------------------------------");

      char jsonBuffer[512];
      serializeJson(doc, jsonBuffer);
      client.publish(AWS_IOT_PUBLISH_TOPIC_DATA, jsonBuffer);

      Serial.println("Data Published to AWS IOT Core");
      vTaskDelay(3000 / portTICK_PERIOD_MS);
      esp_task_wdt_reset();
    }
  }
}

void pulseMotorActiveTask(void *parameters)
{

  for (;;)
  {

    if (motorOnActive)
    {
      digitalWrite(MOTOR_PUL1_PIN, LOW);
      digitalWrite(MOTOR_PUL1_PIN, HIGH);
      delayMicroseconds(60);
      //  vTaskDelay(60 / portTICK_PERIOD_MS);
      // ets_delay_us(60);
      // esp_task_wdt_reset();
    }
    // vTaskDelay(1 / portTICK_PERIOD_MS);
  }
}

void pulseMotorCuringTask(void *parameters)
{

  for (;;)
  {
    if (motorOnCuring)
    {
      Serial.println("Motor Curing On");

      digitalWrite(MOTOR_PUL2_PIN, LOW);

      digitalWrite(MOTOR_PUL2_PIN, HIGH);
      delayMicroseconds(60);
      esp_task_wdt_reset();
    }
    vTaskDelay(1 / portTICK_PERIOD_MS);
  }
}

void updateAutomationActive()
{

  // Check automatin motor and airpump off
  if (!automation_motor_status && !automation_airpump_status)
  {
    automation_active = false;
  }
  else
  {
    automation_active = true;
  }
}

void motorAutomationTask(void *parameter)
{
  for (;;)
  {
    if (automation_motor_status)
    {
      if (automation_phase == "active")
      {

        Serial.println("\nAutomation: Motor Active");

        // Turn on air pump
        Serial.println("Motor Active On");
        motorOnActive = true;

        // delay
        vTaskDelay(automation_motor_time / portTICK_PERIOD_MS);
        esp_task_wdt_reset();

        // Turn off air pump
        Serial.println("Motor Active Off");
        motorOnActive = false;
        digitalWrite(MOTOR_PUL1_PIN, LOW);

        automation_motor_status = false;
        updateAutomationActive();
      }
      else if (automation_phase == "curing")
      {
        Serial.println("\nAutomation: Motor Curing");

        // Turn on air pump
        Serial.println("Motor Curing On");
        motorOnCuring = true;

        // delay
        vTaskDelay(automation_motor_time / portTICK_PERIOD_MS);
        esp_task_wdt_reset();

        // Turn off air pump
        Serial.println("Motor Curing Off");
        motorOnCuring = false;
        digitalWrite(MOTOR_PUL2_PIN, LOW);

        automation_motor_status = false;
        updateAutomationActive();
      }
    }
    vTaskDelay(100 / portTICK_PERIOD_MS);
  }
}

void airPumpAutomationTask(void *parameter)
{
  for (;;)
  {
    if (automation_airpump_status)
    {
      if (automation_phase == "active")
      {

        Serial.println("\nAutomation: AirPump Active");

        // Turn on air pump
        airPumpActive(true, automation_compartment);

        // delay
        vTaskDelay(automation_airpump_time / portTICK_PERIOD_MS);
        esp_task_wdt_reset();

        // Turn off air pump
        airPumpActive(false, automation_compartment);

        automation_airpump_status = false;
        updateAutomationActive();
      }
      else if (automation_phase == "curing")
      {
        Serial.println("\nAutomation: AirPump Curing");

        // Turn on air pump
        airPumpCuring(true, automation_compartment);

        // delay
        vTaskDelay(automation_airpump_time / portTICK_PERIOD_MS);
        esp_task_wdt_reset();

        // Turn off air pump
        airPumpCuring(false, automation_compartment);

        automation_airpump_status = false;
        updateAutomationActive();
      }
    }
    vTaskDelay(100 / portTICK_PERIOD_MS);
  }
}

void setup()
{
  Serial.begin(9600);
  sensors.begin();
  Serial.print("Number of devices: ");
  Serial.println(sensors.getDeviceCount());  // Check device count
  connectAWS();
  Serial.println("Starting up");
  Serial.print("Device Name:");
  Serial.println(DEVICE_NAME);
  Serial.println("------");


  oxygenSensor.begin(Oxygen_IICAddress);

  pinMode(DOOR_PIN, INPUT_PULLUP);
  pinMode(3, OUTPUT);

  //pinMode(6, OUTPUT); //Linear Actuator
  //pinMode(7, OUTPUT); //Linear Actuator

  // motor 1
  pinMode(MOTOR_DIR1_PIN, OUTPUT);
  pinMode(MOTOR_PUL1_PIN, OUTPUT);
  pinMode(MOTOR_DIR1_PIN, HIGH);

  // motor 2
  pinMode(MOTOR_DIR2_PIN, OUTPUT);
  pinMode(MOTOR_PUL2_PIN, OUTPUT);

  // set motor direction
  digitalWrite(MOTOR_DIR1_PIN, LOW);
  digitalWrite(MOTOR_DIR2_PIN, LOW);

  // air pumps
  pinMode(AIRPUMP_ACTIVE1_PIN, OUTPUT);
  pinMode(AIRPUMP_ACTIVE2_PIN, OUTPUT);
  pinMode(AIRPUMP_CURING1_PIN, OUTPUT);
  pinMode(AIRPUMP_CURING2_PIN, OUTPUT);

  digitalWrite(AIRPUMP_ACTIVE1_PIN, HIGH);
  digitalWrite(AIRPUMP_ACTIVE2_PIN, HIGH);
  digitalWrite(AIRPUMP_CURING1_PIN, HIGH);
  digitalWrite(AIRPUMP_CURING2_PIN, HIGH);

  // make sure we don't get killed for our long running tasks
  //esp_task_wdt_init(30, false);
  delay(30);

  // Connect to AWS

  // Keep AWS IOT connection
  xTaskCreatePinnedToCore(keepAwsAliveTask, "Keep AWS IOT Alive", 2000, NULL, 1, NULL, CONFIG_ARDUINO_RUNNING_CORE);

  // Publish Data
  xTaskCreate(publishDataTask, "Publish Data", 10000, NULL, 1, NULL);

  //  Run motor 1
  // xTaskCreate(pulseMotorActiveTask, "Motor Active", 1000, NULL, 1, NULL);

  //  Run motor 2
  // xTaskCreate(pulseMotorCuringTask, "Motor Curing", 1000, NULL, 1, NULL);

  // Automation Task
  // Motor automation
  //xTaskCreate(motorAutomationTask, "Motor Automation", 1000, NULL, 1, NULL);
  // AirPump automation
  //xTaskCreate(airPumpAutomationTask, "Air Pump Automation", 1000, NULL, 1, NULL);
}

void PulseMotorActive()
{

  digitalWrite(MOTOR_PUL1_PIN, LOW);
  digitalWrite(MOTOR_PUL1_PIN, HIGH);
  delayMicroseconds(60);
  // Serial.println("Motor Active");
}

void PulseMotorCuring()
{
  digitalWrite(MOTOR_PUL2_PIN, LOW);
  digitalWrite(MOTOR_PUL2_PIN, HIGH);
  delayMicroseconds(60);
  // Serial.println("Motor Active");
}

void loop()
{
  client.loop();
  if (motorOnActive)
  {
    PulseMotorActive();
  }

  if (motorOnCuring)
  {
    PulseMotorCuring();
  }
}
