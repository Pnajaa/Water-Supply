import serial
import paho.mqtt.client as mqtt
import threading
import time

# Configuration
SERIAL_PORT = 'COM6'  # Update with your Pico's COM port
BAUDRATE = 115200
MQTT_BROKER = 'broker.hivemq.com'
TOPIC_PUB = 'pico/status'
TOPIC_SUB = 'pico/control'

# Initialize serial port
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

# MQTT Client Setup
mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC_SUB)
    else:
        print(f"Connection failed with code {reason_code}")

def on_disconnect(client, userdata, reason_code, properties=None):
    print(f"Disconnected from MQTT broker (code: {reason_code})")
    reconnect(client)

def reconnect(client):
    while True:
        try:
            client.reconnect()
            return
        except Exception as e:
            print(f"Reconnection failed: {str(e)}")
            time.sleep(5)

def on_mqtt_message(client, userdata, msg, properties=None):
    try:
        payload = msg.payload.decode('utf-8').strip()
        ser.write(f"{payload}\n".encode('utf-8'))
        print(f"Forwarded to Pico: {payload}")
    except UnicodeDecodeError:
        print("Error: Received non-UTF-8 MQTT payload")
    except serial.SerialException as e:
        print(f"Serial write error: {str(e)}")
    except Exception as e:
        print(f"MQTT handler error: {str(e)}")

def serial_to_mqtt():
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"From Pico: {line}")
                mqttc.publish(TOPIC_PUB, line)
        except UnicodeDecodeError:
            print("Error: Received non-UTF-8 serial data")
        except serial.SerialException as e:
            print(f"Serial read error: {str(e)}")
            time.sleep(1)
        except Exception as e:
            print(f"Serial thread error: {str(e)}")

# MQTT Callbacks
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_mqtt_message

# Start MQTT connection
mqttc.connect(MQTT_BROKER, 1883, 60)

# Start threads
serial_thread = threading.Thread(target=serial_to_mqtt, daemon=True)
serial_thread.start()

# Start MQTT loop
mqttc.loop_forever()
