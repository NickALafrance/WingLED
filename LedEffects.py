import array, time
import uasyncio as asyncio
from Constants import Colors, MachineSetup
import LightStrip

class LedEffects:
    def __init__(self, observer):
        self.observer = observer
        #configuration
        self.firstLoop = True
        self.colors = (Colors.BLACK, Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.PURPLE, Colors.WHITE)
        self.lightStrips = []

        #Create LED lines based on configuration
        for config in MachineSetup.LINES:
            self.lightStrips.append(LightStrip.LightStrip(config))
        # register events
        self.observer.on('setLight', self.setLight)
        self.observer.on('fill', self.fill)
        self.observer.on('chase', self.chase)

    def setLight(self, state):
        if len(self.lightStrips) > state['strip'] and len(self.lightStrips[state['strip']].lights) > state['position']:
            target = self.lightStrips[state['strip']].lights[state['position']]
            target.setHSV(state.get('hue', 0), state.get('saturation', 1), state.get('value', 1))
            target.setStrategy(state.get('updateOptions', {}))

    def fill(self, opts):
        for strip in self.lightStrips:
            strip.fill(opts['colors'])

    def chase(self, opts):
        for strip in self.lightStrips:
            strip.chase(opts['colors'], opts['speed'])

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