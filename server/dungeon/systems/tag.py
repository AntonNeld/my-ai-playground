class TagSystem:

    def get_tags(self, tags_components, inventory_components):
        tags = {}
        for entity_id in set([*tags_components.keys(),
                              *inventory_components.keys()]):
            try:
                innate_tags = set(tags_components[entity_id])
            except KeyError:
                innate_tags = set()

            item_tags = set()
            if entity_id in inventory_components:
                for item in inventory_components[entity_id].items:
                    if item.pickup is not None and item.pickup.kind == "item":
                        for tag in item.pickup.provides_tags:
                            item_tags.add(tag)
            if innate_tags | item_tags:
                tags[entity_id] = innate_tags | item_tags
        return tags
