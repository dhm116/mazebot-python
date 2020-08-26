from __future__ import annotations

from typing import List, Mapping, Optional, Tuple

from mazebot.graph.node import Node
from mazebot.noops.enums import GraphCharacters
from mazebot.shared.logging import Logging

GridMapping = Mapping[int, Mapping[int, str]]
DirectionalReference = Tuple[Node, Node, str]


class SolutionError(Exception):

  def __init__(self,
               message: str = 'Invalid maze solution provided',
               solution: Optional[List[Node]] = None,
               stringify_solution: bool = True):
    self.message = message
    self.solution = solution
    self.stringify_solution = stringify_solution

    if self.solution is not None and stringify_solution:
      steps = [repr(node.data) for node in solution]
      self.message = f'{self.message}: [{", ".join(steps)}]'


class MazeSolution(object):

  def __init__(self, *args: Node):
    self.__raw_directions = list(args)
    self.__directions: List[DirectionalReference] = []
    self.__directions_grid: GridMapping = {}

    self._initialize_logger()
    self._initialize_directions()

  @property
  def logger(self):
    return self.__logger__

  def _initialize_directions(self) -> None:
    first_char = GraphCharacters(self.__raw_directions[0].character)

    if first_char == GraphCharacters.START:
      # Flip the solution around (for ease of use)
      self.__raw_directions = list(reversed(self.__raw_directions))
    elif not first_char == GraphCharacters.END:
      # Solution didn't begin with the Maze end location - something isn't right...
      raise SolutionError(solution=self.__raw_directions)

    self._create_directions()
    self._create_directions_grid()

  def _create_directions(self) -> None:
    self.__directions.clear()

    while len(self.__raw_directions) > 0:
      last_node = self.__raw_directions.pop()

      if not len(self.__raw_directions) > 0:
        continue

      next_node = self.__raw_directions[-1]

      self.__directions.append(
          (last_node, next_node, last_node.direction_to(next_node)))

  def _create_directions_grid(self) -> None:
    self.__directions_grid.clear()

    # pylint: disable=unused-variable
    for from_node, to_node, direction in self.__directions:
      row = self.__directions_grid.setdefault(to_node.y, {})
      row[to_node.x] = direction

  def _initialize_logger(self) -> None:
    self.__logger__ = Logging.getLogger(__name__)

  def __contains__(self, key: int) -> bool:
    return key in self.__directions_grid

  def __getitem__(self, key: int) -> Mapping[int, str]:
    return self.__directions_grid[key]

  def __repr__(self) -> str:
    # pylint: disable=unused-variable
    directions = [char for a, b, char in self.__directions]
    return "".join(directions)

  def get(self,
          key: int,
          default: Mapping[int, str] = None) -> Mapping[int, str]:
    return self.__directions_grid.get(key, default)
