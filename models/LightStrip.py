import array, time
from machine import Pin
from Constants import Colors
from models.ws2812 import WS2812
from models.Light import Light

class LightStrip:
    def __init__(self, config):
        self.brightness = config.BRIGHTNESS
        self.count = config.LED_COUNT
        self.ws = WS2812(Pin(config.DATA_PIN), config.LED_COUNT)
        # Display a pattern on the LEDs via an array of LED RGB values.
        self.lights = [(Light(i)) for i in range(config.LED_COUNT)]

    def update(self, heartBeat):
        dimmer_ar = array.array("I", [0 for _ in range(self.count)])
        for i,led in enumerate(self.lights):
            led.update(heartBeat)
            self.ws[i] = led.getRGB()

    def write(self):
        self.ws.write()

    def setPixel(self, position, h, s, v):
        if (len(self.lights) > position):
            self.light[position].setHSV(h, s, v)

    def fill(self, colors):
        options = {
            "colors": colors,
            "type": "Jump"
        }
        for led in self.lights:
            led.setStrategy(options)

    def chase(self, colors, speed):
        for i,led in enumerate(self.lights):
            options = {
                "colors": colors,
                "type": "Jump",
                "updateFrequency": speed,
                "updateOffset": i * int(speed / self.count)
            }
            led.setStrategy(options)
