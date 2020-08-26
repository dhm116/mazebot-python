from enum import Enum


class DirectionCharacters(Enum):
  NORTH: str = 'N'
  SOUTH: str = 'S'
  EAST: str = 'E'
  WEST: str = 'W'


class GraphCharacters(Enum):
  WALL: str = 'X'
  FLOOR: str = ' '
  START: str = 'A'
  END: str = 'B'


class MazeCharacters(Enum):
  WALL: str = u'\uFF38'
  FLOOR: str = u'\u3000'
  START: str = u'\uFF21'
  END: str = u'\uFF22'
  NORTH: str = u'\uFF2E'
  SOUTH: str = u'\uFF33'
  EAST: str = u'\uFF25'
  WEST: str = u'\uFF37'


class BorderCharacters(object):
  TOP: Enum = Enum(
      value='MazeBorderTop',
      names={
          'LEFT': u'\uFF62',
          'RIGHT': u'\uFFA1',
          'MIDDLE': u'\uFFE3',
      },
  )

  BOTTOM: Enum = Enum(
      value='MazeBorderBottom',
      names={
          'LEFT': u'\uFFA4',
          'RIGHT': u'\uFF63',
          'MIDDLE': u'\uFF3F',
      },
  )

  SIDE: Enum = Enum(
      value='MazeBorderSide', names={
          'LEFT': u'\uFFDC',
          'RIGHT': u'\uFF5C',
      })
