import uuid

from errors import ResourceNotFoundError


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
