from updateStrategies.UpdateStrategyInterface import UpdateStrategyInterface

# This strategy will fade the current color to the next color, making one step per BPM towards the next color.
# It uses four parameters, colors, function, stepCount, and clockwise
# COLORS should be an array of tuples, where each tuple is 1 integer between 0 and 360 for Hue, and 2 floats between 0 and 1 for Saturation and Value.
# The function is a string that should be one of the ways to fade from one color to the next.  The enumerations are as follows: 'linear', 'gaussian'
# The stepCount is how many steps should it take to fade from one color to the next.
# clockwise is a boolean and will represent which direction the fade is going along the color wheel for hue, and wether its increasing or decreaing between 0 and 1 for S and V
# Example of options ->
#{
#    type: "Fade",
#    colors: [
#        [0, 1, 1],   # RED
#        [120, 1, 1], # GREEN
#        [240, 1, 1]  # BLUE
#    ],
#    function: "linear", # OPTIONAL, defaults to linear
#    steps: 10, # OPTIONAL, defaults to 10
#    clockwise: true # OPTIONAL, defaults to True
#}

class Fade(UpdateStrategyInterface):
    def init(self):
        self.currentColor = self.options['colors'][0]
        self.stepAmount = 1 / self.options.get('steps', 10)
        self.step = 0
        self.targetColor = self.options['colors'][1]
        self.clockwise = self.options.get('clockwise', True)
        function = self.options.get('function', 'linear')
        self.isLinear = function == 'linear'
        self.isGaussian = function == 'gaussian'

    def getNextColor(self):
        if self.isLinear:
            return self.linear()
        if self.isGaussian:
            return self.gaussian()
        return self.linear()

    def linear(self):
        self.step = self.step + self.stepAmount
        currentHue = self.currentColor[0]
        targetHue = self.targetColor[0]
        hue = 0
        if self.clockwise:
            if currentHue > targetHue:
                targetHue += 360
            hue = (currentHue + (targetHue - currentHue) * self.step) % 360
        else:
            if currentHue < self.targetColor[0]:
                currentHue += 360
            hue = (currentHue - (currentHue - targetHue) * self.step) % 360

        saturation = self.currentColor[1] + ((self.currentColor[1] - self.targetColor[1]) * self.step)
        value = self.currentColor[2] + ((self.currentColor[2] - self.targetColor[2]) * self.step)

        if self.step == 1:
            self.step = 0
            self.currentColor = self.targetColor
            self.targetColor = self.options['colors'][1 + self.options['colors'].index(self.currentColor) % len(self.options['colors'])]
        return [hue, saturation, value]

    def gaussian(self):
        return[0, 1, 1]
