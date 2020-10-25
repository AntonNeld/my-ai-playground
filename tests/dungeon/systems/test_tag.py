from dungeon.systems import TagSystem
from dungeon.entity import Inventory, Entity, ItemPickup


def test_include_inherent_tags():
    system = TagSystem()
    tags_components = {"a": ["tagOne", "tagTwo"]}
    inventory_components = {}
    tags = system.get_tags(tags_components, inventory_components)
    assert tags == {"a": {"tagOne", "tagTwo"}}


def test_include_item_tags():
    system = TagSystem()
    tags_components = {}
    inventory_components = {
        "a": Inventory(items=[
            Entity(pickup=ItemPickup(kind="item",
                                     providesTags=["tagTwo", "tagThree"]))
        ])
    }
    tags = system.get_tags(tags_components, inventory_components)
    assert tags == {"a": {"tagTwo", "tagThree"}}


def test_combine_tags():
    system = TagSystem()
    tags_components = {"a": ["tagOne", "tagTwo"]}
    inventory_components = {
        "a": Inventory(items=[
            Entity(pickup=ItemPickup(kind="item",
                                     providesTags=["tagTwo", "tagThree"]))
        ])
    }
    tags = system.get_tags(tags_components, inventory_components)
    assert tags == {"a": {"tagOne", "tagTwo", "tagThree"}}
