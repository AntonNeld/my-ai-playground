import pyglet

# Images go here
IMAGES = {
    "block": pyglet.resource.image('res/img/block.png'),
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
        self.target_x = None
        self.target_y = None
        self.sprite.scale_x = self.scale_x/IMAGE_SIZE
        self.sprite.scale_y = self.scale_y/IMAGE_SIZE
        self.label = None
        self.set_pos(x, y)

    def set_pos(self, x, y, duration=0):
        self.x = x
        self.y = y
        # In case we are not done with last move
        if self.target_x is not None and self.target_y is not None:
            self.sprite.x = self.target_x
            self.sprite.y = self.target_y

        self.target_x = x*self.scale_x + self.offset_x
        self.target_y = y*self.scale_y + self.offset_y
        self.animation_time_left = duration
        if duration == 0:
            self.sprite.x = self.target_x
            self.sprite.y = self.target_y
        self._set_label_pos()

    def animate(self, dt):
        if self.animation_time_left != 0:
            if self.animation_time_left - dt <= 0:
                self.animation_time_left = 0
                self.sprite.x = self.target_x
                self.sprite.y = self.target_y
            else:
                self.sprite.x += ((self.target_x-self.sprite.x) *
                                  dt/self.animation_time_left)
                self.sprite.y += ((self.target_y-self.sprite.y) *
                                  dt/self.animation_time_left)
                self.animation_time_left -= dt
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
        if self.label:
            self.label.begin_update()
            self.label.x = self.sprite.x + self.scale_x
            self.label.y = self.sprite.y + self.scale_y + 10
            self.label.end_update()
