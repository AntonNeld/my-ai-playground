import pyglet

from thing import Thing


class View:

    def __init__(self, bounding_box=(0, 640, 0, 480),
                 show_steps=True, step_duration=0, camera=(0, 20, 0, 15)):
        self.things = {}
        self.min_x = bounding_box[0]
        self.max_x = bounding_box[1]
        self.min_y = bounding_box[2]
        self.max_y = bounding_box[3]
        self.scale = ((self.max_x - self.min_x)/(camera[1]-camera[0]),
                      (self.max_y - self.min_y)/(camera[3]-camera[2]))
        self.camera = camera
        self.step_duration = step_duration
        if show_steps:
            self.steplabel = pyglet.text.Label('N/A',
                                               font_name='Times New Roman',
                                               font_size=18,
                                               color=(0, 128, 255, 255),
                                               x=self.min_x + 8, y=self.max_y,
                                               anchor_x='left', anchor_y='top')
        else:
            self.steplabel = None

    def draw(self):
        for sprite in [self.things[identity].sprite
                       for identity in self.things
                       if self._visible(identity)]:
            sprite.draw()
        for label in [self.things[identity].label for
                      identity in self.things if self.things[identity].label
                      and self._visible(identity)]:
            label.draw()
        if self.steplabel:
            self.steplabel.draw()

    def set_state(self, state):
        new_things = state["view"]
        scores_list = state["score"]
        if self.steplabel:
            steps = state["steps"]
            self.steplabel.text = 'Steps: ' + str(steps)
        scores = {}
        for item in scores_list:
            scores[item["id"]] = item["score"]
        for thing in new_things:
            identity = thing["id"]
            # Create new things
            if identity not in self.things:
                self.things[identity] = Thing(
                    thing["x"], thing["y"], thing["looks_like"],
                    offset=(self.min_x, self.min_y), scale=self.scale)
            # Update existing things
            else:
                self.things[identity].set_pos(
                    thing["x"], thing["y"], duration=self.step_duration)
            # Set score label
            if identity in scores:
                self.things[identity].set_label(str(scores[identity]))
            else:
                self.things[identity].set_label(None)
        # Remove nonexistent things
        identities = list(self.things.keys())
        for identity in identities:
            if identity not in [thing["id"] for thing in new_things]:
                del self.things[identity]

    def animate(self, dt):
        for _, thing in self.things.items():
            thing.animate(dt)

    def _visible(self, identity):
        if identity not in self.things:
            return False
        x = self.things[identity].x
        y = self.things[identity].y
        return (x >= self.camera[0] and x < self.camera[1] and
                y >= self.camera[2] and y < self.camera[3])
