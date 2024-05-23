from Constants import MachineSetup

# STRATEGY PATTERN INTERFACE for controlling lights.
# There are some default settings all light types can use.  they include updateOffset and updateFrequency
# updateFrequency dictates how many heart beats should elapse before triggering a color update.  There are MachineSetup.FREQUENCY heart beats per minute.
# updateOffset will allow a user to control which heart beat the color should update on, allowing for colors with the same frequency to update at different moments.
# Example of options ->
# {
#     type: "???", # Must be a string that matches one of the specific strategies, either Jump or Fade
#     # Other options, depending on the strategy
#     updateFrequency: 10
#     updateOffset: 0
# }
class UpdateStrategyInterface:
    def __init__(self, options, light):
        self.light = light
        self.options = options
        self.updateFrequency = options.get('updateFrequency', 10)
        self.updateOffset = options.get('updateOffset', 0)
        self.type = options.get('type', 'Null')
        self.first = True
        self.init()
    # sub classes can init too
    def init(self):
        return
    #Returns true if our light should start.  This will recieve the current heart beat and
    #should use the total run time of the effect to start on a heartbeat number that modulous 0.
    #This will allow for synchronization of lights as new commands flow in, though it may slow down update speeds
    # since the light will stop updating until the next 'first' moment for it to start begins.
    #By default we start instantly.
    def shouldStart(self, t):
        return True

    #Returns true if the light should update.  This will be based on the selected BPM.
    # We will update our time 10 times per second, so the max BPM is MachineSetup.FREQUENCY.  BPM must be a multiple of MachineSetup.FREQUENCY.
    def shouldUpdate(self, t):
        if self.first == True:
            if not self.shouldStart(t):
                return False
            self.first = False
            return True
        return not ((t + self.updateOffset) % self.updateFrequency)
    #Return next HSV for a light.
    def getNextColor(self):
        return [self.light.hue, self.light.saturation, self.light.value]
    def serialize(self):
        v = self.__dict__
        updateStrategy = {}
        for key in v:
            updateStrategy.update({ key: v[key] })
        updateStrategy.pop('light')
        updateStrategy.pop('options')
        updateStrategy.pop('first')
        return updateStrategy
