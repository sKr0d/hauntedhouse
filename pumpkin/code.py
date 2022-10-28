# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials NeoPixel RGBW example"""
import time
import board
import neopixel
import random

pixel_pin = board.A0
num_pixels = 21

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False, pixel_order=(1, 0, 2, 3))


def colorwheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3, 0)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3, 0)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


RED = (255, 0, 0, 0)
YELLOW = (255, 150, 0, 0)
GREEN = (0, 255, 0, 0)
CYAN = (0, 255, 255, 0)
BLUE = (0, 0, 255, 0)
PURPLE = (180, 0, 255, 0)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 0)

while True:
    ss = random.randint(2, 5)
    print(f'FLASH',ss)
    for i in range (ss):
        pixels.fill(WHITE)
        pixels.show()
        time.sleep(0.02)

        pixels.fill(BLACK)
        pixels.show()
        time.sleep(0.01)

    rr = random.randint(1, 5)
    print(f'RAINBOW', rr)
    for i in range (rr):
        rainbow_cycle(0.02)  # Increase the number to slow down the rainbow
