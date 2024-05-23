from models.updateStrategies.UpdateStrategyInterface import UpdateStrategyInterface

# This strategy will JUMP the color of a light with the next color every update cycle.
# It uses ONE option, which is COLORS.
# COLORS should be an array of tuples, where each tuple is 1 integer between 0 and 360 for Hue, and 2 floats between 0 and 1 for Saturation and Value.
# Example of options ->
# {
#     type: "Jump",
#     colors: [
#         [0, 1, 1],   # RED
#         [120, 1, 1], # GREEN
#         [240, 1, 1]  # BLUE
#     ]
# }
class Jump(UpdateStrategyInterface):
    def init(self):
        self.currentColor = 0

    def getNextColor(self):
            color = self.options['colors'][self.currentColor % len(self.options['colors'])]
            self.currentColor += 1
            return color
    def shouldStart(self, t):
        return t % (len(self.options['colors']) * self.updateFrequency + self.updateOffset) == 0
    def serialize(self):
        obj = super().serialize()
        obj.pop('currentColor')
        obj.update({'colors': self.options['colors']})
        return obj