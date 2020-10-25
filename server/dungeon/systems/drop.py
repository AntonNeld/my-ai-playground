class DropSystem:

    def drop_items(self, inventory_components, actions, position_components):
        for dropper_id, inventory in inventory_components.items():
            if (dropper_id not in actions
                    or actions[dropper_id].action_type != "drop"):
                continue
            try:
                items = inventory.items
                dropped_entity = items.pop(actions[dropper_id].index)
                new_position = position_components[dropper_id].copy(
                    deep=True)
                position_components[dropped_entity] = new_position
            except IndexError:
                # If we try to drop something that isn't in our inventory,
                # do nothing
                pass
