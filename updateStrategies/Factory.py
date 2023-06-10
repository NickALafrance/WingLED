from updateStrategies.Wheel import Wheel
from updateStrategies.Null import Null

strategies = {
    "Wheel": Wheel,
    "Null": Null
}

def UpdateStrategyFactory(options, light):
    return strategies[options.get('type', 'Null')](options, light)
