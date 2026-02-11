import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import time

# Set up the switch pins
state1_pin = digitalio.DigitalInOut(board.GP1)
state1_pin.direction = digitalio.Direction.INPUT
state1_pin.pull = digitalio.Pull.UP

state2_pin = digitalio.DigitalInOut(board.GP2)
state2_pin.direction = digitalio.Direction.INPUT
state2_pin.pull = digitalio.Pull.UP

def enter():
    kbd.press(Keycode.ENTER)
    time.sleep(0.1)
    kbd.release_all()

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# print("Waiting for switch to be in State 1 (GP1 to GND)...")
# 
# # Wait until switch is in State 1
# while True:
#     s1 = state1_pin.value
#     s2 = state2_pin.value
#     
#     if not s1 and s2:  # State 1: GP1 to GND
#         print("State 1 detected! Executing script...")
#         break
#     
#     time.sleep(0.1)

# Execute the HID script
time.sleep(3)  # Give host time to recognize Pico

# Open Start menu
kbd.press(Keycode.WINDOWS)
time.sleep(0.1)
kbd.release_all()
time.sleep(0.5)

# Launch Microsoft Edge
layout.write("edge")
enter()
time.sleep(1)
enter()
time.sleep(5)  # Allow Edge to fully open

# Focus address bar
kbd.press(Keycode.CONTROL, Keycode.L)
time.sleep(0.1)
kbd.release_all()
time.sleep(0.2)

# Navigate to URL
layout.write("https://beav.es/TJx")
enter()
time.sleep(2)  # Wait for page load

# Fullscreen browser (F11)
kbd.press(Keycode.F11)
time.sleep(0.1)
kbd.release_all()

time.sleep(100000000)


