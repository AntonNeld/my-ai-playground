import pyglet


class Draw():

    def __init__(self):
        self.window = pyglet.window.Window()

    def draw(self):
        label = pyglet.text.Label('Hello, world',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=window.width//2, y=window.height//2,
                                  anchor_x='center', anchor_y='center')


@window.event
def on_draw():
    window.clear()
    label.draw()
