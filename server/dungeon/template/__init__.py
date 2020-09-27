from typing import Union

from .common import ParseError
from .raw import RawTemplate
from .visual import VisualTemplate
from .cave_generation import CaveGenerationTemplate

Template = Union[RawTemplate, VisualTemplate, CaveGenerationTemplate]

__all__ = (Template, ParseError)
