import pyglet
import requests
from pyglet.window import key

from view import View

window = pyglet.window.Window(width=800, height=600)

view = View((30, 670, 80, 560))


@window.event
def on_draw():
    window.clear()
    view.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.RIGHT:
        set_action("move_right")
    elif symbol == key.LEFT:
        set_action("move_left")
    elif symbol == key.UP:
        set_action("move_up")
    elif symbol == key.DOWN:
        set_action("move_down")
    else:
        set_action("none")

    if symbol == key.R:
        requests.put("http://127.0.0.1:5000/api/reset")
    else:
        requests.post("http://127.0.0.1:5000/api/step")
    view.get_state()


def set_action(action):
    try:
        requests.put("http://127.0.0.1:5100/api/setmove", json=action)
    except requests.exceptions.ConnectionError:
        pass


view.get_state()
pyglet.app.run()
event_loop = pyglet.app.EventLoop()


@event_loop.event
def on_window_close(window):
    event_loop.exit()
