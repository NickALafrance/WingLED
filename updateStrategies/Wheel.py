from updateStrategies.UpdateStrategyInterface import UpdateStrategyInterface

# This strategy will FILL the light with the next color every update cycle.
# It uses ONE option, which is COLORS.
# COLORS should be an array of tuples, where each tuple is 1 integer between 0 and 360 for Hue, and 2 floats between 0 and 1 for Saturation and Value.
# Example of options ->
# {
#     type: "Wheel",
#     colors: [
#         [0, 1, 1],   # RED
#         [120, 1, 1], # GREEN
#         [240, 1, 1]  # BLUE
#     ]
# }
class Wheel(UpdateStrategyInterface):
    def getNextColor(self):
        try:
            color = self.options['colors'][1 + self.options['colors'].index([self.light.hue, self.light.saturation, self.light.value]) % len(self.options['colors'])]
            return color
        except:
            return self.options['colors'][0]
