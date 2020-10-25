class TagSystem:

    def get_tags(self, tags_components, inventory_components,
                 pickup_components):
        tags = {}
        for entity_id in set([*tags_components.keys(),
                              *inventory_components.keys()]):
            try:
                innate_tags = set(tags_components[entity_id])
            except KeyError:
                innate_tags = set()

            item_tags = set()
            if entity_id in inventory_components:
                for item_id in inventory_components[entity_id].items:
                    if (item_id in pickup_components
                            and pickup_components[item_id].kind == "item"):
                        for tag in pickup_components[item_id].provides_tags:
                            item_tags.add(tag)
            if innate_tags | item_tags:
                tags[entity_id] = innate_tags | item_tags
        return tags
