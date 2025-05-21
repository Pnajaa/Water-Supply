 
# Water-Supply
Project for **MECHATRONICS 2103535**
## Table of Contents
1. [The rational of the project](#1-the-rational-of-the-project)
2. [Background and Related Previous Works](#2-background-and-related-previous-works)
3. [Overall diagram](#3-overall-diagram)
4. [Python program](#4-python-program)
5. [Part lists](#5-part-lists)
6. [Demonstration Clips](#6-demonstration-clips)


## 1. The rational of the project
The objective of this project is to design a Small Mechatronics System that automates the water supply system. A Raspberry Pi Pico is used to control a solenoid valve, a compressed air regulator, and a non-contact water-level sensor, emulating the functionality of an automated water supply system. The system is IoT-enabled: sensor readings are published via MQTT, while a web application provides visualization and historical data, allowing users to remotely monitor water levels and sensor status.

## 2. Background and Related Previous Works
Efficient water management is a growing concern in both urban and rural settings, where traditional manual systems often lead to inefficiencies, delays, and resource wastage. The integration of automation and IoT technologies into water supply systems offers a promising solution by enabling real-time monitoring, remote control, and data-driven decision-making.

Recent developments in embedded systems and low-cost microcontrollers have made it feasible to design compact, intelligent water management solutions. The Raspberry Pi Pico, with its dual-core RP2040 processor and support for MicroPython, has emerged as a popular platform for such applications due to its affordability and versatility.

Previous studies have demonstrated the effectiveness of using non-contact sensors for water level detection that can be placed on the outside of the tank. Additionally, the use of MQTT protocol has become standard in IoT systems for its efficiency in transmitting sensor data.
Web-based interfaces are also commonly employed to visualize real-time data and historical trends, enhancing user engagement and system transparency.

This project builds upon these advancements by integrating a Raspberry Pi Pico-controlled system with a solenoid valve, compressed air regulator, and non-contact water level sensor. It leverages MQTT for data communication and a web application for visualization, creating a fully automated, remotely accessible water supply system.

## 3. Overall diagram
![Image](https://github.com/Pnajaa/Water-Supply/blob/ce17080890708fbf71c941f88fd8711987513dea/pic/Overview.jpg)

![Image](https://github.com/Pnajaa/Water-Supply/blob/524950d4a7a8e27ce3690d60b75727e4ec2e6dcc/pic/Overall%20Diagram.jpg)
## 4. Python program

=======How to Run=======

=== libary needed ===

Install Required Python Packages on PC/Server

1. flask

2. MongoDB

-command-

pip install flask flask-socketio eventlet flask-pymongo paho-mqtt pyserial

=== Hardware Setup ===

1. Connect wire by fllow the wiring diagram

2. Pico (main.py) :

Upload main.py and your DAC library (e.g., DfrobotGP8403.py) to your Maker Pi Pico using Thonny or ampy.

3. PC/Server :

Place app.py and bridge.py in the same project folder.

Place History.html and index.html in the floder name "template" and also in the project the have the 2 app and bridge files

bridge.py in Flisk floder -- sending sensor data from pico to Laptop over a USB port handle by MQTT Edit SERIAL_PORT = 'COM6' in bridge.py to match your Pico’s serial port (e.g., COM3 on Windows, /dev/ttyACM0 on Linux).

app.py in Flisk floder -- act to be web framework sending data from backend to frontend(web interface)

Ensure MongoDB is running locally (mongodb://localhost:27017/water_system).


===Web Interface===

 Use the Web Interface
Open your browser and go to http://localhost:5000
![Image](https://github.com/Pnajaa/Water-Supply/blob/7bb21513c3efc68fa7205d741812e0587b6468ff/pic/Web%20Interface.png)

You can:

1. _**Change mode (OFF, MANUAL, AUTO)**_
* System **OFF**

![Image](https://github.com/Pnajaa/Water-Supply/blob/0de9ad2e907146cb8bc6b250a59a2169d2b90ee2/pic/System%20OFF.png)

* System in **Manual Mode**

![Image](https://github.com/Pnajaa/Water-Supply/blob/0de9ad2e907146cb8bc6b250a59a2169d2b90ee2/pic/Manual%20Mode.png)

* System in **Auto Mode**

![Image](https://github.com/Pnajaa/Water-Supply/blob/af4880f4727c48cc897db92e6f51aedd7669d7a4/pic/Auto%20Mode.png)


2. _**Can handle machine mode (manual-auto-off) and function(Auto - use action button to chagne state, Manual - hold to use pump)**_

**LED Indicators:** [Pico LED Status](https://youtu.be/J_779zv18d4?si=_UDpGzsGQTG2D5w2)

[![Watch the video](https://img.youtube.com/vi/J_779zv18d4/0.jpg)](https://youtu.be/J_779zv18d4?si=_UDpGzsGQTG2D5w2)

1. **Solid Red LED:** System is OFF.

![Image](https://github.com/Pnajaa/Water-Supply/blob/e50853c813abe51ee55f43cc403186f92382b058/pic/S__13352969_0.jpg)

3. **Solid Green LED:** System is operating under Manual Mode.

![Image](https://github.com/Pnajaa/Water-Supply/blob/e50853c813abe51ee55f43cc403186f92382b058/pic/S__13352971_0.jpg)

5. **Solid Blue LED:** System is filling the water; water is not detected at the level sensor during Auto Mode.

![Image](https://github.com/Pnajaa/Water-Supply/blob/e50853c813abe51ee55f43cc403186f92382b058/pic/S__13352972_0.jpg)
   
7. **Blink Blue LED:** System is Idle in Auto Mode.

![Image](https://github.com/Pnajaa/Water-Supply/blob/e50853c813abe51ee55f43cc403186f92382b058/pic/S__13352974_0.jpg)

9. **Solid Yellow LED:** System is under Auto Mode and water is detected at the level sensor.

![Image](https://github.com/Pnajaa/Water-Supply/blob/e50853c813abe51ee55f43cc403186f92382b058/pic/S__13352973_0.jpg)


3. _**Set the pressure setpoint (0.05–5.0 bar) and click Set Pressure**_

**Setpoint at 1 Bar of Compressed Air Pressure**

![Image](https://github.com/Pnajaa/Water-Supply/blob/e50853c813abe51ee55f43cc403186f92382b058/pic/Set%201%20Bar.png)

**Setpoint at 3 Bar of Compressed Air Pressure**

![Image](https://github.com/Pnajaa/Water-Supply/blob/e50853c813abe51ee55f43cc403186f92382b058/pic/Set%203%20Bar.png)


4. _**View real-time status and history**_


![Image](https://github.com/Pnajaa/Water-Supply/blob/e153e7df6c6638072207272dd43a5990863a4ea8/pic/System%20Log.png)


=== If needed ===

If you change hardware pins, update them in main.py

If you use a different MQTT broker, update it in app.py and bridge.py

If you use a different MongoDB URI, update it in app.py

## 5. Part lists
1. [Microcontroller: Raspberry Pi Pico](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf) 1 Ea, *230.00 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352988_0.jpg)
2. [Solenoid Valve: SMC SY5120-5LZD-01](https://th.misumi-ec.com/en/vona2/detail/221300029672/?HissuCode=SY5120-5LZD-01) 1 Ea, *1,733.15 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352990_0.jpg)
4. [Electro-Pneumatic Regulators: SMC ITV2030-322S](https://th.misumi-ec.com/en/vona2/detail/221006475030/?HissuCode=ITV2030-322S) 1 Ea, *12,557.90 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352994_0.jpg)
5. [Non-contact liquid level sensor: XKC-Y26-NPN](https://xkc-sensor.com/detail/1428.html) 1 Ea, *240.00 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352976_0.jpg)
6. [Brushed DC Motor Driver: DRV8871](https://www.ti.com/lit/ds/symlink/drv8871.pdf?ts=1747713296454&ref_url=https%253A%252F%252Fwww.google.com%252F) 1 Ea, *250.00 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352992_0.jpg)
7. [Digital to Analog Convertor Module: ET-MINI I2C D/A](https://www.etteam.com/prodintf/ET-MINI-I2C-DA-10V/th-man-ET-MINI-I2C-DA-10V.pdf) 1 Ea, *330.00 ฿*
![Image](https://github.com/Pnajaa/Water-Supply/blob/7eb20fb6e453c3e6e84c3923cec3ffeb01c6f8a4/pic/S__13352993_0.jpg)
## 6. Demonstration Clips
[Water Supply @ 2 Bar of Compressed Air Pressure with Auto level control](https://youtu.be/-4KKM27_0G8?si=PFsfHLVXcu9kw8Zn)

[![Watch the video](https://img.youtube.com/vi/-4KKM27_0G8/0.jpg)](https://youtu.be/-4KKM27_0G8?si=PFsfHLVXcu9kw8Zn)

[Water Supply @ 2 Bar of Compressed Air Pressure with Manual level control](https://youtu.be/t14_QqYX_wY?si=O16tVIrwNscYOhKn)

[![Watch the video](https://img.youtube.com/vi/t14_QqYX_wY/0.jpg)](https://youtu.be/t14_QqYX_wY?si=O16tVIrwNscYOhKn)

[Water Supply @ 3 Bar of Compressed Air Pressure with Auto level control](https://youtu.be/GVrn9ShbKTY?si=fIKZL0MBUtPXyBzl)

[![Watch the video](https://img.youtube.com/vi/GVrn9ShbKTY/0.jpg)](https://youtu.be/GVrn9ShbKTY?si=fIKZL0MBUtPXyBzl)

[Water Supply under Varying Compressed Air Pressure with Manual level control](https://youtu.be/gGz0Z9c_rH0?si=NRW8_H563wOkiUoJ)

[![Watch the video](https://img.youtube.com/vi/gGz0Z9c_rH0/0.jpg)](https://youtu.be/gGz0Z9c_rH0?si=NRW8_H563wOkiUoJ)

[Web Interface During System Opearation](https://youtu.be/8oSqg5JCmNs)

[![Watch the video](https://img.youtube.com/vi/8oSqg5JCmNs/0.jpg)](https://youtu.be/8oSqg5JCmNs)


## Authors
1. Pee Netsuk 6130373821
2. Supasin Sinkittiyanont 6472087021
