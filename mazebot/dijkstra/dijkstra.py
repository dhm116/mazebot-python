from collections import OrderedDict
import math
from typing import List, Mapping, Optional

from mazebot.dijkstra.collections import LinkedNodeList
from mazebot.dijkstra.priority_queue import PriorityQueue
from mazebot.graph.node import Node
from mazebot.shared.logging import Logging


class Dijkstra(object):

  def __init__(self, nodes: List[Node], starting_node: Optional[Node] = None):
    self.__queue__: PriorityQueue = PriorityQueue()
    self.__nodes__: List[Node] = nodes
    self.__starting_node__: Node = starting_node

    self.__distance_to__: Mapping[Node, float] = {}
    # self.__path_to__: OrderedDict[Node, Node] = OrderedDict()
    self.__path_to__: LinkedNodeList = LinkedNodeList()

    self._initialize_logger()

    self.compute_shortest_path()

  @property
  def distance_to(self) -> Mapping[Node, float]:
    return self.__distance_to__

  @property
  def logger(self):
    return self.__logger__

  @property
  def nodes(self) -> List[Node]:
    return self.__nodes__

  @property
  def path_to(self) -> LinkedNodeList:  # OrderedDict[Node, Node]:
    return self.__path_to__

  @property
  def queue(self) -> PriorityQueue:
    return self.__queue__

  @property
  def starting_node(self) -> Node:
    return self.__starting_node__

  def _initialize_logger(self) -> None:
    self.__logger__ = Logging.getLogger(__name__)

  def compute_shortest_path(self) -> None:
    """Computes the shortest path from the starting node to all of the other
    nodes provided"""
    self.update_distance_of_all_edges_to(math.inf)
    self.distance_to[self.starting_node] = 0

    self.queue.insert(self.starting_node, 0)

    while self.queue.any:
      (node, _) = self.queue.remove_min()
      for neighbor, weight in node.neighbors.items():
        self.relax(node, neighbor, weight)

  def update_distance_of_all_edges_to(self, distance: float) -> None:
    for node in self.nodes:
      self.distance_to[node] = distance

  def relax(self, source: Node, dest: Node, weight: float) -> None:
    """Edge relaxation essentially checks if the shortest known path to a
    given node is still valid (i.e. we didn't find an even shorter path)"""
    if self.distance_to[dest] <= (self.distance_to[source] + weight):
      return

    if self.distance_to[source] == math.inf:
      self.distance_to[source] = 0

    self.distance_to[dest] = self.distance_to[source] + weight
    self.path_to[dest] = source

    self.queue.insert(dest, self.distance_to[dest])

  def shortest_path_to(self, dest: Node) -> List[Node]:
    path: List[Node] = []

    node: Node = dest

    while node is not None and not node == self.starting_node:
      path.append(node)
      node = self.path_to.get(node, None)

    path.append(self.starting_node)

    return path
