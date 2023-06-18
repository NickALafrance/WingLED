from models.LedEffects import LedEffects
from controller.Server import Server
from lib.observable import Observer
from views import Views
import uasyncio as asyncio

Observer.reset()
Model = LedEffects()
Controller = Server()
View = Views()

async def main():
    asyncio.create_task(Model.run())
    Controller.run()
    while True:
        await asyncio.sleep(100)

asyncio.run(main())
