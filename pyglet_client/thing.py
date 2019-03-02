import pyglet

# Images go here
IMAGES = {
    "wall": pyglet.resource.image('res/img/block.png'),
    "player": pyglet.resource.image('res/img/player.png'),
    "coin": pyglet.resource.image('res/img/coin.png')}
DEFAULT_IMAGE = pyglet.resource.image('res/img/default.png')


class Thing:

    def __init__(self, x, y, looks_like):
        if looks_like in IMAGES:
            image = IMAGES[looks_like]
        else:
            image = DEFAULT_IMAGE
        self.sprite = pyglet.sprite.Sprite(image, x=x*32, y=y*32)
        self.label = None

    def set_pos(self, x, y):
        self.sprite.x = x*32
        self.sprite.y = y*32

    def set_label(self, label):
        if label:
            x = self.sprite.x + 32
            y = self.sprite.y + 42
            if self.label:
                self.label.text = label
                self.label.x = x
                self.label.y = y
            else:
                self.label = pyglet.text.Label(
                    label,
                    font_name='Times New Roman',
                    font_size=10,
                    color=(
                        255, 255, 255, 255),
                    x=x, y=y,
                    anchor_x='left', anchor_y='top')
        else:
            self.label = None
