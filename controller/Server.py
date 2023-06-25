import uasyncio as asyncio
import network
import time
import re
from Constants import Wifi, Logs
import lib.picoweb.__init__ as picoweb
from lib.observable import Observer
from controller.WebEvent import WebEvent

class Server:
    def __init__(self):
        self.connectToWifi()
        self.wifi = Wifi
        ROUTES = [
            ("/", self.index),
            ("/strips", self.strips),
            (re.compile("\/strips\/\d+\/?$"), self.strip),
            (re.compile("\/strips\/\d+\/lights\/?$"), self.stripLights),
            (re.compile("\/strips\/\d+\/lights\/\d+\/?$"), self.stripLight),
            ("/lights", self.lights),
            (re.compile("\/lights\/\d+\/?$"), self.light),
            ("/disconnect", self.disconnect)
        ]
        self.app = picoweb.WebApp('picoweb', ROUTES)

    def connectToWifi(self):
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(Wifi.SSID, Wifi.PASSWORD)

        while(not station.isconnected()):
            print('connecting to ' + Wifi.SSID + '...')
            time.sleep(2)
        print(station.ifconfig())

    def run(self):
        self.app.run(
            host=Wifi.HOST,
            port=Wifi.PORT,
            debug=True,
            log=Logs.WEBLOG
        )

    def makeEvent(self, req):
        if req.method != 'GET':
            yield from req.read_form_data()
        else:
            req.parse_qs()
        return WebEvent(req)

    def index(self, req, resp):
        event = WebEvent(req)
        Observer.trigger('index', event)
        yield from picoweb.start_response(resp)
        yield from resp.awrite(event.responseData)

    def disconnect(self, req, resp):
        self.station.disconnect()
        event = WebEvent(req)
        Observer.trigger('disconnect', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def strips(self, req, resp):
        event = yield from self.makeEvent(req)
        Observer.trigger('strips', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def strip(self, req, resp):
        event = yield from self.makeEvent(req)
        Observer.trigger('strips/' + str(event.getIdFromPath()), event)
        Observer.trigger('strip', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def stripLights(self, req, resp):
        event = yield from self.makeEvent(req)
        Observer.trigger('strips/' + str(event.getIdFromPath()), event)
        Observer.trigger('strip', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def stripLight(self, req, resp):
        event = yield from self.makeEvent(req)
        Observer.trigger('strips/' + str(event.getIdFromPath()) + '/lights/' + str(event.getSecondIdFromPath()), event)
        Observer.trigger('light', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def lights(self, req, resp):
        event = yield from self.makeEvent(req)
        Observer.trigger('lights', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def light(self, req, resp):
        event = yield from self.makeEvent(req)
        Observer.trigger('lights', event)
        yield from picoweb.jsonify(resp, event.responseData)
