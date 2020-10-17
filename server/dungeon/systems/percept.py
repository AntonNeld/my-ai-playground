class PerceptSystem:

    def get_percepts(self, perception_components, position_components,
                     looks_like_components, pickupper_components):
        percepts = {}
        for perceptor_id, perception in perception_components.items():
            if perceptor_id not in position_components:
                continue

            percept = {}
            my_x = position_components[perceptor_id].x
            my_y = position_components[perceptor_id].y
            if perception.include_position:
                percept["position"] = {"x": my_x, "y": my_y}

            entities_view = []
            for entity_id, looks_like in looks_like_components.items():
                if entity_id == perceptor_id:
                    continue
                if (entity_id not in position_components):
                    continue
                other_x = position_components[entity_id].x
                other_y = position_components[entity_id].y
                max_dist = perception.distance
                if (max_dist is not None
                        and abs(other_x-my_x) + abs(other_y-my_y) > max_dist):
                    continue
                entity_view = {"x":          other_x - my_x,
                               "y":          other_y - my_y,
                               "looks_like": looks_like}
                entities_view.append(entity_view)
            percept["entities"] = entities_view

            if perceptor_id in pickupper_components:
                percept["inventory"] = [
                    e.looks_like for
                    e in pickupper_components[perceptor_id].inventory
                ]
            percepts[perceptor_id] = percept
        return percepts
