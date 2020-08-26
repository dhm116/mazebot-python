from typing import Iterator, List
from mazebot.shared.logging import Logging


def chunkify(data: List, chunk_size: int) -> List[List]:
  return list(iter_chunkify(data, chunk_size))


def iter_chunkify(data: List, chunk_size: int) -> Iterator[List]:
  return (data[x:x + chunk_size] for x in range(0, len(data), chunk_size))


def _is_dunder(attr):
  return attr.startswith('__') and attr.endswith('__')


class ObjectDict(object):
  # By default, just assign any incoming keyword arguments as instance attributes
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)

    self._initialize_logger()

  @property
  def logger(self):
    return self.__logger__

  @classmethod
  def from_dict(cls, data):
    return cls(**data)

  def _initialize_logger(self):
    self.__logger__ = Logging.getLogger(__name__)

  def __repr__(self):
    cls_name = type(self).__name__
    args_str = []

    items = [(key, value)
             for key, value in self.__dict__.items()
             if not _is_dunder(key)]

    for name, value in sorted(items):
      args_str.append(f'{name}={value}')
    return f'{cls_name}({", ".join(args_str)})'
