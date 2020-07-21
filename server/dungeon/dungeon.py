import uuid

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
