/*
 * AgroFlow Pro - Smart Irrigation System
 * Main Firmware for ESP32
 * 
 * Features:
 * - Solar-powered IoT irrigation system
 * - Real-time soil moisture monitoring
 * - Rain detection & automatic shutdown
 * - SMS alerts via GSM
 * - Web dashboard + Bluetooth fallback
 * - Battery backup system
 * 
 * Author: Bal Vigyan Project
 * Date: December 2025
 * Version: 1.0
 */

#include <Arduino.h>
#include <WiFi.h>
#include <MQTT.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <BluetoothSerial.h>

// ==================== CONFIGURATION ====================

// WiFi Configuration
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "mqtt.example.com";
const int mqtt_port = 1883;

// Pin Definitions
#define SOIL_MOISTURE_PIN A0      // Analog pin for soil moisture
#define RAIN_SENSOR_PIN 34        // Digital pin for rain sensor
#define WATER_LEVEL_PIN A1        // Analog pin for water level
#define TEMP_HUMIDITY_PIN 32      // DHT11 pin
#define PUMP_RELAY_PIN 25         // Relay control for pump
#define SOLENOID_VALVE_PIN 26     // Solenoid valve control
#define BATTERY_VOLTAGE_PIN A2    // Battery voltage monitoring
#define LCD_SDA 21                // I2C SDA
#define LCD_SCL 22                // I2C SCL

// Thresholds
#define SOIL_MOISTURE_DRY 1800    // Raw value for dry soil
#define SOIL_MOISTURE_WET 700     // Raw value for wet soil
#define MOISTURE_THRESHOLD_LOW 35 // Start watering at 35%
#define MOISTURE_THRESHOLD_HIGH 80 // Stop watering at 80%
#define WATER_TANK_MIN 200        // Minimum water level alert
#define BATTERY_MIN_VOLTAGE 10.5  // Minimum battery voltage

// ==================== GLOBAL VARIABLES ====================

LiquidCrystal_I2C lcd(0x27, 16, 2); // I2C address 0x27, 16x2 display
BluetoothSerial SerialBT;
WiFiClient espClient;
MQTTClient client;

// System State Variables
struct SystemState {
  float soilMoisture;
  float waterLevel;
  float temperature;
  float humidity;
  float batteryVoltage;
  bool rainDetected;
  bool pumpActive;
  bool systemError;
  unsigned long lastUpdate;
};

SystemState currentState = {0, 0, 0, 0, 0, false, false, false, 0};

// ==================== SETUP ====================

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n\n========== AgroFlow Pro Initializing ==========");
  
  // Initialize pins
  pinMode(PUMP_RELAY_PIN, OUTPUT);
  pinMode(SOLENOID_VALVE_PIN, OUTPUT);
  pinMode(RAIN_SENSOR_PIN, INPUT);
  
  // Default: pump off
  digitalWrite(PUMP_RELAY_PIN, LOW);
  digitalWrite(SOLENOID_VALVE_PIN, LOW);
  
  // Initialize I2C LCD
  Wire.begin(LCD_SDA, LCD_SCL);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("AgroFlow Pro");
  lcd.setCursor(0, 1);
  lcd.print("Initializing...");
  
  // Initialize Bluetooth
  SerialBT.begin("AgroFlow_Pro"); // Bluetooth device name
  Serial.println("Bluetooth started, name: AgroFlow_Pro");
  
  // Initialize WiFi
  initWiFi();
  
  // Initialize MQTT
  client.begin(mqtt_server, mqtt_port, espClient);
  client.onMessage(onMqttMessage);
  
  // Test sensors
  testSensors();
  
  Serial.println("Setup complete!");
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Ready!");
}

// ==================== MAIN LOOP ====================

void loop() {
  // Update system state
  updateSensorReadings();
  
  // Check connectivity
  if (!client.connected()) {
    reconnectMqtt();
  }
  client.loop();
  
  // Main irrigation logic
  irrigationControl();
  
  // Check for alerts
  checkAlerts();
  
  // Update display
  updateDisplay();
  
  // Log data to MQTT
  publishData();
  
  // Handle Bluetooth commands
  handleBluetoothInput();
  
  // Delay before next iteration
  delay(5000); // 5-second update interval
}

// ==================== SENSOR READING FUNCTIONS ====================

void updateSensorReadings() {
  // Read soil moisture
  int rawMoisture = analogRead(SOIL_MOISTURE_PIN);
  currentState.soilMoisture = mapMoisture(rawMoisture);
  
  // Read water level
  int rawWaterLevel = analogRead(WATER_LEVEL_PIN);
  currentState.waterLevel = mapWaterLevel(rawWaterLevel);
  
  // Read rain sensor
  currentState.rainDetected = digitalRead(RAIN_SENSOR_PIN) == LOW;
  
  // Read battery voltage
  int rawBattery = analogRead(BATTERY_VOLTAGE_PIN);
  currentState.batteryVoltage = (rawBattery / 4095.0) * 15.0; // Scale for voltage divider
  
  // Read temperature/humidity (DHT11)
  // TODO: Add DHT11 library and implement
  currentState.temperature = 28.5; // Placeholder
  currentState.humidity = 65.0;    // Placeholder
  
  currentState.lastUpdate = millis();
}

float mapMoisture(int rawValue) {
  // Convert raw ADC value to percentage (0-100%)
  if (rawValue > SOIL_MOISTURE_DRY) return 0;
  if (rawValue < SOIL_MOISTURE_WET) return 100;
  
  return ((float)(SOIL_MOISTURE_DRY - rawValue) / (SOIL_MOISTURE_DRY - SOIL_MOISTURE_WET)) * 100;
}

float mapWaterLevel(int rawValue) {
  // Convert raw ADC value to tank percentage
  return (rawValue / 4095.0) * 100;
}

// ==================== IRRIGATION CONTROL ====================

void irrigationControl() {
  // Override: Stop if it's raining
  if (currentState.rainDetected) {
    stopPump();
    return;
  }
  
  // Override: Stop if water tank is low
  if (currentState.waterLevel < WATER_TANK_MIN) {
    stopPump();
    return;
  }
  
  // Override: Stop if battery is critically low
  if (currentState.batteryVoltage < BATTERY_MIN_VOLTAGE) {
    stopPump();
    return;
  }
  
  // Main irrigation logic
  if (currentState.soilMoisture < MOISTURE_THRESHOLD_LOW) {
    // Soil is dry, start watering
    startPump();
  } 
  else if (currentState.soilMoisture > MOISTURE_THRESHOLD_HIGH) {
    // Soil is wet, stop watering
    stopPump();
  }
  // Otherwise maintain current state
}

void startPump() {
  if (!currentState.pumpActive) {
    digitalWrite(PUMP_RELAY_PIN, HIGH);
    digitalWrite(SOLENOID_VALVE_PIN, HIGH);
    currentState.pumpActive = true;
    
    Serial.println("Pump started");
    SerialBT.println("Pump started");
  }
}

void stopPump() {
  if (currentState.pumpActive) {
    digitalWrite(PUMP_RELAY_PIN, LOW);
    digitalWrite(SOLENOID_VALVE_PIN, LOW);
    currentState.pumpActive = false;
    
    Serial.println("Pump stopped");
    SerialBT.println("Pump stopped");
  }
}

// ==================== ALERT SYSTEM ====================

void checkAlerts() {
  // Low water level alert
  if (currentState.waterLevel < WATER_TANK_MIN) {
    sendAlert("ALERT: Water tank low! Level: " + String(currentState.waterLevel) + "%");
  }
  
  // Low battery alert
  if (currentState.batteryVoltage < BATTERY_MIN_VOLTAGE) {
    sendAlert("ALERT: Battery low! Voltage: " + String(currentState.batteryVoltage) + "V");
  }
  
  // Rain detected
  if (currentState.rainDetected) {
    sendAlert("INFO: Rain detected, irrigation stopped");
  }
  
  // System error
  if (currentState.systemError) {
    sendAlert("ERROR: System malfunction detected!");
  }
}

void sendAlert(String message) {
  Serial.println(message);
  SerialBT.println(message);
  // TODO: Add SMS functionality via GSM module
}

// ==================== DISPLAY FUNCTIONS ====================

void updateDisplay() {
  static unsigned long lastDisplayUpdate = 0;
  
  if (millis() - lastDisplayUpdate > 2000) { // Update display every 2 seconds
    lcd.clear();
    
    // Line 1: Moisture | Temp
    lcd.setCursor(0, 0);
    lcd.print("M:");
    lcd.print((int)currentState.soilMoisture);
    lcd.print("% ");
    
    if (currentState.pumpActive) {
      lcd.print("P:ON ");
    } else {
      lcd.print("P:OFF");
    }
    
    // Line 2: Battery | Rain
    lcd.setCursor(0, 1);
    lcd.print("B:");
    lcd.print(currentState.batteryVoltage, 1);
    lcd.print("V ");
    
    if (currentState.rainDetected) {
      lcd.print("RAIN");
    } else {
      lcd.print("OK  ");
    }
    
    lastDisplayUpdate = millis();
  }
}

// ==================== MQTT FUNCTIONS ====================

void initWiFi() {
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi failed! Using Bluetooth fallback");
  }
}

void reconnectMqtt() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    if (client.connect("AgroFlow_ESP32")) {
      Serial.println("connected");
      client.subscribe("agroflow/command");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.lastError());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void publishData() {
  if (client.connected()) {
    // Create JSON payload
    String payload = "{";
    payload += "\"moisture\":" + String(currentState.soilMoisture, 2) + ",";
    payload += "\"waterLevel\":" + String(currentState.waterLevel, 2) + ",";
    payload += "\"temperature\":" + String(currentState.temperature, 2) + ",";
    payload += "\"humidity\":" + String(currentState.humidity, 2) + ",";
    payload += "\"battery\":" + String(currentState.batteryVoltage, 2) + ",";
    payload += "\"rain\":" + String(currentState.rainDetected ? "true" : "false") + ",";
    payload += "\"pump\":" + String(currentState.pumpActive ? "true" : "false");
    payload += "}";
    
    client.publish("agroflow/data", payload);
  }
}

void onMqttMessage(String &topic, String &payload) {
  Serial.println("MQTT message: " + topic + " = " + payload);
  
  if (payload == "PUMP_ON") {
    startPump();
  } else if (payload == "PUMP_OFF") {
    stopPump();
  }
}

// ==================== BLUETOOTH FUNCTIONS ====================

void handleBluetoothInput() {
  if (SerialBT.available()) {
    String command = SerialBT.readStringUntil('\n');
    command.trim();
    
    if (command == "PUMP_ON") {
      startPump();
    } else if (command == "PUMP_OFF") {
      stopPump();
    } else if (command == "STATUS") {
      printStatus();
    } else if (command == "RESTART") {
      ESP.restart();
    }
  }
}

void printStatus() {
  String status = "=== AgroFlow Status ===\n";
  status += "Moisture: " + String(currentState.soilMoisture, 1) + "%\n";
  status += "Water Level: " + String(currentState.waterLevel, 1) + "%\n";
  status += "Temperature: " + String(currentState.temperature, 1) + "°C\n";
  status += "Humidity: " + String(currentState.humidity, 1) + "%\n";
  status += "Battery: " + String(currentState.batteryVoltage, 2) + "V\n";
  status += "Pump: " + String(currentState.pumpActive ? "ON" : "OFF") + "\n";
  status += "Rain: " + String(currentState.rainDetected ? "YES" : "NO") + "\n";
  
  SerialBT.println(status);
}

// ==================== TESTING FUNCTIONS ====================

void testSensors() {
  Serial.println("\nTesting sensors...");
  
  // Test soil moisture
  int moisture = analogRead(SOIL_MOISTURE_PIN);
  Serial.println("Soil Moisture: " + String(moisture));
  
  // Test rain sensor
  int rain = digitalRead(RAIN_SENSOR_PIN);
  Serial.println("Rain Sensor: " + String(rain));
  
  // Test water level
  int water = analogRead(WATER_LEVEL_PIN);
  Serial.println("Water Level: " + String(water));
  
  // Test battery voltage
  int battery = analogRead(BATTERY_VOLTAGE_PIN);
  Serial.println("Battery ADC: " + String(battery));
  
  Serial.println("Sensor test complete!\n");
}

// ==================== END OF FIRMWARE ====================
