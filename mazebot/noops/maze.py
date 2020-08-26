from __future__ import annotations

import requests
from typing import List, Mapping

from rich import print as rich_print
from mazebot.graph.node import Node
from mazebot.shared.collections import chunkify, ObjectDict
from mazebot.noops.enums import BorderCharacters, DirectionCharacters, GraphCharacters, MazeCharacters
from mazebot.noops.solution import MazeSolution


class ExampleSolution(ObjectDict):

  def __init__(self, directions='', **kwargs):
    self.directions = directions

    super().__init__(**kwargs)


class SolutionResponse(ObjectDict):

  def __init__(self,
               elapsed=None,
               local_timing=None,
               message=None,
               nextMaze=None,
               result=None,
               size=None,
               shortestSolutionLength=None,
               yourSolutionLength=None,
               **kwargs):

    self.elapsed = elapsed
    self.local_timing = local_timing
    self.message = message
    self.nextMaze = nextMaze
    self.result = result
    self.size = size
    self.shortestSolutionLength = shortestSolutionLength
    self.yourSolutionLength = yourSolutionLength

    super().__init__(**kwargs)


class Maze(ObjectDict):

  base_url = 'https://api.noopschallenge.com'

  def __init__(self,
               name='',
               mazePath=None,
               startingPosition=None,
               endingPosition=None,
               exampleSolution=None,
               message=None,
               map=None,
               **kwargs):
    if map is None:
      map = [[]]

    if startingPosition is None:
      startingPosition = []

    if endingPosition is None:
      endingPosition = []

    self.endingPosition = endingPosition
    self.exampleSolution = exampleSolution
    self.finish = None
    self.map = map
    self.mazePath = mazePath
    self.message = message
    self.name = name
    self.start = None
    self.startingPosition = startingPosition

    super().__init__(**kwargs)

  @property
  def size(self):
    return len(self.map)

  def print(self, solution: MazeSolution = None):
    if not len(self.map) > 0:
      return

    top_border = f'{BorderCharacters.TOP.LEFT.value}{BorderCharacters.TOP.MIDDLE.value * len(self.map)}{BorderCharacters.TOP.RIGHT.value}'
    rich_print(f'[grey62]{top_border}[/grey62]')

    # For Each Row
    for y, row in enumerate(self.map):
      row_chars = [f'[grey62]{BorderCharacters.SIDE.LEFT.value}[/grey62]']

      # For Each Cell
      for x, space in enumerate(row):
        # Map the raw character to the visualized representation
        char = Maze.map_character_type(space)

        # Apply colors based upon space type
        if char == MazeCharacters.WALL:
          row_chars.append(f'[dark_red]{char.value}[/dark_red]')
        elif char == MazeCharacters.START:
          row_chars.append(f'[sea_green2]{char.value}[/sea_green2]')
        elif char == MazeCharacters.END:
          row_chars.append(f'[orange3]{char.value}[/orange3]')
        elif solution and y in solution and x in solution[y]:
          row_chars.append(
              f'[black on steel_blue]{MazeCharacters[DirectionCharacters(solution[y][x]).name].value}[/black on steel_blue]'
          )
        else:
          row_chars.append(char.value)

      row_chars.append(f'[grey62]{BorderCharacters.SIDE.RIGHT.value}[/grey62]')

      rich_print(''.join(row_chars))

    bottom_border = f'{BorderCharacters.BOTTOM.LEFT.value}{BorderCharacters.BOTTOM.MIDDLE.value * len(self.map)}{BorderCharacters.BOTTOM.RIGHT.value}'
    rich_print(f'[grey62]{bottom_border}[/grey62]')

  def submit(self, solution: MazeSolution) -> SolutionResponse:
    directions = repr(solution)
    self.logger.debug(f'Submitting Maze Solution: {directions}')

    url = f'{Maze.base_url}{self.mazePath}'
    response = requests.post(url, json={'directions': directions})
    return response.json()

  @classmethod
  def fetch(cls, size=10) -> Maze:
    url = f'{cls.base_url}/mazebot/random?minSize={size}&maxSize={size}'
    response = requests.get(url)
    return response.json(object_hook=cls.__from_json)

  @classmethod
  def __from_json(cls, data: object) -> Maze:
    class_map = {
        'directions': ExampleSolution,
        'startingPosition': Maze,
    }

    for field, klass in class_map.items():
      if field in data:
        return klass.from_dict(data)

    print(f'Unknown JSON data received: {data}')

  @staticmethod
  def map_character_type(character: str) -> MazeCharacters:
    match = GraphCharacters(character)

    if match is None:
      return match

    return MazeCharacters[match.name]
