# AgroFlow Pro - User Manual

**Solar-Powered IoT Smart Irrigation System**

---

## Table of Contents
1. [Getting Started](#getting-started)
2. [System Overview](#system-overview)
3. [Daily Operation](#daily-operation)
4. [Mobile App Guide](#mobile-app-guide)
5. [Troubleshooting](#troubleshooting)
6. [FAQs](#faqs)

---

## Getting Started

### Initial Setup (5-10 minutes)

#### Step 1: Physical Installation
1. Mount the solar panel facing south at 30° angle
2. Place the controller box in a shaded, weatherproof location
3. Connect water pipes to the system
4. Position soil sensors at 10-15cm depth in root zone
5. Place water level sensor in tank

#### Step 2: Power Up
1. Flip the power switch to ON
2. The LCD screen should light up with "AgroFlow Pro"
3. Wait 30 seconds for system startup
4. Check that all lights are green

#### Step 3: Connect to WiFi (Optional)
1. Press and hold the SETUP button for 3 seconds
2. LCD will show WiFi pairing mode
3. Use phone to connect to "AgroFlow_Pro" network
4. Open browser and enter WiFi credentials
5. System will automatically restart

#### Step 4: Calibration
1. Place soil moisture sensor in dry soil
2. Press CALIBRATE button - note the dry reading
3. Place sensor in fully wet soil (water bucket)
4. Press CALIBRATE again - note the wet reading
5. System will adjust automatically

---

## System Overview

### Main Components

#### LCD Display
```
┌──────────────────┐
│ M:65% P:ON      │
│ B:12.5V OK      │
└──────────────────┘
```
- **M**: Soil moisture percentage
- **P**: Pump status (ON/OFF)
- **B**: Battery voltage
- **Status**: OK/RAIN/LOW WATER/ERROR

#### Control Buttons
- **POWER**: Turn system on/off
- **SETUP**: Configure WiFi/settings
- **CALIBRATE**: Sensor calibration mode
- **OVERRIDE**: Manual pump control

#### LED Indicators
- 🟢 **Green**: System operating normally
- 🟡 **Yellow**: Warning (low water/battery)
- 🔴 **Red**: Error or critical issue
- 🔵 **Blue**: WiFi connected

---

## Daily Operation

### Automatic Mode (Recommended)

The system runs completely automatically:

1. **Soil Monitoring**: Checks moisture every 5 minutes
2. **Smart Watering**: Automatically starts pump when moisture drops below 35%
3. **Precise Control**: Stops pump when moisture reaches 80%
4. **Rain Detection**: Stops watering during rainfall
5. **Alerts**: Sends notifications when issues occur

### What You Need to Do

#### Daily (2 minutes)
- [ ] Check LCD for status
- [ ] Verify no error lights
- [ ] Check water tank level visually

#### Weekly (10 minutes)
- [ ] Clean solar panel with dry cloth
- [ ] Check for any leaks
- [ ] Review app data/alerts
- [ ] Verify battery voltage (should be > 11V)

#### Monthly
- [ ] Full system inspection
- [ ] Recalibrate soil sensor
- [ ] Check pump operation
- [ ] Backup data from cloud

---

## Mobile App Guide

### Installation
1. Download "AgroFlow" app from App Store or Play Store
2. Open app and create account
3. Tap "+" to add device
4. Scan QR code on system (under solar panel)
5. Tap "Connect" and wait for pairing

### Dashboard
Shows real-time data:
- Current soil moisture
- Tank water level
- Battery status
- Pump operation status
- Environmental conditions (temp/humidity)

### Controls
- **Water Now**: Start pump immediately
- **Stop Water**: Stop pump immediately
- **Schedule**: Set custom watering times
- **Settings**: Configure thresholds and preferences

### Analytics
- **Water Usage**: See daily/weekly/monthly water consumption
- **Cost Savings**: Calculate electricity and water savings
- **Carbon Impact**: Track environmental benefits
- **Alerts**: Review all system alerts and history

### Notifications
You'll receive alerts for:
- Low water level
- Low battery
- Pump malfunction
- High moisture (overwatering warning)
- Rain detected
- System offline for >1 hour

---

## Troubleshooting

### Problem: System Won't Turn On
**Solutions:**
1. Check if power switch is ON
2. Verify battery voltage (use multimeter)
3. If battery < 10V, charge from solar or external source
4. Try pressing RESET button

### Problem: LCD Shows "LOW BATT"
**Solutions:**
1. Place in sunny location for solar charging (2-3 hours)
2. Check if solar panel is clean
3. Verify panel angle is 20-30°
4. Connect external charger if available

### Problem: Pump Not Turning On
**Solutions:**
1. Check if water tank is full (minimum 30%)
2. Verify soil is actually dry (LCD shows < 35%)
3. Press OVERRIDE button to test manually
4. Check water line for blockage

### Problem: False Rain Detection
**Solutions:**
1. Check rain sensor is clean
2. Wipe off any dust or dew
3. Adjust sensitivity setting in app (if available)
4. Check for sensor malfunction

### Problem: WiFi Won't Connect
**Solutions:**
1. Check WiFi network is 2.4GHz (not 5GHz)
2. Verify password is correct
3. Move system closer to router
4. Restart system and try again
5. System works offline via Bluetooth if WiFi fails

### Problem: High Water Bills (No Savings)
**Check:**
1. Are thresholds set correctly? (Should be 35% low, 80% high)
2. Is rain sensor working?
3. Are drip lines leaking?
4. Is soil naturally very dry?

---

## FAQs

### Q: Does the system work without WiFi?
**A:** Yes! The system works 100% offline. WiFi is optional for cloud backup and app monitoring. Even without WiFi, the pump operates automatically based on soil moisture.

### Q: What happens during rain?
**A:** The rain sensor automatically stops the pump and prevents watering for 30 minutes after rain stops. No water wastage!

### Q: How often should I water?
**A:** The system decides! It waters when soil moisture drops below 35%, so frequency depends on weather, soil type, and crop. Typically 1-3 times per week.

### Q: Can I control it remotely?
**A:** Yes, if WiFi is connected. The mobile app lets you view status and manually control the pump from anywhere. Without WiFi, use Bluetooth within 10-50 meters.

### Q: What's the battery life?
**A:** With solar charging, the system runs 24/7 indefinitely. Even on cloudy days, the battery provides 12-24 hours of backup (depending on usage).

### Q: Can I use this for multiple fields?
**A:** Currently, one system per field. Multiple systems can be grouped in the app to manage together.

### Q: What crops is it suitable for?
**A:** Works for all crops: vegetables, fruits, grains, orchards. The moisture thresholds can be adjusted per crop in settings.

### Q: Does it work in very hot climates?
**A:** Yes, but may need more frequent watering. Increase the watering frequency by lowering the "high moisture threshold" from 80% to 70% in settings.

### Q: Is it safe to leave unattended for weeks?
**A:** Absolutely! The system is designed for this. Set it to automatic mode and it will handle everything. Check the app occasionally for alerts.

### Q: What's the warranty?
**A:** 1-year hardware warranty. Extended warranty available. Check with your dealer.

### Q: Can I upgrade the system later?
**A:** Yes! You can add more sensors, expand to multiple zones, or upgrade to the Premium version with advanced AI features.

---

## Emergency Override

### Manual Pump Control
If you need to water immediately (e.g., emergency):

1. Press and hold OVERRIDE button (bottom, red)
2. LCD will show "Manual Mode"
3. Pump will start immediately
4. Press OVERRIDE again to stop
5. System returns to auto mode after 30 minutes

⚠️ **Warning**: Manual mode ignores all safety checks (rain, low water, etc.). Use sparingly!

---

## Maintenance Schedule

### Daily
- [ ] Check LED status (should be green)

### Weekly
- [ ] Clean solar panel
- [ ] Check water tank level
- [ ] Review app notifications

### Monthly
- [ ] Inspect connections for corrosion
- [ ] Test manual override
- [ ] Download and backup data

### Quarterly
- [ ] Recalibrate soil sensor
- [ ] Deep clean all components
- [ ] Check battery health

### Annually
- [ ] Professional inspection
- [ ] Battery replacement (if needed)
- [ ] Software update

---

## Safety Warnings

⚠️ **DO NOT:**
- Submerge controller unit in water
- Use damaged cables or connectors
- Exceed maximum water pressure (2 bar)
- Leave manual override on for > 1 hour
- Modify internal electronics

✅ **DO:**
- Keep solar panel clean
- Protect from extreme heat (> 50°C)
- Store in cool, dry place if not in use
- Regular maintenance checks
- Follow local regulations for water usage

---

## Support & Contact

**For Help:**
- 📱 Mobile App: Help section
- 🌐 Website: www.agroflowpro.com
- 📧 Email: support@agroflowpro.com
- 📞 Phone: +91-XXXXXXXXXX

**Available in:**
- English
- Hindi
- Marathi
- Tamil

---

**Document Version**: 1.0
**Last Updated**: December 2025
**Suitable for AgroFlow Pro v1.0**
