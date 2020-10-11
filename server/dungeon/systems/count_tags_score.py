class CountTagsScoreSystem:

    def add_tag_scores(self, count_tags_score, position, tags, label, score):
        for counter_id, counter_details in count_tags_score.items():
            overlapping_entities = [
                e for e in position.get_entities_at(
                    position[counter_id].x,
                    position[counter_id].y
                )
                if e is not counter_id
            ]

            tile_tags = {tag: 0 for tag in counter_details.tags}
            for overlapping_entity in [e for e in overlapping_entities
                                       if e in tags]:
                for tag in tags[overlapping_entity]:
                    if tag in tile_tags:
                        tile_tags[tag] += 1
            if tile_tags == counter_details.tags:
                for entity_id in label:
                    if (label[entity_id] == counter_details.add_to
                            and entity_id in score):
                        score[entity_id] += counter_details.score
