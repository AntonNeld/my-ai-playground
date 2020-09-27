from typing import Union

from .common import ParseError
from .raw_template import RawTemplate
from .visual_template import VisualTemplate

Template = Union[RawTemplate, VisualTemplate]

__all__ = (Template, ParseError)
