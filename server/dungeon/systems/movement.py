from dungeon.consts import Position


class MovementSystem:

    def move_entities(self, actions, position_components,
                      blocks_movement_components, tags,
                      random_generator):
        new_positions = {}  # Map of (x,y) -> list of entity IDs
        for mover_id, action in actions.items():
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

            x = position_components[mover_id].x + dx
            y = position_components[mover_id].y + dy
            colliding_entities = position_components.get_entities_at(x, y)
            if all([
                    can_coexist(mover_id, e, blocks_movement_components, tags)
                    for e in colliding_entities
            ]):
                if (x, y) not in new_positions:
                    new_positions[(x, y)] = []
                new_positions[(x, y)].append(mover_id)
        for (x, y), entities in new_positions.items():
            while entities:
                # If there are multiple entities trying to move to the same
                # location, their moves are evaluated in random order.
                chosen = random_generator.choice(entities)
                position_components[chosen] = Position(x=x, y=y)
                entities.remove(chosen)
                entities = [e for e in entities if can_coexist(
                    e, chosen, blocks_movement_components, tags)]


def can_coexist(an_entity, another_entity, blocks_movement_components, tags):
    for (first, second) in [
        (an_entity, another_entity), (another_entity, an_entity)
    ]:
        if first in blocks_movement_components:
            if second not in tags:
                return False
            pass_tags = blocks_movement_components[first].passable_for_tags
            if not set(tags[second]) & set(pass_tags):
                return False
    return True
