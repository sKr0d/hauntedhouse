#https://github.com/sKr0d/hauntedhouse/blob/main/marquee/main.py
import time
import board
import neopixel
import pwmio
from random import randrange

fill_wait = 1.00
rainbow_step = 2

def left_side(color):
    r,g,b = color
    print(f'left side')
    for i in range(0, 75):
        pixels[i] = (r, g, b)
    pixels.show()

def right_side(color):
    r,g,b = color
    print(f'right_side')
    for i in range(75, 150):
        pixels[i] = (r, g, b)
    pixels.show()

def chase_cw(color):
    r,g,b = color
    print(f'chase clockwise')
    for i in range (149, 1, -1):
        pixels[i] = (r, g, b)
        pixels.show()

def chase_ccw(color):
    r,g,b = color
    print(f'chase counterclockwise')
    for i in range (1, 150):
        pixels[i] = (r, g, b)
        pixels.show()

def alternate(color, color2):
    r,g,b = color
    r2,g2,b2 = color2
    print(f'alternate')
    for i in range (1, 150):
        if i % 2 == 0:
            pixels[i] = (r, g, b)
        else:
            pixels[i] = (r2, g2, b2)
    pixels.show()
    time.sleep(0.1)

    for i in range (1, 150):
        if i % 2 == 0:
            pixels[i] = (r2, g2, b2)
        else:
            pixels[i] = (r, g, b)
    pixels.show()
    time.sleep(0.1)

def flash(color,times):
    for i in range(times):
        print(f'flash')
        pixels.fill(BLACK)
        pixels.show()
        time.sleep(0.10)
        pixels.fill(color)
        pixels.show()
        time.sleep(0.10)

pixel_pin = board.D9
#led = pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)
#led.duty_cycle = 32768

# The number of NeoPixels
num_pixels = 150

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
)

ORANGE = (210, 80, 0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def rainbow_cycle(wait):
    for j in range(0, 255, rainbow_step):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

while True:
    flash(ORANGE,2)
    repeat = randrange(8)
    for i in range (repeat):
        print(f'rainbow cycle')
        rainbow_cycle(0.01)

    flash(PURPLE,2)
    repeat = randrange(8,40)
    for j in range (repeat):
        alternate(ORANGE,PURPLE)

