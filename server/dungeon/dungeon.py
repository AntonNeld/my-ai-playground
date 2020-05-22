import uuid

from dungeon import room
from dungeon.ais import ManualAI


class Dungeon:

    def __init__(self):
        self._rooms = {}

    def get_view(self, room_id):
        return self._rooms[room_id].get_view(include_id=True)

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

    def create_room(self, data):
        room_id = uuid.uuid4().hex
        self._rooms[room_id] = room.create_room_from_list(data)
        return room_id

    def create_room_with_id(self, room_id, data):
        self._rooms[room_id] = room.create_room_from_list(data)

    def delete_room(self, room_id):
        if room_id in self._rooms:
            del self._rooms[room_id]

    def manual_set_move(self, room_id, agent_id, action):
        entity = next(
            agent for agent in self._rooms[room_id].get_agents()
            if agent.id == agent_id)
        if isinstance(entity.ai, ManualAI):
            entity.ai.set_move(action)
        else:
            raise RuntimeError("Agent doesn't have manual AI")
