The arming switch was first intended for avoiding executing scripts on yourself while writing payloads, but can be used if a script requires a physical state change.


Define pins used by switch
```
pin1 = board.GP1
pin2 = board.GP2
```

Configure pin behavior to read when switch bridges pin -> gnd
```
state1_pin = digitalio.DigitalInOut(pin1)
state1_pin.direction = digitalio.Direction.INPUT
state1_pin.pull = digitalio.Pull.UP

state2_pin = digitalio.DigitalInOut(pin2)
state2_pin.direction = digitalio.Direction.INPUT
state2_pin.pull = digitalio.Pull.UP
```

Loiter until armed
```
print(f"Waiting for switch to be in State 1 ({pin1} to GND)...")
while True:
    s1 = state1_pin.value
    s2 = state2_pin.value
    
    if not s1 and s2:
        print("Armed!! Executing script...")
        break
    
    # loop, waiting for switch to be flipped
    time.sleep(0.1)
```