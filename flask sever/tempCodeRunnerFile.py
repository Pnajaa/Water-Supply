import serial
import paho.mqtt.client as mqtt
import threading

SERIAL_PORT = 'COM6'  # Change to your Pico's COM port!
BAUDRATE = 115200

MQTT_BROKER = 'broker.hivemq.com'
TOPIC_PUB = 'pico/status'
TOPIC_SUB = 'pico/control'

ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

def on_mqtt_message(client, userdata, msg, properties=None):
    ser.write((msg.payload.decode() + '\n').encode())

mqttc.on_message = on_mqtt_message
mqttc.connect(MQTT_BROKER, 1883, 60)
mqttc.subscribe(TOPIC_SUB)

def serial_to_mqtt():
    while True:
        line = ser.readline().decode().strip()
        if line:
            print("From Pico:", line)
            mqttc.publish(TOPIC_PUB, line)
        mqttc.loop(0.01)

if __name__ == '__main__':
    threading.Thread(target=serial_to_mqtt, daemon=True).start()
    mqttc.loop_forever()
