class AttackSystem:

    def do_attacks(self, actions, position, vulnerable):
        removed_entities = set()
        for attacker_id, action in actions.items():
            if action.action_type != "attack":
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

            target_x = position[attacker_id].x + dx
            target_y = position[attacker_id].y + dy

            for target in position.get_entities_at(
                    target_x, target_y):
                if target in vulnerable:
                    removed_entities.add(target)
        return removed_entities
