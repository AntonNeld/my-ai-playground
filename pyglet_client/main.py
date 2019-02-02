import pyglet
import math
import requests
import json
from pyglet.window import key
import manual_ai

verbose = False
gold = 1337
steps = 42
window = pyglet.window.Window()

# Images go here
block = pyglet.resource.image('res/img/block.png')
player = pyglet.resource.image('res/img/player.png')
default = pyglet.resource.image('res/img/default.png')


r = requests.get("http://127.0.0.1:5000/api/view")
things = json.loads(r.text)


SYMBOLS = {"wall": block,
           "player": player}
DEFAULT_SYMBOL = default

[{"looks_like": "wall", "x": 1, "y": 2},
 {"looks_like": "wall", "x": 4, "y": 2}]


@window.event
def on_draw():
    goldlabel = pyglet.text.Label('Gold: ' + str(gold),
                                  font_name='Times New Roman',
                                  font_size=18,
                                  color=(200, 200, 0, 255),
                                  x=8, y=window.height,
                                  anchor_x='left', anchor_y='top')
    steplabel = pyglet.text.Label('Steps: ' + str(steps),
                                  font_name='Times New Roman',
                                  font_size=18,
                                  color=(0, 128, 255, 255),
                                  x=8, y=window.height-32,
                                  anchor_x='left', anchor_y='top')

    window.clear()

    for thing in things:

        if thing["looks_like"] in SYMBOLS:
            obj = SYMBOLS[thing["looks_like"]]
        else:
            obj = DEFAULT_SYMBOL

        obj.blit(thing["x"]*32, thing["y"]*32)

    goldlabel.draw()
    steplabel.draw()


@window.event
def on_key_press(symbol, modifiers):
    global x, y, n, things

    if symbol == key.RIGHT:
        manual_ai.set_action("move_right")
    elif symbol == key.LEFT:
        manual_ai.set_action("move_left")
    elif symbol == key.UP:
        manual_ai.set_action("move_up")
    elif symbol == key.DOWN:
        manual_ai.set_action("move_down")
    r = requests.post("http://127.0.0.1:5000/api/step")
    r = requests.get("http://127.0.0.1:5000/api/view")
    things = json.loads(r.text)
    if verbose:
        print(things)


manual_ai.run()
pyglet.app.run()
