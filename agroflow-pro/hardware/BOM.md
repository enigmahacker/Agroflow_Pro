# Bill of Materials (BOM) - AgroFlow Pro

**Total Budget: ₹5,000**

---

## Main Controller & Processing

| Part | Specification | Qty | Cost (₹) | Source |
|------|---------------|-----|---------|--------|
| ESP32 DevKit | 32-bit, WiFi+BT | 1 | 500 | Amazon/eBay |
| Micro USB Cable | For programming | 1 | 50 | Local |
| **Subtotal** | | | **₹550** | |

---

## Power Management

| Part | Specification | Qty | Cost (₹) | Source |
|------|---------------|-----|---------|--------|
| Solar Panel | 20W, 18V, Monocrystalline | 1 | 1,500 | Amazon/Flipkart |
| Li-ion Battery 18650 | 3.7V, 2600mAh | 4 | 400 | Local battery shop |
| Battery Holder | 4-slot 18650 holder | 1 | 50 | Local |
| Solar Charge Controller | MPPT 10A, 12V | 1 | 800 | Amazon |
| DC-DC Buck Converter | 12V→5V, 3A | 2 | 200 | eBay |
| Voltage Regulator | LM7805 (5V) | 5 | 50 | Local |
| Capacitors | 1000µF, 100µF mix | 10 | 100 | Local |
| **Subtotal** | | | **₹3,150** | |

---

## Sensors

| Part | Specification | Qty | Cost (₹) | Source |
|------|---------------|-----|---------|--------|
| Capacitive Soil Moisture Sensor | Analog, resistant | 2 | 300 | Amazon/eBay |
| Rain Sensor Module | Digital, sensitivity adjustable | 1 | 200 | eBay |
| Water Level Sensor | Capacitive, 15-80mm range | 1 | 200 | Amazon |
| DHT11 Sensor | Temperature + Humidity | 1 | 150 | Amazon/eBay |
| **Subtotal** | | | **₹850** | |

---

## Actuators & Control

| Part | Specification | Qty | Cost (₹) | Source |
|------|---------------|-----|---------|--------|
| 12V DC Water Pump | 5L/min, submersible option | 1 | 800 | Local hardware store |
| 5V Relay Module | 2-channel, for pump control | 2 | 200 | Amazon/eBay |
| Solenoid Valve | 12V, 1/2" NPT thread | 1 | 300 | Hardware store |
| Diode | 1N4007 (flyback protection) | 5 | 25 | Local |
| **Subtotal** | | | **₹1,325** | |

---

## Display & Interface

| Part | Specification | Qty | Cost (₹) | Source |
|------|---------------|-----|---------|--------|
| LCD Display | 16x2, I2C backpack | 1 | 200 | Amazon/eBay |
| Push Button | 6mm tactile switches | 3 | 30 | Local |
| Buzzer | 5V, 85dB | 1 | 30 | eBay |
| Status LEDs | Red, Green, Yellow | 3 | 20 | Local |
| **Subtotal** | | | **₹280** | |

---

## Connectivity (Optional)

| Part | Specification | Qty | Cost (₹) | Source |
|------|---------------|-----|---------|--------|
| GSM Module | SIM800L or equivalent | 1 | 400 | Optional |
| SIM Card | Any carrier | 1 | 99 | Any telecom |
| **Subtotal** | | | **₹499** (Optional) |

---

## Miscellaneous & Assembly

| Part | Specification | Qty | Cost (₹) | Source |
|------|---------------|-----|---------|--------|
| PCB/Breadboard | For circuitry | 1 | 100 | Local |
| Jumper Wires | Male-Male, Male-Female mix | 1 | 100 | Local |
| Resistors Mix | 10Ω-1MΩ (1/4W) | 1 | 50 | Local |
| Solder & Flux | Lead-free | 1 | 50 | Local |
| PVC Pipes & Fittings | For water system | 1 | 200 | Hardware store |
| Project Enclosure | IP65 waterproof box | 1 | 150 | Amazon |
| Heat Shrink Tubing | Assorted sizes | 1 | 50 | Local |
| Mounting Hardware | Screws, nuts, bolts | 1 | 100 | Local |
| Wire/Cable | 18 AWG, multicore | 1 | 150 | Local |
| **Subtotal** | | | **₹950** | |

---

## Summary

| Category | Cost (₹) |
|----------|---------|
| Main Controller | 550 |
| Power Management | 3,150 |
| Sensors | 850 |
| Actuators & Control | 1,325 |
| Display & Interface | 280 |
| Miscellaneous | 950 |
| **TOTAL** | **₹7,105** |

---

## Cost Optimization Notes

### Budget Adjustment (₹5,000 Version)
To fit the ₹5,000 budget, reduce:
- Remove GSM module (save ₹400)
- Use smaller solar panel (12W instead of 20W, save ₹500)
- Use basic relay instead of relay module (save ₹100)
- Reduce sensor count (remove one sensor, save ₹200)

**Adjusted Total: ₹5,005**

---

## Recommended Suppliers

### India
- **Amazon.in** - General electronics
- **eBay.in** - Components & modules
- **Flipkart** - Consumer electronics
- **Local Electronics Shops** - Common components
- **Hardware Stores** - Plumbing & mechanical parts

### Online International
- **AliExpress** - Bulk purchase discounts
- **Banggood** - Competitive pricing
- **eBay Global** - Wide selection

---

## Assembly Sequence

1. **Power System First**: Solar panel → Charge controller → Battery
2. **Controller Setup**: ESP32 + power regulation
3. **Sensor Integration**: Connect all sensors to analog/digital pins
4. **Display Connection**: LCD via I2C
5. **Pump Control**: Relay + pump connection
6. **Enclosure**: Mount all components in waterproof box
7. **Testing**: Verify each component before final assembly

---

## Quality Assurance

- [ ] Verify all components before purchase
- [ ] Test power supply under load
- [ ] Check sensor calibration
- [ ] Verify waterproof integrity
- [ ] Test pump operation
- [ ] Verify ESP32 connectivity

**Last Updated**: December 2025
**Version**: 1.0
