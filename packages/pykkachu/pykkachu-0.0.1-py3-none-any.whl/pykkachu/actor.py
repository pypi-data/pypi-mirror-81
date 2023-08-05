import functools
import logging
from pysm import StateMachine
from pykka import ThreadingActor
from pykkachu.dispatcher import Dispatcher


class Actor(ThreadingActor):
    def __init__(self):
        super().__init__()
        self.sm = StateMachine("sm")

    def on_receive(self, msg):
        event_type = type(msg)
        event_name = msg.name
        try:
            _dispatchers[_klass(self)].get(event_type, event_name, self.sm.state)(self, msg)
        except:
            raise Exception("function undispatchable: " + str(msg) + ", " + str(self.sm.state))


def on(event_type=None, event_name=None, state=None):
    def dec(func):
        trigger = (event_type, event_name, state)
        kls = _klass_func(func)
        if kls not in _dispatchers:
            _dispatchers[kls] = Dispatcher()

        _dispatchers[kls].add(func, event_type, event_name, state)

        @functools.wraps(func)
        def wrapper(*args):
            # TODO: Should be able to pass in log level
            logging.info(map(str, list(trigger)))
            return func(*args)

        return wrapper

    return dec


# TODO: Find another design pattern which lets me avoid this janky global hash and class lookups
_dispatchers = {}


def _klass(kls):
    return type(kls).__qualname__


def _klass_func(func):
    return ".".join(func.__qualname__.split('.')[:-1])
