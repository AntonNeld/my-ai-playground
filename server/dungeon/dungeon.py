import uuid

from dungeon import rooms
from dungeon.ais import ai_types


class Dungeon:

    def __init__(self):
        pass

    def get_view(self, room):
        return rooms.get_room(room).get_view(include_id=True)

    def get_score(self, room, agents=None):
        scores = []
        for agent in rooms.get_room(room).get_agents():
            if agents is None or agent in agents:
                scores.append({"id": agent.id, "score": agent.score})
        return scores

    def get_steps(self, room):
        return rooms.get_room(room).steps

    def step(self, room):
        rooms.get_room(room).step()

    def create_room(self, data):
        room_id = uuid.uuid4().hex
        rooms.init_room(room_id, data)
        return room_id

    def create_room_with_id(self, room, data):
        rooms.init_room(room, data)

    def delete_room(self, room):
        rooms.delete_room(room)

    def manual_set_move(self, agent, action):
        ai_types["manual"].set_move(agent, action)
