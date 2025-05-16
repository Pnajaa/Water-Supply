#Water Supply
from machine import Pin, I2C
import time
from neopixel import NeoPixel
import ujson
import sys
import select
from DfrobotGP8403 import DfrobotGP8403

# ====== Regulator Pressure Control ======
# Set this to your desired pressure (in bar): 0.05 for lowest, 3.0 for highest
PRESSURE_SETPOINT = 1 #running state
PRESSURE_RESTPOINT = 0.05 #resting state 0.05 == 0V
# ====== Pin Setup ======
Water_pin = 11         # Water sensor input pin
Button_pin1 = 20       # Mode select button
Button_pin2 = 21       # Action button (manual/auto)
SOLENOID_IN1_PIN = 4   # DRV8871 IN1 
SOLENOID_IN2_PIN = 5   # DRV8871 IN2 
RGB_PIN = 28           # NeoPixel RGB data pin

# I2C DAC pins
I2C_SDA_PIN = 2  # Verify your Maker Pi Pico pins
I2C_SCL_PIN = 3
DAC_ADDR = 0x58   # Default for ET-MINI (A2/A1/A0=0/0/0)
i2c = I2C(1, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=100000)


DEBOUNCE_TIME = 50     # ms, for button debounce (not used in this IRQ setup)
HOLD_THRESHOLD = 2000  # ms, long press for OFF
BLINK_INTERVAL = 500   # ms, for blinking LED in paused state
RGB_level = 15         # RGB LED brightness (0-255)

# ====== Hardware Initialization ======
button1 = Pin(Button_pin1, Pin.IN, Pin.PULL_UP)
button2 = Pin(Button_pin2, Pin.IN, Pin.PULL_UP)
water_sensor = Pin(Water_pin, Pin.IN, Pin.PULL_UP)
solenoid_in1 = Pin(SOLENOID_IN1_PIN, Pin.OUT)
solenoid_in2 = Pin(SOLENOID_IN2_PIN, Pin.OUT)
rgb = NeoPixel(Pin(RGB_PIN, Pin.OUT), 1)
web_manual_hold = 1  # 1 = released, 0 = pressed (like button2_stable_state)

# Initialize DAC
dac = DfrobotGP8403(addr=0x58, sclpin=3, sdapin=2, i2cfreq=100000, hard=False)
channel = 1 #Vout0 = 0 or Vout1 = 1 if both use 3
dac.begin()
dac.set_dac_out_range(17) # 0 = OUTPUT_RANGE_5V  #17 = OUTPUT_RANGE_10V
def set_regulator_bar(bar):
    """Convert 0.05-5.0 bar → 0-10V and set DAC output"""
    voltage = ((bar - 0.05) / (5.0 - 0.05) * 10.0)*1000 # Linear conversion in milivoolt
    dac.set_dac_out_voltage(voltage, channel)
    # ====== Solenoid Control Functions ======
def solenoid_on():
    # Activate solenoid: IN1=1, IN2=0
    solenoid_in1.value(1)
    solenoid_in2.value(0)

def solenoid_off():
    # Deactivate solenoid: IN1=0, IN2=0 (safe state)
    solenoid_in1.value(0)
    solenoid_in2.value(0)

def solenoid_status():
    # Returns 1 if ON, 0 if OFF (for status reporting)
    return 1 if (solenoid_in1.value() == 1 and solenoid_in2.value() == 0) else 0

# ====== System Modes and State ======
MODES = {
    0: "OFF",
    1: "MANUAL",
    2: "AUTO"
}

class SystemState:
    def __init__(self):
        self.current_mode = 0          # 0=OFF, 1=MANUAL, 2=AUTO
        self.last_press_time = 0       # For button 1 press timing
        self.button1_pressed = False   # Track button 1 state
        self.button2_pressed = False   # Track button 2 state (for AUTO toggling)
        self.auto_running = False      # AUTO mode running flag
        self.auto_waiting = False      # AUTO mode waiting for water
        self.last_blink_time = 0       # For blinking LED
        self.blink_state = False       # For blinking LED

state = SystemState()

# ====== Debounce variables for Button 2 (manual mode hold) ======
button2_last_state = 1  # Start unpressed (pull-up)
button2_last_change_time = 0
button2_stable_state = 1
BUTTON2_DEBOUNCE_MS = 50  # ms

# ====== RGB LED Feedback ======
def update_led():
    # Set RGB LED color based on system state
    current_time = time.ticks_ms()
    if state.current_mode == 0:  # OFF: Red
        rgb[0] = (RGB_level, 0, 0)
    elif state.current_mode == 1:  # MANUAL: Green
        rgb[0] = (0, RGB_level, 0)
    elif state.current_mode == 2:  # AUTO
        if state.auto_waiting:
            rgb[0] = (RGB_level, RGB_level, 0)  # Yellow: waiting for water
        elif state.auto_running:
            rgb[0] = (0, 0, RGB_level)          # Blue: running
        else:
            # Blinking blue when paused
            if time.ticks_diff(current_time, state.last_blink_time) > BLINK_INTERVAL:
                state.blink_state = not state.blink_state
                state.last_blink_time = current_time
            rgb[0] = (0, 0, RGB_level) if state.blink_state else (0, 0, 0)
    rgb.write()

# ====== Status Reporting (Serial JSON) ======
def send_status():
    # Send current system status as JSON over USB serial
    status = {
        "mode": MODES[state.current_mode],
        "solenoid": solenoid_status(),
        "water": 1 if water_sensor.value() == 0 else 0,  # 1=water present, 0=no water
        "auto_running": state.auto_running,
        "auto_waiting": state.auto_waiting,
        "pressure_bar": PRESSURE_SETPOINT  # Report the water pressure while runing
    }
    print(ujson.dumps(status))

# ====== Handle Serial Commands from Web/Bridge ======
def handle_serial_command(cmd):
    global button2_stable_state
    global web_manual_hold
    global PRESSURE_SETPOINT
    try:
        data = ujson.loads(cmd)
        # Direct solenoid control (used by web "Action" button in MANUAL)
        if "solenoid" in data:
            web_manual_hold = 0 if data["solenoid"] else 1  # 0 = pressed, 1 = released
        #pressure change
        if "pressure_setpoint" in data:
            try:
                new_setpoint = float(data["pressure_setpoint"])
                if 0.05 <= new_setpoint <= 5.0:
                    PRESSURE_SETPOINT = new_setpoint
                    print("Pressure setpoint changed to", PRESSURE_SETPOINT)
                else:
                    print("Setpoint out of range")
            except Exception as e:
                print("Invalid setpoint:", e)
        # Change mode (simulate Button 1 short press)        
        if data.get("action") == "change_mode":
            if state.current_mode == 0:
                new_mode = 1
            else:
                new_mode = 2 if state.current_mode == 1 else 1
            state.current_mode = new_mode
            if new_mode == 2:
                state.auto_running = False
                state.auto_waiting = False
                state.blink_state = False
            if new_mode != 1:
                solenoid_off()
            update_led()
        # Action button (simulate Button 2 press in AUTO mode)
        if data.get("action") == "button2_press":
            if state.current_mode == 2:
                state.auto_running = not state.auto_running
                state.auto_waiting = False
                state.blink_state = False
                state.last_blink_time = time.ticks_ms()
                update_led()
                
        if data.get("action") == "off_mode":
            state.current_mode = 0
            solenoid_off()
            state.auto_running = False
            state.auto_waiting = False
            update_led()

    except:
        pass

# ====== Button 1 Interrupt Handler (Mode Select) ======
def button1_handler(pin):
    global state
    current_time = time.ticks_ms()
    if pin.value() == 0:  # Button pressed
        if not state.button1_pressed:
            state.last_press_time = current_time
            state.button1_pressed = True
    else:  # Button released
        if state.button1_pressed:
            press_duration = time.ticks_diff(current_time, state.last_press_time)
            state.button1_pressed = False
            if press_duration >= HOLD_THRESHOLD:
                # Long press: force OFF
                state.current_mode = 0
                solenoid_off()
                state.auto_running = False
                state.auto_waiting = False
            else:
                # Short press: cycle MANUAL/AUTO
                new_mode = 1 if state.current_mode == 0 else 2 if state.current_mode == 1 else 1
                state.current_mode = new_mode
                if new_mode == 2:
                    state.auto_running = False
                    state.auto_waiting = False
                    state.blink_state = False
                if new_mode != 1:
                    solenoid_off()
            update_led()

# Attach interrupt to Button 1
button1.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=button1_handler)

# ====== Main Loop ======
last_status_time = time.ticks_ms()
while True:
    current_time = time.ticks_ms()
    if state.current_mode == 0:
        set_regulator_bar(PRESSURE_RESTPOINT)
    # ====== MANUAL MODE: Web/Physical Button Control ======
    if state.current_mode == 1:
        # Physical button debouncing
        current_button2 = button2.value()
        if current_button2 != button2_last_state:
            button2_last_change_time = time.ticks_ms()
        button2_last_state = current_button2
        
        # Update stable state only if debounce time passed
        if time.ticks_diff(time.ticks_ms(), button2_last_change_time) > BUTTON2_DEBOUNCE_MS:
            button2_stable_state = current_button2

        # Priority: Web command OVERRIDES physical button
        if web_manual_hold == 0:  # Web button held
            set_regulator_bar(PRESSURE_SETPOINT)
            solenoid_on()
        elif button2_stable_state == 0:  # Physical button held
            set_regulator_bar(PRESSURE_SETPOINT)
            solenoid_on()
        else:
            set_regulator_bar(PRESSURE_RESTPOINT)
            solenoid_off()


    # --- AUTO MODE: Button 2 toggles auto_running, water sensor controls solenoid ---
    elif state.current_mode == 2:
        # Detect Button 2 press/release to toggle auto_running
        if button2.value() == 0:
            if not state.button2_pressed:
                state.button2_pressed = True
        else:
            if state.button2_pressed:
                state.button2_pressed = False
                state.auto_running = not state.auto_running
                state.auto_waiting = False
                state.blink_state = False
                state.last_blink_time = current_time
                update_led()
        # If running and water present, solenoid Off; else wait for water
        if state.auto_running and not state.auto_waiting:
            if water_sensor.value() == 1:  # Water detected (active low)
                set_regulator_bar(PRESSURE_SETPOINT)
                solenoid_on()
            else:
                set_regulator_bar(PRESSURE_RESTPOINT)
                solenoid_off()
                state.auto_waiting = True
                state.last_blink_time = current_time
                update_led()
        # If waiting and water returns, resume running
        if state.auto_waiting and water_sensor.value() == 1:
            state.auto_waiting = False
            state.auto_running = True
            update_led()

    # --- LED Feedback for AUTO paused/waiting ---
    if state.current_mode == 2 and (state.auto_waiting or not state.auto_running):
        set_regulator_bar(PRESSURE_RESTPOINT)
        update_led()

    # --- Send status over serial every 0.5s ---
    if time.ticks_diff(current_time, last_status_time) > 500:
        send_status()
        last_status_time = current_time

    # --- Handle incoming serial commands from web/bridge ---
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        cmd = sys.stdin.readline().strip()
        handle_serial_command(cmd)

    time.sleep_ms(50)  # Main loop delay for stability
    
