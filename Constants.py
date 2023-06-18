import lib.ulogging.ulogging as ulogging

class ColorConstants:
    BLACK = (0, 0, 0)
    RED = (0, 1, 1)
    YELLOW = (60, 1, 1)
    GREEN = (120, 1, 1)
    CYAN = (180, 1, 1)
    BLUE = (240, 1, 1)
    PURPLE = (300, 1, 1)
    WHITE = (0, 0, 1)

class WifiConstants:
    def __init__(self):
        self.SSID = 'Firedactyle'
        self.PASSWORD = 'Amethyst0508'
        self.HOST = '192.168.1.222'
        self.PORT = 80
        self.TIMEOUT = 20

    def baseURL(self):
        return self.HOST + ':' + str(self.PORT) + '/'
    
class Line:
    def __init__(self, pin, count, brightness):
        self.DATA_PIN = pin
        self.LED_COUNT = count
        self.BRIGHTNESS = brightness

class MachineSetupConstants:
    FREQUENCY = 600
    def __init__(self):                
        self.LINES = [
            Line(18, 8, 0.25)
        ]

class LogsConstants:
    WEBLOG = ulogging.getLogger('picoweb')

Colors = ColorConstants()
Wifi = WifiConstants()
MachineSetup = MachineSetupConstants()
Logs = LogsConstants()