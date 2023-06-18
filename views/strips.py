from controller.WebEvent import WebEvent
from Constants import Wifi

def strips(event: WebEvent):
    if event.isRead():
        event.responseData.update({ "count": len(event.modelData) })
        strips = []
        for i, strip in enumerate(event.modelData):
            strips.append({ 'lights': strip.count, 'self': Wifi.baseURL() + 'strips/' + str(i) })
        event.responseData.update({ "strips": strips })
