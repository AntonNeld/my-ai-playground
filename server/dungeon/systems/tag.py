class TagSystem:

    def get_tags(self, tags, pickupper):
        output_tags = {}
        for entity_id in set([*tags.keys(), *pickupper.keys()]):
            try:
                innate_tags = set(tags[entity_id])
            except KeyError:
                innate_tags = set()

            item_tags = set()
            if entity_id in pickupper:
                for item in pickupper[entity_id].inventory:
                    if item.pickup is not None and item.pickup.kind == "item":
                        for tag in item.pickup.provides_tags:
                            item_tags.add(tag)
            if innate_tags | item_tags:
                output_tags[entity_id] = innate_tags | item_tags
        return output_tags
