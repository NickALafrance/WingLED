import LedEffects
import Server
import Observable
import uasyncio as asyncio

Observer = Observable.Observable()
Controller = LedEffects.LedEffects(Observer)
Serv = Server.Server(Observer)

async def main():
    asyncio.create_task(Controller.run())
    Serv.run()
    while True:
        await asyncio.sleep(100)

asyncio.run(main())
