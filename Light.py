import lib.colorsys.__init__ as colorsys

class Light:
    def __init__(self):
        self.nextLight = None
        self.previousLight = None
        
        self.brightness = 1
        self.colorSpace = None
        
        self.hertz = 1
        
        self.hue = 0
        self.saturation = 1
        self.value = 1
        
        updateStrategy = None
        return

    #Progress the light one step using the update strategy
    def update(self):
        return
    #Get the color code for the LED strip
    def getRGB(self):
        rgb = colorsys.hsv_to_rgb(self.hue, self.saturation, self.value, 1)
        return [
            int(rgb[0] * 255 * self.brightness),
            int(rgb[1] * 255 * self.brightness),
            int(rgb[2] * 255 * self.brightness)
        ]

    def setHSV(self, h, s, v):
        self.hue = h / 360
        self.saturation = s
        self.value = v