import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Give the host time to recognize the device
time.sleep(2)

# register keyboard
keyboard = Keyboard(usb_hid.devices)
# setup keyboard layout so we can "type" rather than
# calling each keypress individually
layout = KeyboardLayoutUS(keyboard)

# write!
layout.write("hello world\n")
