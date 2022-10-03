# https://github.com/sKr0d/hauntedhouse/blob/main/tank_monitor/code.py
import time
import board
import pwmio

from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

sensor_enable = DigitalInOut(board.D3) # Pin to power on the sensor
sensor_enable.switch_to_output()
sensor_level = AnalogIn(board.A0) # Pin to read the sensor

pump = DigitalInOut(board.D4)  # Pin to control the pump
pump.direction = Direction.OUTPUT
pump.value = False # start with the pump turned off

## reading interval
INTERVAL = 30

## liquid Level
FULL = 25000

def pump_on():
    print("pump on, ", end = '')
    pump.value = True

def pump_off():
    print("pump off")
    pump.value = False

def sensor_on():
    print("sensor on, ", end = '')
    sensor_enable.value = True

def sensor_off():
    print("sensor off")
    sensor_enable.value = False

def get_level():
    sensor_on()
    time.sleep(0.25) # Warm up time
    #print("reading = ", end = '')
    level = sensor_level.value
    print(level, ", ", end = '')
    sensor_off()
    return level

def fill_tank():
    print("    ==Filling Tank==")
    wlsv = get_level() # Water Level Sensor Value
    while wlsv < FULL:
        pump_on()
        time.sleep(01.00) # Pump for a second before checking the level
        wlsv = get_level()

    print("    ==Tank is Full==")
    pump_off()
    sensor_off()

##
## START HERE
##
print("\nTank Monitor\n")
print("Sensor will take a reading every", INTERVAL, "seconds and will\nturn on the pump when the level dips below", FULL,"\n")

while True:
    water_level = get_level()
    if water_level < FULL:
        fill_tank()
    print("    ==sleep== ", INTERVAL)
    time.sleep(INTERVAL)

