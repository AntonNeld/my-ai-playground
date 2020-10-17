class TagSystem:

    def get_tags(self, tags_components, pickupper_components):
        tags = {}
        for entity_id in set([*tags_components.keys(),
                              *pickupper_components.keys()]):
            try:
                innate_tags = set(tags_components[entity_id])
            except KeyError:
                innate_tags = set()

            item_tags = set()
            if entity_id in pickupper_components:
                for item in pickupper_components[entity_id].inventory:
                    if item.pickup is not None and item.pickup.kind == "item":
                        for tag in item.pickup.provides_tags:
                            item_tags.add(tag)
            if innate_tags | item_tags:
                tags[entity_id] = innate_tags | item_tags
        return tags
