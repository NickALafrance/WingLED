from models.updateStrategies.UpdateStrategyInterface import UpdateStrategyInterface

class Null(UpdateStrategyInterface):
    def init(self):
        self.color = self.options.get('color', (self.light.hue, self.light.saturation, self.light.value))
        self.first = True
    def shouldUpdate(self, t):
        if (self.first):
            self.first = False
            return True
        return False

    def getNextColor(self):
        return self.color