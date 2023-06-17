from updateStrategies.Wheel import Wheel
from updateStrategies.Null import Null
from updateStrategies.Jump import Jump
from updateStrategies.Fade import Fade

strategies = {
    "Wheel": Wheel,
    "Null": Null,
    "Jump": Jump,
    "Fade": Fade
}

def UpdateStrategyFactory(options, light):
    return strategies[options.get('type', 'Null')](options, light)
