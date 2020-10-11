class PerceptSystem:

    def get_percepts(self, perception, position, looks_like, pickupper):
        percepts = {}
        for perceptor_id in perception:
            if perceptor_id not in perception or perceptor_id not in position:
                continue

            percept = {}
            my_x = position[perceptor_id].x
            my_y = position[perceptor_id].y
            if perception[perceptor_id].include_position:
                percept["position"] = {"x": my_x, "y": my_y}

            entities_view = []
            for entity_id in looks_like:
                if entity_id == perceptor_id:
                    continue
                if (entity_id not in position):
                    continue
                other_x = position[entity_id].x
                other_y = position[entity_id].y
                max_dist = perception[perceptor_id].distance
                if (max_dist is not None
                        and abs(other_x-my_x) + abs(other_y-my_y) > max_dist):
                    continue
                entity_view = {"x":          other_x - my_x,
                               "y":          other_y - my_y,
                               "looks_like": looks_like[entity_id]}
                entities_view.append(entity_view)
            percept["entities"] = entities_view

            if perceptor_id in pickupper:
                percept["inventory"] = [
                    e.looks_like for e in pickupper[perceptor_id].inventory
                ]
            percepts[perceptor_id] = percept
        return percepts
