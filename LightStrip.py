import array, time
from machine import Pin
from Constants import Colors
from ws2812 import WS2812
import Light

class LightStrip:
    def __init__(self, config):
        self.brightness = config.BRIGHTNESS
        self.count = config.LED_COUNT
        self.ws = WS2812(Pin(config.DATA_PIN), config.LED_COUNT)
        # Display a pattern on the LEDs via an array of LED RGB values.
        self.lights = [(Light.Light()) for _ in range(config.LED_COUNT)]

    def render(self):
        dimmer_ar = array.array("I", [0 for _ in range(self.count)])
        for i,led in enumerate(self.lights):
            self.ws[i] = led.getRGB()
        self.ws.write()

    def setPixel(self, position, h, s, v):
        if (len(self.lights) > position):
            self.light[position].setHSV(h, s, v)
