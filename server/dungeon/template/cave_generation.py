from random import Random
from typing import Dict, Optional

from typing_extensions import Literal
from pydantic import BaseModel, Field

from dungeon.consts import Position
from dungeon.room import Room
from .common import Definitions, translate_definition_symbol


class PlacementDetails(BaseModel):
    amount: Optional[int]


class CaveGenerationTemplate(BaseModel):
    template_type: Literal["caveGeneration"] = Field(..., alias="templateType")
    room_seed: Optional[int] = Field(None, alias="roomSeed")
    definitions: Definitions
    seed: int
    width: int
    height: int
    wall: str
    bypass_neighbour_chance: float = Field(0.1, alias="bypassNeighbourChance")
    stuff: Dict[str, PlacementDetails]

    def create_room(self):
        random_generator = Random(self.seed)
        free_locations = get_free_locations(
            self.width, self.height, self.bypass_neighbour_chance,
            random_generator)
        wall_entities = translate_definition_symbol(
            self.wall, self.definitions)
        if self.room_seed is not None:
            room = Room(randomSeed=self.room_seed)
        else:
            room = Room()
        for entity in wall_entities:
            fill_room(room, entity, self.width, self.height, free_locations)
        symbols_to_place = []
        for symbol, placement_details in self.stuff.items():
            if placement_details.amount:
                symbols_to_place += [symbol] * placement_details.amount
        locations = random_generator.sample(
            free_locations, len(symbols_to_place))
        for location, symbol in zip(locations, symbols_to_place):
            entities = translate_definition_symbol(symbol, self.definitions)
            for entity in entities:
                new_entity = entity.copy(deep=True)
                new_entity.position = Position(x=location[0], y=location[1])
                room.add_entity(new_entity)
        return room


def fill_room(room, wall_entity, width, height, free_locations):
    for x in range(width):
        for y in range(height):
            if (x, y) not in free_locations:
                new_entity = wall_entity.copy(deep=True)
                new_entity.position = Position(x=x, y=y)
                room.add_entity(new_entity)


def get_free_locations(width, height, bypass_neighbour_chance,
                       random_generator):
    start_x = random_generator.randrange(1, width-1)
    start_y = random_generator.randrange(1, height-1)
    free_locations = set()
    frontier = [(start_x, start_y)]
    iterations = 0
    while frontier:
        iterations += 1
        if iterations > 10000:
            raise RuntimeError("Too many iterations")
        location = frontier.pop()
        if not permissible_free_location(
            location, width, height, free_locations,
            bypass_neighbour_chance, random_generator,
        ):
            continue
        free_locations.add(location)
        x = location[0]
        y = location[1]
        neighbours = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        random_generator.shuffle(neighbours)
        for neighbour in neighbours:
            if neighbour not in free_locations:
                frontier.append(neighbour)

    return free_locations


def permissible_free_location(location, width, height, existing_locations,
                              bypass_neighbour_chance, random_generator):
    x, y = location
    # Check if it's outside the room
    if (x > width-2 or x < 1 or y > height-2 or y < 1):
        return False
    # Check if it's too close to more than one existing location.
    # One is allowed, since that's the parent. There is a small chance of
    # bypassing this, to get loops and rooms.
    if (
        len(set([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
            & existing_locations) > 1
            and random_generator.random() > bypass_neighbour_chance
    ):
        return False
    # Check if adding it would create an ugly corner
    for corner in [(x+1, y+1), (x-1, y+1), (x+1, y-1), (x-1, y-1)]:
        dx = corner[0]-x
        dy = corner[1]-y
        if (corner in existing_locations
                and not set([(x+dx, y), (x, y+dy)]) & existing_locations):
            return False
    return True
