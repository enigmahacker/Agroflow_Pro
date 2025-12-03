# AgroFlow Pro – Solar-Powered IoT Smart Irrigation System

**₹5000 Pro Edition | Bal Vigyan Project – Sustainable Smart Farming Technology**

---

## 🌱 Project Overview

AgroFlow Pro is a solar-powered smart irrigation system that uses IoT, automation, real-time sensors, AI-driven crop moisture database, and renewable energy to irrigate farms efficiently. It reduces water usage by up to 50%, cuts electricity costs, and supports farmers in remote areas with unreliable networks through Bluetooth fallback mode.

## 📋 Abstract

Traditional irrigation wastes huge amounts of water and electricity due to manual operation and fixed-schedule watering. In many rural areas, farmers face unstable power supply and weak internet connection, leading to crop damage and excessive water loss.

AgroFlow Pro solves this with:
- ✅ Real-time soil moisture monitoring via capacitive sensors
- ✅ 100% solar-powered operation (no grid dependency)
- ✅ Automatic rain detection to prevent water waste
- ✅ SMS/App alerts for low tank water levels
- ✅ IoT dashboard + LCD local monitoring
- ✅ Voice control via Alexa/Google Assistant
- ✅ Offline Bluetooth fallback mode
- ✅ Water savings & carbon credit tracking

---

## 🎯 Problem Statement

- **Water Wastage**: Up to 50% loss in conventional farming
- **Manual Labor**: Unpredictable irrigation timing and human error
- **Electricity Shortage**: Rural areas lack reliable power supply
- **Lack of Precision**: No monitoring of soil, weather, and crop-specific needs
- **No Automation**: No emergency alert system or intelligent control

---

## 💡 Proposed Solution

A smart, self-powered irrigation controller featuring:

### Core Features
- 🌞 **100% Solar Powered**: Runs independently without grid dependency
- 💧 **Soil Moisture Sensing**: Capacitive sensors for precise water needs detection
- 🌧️ **Rain Detection**: Automatically stops watering during rainfall
- 📱 **Multi-Interface Monitoring**: IoT dashboard, LCD display, mobile app
- 🔊 **Voice Assistant Support**: Alexa & Google Assistant integration
- 📡 **Dual Connectivity**: Wi-Fi + Bluetooth fallback for remote areas
- 📊 **Data Analytics**: Water savings tracking & carbon credit impact
- ⚠️ **Alert System**: SMS & push notifications for critical events
- 🔌 **Pump Control**: Automatic on/off based on soil moisture levels

## 📦 Hardware Components (₹5000 Budget)

| Component | Qty | Cost (₹) | Notes |
|-----------|-----|---------|-------|
| ESP32 Microcontroller | 1 | 500 | Main controller |
| Solar Panel (20W) | 1 | 1500 | Power source |
| Li-ion Battery (18650) | 4 | 400 | Energy storage |
| Capacitive Soil Moisture Sensor | 2 | 300 | Moisture detection |
| Rain Sensor Module | 1 | 200 | Rain detection |
| Water Level Sensor | 1 | 200 | Tank monitoring |
| DHT11 Temperature/Humidity | 1 | 150 | Environmental data |
| DC Water Pump (12V) | 1 | 800 | Irrigation control |
| Relay Module (5V) | 2 | 200 | Pump switching |
| Battery Charging Module | 1 | 300 | Solar charge control |
| LCD 16x2 Display | 1 | 200 | Local monitoring |
| Wireless Modules (WiFi/BT) | 1 | 400 | Already in ESP32 |
| Miscellaneous (PCB, wires, connectors) | - | 450 | Assembly materials |
| **Total** | | **₹5000** | |

---

## 🔧 Technical Stack

### Firmware
- **Language**: C++ (Arduino)
- **Platform**: ESP32 microcontroller
- **Libraries**: Arduino IoT Cloud, Bluetooth Classic, WiFi

### Backend
- **Language**: Python/Node.js
- **Framework**: Flask/Express
- **Database**: PostgreSQL/MongoDB
- **Real-time**: WebSocket/MQTT

### Frontend
- **Dashboard**: React/Vue.js
- **Mobile App**: Flutter/React Native
- **Protocol**: REST API + WebSocket

### Cloud Services
- **Server**: AWS/Google Cloud/Heroku
- **IoT Platform**: AWS IoT Core / Azure IoT Hub
- **Storage**: Cloud database with S3 backup

---

## 🚀 Getting Started

### Prerequisites
- ESP32 development board
- Arduino IDE or PlatformIO
- Python 3.8+
- Node.js 14+
- Hardware components (as per BOM)

### Installation
1. Clone the repository
2. Install firmware dependencies: See `firmware/README.md`
3. Install backend dependencies: `pip install -r requirements.txt`
4. Install frontend dependencies: `cd dashboard && npm install`
5. Configure `config.json` with your settings
6. Run tests: `pytest tests/`

---

## 📊 Key Benefits

| Benefit | Impact |
|---------|--------|
| Water Savings | 40-50% reduction in water usage |
| Cost Reduction | ₹15,000-20,000/year electricity savings |
| Solar Independence | 100% renewable energy, no grid dependence |
| Precision Farming | AI-driven, crop-specific irrigation |
| Remote Monitoring | Real-time alerts & dashboard access |
| Emergency Resilience | Works offline via Bluetooth |

---

## 📚 Documentation

- [Project Report](docs/PROJECT_REPORT.md)
- [Setup Guide](docs/SETUP_GUIDE.md)
- [API Documentation](docs/API_DOCUMENTATION.md)
- [User Manual](docs/USER_MANUAL.md)
- [Hardware BOM](hardware/BOM.md)

---

## 👥 Team

**Bal Vigyan Project** - Sustainable Smart Farming Technology

---

## 📝 License

This project is open-source and available for educational and non-commercial use.

---

## 📞 Support

For questions or issues, please contact the development team or check the documentation.

**Last Updated**: December 2025

