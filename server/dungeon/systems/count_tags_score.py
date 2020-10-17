class CountTagsScoreSystem:

    def add_tag_scores(self, count_tags_score_components,
                       position_components, tags_components,
                       label_components, score_components):
        scores = self.calculate_tag_scores(
            count_tags_score_components,
            position_components, tags_components,
            label_components, score_type="additive"
        )
        for entity_id, score in scores.items():
            if entity_id in score_components:
                score_components[entity_id] += score

    def get_constant_tag_scores(self, count_tags_score_components,
                                position_components, tags_components,
                                label_components):
        return self.calculate_tag_scores(
            count_tags_score_components,
            position_components, tags_components,
            label_components, score_type="constant"
        )

    def calculate_tag_scores(self, count_tags_score_components,
                             position_components, tags_components,
                             label_components, score_type):
        scores = {}
        items = count_tags_score_components.items()
        for counter_id, count_tags_score in items:
            entities = [
                e for e in position_components.get_entities_at(
                    position_components[counter_id].x,
                    position_components[counter_id].y
                )
            ]

            tile_tags = {tag: 0 for tag in count_tags_score.tags}
            for overlapping_entity in [e for e in entities
                                       if e in tags_components]:
                for tag in tags_components[overlapping_entity]:
                    if tag in tile_tags:
                        tile_tags[tag] += 1
            if tile_tags == count_tags_score.tags:
                entity_id = label_components.get_entity_with_label(
                    count_tags_score.add_to)
                if count_tags_score.score_type == score_type:
                    if entity_id not in scores:
                        scores[entity_id] = 0
                    scores[entity_id] += count_tags_score.score
        return scores
