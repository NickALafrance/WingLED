from updateStrategies.UpdateStrategyInterface import UpdateStrategyInterface

class Null(UpdateStrategyInterface):
    def shouldUpdate(self, t):
        return False