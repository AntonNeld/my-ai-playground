class DropSystem:

    def drop_items(self, pickupper_components, actions, position_components):
        created_entities = []
        for dropper_id, pickupper in pickupper_components.items():
            if (dropper_id not in actions
                    or actions[dropper_id].action_type != "drop"):
                continue
            try:
                inventory = pickupper.inventory
                dropped_entity = inventory.pop(actions[dropper_id].index)
                new_position = position_components[dropper_id].copy(
                    deep=True)
                dropped_entity.position = new_position
                created_entities.append(dropped_entity)
            except IndexError:
                # If we try to drop something that isn't in our inventory,
                # do nothing
                pass
        return created_entities
