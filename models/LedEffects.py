import array, time
import uasyncio as asyncio
from Constants import Colors, MachineSetup
from models.LightStrip import LightStrip
from lib.observable import Observer

class LedEffects:
    def __init__(self):
        #configuration
        self.firstLoop = True
        self.colors = (Colors.BLACK, Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.PURPLE, Colors.WHITE)
        self.lightStrips = []

        #Create LED lines based on configuration
        for i, config in enumerate(MachineSetup.LINES):
            self.lightStrips.append(LightStrip(config, i))
        # register events
        Observer.on('strips', self.strips)

    def strips(self, event):
        if event.isRead():
            event.modelData = self.lightStrips

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