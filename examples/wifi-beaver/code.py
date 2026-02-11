import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import board
import busio
import time

# Setup UART on pins GP8 (TX) and GP9 (RX) - physical pins 11 & 12
uart = busio.UART(board.GP8, board.GP9, baudrate=115200, timeout=0.1)

# Setup USB HID Keyboard
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

def process_command(cmd):
    """Process a command received from ESP8266"""
    cmd = cmd.strip()
    
    if cmd.startswith("TYPE:"):
        text = cmd[5:]
        type_text(text)
    
    elif cmd.startswith("KEY:"):
        key = cmd[4:]
        press_key(key)
    
    elif cmd.startswith("COMBO:"):
        combo = cmd[6:]
        press_combo(combo)
    
    elif cmd.startswith("DELAY:"):
        delay_ms = int(cmd[6:])
        time.sleep(delay_ms / 1000.0)

def type_text(text):
    """Type out a string of text"""
    layout.write(text)

def press_key(key):
    """Press a single key"""
    keycode = get_keycode(key)
    if keycode:
        kbd.press(keycode)
        time.sleep(0.05)
        kbd.release(keycode)

def press_combo(combo):
    """Press a key combination like CTRL+ALT+DEL or GUI+R"""
    modifiers = []
    
    # Parse modifiers
    if "CTRL" in combo:
        modifiers.append(Keycode.CONTROL)
    if "ALT" in combo:
        modifiers.append(Keycode.ALT)
    if "SHIFT" in combo:
        modifiers.append(Keycode.SHIFT)
    if "GUI" in combo or "WIN" in combo:
        modifiers.append(Keycode.GUI)
    
    # Get the final key
    last_plus = combo.rfind('+')
    if last_plus >= 0:
        final_key = combo[last_plus + 1:].strip()
        keycode = get_keycode(final_key)
        
        if keycode:
            # Press all modifiers
            for mod in modifiers:
                kbd.press(mod)
            
            # Press the main key
            kbd.press(keycode)
            time.sleep(0.05)
            
            # Release everything
            kbd.release(keycode)
            for mod in modifiers:
                kbd.release(mod)

def get_keycode(key):
    """Convert a key name to a Keycode"""
    key = key.upper().strip()
    
    # Special keys
    key_map = {
        "ENTER": Keycode.ENTER,
        "ESC": Keycode.ESCAPE,
        "TAB": Keycode.TAB,
        "SPACE": Keycode.SPACE,
        "DEL": Keycode.DELETE,
        "DELETE": Keycode.DELETE,
        "BACKSPACE": Keycode.BACKSPACE,
        "UP": Keycode.UP_ARROW,
        "DOWN": Keycode.DOWN_ARROW,
        "LEFT": Keycode.LEFT_ARROW,
        "RIGHT": Keycode.RIGHT_ARROW,
        "HOME": Keycode.HOME,
        "END": Keycode.END,
        "PAGEUP": Keycode.PAGE_UP,
        "PAGEDOWN": Keycode.PAGE_DOWN,
        
        # Function keys
        "F1": Keycode.F1,
        "F2": Keycode.F2,
        "F3": Keycode.F3,
        "F4": Keycode.F4,
        "F5": Keycode.F5,
        "F6": Keycode.F6,
        "F7": Keycode.F7,
        "F8": Keycode.F8,
        "F9": Keycode.F9,
        "F10": Keycode.F10,
        "F11": Keycode.F11,
        "F12": Keycode.F12,
    }
    
    # Check special keys first
    if key in key_map:
        return key_map[key]
    
    # Single letter keys
    if len(key) == 1:
        if key >= 'A' and key <= 'Z':
            return getattr(Keycode, key)
        if key >= '0' and key <= '9':
            key_digit_map = {
                '0': Keycode.ZERO, '1': Keycode.ONE, '2': Keycode.TWO,
                '3': Keycode.THREE, '4': Keycode.FOUR, '5': Keycode.FIVE,
                '6': Keycode.SIX, '7': Keycode.SEVEN, '8': Keycode.EIGHT,
                '9': Keycode.NINE
            }
            return key_digit_map.get(key)
    
    return None

# Main loop
print("USB Rubber Ducky Ready")
buffer = ""

while True:
    # Read from UART
    if uart.in_waiting > 0:
        data = uart.read(uart.in_waiting)
        if data:
            try:
                text = data.decode('utf-8')
                buffer += text
                
                # Process complete lines
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        print(f"Received: {line.strip()}")
                        process_command(line)
            except:
                pass  # Ignore decoding errors
    
    time.sleep(0.01)
