from dungeon.systems import TagSystem
from dungeon.entity import Pickupper, Entity, ItemPickup


def test_include_inherent_tags():
    system = TagSystem()
    tags_components = {"a": ["tagOne", "tagTwo"]}
    pickupper_components = {}
    tags = system.get_tags(tags_components, pickupper_components)
    assert tags == {"a": {"tagOne", "tagTwo"}}


def test_include_item_tags():
    system = TagSystem()
    tags_components = {}
    pickupper_components = {
        "a": Pickupper(inventory=[
            Entity(pickup=ItemPickup(kind="item",
                                     providesTags=["tagTwo", "tagThree"]))
        ])
    }
    tags = system.get_tags(tags_components, pickupper_components)
    assert tags == {"a": {"tagTwo", "tagThree"}}


def test_combine_tags():
    system = TagSystem()
    tags_components = {"a": ["tagOne", "tagTwo"]}
    pickupper_components = {
        "a": Pickupper(inventory=[
            Entity(pickup=ItemPickup(kind="item",
                                     providesTags=["tagTwo", "tagThree"]))
        ])
    }
    tags = system.get_tags(tags_components, pickupper_components)
    assert tags == {"a": {"tagOne", "tagTwo", "tagThree"}}
