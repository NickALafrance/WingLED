from controller.WebEvent import WebEvent
from Constants import Wifi

def strips(event: WebEvent):
    if event.isRead():
        event.responseData.update({ "count": len(event.modelData) })
        strips = []
        for i, strip in enumerate(event.modelData):
            strips.append({ 'lights': strip.count, 'self': Wifi.baseURL() + 'strips/' + str(i) })
        event.responseData.update({ "strips": strips })
    if event.isOptions():
        event.headers.update({ 'Access-Control-Allow-Methods': 'PUT, POST' });

def strip(event: WebEvent):
    if event.isRead():
        event.responseData.update({ "count": event.modelData.count })
        event.responseData.update({ "position": event.modelData.position })
        lights = []
        for i, light in enumerate(event.modelData.lights):
            lights.append({ 'self': Wifi.baseURL() + 'strips/' + str(event.modelData.position) + '/lights/' + str(i) })
        event.responseData.update({ "lights": lights })
    if event.isOptions():
        event.headers.update({ 'Access-Control-Allow-Methods': 'PUT, POST' });
