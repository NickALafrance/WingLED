from models.updateStrategies.Wheel import Wheel
from models.updateStrategies.Null import Null
from models.updateStrategies.Jump import Jump
from models.updateStrategies.Fade import Fade

strategies = {
    "Wheel": Wheel,
    "Null": Null,
    "Jump": Jump,
    "Fade": Fade
}

def UpdateStrategyFactory(options, light):
    return strategies[options.get('type', 'Null')](options, light)
