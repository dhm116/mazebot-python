from __future__ import annotations

import heapq
import itertools
from typing import Generic, Iterator, List, Mapping, Tuple, Union, TypeVar

K = TypeVar('K')  # Key Generic
V = TypeVar('V', int, float)
QueueEntry = Tuple[V, int, K]

REMOVED = '<removed-task>'


class PriorityQueue(Generic[K, V]):

  def __init__(self):
    self.__counter__: Iterator = itertools.count()
    self.__key_map__: Mapping[K, QueueEntry] = {}
    self.__queue__: List[QueueEntry] = []

  @property
  def counter(self) -> Iterator:
    return self.__counter__

  @property
  def queue(self) -> List[Tuple[K, V]]:
    return self.__queue__

  @property
  def any(self) -> bool:
    """Returns `True` if there are any values currently in the `queue`,
    `False` otherwise"""
    return len(self.queue) > 0

  def insert(self, key: K, value: V) -> None:
    """Adds or updates K/V pairs to the queue and re-prioritizes the entries"""
    if key in self.__key_map__:
      self.remove(key)

    entry = (value, next(self.counter), key)
    self.__key_map__[key] = entry

    heapq.heappush(self.queue, entry)

  def remove_min(self) -> Tuple[K, V]:
    """Removes the first item (lowest value) from the queue and returns it"""
    while self.queue:
      # pylint: disable=unused-variable
      value, count, key = heapq.heappop(self.queue)
      if value is not REMOVED:
        del self.__key_map__[key]
        return (key, value)
    return None

  def remove(self, key: K) -> None:
    entry = self.__key_map__.pop(key, None)

    if entry is not None:
      entry[-1] = REMOVED
