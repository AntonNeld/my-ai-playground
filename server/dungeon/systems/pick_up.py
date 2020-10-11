class PickUpSystem:

    def pick_up_items(self, pickupper, actions, position, pickup, score):
        picked_up_items = {}
        removed_entities = set()
        for pickupper_id in pickupper:
            if pickupper_id not in position:
                continue
            if (pickupper[pickupper_id].mode == "action"
                    and (pickupper_id not in actions
                         or actions[pickupper_id].action_type != "pick_up")):
                continue

            x = position[pickupper_id].x
            y = position[pickupper_id].y
            pickups = [e for e in position.get_entities_at(x, y)
                       if e in pickup]
            for pickup_id in pickups:
                kind = pickup[pickup_id].kind
                if (
                    kind == "item" and not
                    pickupper[pickupper_id].full_inventory()
                ):
                    picked_up_items[pickup_id] = pickupper_id
                elif kind == "vanish":
                    removed_entities.add(pickup_id)
                elif kind == "addScore":
                    removed_entities.add(pickup_id)
                    added_score = pickup[pickup_id].score
                    if pickupper_id in score:
                        score[pickupper_id] += added_score
        return picked_up_items, removed_entities
