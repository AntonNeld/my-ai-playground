from dungeon.entity import Entity
from typing import Dict, List, Union


class ParseError(Exception):
    pass


Definitions = Dict[str, Union[Entity, str, List[Union[Entity, str]]]]


def translate_definition_symbol(symbol, definitions, original_symbol=None):
    if symbol == original_symbol:
        raise ParseError(f"Circular reference: {symbol}")
    if symbol not in definitions:
        raise ParseError(f"Unknown symbol: {symbol}")
    if isinstance(definitions[symbol], list):
        definition_list = definitions[symbol]
    else:
        definition_list = [definitions[symbol]]
    entities = []
    for item in definition_list:
        if isinstance(item, Entity):
            entities.append(item)
        else:
            entities.extend(
                translate_definition_symbol(
                    item, definitions,
                    (original_symbol if original_symbol is not None
                        else symbol)
                )
            )
    return entities
