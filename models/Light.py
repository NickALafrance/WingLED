import lib.colorsys.__init__ as colorsys
from Constants import MachineSetup
from models.updateStrategies.Factory import UpdateStrategyFactory

class Light:
    def __init__(self, position):
        self.position = position
        self.brightness = 1

        self.hue = 0
        self.saturation = 1
        self.value = 1

        self.updateStrategy = UpdateStrategyFactory({}, self)

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
            int(rgb[0] * 255 * self.brightness),
            int(rgb[1] * 255 * self.brightness),
            int(rgb[2] * 255 * self.brightness)
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
