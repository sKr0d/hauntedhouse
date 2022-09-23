# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials: PWM with Fixed Frequency example."""
import time
import board
import pwmio
from digitalio import DigitalInOut, Direction, Pull

switch_up = DigitalInOut(board.D3)
switch_dn = DigitalInOut(board.D4)
switch_up.direction = Direction.INPUT
switch_up.pull = Pull.UP
switch_dn.direction = Direction.INPUT
switch_dn.pull = Pull.UP

fan = pwmio.PWMOut(board.D2, frequency=25000, duty_cycle=0)
#fan = pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)
fdc = 32768
fan_step = 1024

fan.duty_cycle = fdc

print('fan pwm project')
print('starting at', fdc)
print('')

while True:
    if switch_up.value:
        fdc = fdc
    else:
        fdc += fan_step
        if fdc >= 65535:
            fdc = 65535
        fan.duty_cycle = fdc
        print('>>',fdc)

    if switch_dn.value:
        fdc = fdc
    else:
        fdc -= fan_step
        if fdc <= 0:
            fdc = 0
        fan.duty_cycle = fdc
        print('<<', fdc)
    time.sleep(0.05)


'''
    for i in range(100):
        # PWM LED up and down
        if i < 50:
            ldc = int(i * 2 * 65535 / 100)
            led.duty_cycle = ldc
        else:
            ldc = 65535 - int((i - 50) * 2 * 65535 / 100)
            led.duty_cycle = ldc
        time.sleep(0.01)
'''
