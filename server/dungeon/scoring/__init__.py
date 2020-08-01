from typing import Union

from .held_items import HeldItemsScoring
from .tile_tags import TileTagsScoring

Scoring = Union[HeldItemsScoring, TileTagsScoring]

__all__ = ("Scoring",)
