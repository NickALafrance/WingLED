from models.LedEffects import LedEffects
from controller.Server import Server
from lib.observable import Observer
from views import Views
import uasyncio as asyncio

Observer.reset()
Model = LedEffects()
Controller = Server()
View = Views()

def reset():
    loop = asyncio.get_event_loop()
    loop.stop()
    loop.close()

loop = asyncio.get_event_loop()
loop.create_task(Model.run())
Observer.on('reset', reset)
Controller.run()
