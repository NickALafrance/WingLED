import uasyncio as asyncio
import network
import time
import re
from Constants import Wifi, Logs
import lib.picoweb.__init__ as picoweb

class Server:
    def __init__(self, observer):
        self.connectToWifi()
        self.observer = observer
        self.wifi = Wifi
        ROUTES = [
            ("/", self.index),
            ("/pixel", self.pixel)
        ]
        self.app = picoweb.WebApp('picoweb', ROUTES)

    def connectToWifi(self):
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(Wifi.SSID, Wifi.PASSWORD)

        while(not station.isconnected()):
            print('connecting...')
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
        state = req.form["state"]
        self.observer.trigger('state', state)
        yield from picoweb.start_response(resp)
        yield from resp.awrite(self.html(state))

    def pixel(self, req, resp):
        req.parse_qs()
        self.observer.trigger('pixel', req.form["position"], req.form["r"], req.form["g"], req.form["b"])
        yield from picoweb.start_response(resp)
        yield from resp.awrite(self.html('test'))