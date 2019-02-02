import pyglet
import math
import requests
import json
from pyglet.window import key
from pyglet import sprite
import manual_ai

verbose = False
window = pyglet.window.Window()

# Images go here
block = pyglet.resource.image('res/img/block.png')
player = pyglet.resource.image('res/img/player.png')
coin = pyglet.resource.image('res/img/coin.png')
default = pyglet.resource.image('res/img/default.png')


r = requests.get("http://127.0.0.1:5000/api/view")
things = json.loads(r.text)


SYMBOLS = {"wall": sprite.Sprite(block),
           "player": sprite.Sprite(player),
           "coin": sprite.Sprite(coin)}
DEFAULT_SYMBOL = default


@window.event
def on_draw():
    goldlabel = pyglet.text.Label('Gold: ' + str(things["score"]),
                                  font_name='Times New Roman',
                                  font_size=18,
                                  color=(200, 200, 0, 255),
                                  x=8, y=window.height,
                                  anchor_x='left', anchor_y='top')
    steplabel = pyglet.text.Label('Steps: ' + str(things["steps"]),
                                  font_name='Times New Roman',
                                  font_size=18,
                                  color=(0, 128, 255, 255),
                                  x=8, y=window.height-32,
                                  anchor_x='left', anchor_y='top')

    window.clear()

    for thing in things["things"]:

        if thing["looks_like"] in SYMBOLS:
            obj = SYMBOLS[thing["looks_like"]]
        else:
            obj = DEFAULT_SYMBOL
        obj.x = thing["x"]*32
        obj.y = thing["y"]*32
        obj.draw()

    goldlabel.draw()
    steplabel.draw()


@window.event
def on_key_press(symbol, modifiers):
    global things

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
event_loop = pyglet.app.EventLoop()


@event_loop.event
def on_window_close(window):
    event_loop.exit()
