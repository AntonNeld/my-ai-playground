from dungeon.entities.entity_factories import entity_from_json


class Room:

    def __init__(self):
        self._entities = []
        self.steps = 0

    def add_entities(self, *entities):
        for entity in entities:
            if entity not in self._entities:
                entity.set_room(self)
                self._entities.append(entity)
            else:
                raise RuntimeError("Cannot add entity twice: " + str(entity))

    def remove_entities(self, *entities):
        for entity in entities:
            self._entities.remove(entity)

    def update_entity(self, entity_id, entity):
        old_entity = [old_entity for old_entity in self._entities
                      if old_entity.id == entity_id][0]
        self.remove_entities(old_entity)
        self.add_entities(entity)

    def list_entities(self):
        return [entity.id for entity in self._entities]

    def get_entity(self, entity_id):
        return [entity for entity in self._entities
                if entity.id == entity_id][0].to_json()

    def get_entities(self):
        return self._entities.copy()

    def get_agents(self):
        return [entity for entity in self._entities if hasattr(entity, "ai")]

    def get_view(self, perceptor):
        x = perceptor.x
        y = perceptor.y
        percept = []
        entities = self.get_entities()
        for entity in entities:
            if entity != perceptor:
                entity_view = {"x":          entity.x - x,
                               "y":          entity.y - y,
                               "looks_like": entity.looks_like}
                percept.append(entity_view)

        return percept

    def step(self):
        for entity in self._entities:
            if hasattr(entity, "step"):
                if hasattr(entity, "ai"):
                    action = entity.ai.next_move(self.get_view(entity))
                    entity.step(action)
                else:
                    entity.step()
        self.steps += 1

    def passable(self, x, y):
        for entity in self.get_entities():
            if entity.x == x and entity.y == y and entity.solid:
                return False
        return True

    def to_json(self):
        return [entity.to_json() for entity in self._entities]


def create_room_from_list(data):
    new_room = Room()
    for entity in data:
        new_room.add_entities(entity_from_json(entity))
    return new_room
