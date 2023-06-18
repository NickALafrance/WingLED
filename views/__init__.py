from lib.observable import Observer
from views.index import index
from views.strips import strips

class Views:
    def __init__(self):
        Observer.on('index', index)
        Observer.on('strips', strips)