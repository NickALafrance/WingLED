import array, time
import uasyncio as asyncio
from machine import Pin
import rp2
from Constants import Colors, MachineSetup

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()

class LedController:
    # Configure the number of WS2812 LEDs.
    state = 'test'
    firstLoop = True

    def __init__(self, observer):
        self.observer = observer
        self.colors = (Colors.BLACK, Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.PURPLE, Colors.WHITE)
        # Create the StateMachine with the ws2812 program, outputting on pin
        self.sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(MachineSetup.DATA_PIN))
        # Start the StateMachine, it will wait for data on its FIFO.
        self.sm.active(1)
        # Display a pattern on the LEDs via an array of LED RGB values.
        self.ar = array.array("I", [0 for _ in range(MachineSetup.LED_COUNT)])
        # register events
        self.observer.on('state', self.stateChange);
        self.observer.on('pixel', self.pixelPick);

    def stateChange(self, state):
        print('Now running ' + state)
        self.state = state

    def pixelPick(self, position, r, g, b):
        color = (int(r), int(g), int(b))
        print(color)
        self.pixels_set(int(position), color)
        print('Setting pixel # ' + position + ' to RGB ', color)

    async def pixels_show(self):
        dimmer_ar = array.array("I", [0 for _ in range(MachineSetup.LED_COUNT)])
        for i,c in enumerate(self.ar):
            r = int(((c >> 8) & 0xFF) * MachineSetup.BRIGHTNESS)
            g = int(((c >> 16) & 0xFF) * MachineSetup.BRIGHTNESS)
            b = int((c & 0xFF) * MachineSetup.BRIGHTNESS)
            dimmer_ar[i] = (g<<16) + (r<<8) + b
        self.sm.put(dimmer_ar, 8)
        await asyncio.sleep_ms(10)

    def pixels_set(self, position, color):
        self.ar[position] = (color[1]<<16) + (color[0]<<8) + color[2]

    def pixels_fill(self, color):
        for i in range(len(self.ar)):
            self.pixels_set(i, color)

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
            self.pixels_fill(color)
            await self.pixels_show()
            await asyncio.sleep(0.2)

    async def chase(self):
        for color in self.colors:
            await self.color_chase(color)

    async def rainbow(self):
        await self.rainbow_cycle()
        
    async def test(self):
        if self.firstLoop:
            print('Red Fill')
            self.pixels_fill(Colors.RED)
            self.firstLoop = False
        await self.pixels_show()
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