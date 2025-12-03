"""
AgroFlow Pro - Web Dashboard Backend
Flask REST API for IoT Irrigation System

Author: Bal Vigyan Project
Date: December 2025
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://user:password@localhost:5432/agroflow'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class SensorReading(db.Model):
    """Store sensor data readings"""
    __tablename__ = 'sensor_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    soil_moisture = db.Column(db.Float)
    water_level = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    battery_voltage = db.Column(db.Float)
    rain_detected = db.Column(db.Boolean, default=False)
    pump_active = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'soil_moisture': self.soil_moisture,
            'water_level': self.water_level,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'battery_voltage': self.battery_voltage,
            'rain_detected': self.rain_detected,
            'pump_active': self.pump_active
        }


class Alert(db.Model):
    """Store system alerts"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    alert_type = db.Column(db.String(50))  # 'low_water', 'low_battery', 'rain', 'error'
    message = db.Column(db.String(255))
    severity = db.Column(db.String(20))  # 'info', 'warning', 'critical'
    read = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'alert_type': self.alert_type,
            'message': self.message,
            'severity': self.severity,
            'read': self.read
        }


class SystemConfig(db.Model):
    """Store system configuration"""
    __tablename__ = 'system_config'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True)
    value = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'key': self.key,
            'value': self.value,
            'updated_at': self.updated_at.isoformat()
        }


# ==================== API ROUTES ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/api/data/latest', methods=['GET'])
def get_latest_data():
    """Get latest sensor readings"""
    reading = SensorReading.query.order_by(SensorReading.timestamp.desc()).first()
    
    if not reading:
        return jsonify({'error': 'No data available'}), 404
    
    return jsonify(reading.to_dict()), 200


@app.route('/api/data/history', methods=['GET'])
def get_data_history():
    """Get sensor readings history"""
    hours = request.args.get('hours', 24, type=int)
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    readings = SensorReading.query.filter(
        SensorReading.timestamp >= start_time
    ).order_by(SensorReading.timestamp.desc()).all()
    
    return jsonify({
        'count': len(readings),
        'data': [r.to_dict() for r in readings]
    }), 200


@app.route('/api/data/store', methods=['POST'])
def store_sensor_data():
    """Store new sensor reading (called by ESP32)"""
    try:
        data = request.get_json()
        
        reading = SensorReading(
            soil_moisture=data.get('moisture'),
            water_level=data.get('waterLevel'),
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            battery_voltage=data.get('battery'),
            rain_detected=data.get('rain'),
            pump_active=data.get('pump')
        )
        
        db.session.add(reading)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'id': reading.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get system alerts"""
    unread_only = request.args.get('unread', False, type=bool)
    limit = request.args.get('limit', 20, type=int)
    
    query = Alert.query.order_by(Alert.timestamp.desc())
    
    if unread_only:
        query = query.filter_by(read=False)
    
    alerts = query.limit(limit).all()
    
    return jsonify({
        'count': len(alerts),
        'alerts': [a.to_dict() for a in alerts]
    }), 200


@app.route('/api/alerts', methods=['POST'])
def create_alert():
    """Create a new alert (called by ESP32)"""
    try:
        data = request.get_json()
        
        alert = Alert(
            alert_type=data.get('type'),
            message=data.get('message'),
            severity=data.get('severity', 'info')
        )
        
        db.session.add(alert)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'id': alert.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/alerts/<int:alert_id>/read', methods=['PUT'])
def mark_alert_read(alert_id):
    """Mark alert as read"""
    alert = Alert.query.get(alert_id)
    
    if not alert:
        return jsonify({'error': 'Alert not found'}), 404
    
    alert.read = True
    db.session.commit()
    
    return jsonify({'status': 'success'}), 200


@app.route('/api/commands/pump', methods=['POST'])
def control_pump():
    """Send pump control command"""
    data = request.get_json()
    action = data.get('action')  # 'on' or 'off'
    
    if action not in ['on', 'off']:
        return jsonify({'error': 'Invalid action'}), 400
    
    # TODO: Send command to ESP32 via MQTT or direct connection
    
    return jsonify({
        'status': 'success',
        'command': 'pump_' + action
    }), 200


@app.route('/api/stats/water-savings', methods=['GET'])
def get_water_savings():
    """Calculate water savings statistics"""
    days = request.args.get('days', 30, type=int)
    start_time = datetime.utcnow() - timedelta(days=days)
    
    # Calculate total watering time and estimate water saved
    readings = SensorReading.query.filter(
        SensorReading.timestamp >= start_time
    ).all()
    
    pump_on_count = sum(1 for r in readings if r.pump_active)
    total_readings = len(readings)
    
    # Assuming 5L/min pump, 5-minute sample interval
    watering_time_minutes = pump_on_count * 5
    water_used_liters = watering_time_minutes * 5
    
    # Baseline: conventional farming uses 25mm/day = ~250,000L for 1 hectare
    # Assuming 0.1 hectare plot, baseline = 25,000L for 30 days
    baseline_water = 25000 * (days / 30)
    water_saved = baseline_water - water_used_liters
    
    return jsonify({
        'period_days': days,
        'water_used_liters': water_used_liters,
        'water_saved_liters': water_saved,
        'watering_time_minutes': watering_time_minutes,
        'pump_on_percentage': (pump_on_count / total_readings * 100) if total_readings > 0 else 0
    }), 200


@app.route('/api/stats/carbon-impact', methods=['GET'])
def get_carbon_impact():
    """Calculate carbon footprint reduction"""
    days = request.args.get('days', 30, type=int)
    
    # Solar power instead of grid:
    # Average Indian grid: 0.65 kg CO2 per kWh
    # Assuming 8W average consumption, 24 hours/day
    energy_saved_kwh = (0.008 * 24 * days) / 1000
    co2_saved_kg = energy_saved_kwh * 0.65
    
    return jsonify({
        'period_days': days,
        'energy_saved_kwh': round(energy_saved_kwh, 2),
        'co2_saved_kg': round(co2_saved_kg, 2),
        'equivalent_trees': round(co2_saved_kg / 20, 1)  # 1 tree absorbs ~20kg CO2/year
    }), 200


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get system configuration"""
    configs = SystemConfig.query.all()
    
    return jsonify({
        'config': {c.key: c.value for c in configs}
    }), 200


@app.route('/api/config/<key>', methods=['PUT'])
def update_config(key):
    """Update system configuration"""
    try:
        data = request.get_json()
        value = data.get('value')
        
        config = SystemConfig.query.filter_by(key=key).first()
        
        if config:
            config.value = value
            config.updated_at = datetime.utcnow()
        else:
            config = SystemConfig(key=key, value=value)
            db.session.add(config)
        
        db.session.commit()
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


# ==================== DATABASE INITIALIZATION ====================

def init_db():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")


# ==================== MAIN ====================

if __name__ == '__main__':
    init_db()
    
    # Development server
    debug = os.getenv('DEBUG', 'False') == 'True'
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug
    )
