# Water-Supply
Project for mechatronic class

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

