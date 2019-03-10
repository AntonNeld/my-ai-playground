import pyglet
import requests
from pyglet.window import key

from view import View

FPS = 30

STEP_DURATION = 0.3
STEP_INTERVAL = 0.3

config = {"manual_mode": False, "auto_step": False}

window = pyglet.window.Window(width=800, height=600)
event_loop = pyglet.app.EventLoop()

session = requests.session()

views = [View(step_duration=STEP_DURATION, session=session)]

# Uncomment to test multiple views, currently of the same dungeon
# views = [View((30, 770, 80, 260),step_duration=STEP_DURATION),
#          View((0, 400, 300, 600),step_duration=STEP_DURATION)]


def print_help():
    help_string = """
    m: toggle manual mode
    r: reset dungeon
    h: print this help again
    space: step forward
    a: toggle auto-step

    If in manual mode (and the backend supports it):
        up: move up
        left: move left
        right: move right
        down: move down
        space: do nothing
    """
    print(help_string)


@window.event
def on_draw():
    window.clear()
    for view in views:
        view.draw()


@window.event
def on_key_press(symbol, modifiers):

    if symbol == key.M:
        config["manual_mode"] = not config["manual_mode"]
        print("Manual mode: " + str(config["manual_mode"]))
    elif symbol == key.R:
        reset()
    elif symbol == key.A:
        config["auto_step"] = not config["auto_step"]
        if config["auto_step"]:
            pyglet.clock.schedule_interval(step, STEP_INTERVAL)
        else:
            pyglet.clock.unschedule(step)
    elif symbol == key.H:
        print_help()
    if config["manual_mode"]:
        actions = {key.RIGHT: "move_right",
                   key.LEFT: "move_left",
                   key.UP: "move_up",
                   key.DOWN: "move_down",
                   key.SPACE: "none"}
        if symbol in actions:
            set_action(actions[symbol])
            step()
    elif symbol == key.SPACE:
        step()


@event_loop.event
def on_window_close(window):
    event_loop.exit()


def set_action(action):
    try:
        requests.put("http://127.0.0.1:5100/api/setmove", json=action)
    except requests.exceptions.ConnectionError:
        print("Cannot set next move. Is there a manual AI?")


def step(dt=None):
    session.post("http://127.0.0.1:5000/api/step")
    for view in views:
        view.get_state()


def reset():
    session.put("http://127.0.0.1:5000/api/reset")
    for view in views:
        view.get_state()


def animate(dt):
    for view in views:
        view.animate(dt)


if __name__ == "__main__":
    print_help()
    for view in views:
        view.get_state()
    pyglet.clock.schedule_interval(animate, 1/FPS)
    pyglet.app.run()
