import array, time
import uasyncio as asyncio
from Constants import Colors, MachineSetup
import LightStrip

class LedController:
    def __init__(self, observer):
        self.observer = observer
        #configuration
        self.state = 'test'
        self.firstLoop = True
        self.colors = (Colors.BLACK, Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.PURPLE, Colors.WHITE)
        self.lightStrips = []

        #Create LED lines based on configuration
        for config in MachineSetup.LINES:
            self.lightStrips.append(LightStrip.LightStrip(config))
        # register events
        self.observer.on('state', self.stateChange)
        self.observer.on('pixel', self.pixelPick)
        self.observer.on('setLight', self.setLight)

    def stateChange(self, state):
        print('Now running ' + state)
        self.state = state

    def pixelPick(self, strip, position, h, s, v):
        print('Strip: ', strip, ' Position: ', position, ' HSV: ', h, ' ', s, ' ', v)
        self.lightStrips[strip].setPixel(position, h, s, v)

    def setLight(self, state):
        if len(self.lightStrips) > state['strip'] and len(self.lightStrips[state['strip']].lights) > state['position']:
            target = self.lightStrips[state['strip']].lights[state['position']]
            target.setHSV(state['hue'], state['saturation'], state['value'])
            if state.has_key('hertz'):
                target.hertz = state['hertz']

    async def render(self):
        for strip in self.lightStrips:
            strip.render()
        await asyncio.sleep_ms(10)

    def fillColor(self, color):
        for strip in self.lightStrips:
            for light in strip.lights:
                light.setHSV(color[0], color[1], color[2])

    async def color_chase(self, color):
        for i in range(MachineSetup.LED_COUNT):
            self.pixels_set(i, color)
            await asyncio.sleep_ms(10)
            await self.pixels_show()
        await asyncio.sleep(0.2)
 
    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    async def rainbow_cycle(self):
        for j in range(255):
            for i in range(MachineSetup.LED_COUNT):
                rc_index = (i * 256 // MachineSetup.LED_COUNT) + j
                self.pixels_set(i, self.wheel(rc_index & 255))
            await self.pixels_show()

    async def fill(self):
        for color in self.colors:
            self.fillColor(color)
            await self.render()
            await asyncio.sleep(0.2)

    async def chase(self):
        for color in self.colors:
            await self.color_chase(color)

    async def rainbow(self):
        await self.rainbow_cycle()
        
    async def test(self):
        if self.firstLoop:
            print('Red Fill')
            self.fillColor(Colors.RED)
            self.firstLoop = False
        await self.render()
        await asyncio.sleep(1)

    async def run(self):
        self.exit = True
        while self.exit:
            if self.state == 'rainbow':
                await self.rainbow()
            elif self.state ==  'chase':
                await self.chase()
            elif self.state == 'fill':
                await self.fill()
            elif self.state == 'test':
                await self.test()