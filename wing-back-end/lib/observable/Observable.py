class HandlerNotFound(Exception):
    """Raised if a handler wasn't found"""

    def __init__(self, event: str, handler) -> None:
        super().__init__()
        self.event = event
        self.handler = handler

    def __str__(self) -> str:
        return "Handler {} wasn't found for event {}".format(self.handler, self.event)


class EventNotFound(Exception):
    """Raised if an event wasn't found"""

    def __init__(self, event: str) -> None:
        super().__init__()
        self.event = event

    def __str__(self) -> str:
        return "Event {} wasn't found".format(self.event)


class Observable:
    """Event system for python"""

    def __init__(self) -> None:
        self._events = {}

    def get_all_handlers(self):
        """Returns a dict with event names as keys and lists of
        registered handlers as values."""

        events = {}
        for event, handlers in self._events.items():
            events[event] = handlers
        return events

    def get_handlers(self, event: str):
        """Returns a list of handlers registered for the given event."""
        return self._events[event]

    def is_registered(self, event: str, handler) -> bool:
        """Returns whether the given handler is registered for the
        given event."""
        return handler in self._events[event]

    def on(self, event: str, *handler):
        """Registers one or more handlers to a specified event.
        This method may as well be used as a decorator for the handler."""
        if event not in self._events:
            self._events[event] = []

        def _on_wrapper(*handler):
            """wrapper for on decorator"""
            self._events[event].append(handler[0])
            return handler

        if handler:
            return _on_wrapper(*handler)
        return _on_wrapper

    def off(self, event: str = None, *handler) -> None:
        """Unregisters a whole event (if no handlers are given) or one
        or more handlers from an event.
        Raises EventNotFound when the given event isn't registered.
        Raises HandlerNotFound when a given handler isn't registered."""

        if not event:
            self._events = {}
            return

        if event not in self._events:
            raise EventNotFound(event)

        if not handler:
            self._events.pop(event)
            return

        if handler not in self._events[event]:
            raise HandlerNotFound(event, handler)
        while handler in self._events[event]:
            self._events[event].remove(handler)
        return

    def trigger(self, event: str, *args, **kw) -> bool:
        """Triggers all handlers which are subscribed to an event.
        Returns True when there were callbacks to execute, False otherwise."""

        callbacks = self._events.get(event, False)
        if not callbacks:
            return False

        for callback in callbacks:
            print(callback)
            callback(*args, **kw)
        return True
    
    def reset(self):
        self.trigger('reset', 'Resetting')
        self._events = {}