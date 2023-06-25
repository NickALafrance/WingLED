from models.updateStrategies.UpdateStrategyInterface import UpdateStrategyInterface

class Null(UpdateStrategyInterface):
    def init(self):
        self.first = True
    def shouldUpdate(self, t):
        if (self.first):
            self.first = False
            return True
        return False
