# AgroFlow Pro - API Documentation

## Base URL
```
http://localhost:5000/api
```

---

## Authentication
All API requests should include:
```
Authorization: Bearer YOUR_API_TOKEN
Content-Type: application/json
```

---

## Endpoints

### 1. Health Check
Check if the API is running.

**Request:**
```
GET /health
```

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-01T10:30:45.123456",
  "version": "1.0.0"
}
```

---

### 2. Get Latest Sensor Data
Retrieve the most recent sensor readings.

**Request:**
```
GET /data/latest
```

**Response (200):**
```json
{
  "id": 1,
  "timestamp": "2025-12-01T10:30:45.123456",
  "soil_moisture": 65.5,
  "water_level": 85.0,
  "temperature": 28.5,
  "humidity": 72.0,
  "battery_voltage": 12.4,
  "rain_detected": false,
  "pump_active": true
}
```

**Error (404):**
```json
{"error": "No data available"}
```

---

### 3. Get Sensor Data History
Retrieve historical sensor readings.

**Request:**
```
GET /data/history?hours=24
```

**Parameters:**
- `hours` (optional): Number of hours to look back (default: 24)

**Response (200):**
```json
{
  "count": 288,
  "data": [
    {
      "id": 1,
      "timestamp": "2025-12-01T10:30:45.123456",
      "soil_moisture": 65.5,
      "water_level": 85.0,
      "temperature": 28.5,
      "humidity": 72.0,
      "battery_voltage": 12.4,
      "rain_detected": false,
      "pump_active": true
    },
    ...
  ]
}
```

---

### 4. Store Sensor Data
Store new sensor reading (called by ESP32).

**Request:**
```
POST /data/store
```

**Body:**
```json
{
  "moisture": 65.5,
  "waterLevel": 85.0,
  "temperature": 28.5,
  "humidity": 72.0,
  "battery": 12.4,
  "rain": false,
  "pump": true
}
```

**Response (201):**
```json
{
  "status": "success",
  "id": 1
}
```

**Error (400):**
```json
{"error": "Invalid data"}
```

---

### 5. Get Alerts
Retrieve system alerts.

**Request:**
```
GET /alerts?unread=false&limit=20
```

**Parameters:**
- `unread` (optional): Show only unread alerts (default: false)
- `limit` (optional): Maximum number of alerts to return (default: 20)

**Response (200):**
```json
{
  "count": 5,
  "alerts": [
    {
      "id": 1,
      "timestamp": "2025-12-01T10:30:45.123456",
      "alert_type": "low_water",
      "message": "Water tank level below 20%",
      "severity": "warning",
      "read": false
    },
    ...
  ]
}
```

---

### 6. Create Alert
Create a new system alert (called by ESP32).

**Request:**
```
POST /alerts
```

**Body:**
```json
{
  "type": "low_water",
  "message": "Water tank level below 20%",
  "severity": "warning"
}
```

**Response (201):**
```json
{
  "status": "success",
  "id": 1
}
```

---

### 7. Mark Alert as Read
Mark an alert as read.

**Request:**
```
PUT /alerts/{alert_id}/read
```

**Parameters:**
- `alert_id`: The ID of the alert

**Response (200):**
```json
{"status": "success"}
```

**Error (404):**
```json
{"error": "Alert not found"}
```

---

### 8. Pump Control
Send pump control commands.

**Request:**
```
POST /commands/pump
```

**Body:**
```json
{
  "action": "on"
}
```

**Parameters:**
- `action`: "on" or "off"

**Response (200):**
```json
{
  "status": "success",
  "command": "pump_on"
}
```

**Error (400):**
```json
{"error": "Invalid action"}
```

---

### 9. Water Savings Statistics
Get water savings analytics.

**Request:**
```
GET /stats/water-savings?days=30
```

**Parameters:**
- `days` (optional): Number of days to analyze (default: 30)

**Response (200):**
```json
{
  "period_days": 30,
  "water_used_liters": 5000,
  "water_saved_liters": 20000,
  "watering_time_minutes": 1000,
  "pump_on_percentage": 35.5
}
```

---

### 10. Carbon Impact
Get carbon footprint reduction statistics.

**Request:**
```
GET /stats/carbon-impact?days=30
```

**Parameters:**
- `days` (optional): Number of days to analyze (default: 30)

**Response (200):**
```json
{
  "period_days": 30,
  "energy_saved_kwh": 5.76,
  "co2_saved_kg": 3.74,
  "equivalent_trees": 0.2
}
```

---

### 11. Get Configuration
Get system configuration.

**Request:**
```
GET /config
```

**Response (200):**
```json
{
  "config": {
    "moisture_low_threshold": "35",
    "moisture_high_threshold": "80",
    "pump_runtime_limit": "300",
    "alert_enabled": "true"
  }
}
```

---

### 12. Update Configuration
Update system configuration.

**Request:**
```
PUT /config/{key}
```

**Parameters:**
- `key`: Configuration key name

**Body:**
```json
{
  "value": "40"
}
```

**Response (200):**
```json
{"status": "success"}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Missing/invalid API key |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server-side error |

---

## Rate Limiting
- ESP32 data submissions: Max 1 per 5 seconds
- API queries: Max 100 requests per minute
- Alert creation: Max 10 per minute

---

## Data Ranges

| Field | Min | Max | Unit |
|-------|-----|-----|------|
| soil_moisture | 0 | 100 | % |
| water_level | 0 | 100 | % |
| temperature | -10 | 50 | °C |
| humidity | 0 | 100 | % |
| battery_voltage | 9 | 15 | V |

---

## Example cURL Commands

### Get Latest Data
```bash
curl -X GET http://localhost:5000/api/data/latest \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Submit Data from ESP32
```bash
curl -X POST http://localhost:5000/api/data/store \
  -H "Content-Type: application/json" \
  -d '{
    "moisture": 65.5,
    "waterLevel": 85.0,
    "temperature": 28.5,
    "humidity": 72.0,
    "battery": 12.4,
    "rain": false,
    "pump": true
  }'
```

### Turn On Pump
```bash
curl -X POST http://localhost:5000/api/commands/pump \
  -H "Content-Type: application/json" \
  -d '{"action": "on"}'
```

### Get Water Savings
```bash
curl -X GET "http://localhost:5000/api/stats/water-savings?days=30" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

**Last Updated**: December 2025
**API Version**: 1.0
