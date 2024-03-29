import lib.colorsys.__init__ as colorsys
from Constants import MachineSetup
from models.updateStrategies.Factory import UpdateStrategyFactory
from lib.observable import Observer

class Light:
    def __init__(self, strip, position):
        self.strip = strip
        self.position = position
        self.brightness = 1

        self.hue = 0
        self.saturation = 1
        self.value = 1

        self.updateStrategy = UpdateStrategyFactory({}, self)
        Observer.on('strips/' + str(self.strip.position) + '/lights/' + str(self.position), self.light)

    def light(self, event):
        if event.isRead():
            event.modelData = self
        if event.isWrite():
            self.deserialize(event.requestData)

    #Progress the light one step using the update strategy
    def update(self, heartBeat):
        if self.updateStrategy.shouldUpdate(heartBeat):
            color = self.updateStrategy.getNextColor()
            self.setHSV(color[0], color[1], color[2])
        return
    #Get the color code for the LED strip
    def getRGB(self):
        rgb = colorsys.hsv_to_rgb(self.hue / 360, self.saturation, self.value, 1)
        return [
            int(rgb[0] * 255 * min(self.brightness, self.strip.brightness)),
            int(rgb[1] * 255 * min(self.brightness, self.strip.brightness)),
            int(rgb[2] * 255 * min(self.brightness, self.strip.brightness))
        ]

    def setHSV(self, h, s, v):
        self.hue = h
        self.saturation = s
        self.value = v

    @property
    def bpm(self):
        return MachineSetup.FREQUENCY / self.updateStrategy.updateFrequency

    #BPM must be a multiple of MachineSetup.FREQUENCY
    @bpm.setter
    def bpm(self, bpm):
        if bpm > MachineSetup.FREQUENCY or MachineSetup.FREQUENCY % bpm:
            raise Exception("Provided beat per minute is not a multiple of the machine frequency")
        self.updateStrategy.updateFrequency = int(MachineSetup.FREQUENCY / bpm)

    def setStrategy(self, options):
        del self.updateStrategy
        self.updateStrategy = UpdateStrategyFactory(options, self)

    def serialize(self):
        return {
            'hue': self.hue,
            'saturation': self.saturation,
            'value': self.value,
            'position': self.position,
            'strip': self.strip.position,
            'updateStrategy': self.updateStrategy.serialize()
        }

    def deserialize(self, serialization):
        self.hue = serialization['hue']
        self.saturation = serialization['saturation']
        self.value = serialization['value']
        self.setStrategy(serialization['updateStrategy'])
