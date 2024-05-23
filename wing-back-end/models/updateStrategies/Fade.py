from models.updateStrategies.UpdateStrategyInterface import UpdateStrategyInterface

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
        self.currentColor = -1
        self.step = self.options.get('steps', 10) - 1
        
        self.steps = self.options.get('steps', 10)
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
        self.step = self.step + 1
        if self.step == self.steps:
            self.currentColor += 1
            self.step = 0
            return self.options['colors'][self.currentColor % len(self.options['colors'])]
        c1 = self.options['colors'][self.currentColor % len(self.options['colors'])]
        c2 = self.options['colors'][(self.currentColor + 1) % len(self.options['colors'])]
        percent = self.step / self.steps
        return [
            self.rotateColor(c1[0], c2[0], percent),
            self.approach(c1[1], c2[1], percent),
            self.approach(c1[2], c2[2], percent)
        ]

    def gaussian(self):
        return[0, 1, 1]
    
    def shouldStart(self, t):
        return t % (len(self.options['colors']) * self.updateFrequency * self.steps + self.updateOffset) == 0
    
    def approach(self, n1, n2, percent):
        if n1 == n2:
            return n1
        diff = abs(n1 - n2) * percent
        if n1 > n2:
            return n1 - diff
        return n1 + diff

    def rotateColor(self, n1, n2, percent):
        if n1 == n2:
            return n1
        if self.clockwise and n1 > n2:
            n2 += 360
        elif not self.clockwise and n1 < n2:
            n1 += 360
        if self.clockwise:
            diff = (n2 - n1) * percent
            return (n1 + diff) % 360
        diff = (n1 - n2) * percent
        return (n1 - diff) % 360

    def serialize(self):
        obj = super().serialize()
        obj.pop('step')
        obj.pop('currentColor')
        obj.pop('islinear')
        obj.pop('isGaussian')
        if (self.isLinear):
            obj.update({'function': 'linear'})
        if (self.isGaussian):
            obj.update({'function': 'gaussian'})
        obj.update({'colors': self.options['colors']})
        return obj