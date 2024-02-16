import os
from datetime import datetime
from constants import DEFAULT_LOG_LEVEL

class Logger():
  def log(self, message, level: int = 1) -> None:
    if level <= int(os.getenv('LOG_LEVEL', DEFAULT_LOG_LEVEL)):
      print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {message}')


LOGGER = Logger()
