import pyglet
import requests
from pyglet.window import key

from view import View

FPS = 30

STEP_DURATION = 0.3

window = pyglet.window.Window(width=800, height=600)
event_loop = pyglet.app.EventLoop()

views = [View(step_duration=STEP_DURATION)]

# Uncomment to test multiple views
# views = [View((30, 770, 80, 260),step_duration=STEP_DURATION),
#          View((0, 400, 300, 600),step_duration=STEP_DURATION)]


@window.event
def on_draw():
    window.clear()
    for view in views:
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
    for view in views:
        view.get_state()


@event_loop.event
def on_window_close(window):
    event_loop.exit()


def set_action(action):
    try:
        requests.put("http://127.0.0.1:5100/api/setmove", json=action)
    except requests.exceptions.ConnectionError:
        pass


def animate(dt):
    for view in views:
        view.animate(dt)


if __name__ == "__main__":
    for view in views:
        view.get_state()
    pyglet.clock.schedule_interval(animate, 1/FPS)
    pyglet.app.run()
