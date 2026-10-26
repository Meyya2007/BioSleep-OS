BioSleep OS — Passive Thermal Defense Operating System

Overview

BioSleep OS is a prototype for event-driven thermal monitoring that combines an ESP32 microcontroller, a temperature sensor, a potentiometer-based microbial-index input, a Flask dashboard, and SQLite data logging.

The system monitors temperature and the microbial index, displays live readings, assigns status levels, and stores sensor data for review.

Objectives

- Monitor temperature using a DS18B20 sensor.
- Demonstrate a microbial-index input using a potentiometer.
- Transmit sensor readings from an ESP32 to a Python backend.
- Display readings and status levels on a web dashboard.
- Store sensor records in an SQLite database.
- Explore event-driven monitoring and idle-state concepts.

Hardware

- ESP32 development board
- DS18B20 temperature sensor
- 10K potentiometer
- Jumper wires and USB cable

Software

- Arduino IDE and ESP32 firmware
- Python
- Flask
- SQLite
- HTML and CSS
- Windows PowerShell serial bridge

System Workflow

1. The ESP32 reads the temperature sensor and potentiometer.
2. A PowerShell bridge reads the serial output and sends readings to the Flask endpoint.
3. Flask processes incoming readings and stores records in SQLite.
4. The dashboard displays the latest readings and system status.
5. The analytics page presents recorded sensor data.

Important Note

The potentiometer provides a simulated microbial-index input. It does not directly detect microorganisms. Temperature and status thresholds are configurable demonstration values and are not validated biological safety limits.

Prototype Demonstration

Video link: [Add your prototype video link here]

Project Status

Working prototype with hardware input, a Flask dashboard, and SQLite data logging.

Team / Author

Project: BioSleep OS
