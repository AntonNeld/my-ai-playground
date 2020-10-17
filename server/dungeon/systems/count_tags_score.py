class CountTagsScoreSystem:

    def add_tag_scores(self, count_tags_score_components, position_components,
                       tags_components, label_components, score_components):
        items = count_tags_score_components.items()
        for counter_id, count_tags_score in items:
            overlapping_entities = [
                e for e in position_components.get_entities_at(
                    position_components[counter_id].x,
                    position_components[counter_id].y
                )
                if e is not counter_id
            ]

            tile_tags = {tag: 0 for tag in count_tags_score.tags}
            for overlapping_entity in [e for e in overlapping_entities
                                       if e in tags_components]:
                for tag in tags_components[overlapping_entity]:
                    if tag in tile_tags:
                        tile_tags[tag] += 1
            if tile_tags == count_tags_score.tags:
                entity_id = label_components.get_entity_with_label(
                    count_tags_score.add_to)
                if entity_id in score_components:
                    score_components[entity_id] += count_tags_score.score
