from view import View
from pyglet.window import key
import timeit
import requests
import pyglet
import json


FPS = 30

STEP_DURATION = 0.3
STEP_INTERVAL = 0.3

config = {"manual_mode": False, "auto_step": False}

window = pyglet.window.Window(width=800, height=600)
event_loop = pyglet.app.EventLoop()

session = requests.session()

views = [View(step_duration=STEP_DURATION)]

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
    t: do 150 steps and measure average time

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
        new_room()
    elif symbol == key.A:
        config["auto_step"] = not config["auto_step"]
        if config["auto_step"]:
            pyglet.clock.schedule_interval(step, STEP_INTERVAL)
        else:
            pyglet.clock.unschedule(step)
    elif symbol == key.H:
        print_help()
    elif symbol == key.T:
        number = 150
        print("Measuring average step time...")
        print(timeit.timeit(step, number=number)/number)
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


def get_state():
    view_response = session.get("http://127.0.0.1:5000/api/view?room=tmp")
    score_response = session.get("http://127.0.0.1:5000/api/score?room=tmp")
    step_response = session.get("http://127.0.0.1:5000/api/step?room=tmp")
    return {"view": json.loads(view_response.text),
            "score": json.loads(score_response.text),
            "steps": json.loads(step_response.text)}


def set_action(action):
    try:
        requests.put("http://127.0.0.1:5100/api/setmove", json=action)
    except requests.exceptions.ConnectionError:
        print("Cannot set next move. Is there a manual AI?")


def step(dt=None):
    session.post("http://127.0.0.1:5000/api/step?room=tmp")
    state = get_state()
    for view in views:
        view.set_state(state)


def new_room():
    session.put("http://127.0.0.1:5000/api/room/tmp")
    state = get_state()
    for view in views:
        view.set_state(state)


def animate(dt):
    for view in views:
        view.animate(dt)


if __name__ == "__main__":
    new_room()
    print_help()
    state = get_state()
    for view in views:
        view.set_state(state)
    pyglet.clock.schedule_interval(animate, 1/FPS)
    pyglet.app.run()
