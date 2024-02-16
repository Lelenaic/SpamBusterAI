import os
from dotenv import load_dotenv
from mail_manager import MailManager
from spam_ai import SpamAI

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

  with MailManager() as mail_manager:
    mail_manager.check_for_spam()


def check_for_missing_env_var() -> None:
  for var in REQUIRED_ENV_VARS:
    if var not in os.environ:
      raise Exception(f"Missing required environment variable {var}")


if __name__ == '__main__':
  main()
