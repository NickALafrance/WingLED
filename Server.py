import uasyncio as asyncio
import network
import time
import re
from Constants import Wifi, Logs
import lib.picoweb.__init__ as picoweb

class WebEvent:
    def __init__(self, requestData):
        self.requestData = requestData
        self.responseData = { "OK": True }

class Server:
    def __init__(self, observer):
        self.connectToWifi()
        self.observer = observer
        self.wifi = Wifi
        ROUTES = [
            ("/", self.index),
            ("/strips", self.strips),
            (re.compile("\/strips\/\d+"), self.strip),
            (re.compile("\/strips\/\d+\/lights"), self.stripLights),
            (re.compile("\/strips\/\d+\/lights/\d+"), self.stripLight),
            ("/lights", self.lights),
            (re.compile("\/lights\/\d+"), self.light),
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

    def html(self, state):
        # html code ...
     html = """
     <html>
     <head>
     <title>Pico W Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
     <link rel="icon" href="data:,">
     <style>
     html{font-family: Helvetica; display:inline-block; margin: 0px auto; textalign: center;}
     h1{color: #0F3376; padding: 2vh;}
     p{font-size: 1.5rem;}
     button{display: inline-block; background-color: #4286f4; border: none;borderradius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin:
    2px; cursor: pointer;}
     button2{background-color: #4286f4;}
     </style>
     </head>
     <body> <h1>Pico W Web Server</h1>
     <p>GPIO state: <strong>""" + state + """</strong></p>
     <p><a href="/?state=rainbow"><button class="button">rainbow</button></a></p>
     <p><a href="/?state=fill"><button class="button button2">fill</button></a></p>
     <p><a href="/?state=chase"><button class="button button2">chase</button></a></p>
     </body>
     </html>
     """
     return html

    def index(self, req, resp):
        req.parse_qs()
        yield from picoweb.start_response(resp)
        yield from resp.awrite(self.html('N/A'))

    def disconnect(self, req, resp):
        self.station.disconnect()
        event = WebEvent(req.form)
        self.observer.trigger('disconnect', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def strips(self, req, resp):
        yield from req.read_form_data()
        event = WebEvent(req.form)
        self.observer.trigger('strips', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def strip(self, req, resp):
        print(req.path, ' | ', req.method)
        yield from req.read_form_data()
        event = WebEvent(req.form)
        self.observer.trigger('strips', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def stripLights(self, req, resp):
        yield from req.read_form_data()
        event = WebEvent(req.form)
        self.observer.trigger('stripLights', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def stripLight(self, req, resp):
        yield from req.read_form_data()
        event = WebEvent(req.form)
        self.observer.trigger('stripLights', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def lights(self, req, resp):
        yield from req.read_form_data()
        event = WebEvent(req.form)
        self.observer.trigger('lights', event)
        yield from picoweb.jsonify(resp, event.responseData)

    def light(self, req, resp):
        yield from req.read_form_data()
        event = WebEvent(req.form)
        self.observer.trigger('lights', event)
        yield from picoweb.jsonify(resp, event.responseData)
