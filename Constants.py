import lib.ulogging.ulogging as ulogging

class ColorConstants:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 150, 0)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    BLUE = (0, 0, 255)
    PURPLE = (180, 0, 255)
    WHITE = (255, 255, 255)

class WifiConstants:
    SSID = 'Firedactyle'
    PASSWORD = 'Amethyst0508'
    HOST = '192.168.1.222'
    PORT = 80
    TIMEOUT = 20

class MachineSetupConstants:
    DATA_PIN = 22
    LED_COUNT = 45
    BRIGHTNESS = 0.2
    LINES = (
        { DATA_PIN: 18, LED_COUNT: 45, BRIGHTNESS: 0.2 },
        { DATA_PIN: 19, LED_COUNT: 23, BRIGHTNESS: 0.2 },
        { DATA_PIN: 20, LED_COUNT: 20, BRIGHTNESS: 0.2 },
        { DATA_PIN: 21, LED_COUNT: 18, BRIGHTNESS: 0.2 },
    )

class LogsConstants:
    WEBLOG = ulogging.getLogger('picoweb')

Colors = ColorConstants()
Wifi = WifiConstants()
MachineSetup = MachineSetupConstants()
Logs = LogsConstants()