from dotenv import load_dotenv
from mail_manager import MailManager
from spam_ai import SpamAI

load_dotenv()


def main():
  with MailManager() as mail_manager:
    mail_manager.check_for_spam()


if __name__ == '__main__':
  main()
