import pyglet
import requests
import json
from pyglet.window import key

from thing import Thing

verbose = False
window = pyglet.window.Window()

STEP_DURATION = 0.5

things = {}
steps = 0


@window.event
def on_draw():
    window.clear()
    steplabel = pyglet.text.Label('Steps: ' + str(steps),
                                  font_name='Times New Roman',
                                  font_size=18,
                                  color=(0, 128, 255, 255),
                                  x=8, y=window.height,
                                  anchor_x='left', anchor_y='top')
    for sprite in [things[identity].sprite for identity in things]:
        sprite.draw()
    for label in [things[identity].label for
                  identity in things if things[identity].label]:
        label.draw()
    steplabel.draw()


def set_action(action):
    try:
        requests.put("http://127.0.0.1:5100/api/setmove", json=action)
    except requests.exceptions.ConnectionError as e:
        if verbose:
            print(e)


def get_state():
    global things, scores, steps
    r = requests.get("http://127.0.0.1:5000/api/view")
    new_things = json.loads(r.text)
    r = requests.get("http://127.0.0.1:5000/api/score")
    scores_list = json.loads(r.text)
    scores = {}
    for item in scores_list:
        scores[item["id"]] = item["score"]
    if verbose:
        print(things)
    for thing in new_things:
        identity = thing["id"]
        # Create new things
        if identity not in things:
            things[identity] = Thing(
                thing["x"], thing["y"], thing["looks_like"])
        # Update existing things
        else:
            things[identity].set_pos(thing["x"], thing["y"])
        # Set score label
        if identity in scores:
            things[identity].set_label(str(scores[identity]))
        else:
            things[identity].set_label(None)
    # Remove nonexistent things
    identities = list(things.keys())
    for identity in identities:
        if identity not in [thing["id"] for thing in new_things]:
            del things[identity]
    r = requests.get("http://127.0.0.1:5000/api/step")
    steps = json.loads(r.text)


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
    get_state()


get_state()
pyglet.app.run()
event_loop = pyglet.app.EventLoop()


@event_loop.event
def on_window_close(window):
    event_loop.exit()
