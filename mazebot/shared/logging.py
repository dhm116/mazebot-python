import logging
from rich.logging import RichHandler


class Logging(object):
  logger: logging.Logger = logging.getLogger('mazebot')
  # handler = logging.StreamHandler()
  handler: logging.Handler = RichHandler(markup=True)
  log_format: logging.Formatter = logging.Formatter(
      '{asctime} {name} {levelname:8s} {message}', style='{')

  @staticmethod
  def initialize() -> None:
    Logging.handler.setFormatter(Logging.log_format)
    Logging.logger.addHandler(Logging.handler)

    Logging.disable_debugging()

  @staticmethod
  def enable_debugging() -> None:
    Logging.logger.setLevel(logging.DEBUG)
    Logging.handler.setLevel(logging.DEBUG)

  @staticmethod
  def disable_debugging() -> None:
    Logging.logger.setLevel(logging.INFO)
    Logging.handler.setLevel(logging.INFO)

  @staticmethod
  def getLogger(suffix: str) -> logging.Logger:
    child_logger = Logging.logger.getChild(suffix)
    child_logger.setLevel(Logging.logger.getEffectiveLevel())

    return child_logger


Logging.initialize()
