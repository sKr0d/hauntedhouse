# https://github.com/sKr0d/hauntedhouse/blob/main/tank_monitor/code.py
import time
import board
import pwmio

from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

sensor_ground = DigitalInOut(board.A2) # Pin to ground on the sensor
sensor_ground.direction = Direction.OUTPUT
sensor_ground.value = False

sensor_enable = DigitalInOut(board.A1) # Pin to power on the sensor
sensor_enable.switch_to_output()
sensor_level = AnalogIn(board.A0) # Pin to read the sensor

pump_a1 = DigitalInOut(board.D10)
pump_a1.direction = Direction.OUTPUT
pump_a1.value = False

pump_a2 = DigitalInOut(board.D9)
pump_a2.direction = Direction.OUTPUT
pump_a2.value = False

fan_b1 = DigitalInOut(board.D7)
fan_b1.direction = Direction.OUTPUT
fan_b1.value = False

fan_b2 = DigitalInOut(board.D5)
fan_b2.direction = Direction.OUTPUT
fan_b2.value = False

button_fill = DigitalInOut(board.A5)
button_fill.direction = Direction.INPUT
button_fill.pull = Pull.UP

button_drain = DigitalInOut(board.A4)
button_drain.direction = Direction.INPUT
button_drain.pull = Pull.UP

button_stop = DigitalInOut(board.A3)
button_stop.direction = Direction.INPUT
button_stop.pull = Pull.UP

## set up pmw objects
pwmpump_a = pwmio.PWMOut(board.D11, frequency=40000, duty_cycle=0)
pwmfan_b = pwmio.PWMOut(board.D12, frequency=40000, duty_cycle=0)

#PWM_DUTY = 32768   # 50% duty cycle
#PWM_DUTY = 40960   # 62.5% duty cycle
#PWM_DUTY = 49152   # 75% duty cycle
#PWM_DUTY = 52428   # 80% duty cycle
PWM_DUTY = 65535    # 100%
FAN_DUTY = 52428    # 100%


## reading interval
INTERVAL = 5
clicks = time.time()
clicks2 = clicks + INTERVAL

## liquid Level
FULL = 28000

def fan_on():
    fan_b1.value = True
    fan_b2.value = False
    pwmfan_b.duty_cycle = FAN_DUTY

def fan_off():
    fan_b1.value = False
    fan_b2.value = False
    pwmfan_b.duty_cycle = 0

def pump_fill():
    pump_a1.value = True
    pump_a2.value = False
    pwmpump_a.duty_cycle = PWM_DUTY

def pump_drain():
    pump_a1.value = False
    pump_a2.value = True
    pwmpump_a.duty_cycle = PWM_DUTY
    fan_off()

def pump_off():
    pump_a1.value = False
    pump_a2.value = False
    pwmpump_a.duty_cycle = 0

def sensor_on():
    sensor_enable.value = True

def sensor_off():
    sensor_enable.value = False

def get_level():
    sensor_on()
    time.sleep(0.25) # Warm up time
    level = sensor_level.value
    print(int(level/10))
    sensor_off()
    return level

def fill_tank():
    print("    ==Automatically Filling Tank==")
    wlsv = get_level() # Water Level Sensor Value
    clicks = time.time()
    clicks2 = time.time() + 2
    while button_stop.value:
        pump_fill()
        clicks = time.time()
        if clicks >= clicks2:
            clicks2 = time.time() + 2
            wlsv = get_level()
            if wlsv >= FULL:
                pump_off()
                sensor_off()
                print("    ==Tank is Full==")
                return

    print("    ==Tank is Full==")
    pump_off()
    sensor_off()

def mdrain_tank():
    print("    ==Manually Draining Tank==")
    while button_stop.value == True:
        pump_drain()
    print("    ==Stop==")
    pump_off()

def mfill_tank():
    print("    ==Manually Filling Tank==")
    while button_stop.value == True:
        pump_fill()
    print("    ==Stop==")
    pump_off()

##
## START HERE
##
print("\nTank Monitor\n")
print("Sensor will take a reading every", INTERVAL, "seconds and will\nturn on the pump when the level dips below", FULL,"\n")

print("Turning on fan at", FAN_DUTY,"\n")
fan_on()
#time.sleep(2)
#fan_off()

while True:
    fan_on()

    # get time
    clicks = time.time()

    # see if INTERVAL has elapsed
    if clicks >= clicks2:
        clicks2 = clicks + INTERVAL
        water_level = get_level()
        if water_level < FULL:
            fill_tank()

    # read buttons
    if button_stop.value == False:
        print("STOP = Pressed")
        pump_off()
        time.sleep(0.5)
    if button_fill.value == False:
        print("FILL = Pressed")
        mfill_tank()
    if button_drain.value == False:
        print("DRAIN = Pressed")
        mdrain_tank()

    # button debounce
    time.sleep(0.02)

