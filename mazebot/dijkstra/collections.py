from __future__ import annotations

from collections import OrderedDict
from typing import (Dict, ItemsView, Iterator, List, KeysView, Tuple, Union,
                    ValuesView)
from mazebot.graph.node import Node

NodeIterator = Iterator[Node]
# pylint: disable=used-before-assignment
DictTypes = Union[Dict, 'LinkedNodeList', OrderedDict]
"""
Pretty sure I wasted a lot of time on this idea...
"""


class LinkedNodeList(object):

  def __init__(self):
    self.clear()

  def add(self, key: Node, value: Node) -> None:
    """Adds a new key-value pair to the list"""
    self.__dict__[key] = value

  def clear(self) -> None:
    """Removes all items from the list"""
    self.__dict__ = OrderedDict()

  def copy(self) -> LinkedNodeList:
    """Returns a shallow copy of the list"""
    clone = LinkedNodeList()
    clone.update(self.__dict__)
    return clone

  def get(self, key: Node, default: Node = None) -> Node:
    """Returns the value for `key` if `key` is present in the list, else `default`. If
    `default` is not provided, it defaults to `None`"""
    return self.__dict__.get(key, default)

  def items(self) -> ItemsView[Tuple[Node, Node]]:
    return self.__dict__.items()

  def keys(self) -> KeysView[Node]:
    return self.__dict__.keys()

  def pop(self, key: Node, default: Node = None) -> Node:
    return self.__dict__.pop(key, default)

  def popitem(self) -> Tuple[Node, Node]:
    return self.__dict__.popitem()

  def setdefault(self, key: Node, default: Node = None) -> Node:
    return self.__dict__.setdefault(key, default)

  def update(self, *others: DictTypes, **kwargs: Dict[Node, Node]) -> None:
    """Update the list with the key-value pairs from `*others`, overwriting existing
    keys"""
    self.__dict__.update(*others, **kwargs)

  def values(self) -> ValuesView[Node]:
    return self.__dict__.values()

  def __contains__(self, node: Node) -> bool:
    search = filter(lambda pair: node in pair, self.__dict__.items())
    return len(list(search)) > 0

  def __delitem__(self, key: Node) -> None:
    del self.__dict__[key]

  def __getitem__(self, key: Node) -> Node:
    return self.__dict__[key]

  def __len__(self) -> int:
    return len(self.__dict__)

  def __reversed__(self) -> NodeIterator:
    for key, value in reversed(self.__dict__):
      yield value
      yield key

  def __setitem__(self, key: Node, value: Node) -> None:
    self.add(key, value)

  def __iter__(self) -> NodeIterator:
    for key, value in self.__dict__.items():
      yield key
      yield value
