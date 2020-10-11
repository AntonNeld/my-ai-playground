from dungeon.consts import Position


class MovementSystem:

    def move_entities(self, actions, position, blocks_movement, tags):
        for actor_id, action in actions.items():
            if action.action_type != "move":
                continue

            dx = dy = 0
            if action.direction == "up":
                dy = 1
            elif action.direction == "down":
                dy = -1
            elif action.direction == "left":
                dx = -1
            elif action.direction == "right":
                dx = 1
            else:
                raise RuntimeError(f"Unknown direction {action.direction}")

            new_x = position[actor_id].x + dx
            new_y = position[actor_id].y + dy
            colliding_entities = position.get_entities_at(new_x, new_y)
            if not any(
                map(
                    lambda e: e in blocks_movement
                    and not set(blocks_movement[e].passable_for_tags)
                    & set(tags[actor_id] if actor_id in tags else []),
                    colliding_entities)):
                position[actor_id] = Position(x=new_x, y=new_y)
