import array, time
from machine import Pin
from Constants import Colors
from models.ws2812 import WS2812
from models.Light import Light
from lib.observable import Observer

class LightStrip:
    def __init__(self, config, position):
        self.position = position
        self.brightness = config.BRIGHTNESS
        self.count = config.LED_COUNT
        self.ws = WS2812(Pin(config.DATA_PIN), config.LED_COUNT)
        # Display a pattern on the LEDs via an array of LED RGB values.
        self.lights = [(Light(self, i)) for i in range(config.LED_COUNT)]
        Observer.on('strips/' + str(self.position), self.strip)
        Observer.on('strips/' + str(self.position) + '/lights', self.startEffect)

    def strip(self, event):
        if event.isRead():
            event.modelData = self
        if event.isWrite():
            if event.requestData["effect"] == 'fill':
                self.fill(event.requestData["updateStrategy"])
            elif event.requestData["effect"] == 'chase':
                self.chase(event.requestData["updateStrategy"])

    def update(self, heartBeat):
        for i,led in enumerate(self.lights):
            led.update(heartBeat)
            self.ws[i] = led.getRGB()

    def write(self):
        self.ws.write()
 
    def setPixel(self, position, h, s, v):
        if (len(self.lights) > position):
            self.light[position].setHSV(h, s, v)

    def startEffect(self, event):
        print('starting effect', event.getVerb(), ' with ', event.requestData)
        if event.getVerb() == 'rainbow':
            self.rainbow(event.requestData)
        elif event.getVerb() == 'fill':
            self.fill(event.requestData)
        elif event.getVerb() == 'chase':
            self.chase(event.requestData)

    def fill(self, options):
        for led in self.lights:
            led.setStrategy(options)

    def chase(self, options):
        for i,led in enumerate(self.lights):
            options.update({ "updateOffset": i * round(int(options["updateFrequency"]) / self.count) })
            led.setStrategy(options)

    def rainbow(self, options):
        def shift(seq, n):
            n = n % len(seq)
            return seq[n:] + seq[:n]

        for i,led in enumerate(self.lights):
            options = {
                'type': 'Fade',
                'steps': options['steps'],
                'updateFrequency': options['updateFrequency'],
                'colors': shift([Colors.RED, Colors.ORANGE, Colors.YELLOW, Colors.GREEN, Colors.BLUE, Colors.INDIGO, Colors.PURPLE], i)
            }
            led.setStrategy(options)
        return
