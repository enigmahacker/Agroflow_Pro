# AgroFlow Pro - Setup Guide

## 🔧 Hardware Assembly

### 1. Solar Power System
1. Mount the 20W solar panel on a south-facing surface (20-30° angle)
2. Connect solar panel to the MPPT charge controller:
   - Panel (+) → Controller IN(+)
   - Panel (-) → Controller IN(-)
3. Connect battery to MPPT:
   - Controller OUT(+) → Battery(+)
   - Controller OUT(-) → Battery(-)

### 2. Main Controller (ESP32)
1. Connect power to ESP32:
   - Battery (+) → 5V regulator → ESP32 5V
   - Battery (-) → ESP32 GND
2. Verify 5V and 3.3V regulators have heat sinks
3. Install appropriate capacitors (1000µF, 100µF) near power pins

### 3. Sensor Connections
#### Soil Moisture Sensor
```
Sensor VCC → 3.3V
Sensor GND → GND
Sensor A0  → GPIO34 (ADC)
```

#### Rain Sensor
```
Rain Sensor (+) → 5V
Rain Sensor (-) → GND
Rain Sensor OUT → GPIO32
```

#### Water Level Sensor
```
Sensor VCC → 3.3V
Sensor GND → GND
Sensor OUT → GPIO35 (ADC)
```

#### Temperature/Humidity (DHT11)
```
VCC → 3.3V
GND → GND
DATA → GPIO32
```

#### LCD I2C Display
```
VCC → 5V
GND → GND
SDA → GPIO21
SCL → GPIO22
```

### 4. Pump Control
```
Relay Module:
  VCC → 5V
  GND → GND
  IN → GPIO25

Relay Coil to Pump:
  NC/NO (normally closed/open) → 12V Pump
  COM → 12V +
  
Diode 1N4007 across pump (flyback protection)
```

### 5. Solenoid Valve Control
```
Solenoid Valve:
  Signal → GPIO26 (via relay)
  + → 12V
  - → GND
```

---

## 💾 Firmware Installation

### Prerequisites
- Arduino IDE or PlatformIO
- ESP32 Board Package (v2.0.0+)
- USB-C Cable for programming

### Steps

1. **Install Arduino IDE**
   - Download from: https://www.arduino.cc/en/software

2. **Add ESP32 Board**
   - File → Preferences
   - Board Manager URLs: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
   - Tools → Board Manager → Search "esp32" → Install

3. **Configure Board Settings**
   - Board: ESP32 Dev Module
   - Upload Speed: 921600
   - CPU Frequency: 240 MHz
   - Flash Size: 4MB
   - Partition Scheme: Default 4MB with spiffs

4. **Install Required Libraries**
   - Sketch → Include Library → Manage Libraries
   - Search and install:
     - LiquidCrystal I2C
     - PubSubClient (for MQTT)
     - DHT sensor library
     - BluetoothSerial (built-in)

5. **Upload Firmware**
   - Connect ESP32 via USB
   - Open `firmware/main.ino`
   - Tools → Upload (or Ctrl+U)
   - Wait for completion

---

## 🔐 Configuration

### 1. WiFi Setup
Edit `config.json`:
```json
"wifi": {
  "ssid": "YOUR_NETWORK_NAME",
  "password": "YOUR_NETWORK_PASSWORD"
}
```

### 2. MQTT Configuration
```json
"mqtt": {
  "broker": "mqtt.example.com",
  "port": 1883,
  "username": "agroflow",
  "password": "secure_password"
}
```

### 3. Sensor Calibration
- **Dry soil reading**: Place sensor in dry soil → Note ADC value
- **Wet soil reading**: Place sensor in water → Note ADC value
- Update `config.json`:
```json
"irrigation": {
  "soil_moisture_dry": 1800,
  "soil_moisture_wet": 700
}
```

### 4. Irrigation Thresholds
```json
"irrigation": {
  "moisture_threshold_low": 35,   // Start watering at 35%
  "moisture_threshold_high": 80   // Stop at 80%
}
```

---

## 🌐 Backend Setup

### 1. Install Python Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Database Setup (PostgreSQL)
```bash
# Install PostgreSQL (macOS)
brew install postgresql@15

# Start service
brew services start postgresql@15

# Create database
createdb agroflow

# Create user
psql agroflow -c "CREATE USER agroflow_user WITH PASSWORD 'secure_password';"
psql agroflow -c "ALTER ROLE agroflow_user WITH CREATEDB;"
```

### 3. Environment Variables
Create `.env`:
```
FLASK_ENV=production
DEBUG=False
DATABASE_URL=postgresql://agroflow_user:secure_password@localhost:5432/agroflow
MQTT_BROKER=mqtt.example.com
MQTT_PORT=1883
MQTT_USER=agroflow
MQTT_PASSWORD=secure_password
```

### 4. Run Backend
```bash
python dashboard/app.py
```
Backend will start at `http://localhost:5000`

---

## 📱 Testing

### 1. Sensor Testing
- Monitor serial output: Arduino IDE → Tools → Serial Monitor (115200 baud)
- Expected output:
```
========== AgroFlow Pro Initializing ==========
Soil Moisture: 1200
Rain Sensor: 1
Water Level: 500
Battery ADC: 2048
```

### 2. API Testing
```bash
# Health check
curl http://localhost:5000/api/health

# Get latest data
curl http://localhost:5000/api/data/latest

# Send test data
curl -X POST http://localhost:5000/api/data/store \
  -H "Content-Type: application/json" \
  -d '{
    "moisture": 65.5,
    "waterLevel": 75.0,
    "temperature": 28.5,
    "humidity": 65.0,
    "battery": 12.5,
    "rain": false,
    "pump": true
  }'
```

### 3. Bluetooth Testing
- Use mobile app: "BlueTerm" or "Serial Bluetooth Terminal"
- Connect to "AgroFlow_Pro"
- Send commands:
  - `PUMP_ON` - Start pump
  - `PUMP_OFF` - Stop pump
  - `STATUS` - Get current status

---

## ⚠️ Troubleshooting

### WiFi Connection Issues
- Verify SSID and password in config
- Check WiFi signal strength (should be > -80 dBm)
- Restart ESP32: Press RST button

### MQTT Connection Fails
- Verify broker address and port
- Check firewall settings
- Test connection: `mosquitto_sub -h mqtt.example.com -u agroflow -P password`

### Sensor Readings Incorrect
- Recalibrate dry/wet values
- Check sensor connections
- Verify ADC pins are not floating

### Pump Not Operating
- Check relay coil voltage (should be 5V)
- Verify pump has power (12V)
- Test with manual pump control

### Database Connection Error
- Verify PostgreSQL is running: `pg_isready`
- Check connection string in `.env`
- Create database if missing: `createdb agroflow`

---

## 📊 Monitoring & Maintenance

### Daily Checks
- [ ] Monitor soil moisture readings
- [ ] Verify pump operation
- [ ] Check battery voltage (should be > 11V)
- [ ] Monitor alert system

### Weekly Maintenance
- [ ] Clean solar panel surface
- [ ] Check water tank level
- [ ] Inspect wiring for corrosion
- [ ] Review sensor calibration

### Monthly Tasks
- [ ] Update firmware if available
- [ ] Check battery health
- [ ] Verify cloud data sync
- [ ] Backup local database

### Annual Maintenance
- [ ] Battery replacement (if needed)
- [ ] Full system recalibration
- [ ] Hardware inspection
- [ ] Software performance review

---

## 🆘 Support

For issues or questions:
1. Check this guide's troubleshooting section
2. Review project documentation in `/docs`
3. Check GitHub issues
4. Contact: bal.vigyan@example.com

---

**Last Updated**: December 2025
**Version**: 1.0
