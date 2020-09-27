from typing import Union

from .common import ParseError
from .raw import RawTemplate
from .visual import VisualTemplate

Template = Union[RawTemplate, VisualTemplate]

__all__ = (Template, ParseError)
