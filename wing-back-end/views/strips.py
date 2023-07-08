from controller.WebEvent import WebEvent
from Constants import Wifi

def strips(event: WebEvent):
    if event.isRead():
        event.responseData.update({ "count": len(event.modelData) })
        strips = []
        for i, strip in enumerate(event.modelData):
            strips.append({ 'lights': strip.count, 'self': Wifi.baseURL() + 'strips/' + str(i) })
        event.responseData.update({ "strips": strips })

def strip(event: WebEvent):
    if event.isRead():
        event.responseData.update({ "count": event.modelData.count })
        lights = []
        for i, light in enumerate(event.modelData.lights):
            lights.append({ 'self': Wifi.baseURL() + 'strips/' + str(event.modelData.position) + '/lights/' + str(i) })
        event.responseData.update({ "lights": lights })
