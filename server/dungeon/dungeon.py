import uuid

from dungeon.ai import ManualAI
from dungeon.entities.player import Player
from errors import ResourceNotFoundError


class Dungeon:

    def __init__(self):
        self._rooms = {}

    def add_room(self, room, room_id=None):
        if room_id is None:
            room_id = uuid.uuid4().hex
        self._rooms[room_id] = room
        return room_id

    def get_room(self, room_id):
        try:
            return self._rooms[room_id]
        except KeyError:
            raise ResourceNotFoundError

    def remove_room_by_id(self, room_id):
        if room_id in self._rooms:
            del self._rooms[room_id]

    def list_rooms(self):
        return list(self._rooms.keys())

    def manual_set_move(self, room_id, agent_id, action):
        entity = self._rooms[room_id].get_entity(agent_id)
        if isinstance(entity, Player) and isinstance(entity.ai, ManualAI):
            entity.ai.set_move(action)
        else:
            raise RuntimeError("Agent doesn't have manual AI")
