from __future__ import annotations

from typing import Dict, Optional, Union
from mazebot.shared.collections import ObjectDict


class NodeData(ObjectDict):

  def __init__(self, x: int = 0, y: int = 0, character: str = '', **kwargs):
    self.x = x
    self.y = y
    self.character = character

    super().__init__(**kwargs)

  def __repr__(self):
    return f'"{self.character}"({self.x},{self.y})'


class Node(ObjectDict):

  def __init__(self,
               data: Optional[NodeData] = None,
               x: Optional[int] = None,
               y: Optional[int] = None,
               character: Optional[str] = None,
               parent: Optional[Node] = None,
               neighbors: Optional[Dict[Node, int]] = None,
               **kwargs):
    if data is None and ((x is not None) and (y is not None) and
                         (character is not None)):
      data = NodeData(x=x, y=y, character=character)

    self.data = data

    self.parent = parent

    if neighbors is None:
      neighbors = {}

    self.neighbors = neighbors

    super().__init__(**kwargs)

  @property
  def x(self) -> int:
    if self.data is None:
      return None

    return self.data.x

  @property
  def y(self) -> int:
    if self.data is None:
      return None

    return self.data.y

  @property
  def character(self) -> str:
    if self.data is None:
      return None

    return self.data.character

  def connect_to(self, other: Node, distance: int = 1) -> None:
    if not isinstance(other, Node):
      raise TypeError(f'{type(other).__name__} provided, but Node expected')

    self.neighbors[other] = distance

    other.neighbors[self] = distance

  def direction_to(self, other: Union[Node, NodeData]) -> Union[str, None]:
    if not isinstance(other, (Node, NodeData)):
      raise TypeError(
          f'{type(other).__name__} provided, but must be one of Node or NodeData'
      )

    if other.x < self.x:
      return 'W'

    if other.x > self.x:
      return 'E'

    if other.y < self.y:
      return 'N'

    if other.y > self.y:
      return 'S'

    return None

  def __repr__(self):
    neighbor_str = ''
    if len(self.neighbors):
      neighbor_str = f'[{len(self.neighbors)} neighbors][{" ".join([repr(n.data) for n in self.neighbors])}]'
    return f'{repr(self.data)}{neighbor_str}'
