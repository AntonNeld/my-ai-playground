import uuid

from dungeon import rooms
from dungeon.ais import ai_types


class Dungeon:

    def __init__(self):
        self._rooms = {}

    def get_view(self, room):
        return self._rooms[room].get_view(include_id=True)

    def get_score(self, room, agents=None):
        scores = []
        for agent in self._rooms[room].get_agents():
            if agents is None or agent in agents:
                scores.append({"id": agent.id, "score": agent.score})
        return scores

    def get_steps(self, room):
        return self._rooms[room].steps

    def step(self, room):
        self._rooms[room].step()

    def create_room(self, data):
        room = uuid.uuid4().hex
        self._rooms[room] = rooms.create_room_from_list(data)
        return room

    def create_room_with_id(self, room, data):
        self._rooms[room] = rooms.create_room_from_list(data)

    def delete_room(self, room):
        if room in self._rooms:
            for agent in self._rooms[room].get_agents():
                ai_types[agent.ai].delete(agent.id)
            del self._rooms[room]

    def manual_set_move(self, agent, action):
        ai_types["manual"].set_move(agent, action)
