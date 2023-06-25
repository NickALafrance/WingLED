from lib.observable import Observer
from views.index import index
from views.strips import strips, strip
from views.lights import light

class Views:
    def __init__(self):
        Observer.on('index', index)
        Observer.on('strips', strips)
        Observer.on('strip', strip)
        Observer.on('light', light)