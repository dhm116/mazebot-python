from __future__ import annotations

from itertools import filterfalse
from typing import List, Optional

from mazebot.shared.collections import ObjectDict
from mazebot.graph.node import Node, NodeData
from mazebot.noops.enums import GraphCharacters
from mazebot.noops.maze import Maze


def _is_wall_character(node):
  return node.character == GraphCharacters.WALL.value


class Graph(ObjectDict):

  def __init__(self, nodes: Optional[List[Node]] = None, **kwargs):
    self.__nodes = []

    if nodes is not None:
      pass

    super().__init__(**kwargs)

  @property
  def nodes(self) -> List[Node]:
    return self.__nodes

  def add_node(self, node: Node) -> Node:
    self.__nodes.append(node)
    return self.__nodes[-1]

  @classmethod
  def from_maze(cls, maze: Maze) -> Graph:
    graph = cls()

    for y, row in enumerate(maze.map):
      for x, character in enumerate(row):
        node = graph.add_node(Node(x=x, y=y, character=character))

        if character == GraphCharacters.START.value:
          maze.start = node

        if character == GraphCharacters.END.value:
          maze.finish = node

    graph.logger.debug(f'Graph contains {len(graph.nodes)} total nodes')

    # Filter out all wall nodes
    moveable_nodes = list(filterfalse(_is_wall_character, graph.nodes))

    graph.logger.debug(
        f'There are {len(moveable_nodes)} moveable positions in this maze')

    node_index = {(n.x, n.y): n for n in moveable_nodes}

    for node in moveable_nodes:
      location = (node.data.x, node.data.y)

      possible_neighbors = [
          (location[0] - 1, location[1]),
          (location[0] + 1, location[1]),
          (location[0], location[1] - 1),
          (location[0], location[1] + 1),
      ]

      neighbors = [
          node_index[neighbor]
          for neighbor in possible_neighbors
          if neighbor in node_index
      ]

      for neighbor in neighbors:
        node.connect_to(neighbor)

      graph.logger.debug(repr(node))

    return graph
