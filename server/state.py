from dungeon.dungeon import Dungeon
from dungeon.templating import TemplateKeeper


class StateKeeper:

    def __init__(self, template_dir):
        self._template_dir = template_dir
        self.clear_state()

    def clear_state(self):
        self.dungeon = Dungeon()
        self.template_keeper = TemplateKeeper()
        if self._template_dir:
            self.template_keeper.load_directory(self._template_dir)
