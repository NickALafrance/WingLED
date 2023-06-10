from Constants import MachineSetup

class UpdateStrategyInterface:
    def __init__(self, options, light):
        self.light = light
        self.options = options

    #Returns true if the light should update.  This will be based on the selected BPM.
    # We will update our time 10 times per second, so the max BPM is MachineSetup.FREQUENCY.  BPM must be a multiple of MachineSetup.FREQUENCY.
    def shouldUpdate(self, t):
        return not (t % self.light.updateFrequency)
    #Return next HSV for a light.
    def getNextColor(self):
        return [self.light.hue, self.light.saturation, self.light.value]
