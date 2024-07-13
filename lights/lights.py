import time
import board
import neopixel

# Constants
PIXEL_PIN = board.D7
PIXEL_COUNT = 90
BRIGHTNESS = 0.4  # Adjust as needed (0-1)

# Create the NeoPixel strip
strip = neopixel.NeoPixel(PIXEL_PIN, PIXEL_COUNT, brightness=BRIGHTNESS, auto_write=False)

# Global variables
mode = 0

def setup():
    print("Light strip patterns")
    strip.fill((0, 0, 0))  # Set all pixels to 'off'
    strip.show()

def read_input():
    # Simulated digital read (replace with actual GPIO read if using Raspberry Pi)
    digit_first = 0  # Replace with GPIO.input(13) if using RPi
    digit_second = 0  # Replace with GPIO.input(12)
    digit_third = 0  # Replace with GPIO.input(11)
    digit_fourth = 0  # Replace with GPIO.input(10)

    print(f"Left to Right: {digit_fourth} {digit_third} {digit_second} {digit_first}")
    return (digit_fourth * 8 + digit_third * 4 + digit_second * 2 + digit_first)

def color_wipe(color, wait):
    for i in range(PIXEL_COUNT):
        strip[i] = color
        strip.show()
        time.sleep(wait / 1000.0)

def rainbow(wait):
    for first_pixel_hue in range(0, 2 * 65536, 256):
        # Simulate the rainbow function
        for i in range(PIXEL_COUNT):
            hue = (first_pixel_hue + (i * 65536 // PIXEL_COUNT)) % 65536
            strip[i] = neopixel.hsv_to_rgb(hue / 65536, 1, 1)
        strip.show()
        time.sleep(wait / 1000.0)

def theater_chase(color, wait):
    for _ in range(5):
        for b in range(3):
            strip.fill((0, 0, 0))
            for c in range(b, PIXEL_COUNT, 3):
                strip[c] = color
            strip.show()
            time.sleep(wait / 1000.0)

def comet_chase(hsv_color, tail_len, delay_time):
    dim_factor = 255 // tail_len
    for i in range(PIXEL_COUNT):
        for j in range(tail_len + 1):
            curr_pixel = i - j
            brightness = max(0, 255 - (j * dim_factor)) if j < tail_len else 0
            if curr_pixel >= 0:
                rgbcolor = neopixel.gamma32(neopixel.hsv_to_rgb(hsv_color / 65536, 1, brightness / 255))
                strip[curr_pixel] = rgbcolor
        strip.show()
        time.sleep(delay_time / 1000.0)
    strip.fill((0, 0, 0))
    strip.show()

def breathe(hue, saturation, value):
    for i in range(255):
        strip.fill(neopixel.gamma32(neopixel.hsv_to_rgb(hue / 65536, saturation / 255, i / 255)))
        strip.show()
        time.sleep(0.01)
    for i in range(255, -1, -1):
        strip.fill(neopixel.gamma32(neopixel.hsv_to_rgb(hue / 65536, saturation / 255, i / 255)))
        strip.show()
        time.sleep(0.01)

def loop():
    global mode
    while True:
        print("\n********* Start of Loop ****************************")
        mode = read_input()
        print(f"New mode: {mode}")

        if mode == 0:
            color_wipe((0, 255, 0), 70)
            print("I'm over here-")
        elif mode == 1:
            comet_chase(0x1F7F, 35, 5)  # Adjust color as needed
        elif mode == 2:
            rainbow(0)
        elif mode == 3:
            theater_chase((255, 255, 255), 50)
            time.sleep(0.1)
        elif mode == 4:
            strip.fill((0, 255, 0))
            strip.show()
            time.sleep(0.1)
        elif mode == 5:
            strip.fill((255, 0, 0))
            strip.show()
            time.sleep(0.1)
        elif mode == 6:
            strip.fill((0, 0, 255))
            strip.show()
            time.sleep(0.1)
        elif mode == 7:
            comet_chase(0xCF0F, 20, 50)  # Adjust color as needed
        elif mode == 8:
            strip.fill((255, 255, 255))
            strip.show()
            breathe(0, 100, 100)  # Adjust hue/saturation/value
        else:
            theater_chase((200, 1, 160), 50)

# Run the setup and loop
setup()
loop()