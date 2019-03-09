import pyglet

# Images go here
IMAGES = {
    "wall": pyglet.resource.image('res/img/block.png'),
    "player": pyglet.resource.image('res/img/player.png'),
    "coin": pyglet.resource.image('res/img/coin.png')}
DEFAULT_IMAGE = pyglet.resource.image('res/img/default.png')

IMAGE_SIZE = 32


class Thing:

    def __init__(self, x, y, looks_like, offset=(0, 0), scale=(32, 32)):
        if looks_like in IMAGES:
            image = IMAGES[looks_like]
        else:
            image = DEFAULT_IMAGE
        self.sprite = pyglet.sprite.Sprite(image)
        self.x = x
        self.y = y
        self.offset_x = offset[0]
        self.offset_y = offset[1]
        self.scale_x = scale[0]
        self.scale_y = scale[1]
        self.sprite.scale_x = self.scale_x/IMAGE_SIZE
        self.sprite.scale_y = self.scale_y/IMAGE_SIZE
        self.label = None
        self.set_pos(x, y)

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.sprite.x = x*self.scale_x + self.offset_x
        self.sprite.y = y*self.scale_y + self.offset_y
        if self.label:
            self._set_label_pos()

    def set_label(self, label):
        if label:
            if self.label:
                self.label.text = label
            else:
                self.label = pyglet.text.Label(
                    label,
                    font_name='Times New Roman',
                    font_size=10,
                    color=(
                        255, 255, 255, 255),
                    anchor_x='left', anchor_y='top')
                self._set_label_pos()
        else:
            self.label = None

    def _set_label_pos(self):
        self.label.x = self.sprite.x + self.scale_x
        self.label.y = self.sprite.y + self.scale_y + 10
