from pyglet.window import key
import timeit
import requests
import pyglet
import json
import os
import sys

from view import View
import maps

FPS = 30

STEP_DURATION = 0.3
STEP_INTERVAL = 0.3

if "PLAYER_AI" in os.environ:
    PLAYER_AI = os.environ["PLAYER_AI"]
else:
    PLAYER_AI = "pathfinder"

config = {"manual_mode": [], "auto_step": False}

window = pyglet.window.Window(width=800, height=600)
event_loop = pyglet.app.EventLoop()

session = requests.session()

views = [View(step_duration=STEP_DURATION)]
room_id = None

# Uncomment to test multiple views, currently of the same dungeon
# views = [View((30, 770, 80, 260),step_duration=STEP_DURATION),
#          View((0, 400, 300, 600),step_duration=STEP_DURATION)]


def print_help():
    help_string = """
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
    if symbol == key.R:
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
    view_response = session.get(
        "http://127.0.0.1:8300/api/rooms/{}/view".format(room_id))
    score_response = session.get(
        "http://127.0.0.1:8300/api/rooms/{}/score".format(room_id))
    step_response = session.get(
        "http://127.0.0.1:8300/api/rooms/{}/step".format(room_id))
    return {"view": json.loads(view_response.text),
            "score": json.loads(score_response.text),
            "steps": json.loads(step_response.text)}


def set_action(action):
    for agent in config["manual_mode"]:
        requests.put(
            "http://127.0.0.1:8300/api/rooms/{}/agent/{}/setmove".format(
                room_id, agent),
            json=action)


def step(dt=None):
    session.post("http://127.0.0.1:8300/api/rooms/{}/step".format(room_id))
    state = get_state()
    for view in views:
        view.set_state(state)


def new_room():
    global room_id
    data = maps.load(sys.argv[1], PLAYER_AI)
    if not room_id:
        response = session.post("http://127.0.0.1:8300/api/rooms", json=data)
        room_id = json.loads(response.text)
    else:
        session.put(
            "http://127.0.0.1:8300/api/rooms/{}".format(room_id), json=data)
    state = get_state()
    for view in views:
        view.set_state(state)
    # temporary solution, will change how agent info is fetched,
    # and how manual mode is set
    if PLAYER_AI == "manual":
        config["manual_mode"] = [item["id"] for item in state["score"]]


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
