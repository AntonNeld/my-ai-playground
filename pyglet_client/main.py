import pyglet
import math
import requests
import json
from pyglet.window import key
import manual_ai

n = 0
x = y = 128


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

    label = pyglet.text.Label('Hacker skills baby!!',
                              font_name='Times New Roman',
                              font_size=46,
                              color=(n % 256, (n+100) %
                                     256, (n+200) % 256, 255),
                              x=window.width//2, y=window.height//2,
                              anchor_x='center', anchor_y='center')

    window.clear()
    label.draw()

    for thing in things:

        if thing["looks_like"] in SYMBOLS:
            obj = SYMBOLS[thing["looks_like"]]
        else:
            obj = DEFAULT_SYMBOL

        obj.blit(thing["x"]*32, thing["y"]*32)

    #block.blit(x + math.cos(n/10) * 64, y + math.sin(n/10) * 64)
    # block.blit(x + math.cos(n/10 + math.pi) * 64,
    #           y + math.sin(n/10 + math.pi) * 64)
    #player.blit(x, y)


@window.event
def on_key_press(symbol, modifiers):
    global x, y, n, things

    print('A key was pressed')
    if symbol == key.RIGHT:
        x += 32
        manual_ai.set_action("move_right")
    elif symbol == key.LEFT:
        x -= 32
        manual_ai.set_action("move_left")
    elif symbol == key.UP:
        y += 32
        manual_ai.set_action("move_up")
    elif symbol == key.DOWN:
        y -= 32
        manual_ai.set_action("move_down")
    r = requests.post("http://127.0.0.1:5000/api/step")
    r = requests.get("http://127.0.0.1:5000/api/view")
    things = json.loads(r.text)
    print(things)
    n += 1

    print(n)


manual_ai.run()
pyglet.app.run()
