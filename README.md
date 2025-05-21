
# Pneumatic Water-Supply
Project for MECHATRONICS 2103535
## Table of Contents
1. [The rational of the project](#the-rational-of-the-project)
2. [Background and Related Previous Works](#background-and-related-previous-works)
3. [Overall diagram](#overall-diagram)
4. [Python program](#python-program)
5. [Part lists](#part-lists)
6. [Demonstration Clips](#demonstration-clips)


## 1. The rational of the project
  This project aims to design a Small Mechatronics System that automates the water supply system. A Raspberry Pi Pico is used to control solenoid valve, compressed air regulator and non-contact water-level sensor, emulate the funtionality of an automated water supply mechanism. The system is IoT-enabled: sensor readings are published via MQTT, while a web application provide visualization and historical system data, allowing users to remotely monitor water levels and sensor status.

## 2. Background and Related Previous Works
  Maintaining an appropriate water level in storage tanks is a fundamental requirement in residential, agricultural, and industrial systems. Traditional water-level control methods typically rely on float switches or manual inspection, which are prone to inefficiency and human error. As a result, researchers and engineers have developed automated systems using Microcomputers and sensor technologies to improve reliability, efficiency, and integration with modern digital infrastructure.

Several studies have utilized Arduino-based systems to implement automatic tank filling mechanisms. For instance, Kumar and Kaur (2019) developed an automatic water level monitoring and controlling system using an ultrasonic sensor and Arduino Uno. Their system demonstrated the feasibility of automating the water supply process at low cost and with improved precision.

With the advent of more powerful microcontrollers, such as the Raspberry Pi and ESP32, researchers have integrated Internet of Things (IoT) capabilities into water management systems. These advancements allow for remote monitoring, real-time alerts, and data logging. For example, Patel et al. (2020) proposed an IoT-based water tank monitoring system using ESP8266, Blynk IoT platform, and ultrasonic sensors, achieving real-time status updates via mobile apps.

The Raspberry Pi Pico, released in 2021, has since emerged as a compact and cost-effective microcontroller platform. It supports MicroPython and C/C++, making it suitable for lightweight embedded systems. While less powerful than the Raspberry Pi 4, its deterministic performance and low power consumption make it ideal for standalone mechatronics systems.

The MQTT (Message Queuing Telemetry Transport) protocol, a lightweight messaging protocol for low-bandwidth devices, has become a standard in IoT implementations. It enables efficient communication between embedded systems and cloud platforms or web applications (Light & Banks, 2019). Combined with web technologies such as Flask or Node.js, these systems can visualize sensor data in real time and allow users to interact with remote devices from anywhere.

This project builds upon the principles and success of these prior works by integrating a Raspberry Pi Pico, MQTT communication, a non-contact water-level sensor, and a web application into a single cohesive system. It offers a practical and scalable approach to smart water management and acts as a demonstrative platform for mechatronics, embedded systems, and IoT integration.

## 3. Overall diagram

## 4. Python program
==libary needed==

-flask

-MongoDB

=== Pico ===

main.py -- need to be running in pico

can edit working presure at line 12

PRESSURE_SETPOINT = 1 #running state

=== Sever ===

Next use laptop to be the sever. 
  Run bridge.py in Flisk floder -- sending sensor data from pico to Laptop over a USB port handle by MQTT
  
After that running the app.py to start flask sevice act to be web framework sending data from backend to frontend(web interface)

use DEV ip to test the web interface or http://127.0.0.1:5000/

===Web Interface===

-can handle machine mode (manual-auto-off) and function(Auto - use action button to chagne state, Manual - hold to use pump)

-have interface show the sensor and other setting calue

-have api to the history page that store the machine history data

## 5. Part lists
1. [Microcontroller: Raspberry Pi Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)  *230.00 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352988_0.jpg)
2. [Solenoid Valve: SMC SY5120-5LZD-01](https://th.misumi-ec.com/en/vona2/detail/221300029672/?HissuCode=SY5120-5LZD-01) *1,733.15 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352990_0.jpg)
4. [Electro-Pneumatic Regulators: SMC ITV2030-322S](https://th.misumi-ec.com/en/vona2/detail/221006475030/?HissuCode=ITV2030-322S) *12,557.90 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352994_0.jpg)
5. [Non-contact liquid level sensor: XKC-Y26-NPN](https://xkc-sensor.com/detail/1428.html) *240.00 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352976_0.jpg)
6. [Brushed DC Motor Driver: DRV8871](https://www.ti.com/lit/ds/symlink/drv8871.pdf?ts=1747713296454&ref_url=https%253A%252F%252Fwww.google.com%252F) *250.00 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352992_0.jpg)
7. [Digital to Analog Convertor Module: ET-MINI I2C D/A](https://www.etteam.com/prodintf/ET-MINI-I2C-DA-10V/th-man-ET-MINI-I2C-DA-10V.pdf) *330.00 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352993_0.jpg)
## 6. Demonstration Clips

