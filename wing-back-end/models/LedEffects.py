import array, time
import uasyncio as asyncio
from Constants import MachineSetup
from models.LightStrip import LightStrip
from lib.observable import Observer

class LedEffects:
    def __init__(self):
        #configuration
        self.firstLoop = True
        self.lightStrips = []

        #Create LED lines based on configuration
        for i, config in enumerate(MachineSetup.LINES):
            self.lightStrips.append(LightStrip(config, i))
        # register events
        Observer.on('strips', self.strips)
        Observer.on('reset', self.end)

    def strips(self, event):
        if event.isRead():
            event.modelData = self.lightStrips

    def end(self):
        self.exit = False

    def render(self, heartBeat):
        for strip in self.lightStrips:
            strip.update(heartBeat)
        for strip in self.lightStrips:
            strip.write()

    async def run(self):
        self.exit = True
        heartBeat = 0
        msPerLoop = (60000 / MachineSetup.FREQUENCY) / 1000

        while self.exit:
            start = time.time()
            self.render(heartBeat)
            heartBeat = (heartBeat + 1)
            end = time.time()
            await asyncio.sleep(msPerLoop - (end - start))