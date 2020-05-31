import uuid

from dungeon import room
from dungeon.ai import ManualAI
from errors import ResourceNotFoundError


class Dungeon:

    def __init__(self):
        self._rooms = {}

    def get_score(self, room_id, agents=None):
        scores = []
        for agent in self._rooms[room_id].get_agents():
            if agents is None or agent in agents:
                scores.append({"id": agent.id, "score": agent.score})
        return scores

    def get_steps(self, room_id):
        return self._rooms[room_id].steps

    def step(self, room_id):
        self._rooms[room_id].step()

    def create_room(self, data, room_id=None):
        if room_id is None:
            room_id = uuid.uuid4().hex
        self._rooms[room_id] = room.create_room_from_list(data)
        return room_id

    def get_room(self, room_id):
        try:
            return self._rooms[room_id]
        except KeyError:
            raise ResourceNotFoundError

    def delete_room(self, room_id):
        if room_id in self._rooms:
            del self._rooms[room_id]

    def list_rooms(self):
        return list(self._rooms.keys())

    def manual_set_move(self, room_id, agent_id, action):
        entity = next(
            agent for agent in self._rooms[room_id].get_agents()
            if agent.id == agent_id)
        if isinstance(entity.ai, ManualAI):
            entity.ai.set_move(action)
        else:
            raise RuntimeError("Agent doesn't have manual AI")
