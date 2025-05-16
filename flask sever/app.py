import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "water-system-secret"
app.config["MONGO_URI"] = "mongodb://localhost:27017/water_system"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
mongo = PyMongo(app)

MQTT_BROKER = 'broker.hivemq.com'
MQTT_TOPIC = 'pico/status'
MQTT_CONTROL = 'pico/control'
mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

def on_mqtt_message(client, userdata, msg, properties=None):
    try:
        payload = msg.payload.decode().strip()
        if not payload or payload == "offline":
            return
        #debug
        #print(f"Raw MQTT payload: {payload}")
        data = json.loads(payload)
        data['server_time'] = datetime.now(timezone.utc).isoformat()
        mongo.db.sensor_data.insert_one(data.copy())
        emit_data = {
            'mode': str(data.get('mode', 'UNKNOWN')),
            'solenoid': int(data.get('solenoid', 0)),
            'water': int(data.get('water', 0)),
            'pressure_bar': float(data.get('pressure_bar', 0.0)),
            'auto_running': bool(data.get('auto_running', False)),
            'auto_waiting': bool(data.get('auto_waiting', False)),
            'server_time': data['server_time']
        }
        #debug
        #print(f"Emitting: {emit_data}")
        # FIX: Remove broadcast=True unless you use a namespace
        socketio.emit('status_update', emit_data)
    except Exception as e:
        print(f"MQTT error: {str(e)}")

mqttc.on_message = on_mqtt_message
mqttc.connect(MQTT_BROKER, 1883, 60)
mqttc.subscribe(MQTT_TOPIC)
mqttc.loop_start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    try:
        readings = list(mongo.db.sensor_data.find().sort("_id", -1).limit(100))
        for r in readings:
            r['_id'] = str(r['_id'])
        return render_template('history.html', readings=readings)
    except Exception as e:
        print(f"History error: {str(e)}")
        return render_template('history.html', readings=[])

@socketio.on('control')
def handle_control(data):
    try:
        print(f"Sending control: {data}")
        mqttc.publish(MQTT_CONTROL, json.dumps(data))
    except Exception as e:
        print(f"Control error: {str(e)}")

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False)
