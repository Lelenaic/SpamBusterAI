import os
import sched, time
from dotenv import load_dotenv
from src.mail_manager import MailManager
from src.logger import LOGGER
from src.constants import DEFAULT_RUN_INTERVAL

load_dotenv()

REQUIRED_ENV_VARS = [
  'EMAIL',
  'PASSWORD',
  'HOST',
  'PORT',
  'TLS',
  'OPENAI_API_KEY',
  'AI_MODEL'
]


def main() -> None:
  check_for_missing_env_var()
  start()


def start() -> None:
  with MailManager() as mail_manager:
    mail_manager.check_for_spam()
  
  interval = int(os.getenv('RUN_INTERVAL', DEFAULT_RUN_INTERVAL))
  scheduler = sched.scheduler(time.time, time.sleep)
  scheduler.enter(interval, 1, start, ())
  LOGGER.log(f'Next run in {interval} seconds')
  scheduler.run()

def check_for_missing_env_var() -> None:
  for var in REQUIRED_ENV_VARS:
    if var not in os.environ:
      raise Exception(f'Missing required environment variable {var}')


if __name__ == '__main__':
  main()
