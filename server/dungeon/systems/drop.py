class DropSystem:

    def drop_items(self, pickupper, actions, position):
        created_entities = []
        for dropper_id in pickupper:
            if (dropper_id not in actions
                    or actions[dropper_id].action_type != "drop"):
                continue
            try:
                inventory = pickupper[dropper_id].inventory
                dropped_entity = inventory.pop(actions[dropper_id].index)
                new_position = position[dropper_id].copy(
                    deep=True)
                dropped_entity.position = new_position
                created_entities.append(dropped_entity)
            except IndexError:
                # If we try to drop something that isn't in our inventory,
                # do nothing
                pass
        return created_entities
