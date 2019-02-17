import pyglet
import requests
import json
from pyglet.window import key
from pyglet import sprite

verbose = False
window = pyglet.window.Window()

# Images go here
block = pyglet.resource.image('res/img/block.png')
player = pyglet.resource.image('res/img/player.png')
coin = pyglet.resource.image('res/img/coin.png')
default = pyglet.resource.image('res/img/default.png')


SYMBOLS = {"wall": sprite.Sprite(block),
           "player": sprite.Sprite(player),
           "coin": sprite.Sprite(coin)}
DEFAULT_SYMBOL = default

things = []
scores = []
steps = 0


@window.event
def on_draw():
    steplabel = pyglet.text.Label('Steps: ' + str(steps),
                                  font_name='Times New Roman',
                                  font_size=18,
                                  color=(0, 128, 255, 255),
                                  x=8, y=window.height,
                                  anchor_x='left', anchor_y='top')

    window.clear()
    goldlabels = []
    for thing in things:

        if thing["looks_like"] in SYMBOLS:
            obj = SYMBOLS[thing["looks_like"]]
        else:
            obj = DEFAULT_SYMBOL
        obj.x = thing["x"]*32
        obj.y = thing["y"]*32
        obj.draw()
        if thing["looks_like"] == "player":
            score = ""
            for s in scores:
                if s["id"] == thing["id"]:
                    score = str(s["score"])
            goldlabel = pyglet.text.Label(score,
                                          font_name='Times New Roman',
                                          font_size=10,
                                          color=(255, 255, 255, 255),
                                          x=obj.x+32, y=obj.y+42,
                                          anchor_x='left', anchor_y='top')
            goldlabels.append(goldlabel)
    for goldlabel in goldlabels:
        goldlabel.draw()
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
    things = json.loads(r.text)
    r = requests.get("http://127.0.0.1:5000/api/score")
    scores = json.loads(r.text)
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
    if verbose:
        print(things)


get_state()
pyglet.app.run()
event_loop = pyglet.app.EventLoop()


@event_loop.event
def on_window_close(window):
    event_loop.exit()
