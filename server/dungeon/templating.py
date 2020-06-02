import uuid


from errors import ResourceNotFoundError
from dungeon.entities.entity_factories import entity_from_dict
from dungeon.room import Room


class TemplateKeeper:

    def __init__(self):
        self._templates = {}

    def add_template(self, template, template_id=None):
        if template_id is None:
            template_id = uuid.uuid4().hex
        self._templates[template_id] = template
        return template_id

    def get_template(self, template_id):
        try:
            return self._templates[template_id]
        except KeyError:
            raise ResourceNotFoundError

    def remove_template_by_id(self, template_id):
        if template_id in self._templates:
            del self._templates[template_id]

    def list_templates(self):
        return list(self._templates.keys())

    def create_room(self, template_id):
        template = self.get_template(template_id)
        new_room = Room(0)
        for entity in template["entities"]:
            new_room.add_entity(entity_from_dict(entity, autofill=True))
        return new_room
