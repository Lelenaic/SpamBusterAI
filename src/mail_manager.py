import os
from datetime import datetime
from imaplib import IMAP4_SSL
from src.mail import Mail
from src.spam_ai import SpamAI
from src.db import DB_INSTANCE
from src.logger import LOGGER
from src.constants import LOGGER_SUBJECT_MAX_LENGTH, DEFAULT_SPAM_THRESHOLD

class MailManager:

  def __init__(self):
    self.spam_ai = SpamAI()


  def __enter__(self):
    LOGGER.log('Connecting to IMAP server', 2)
    self.imap = IMAP4_SSL(os.getenv('HOST'), os.getenv('PORT'))
    # Login
    self.imap.login(os.getenv('EMAIL'), os.getenv('PASSWORD'))
    # Select the mailbox
    self.imap.select('inbox')

    return self


  def __exit__(self, *args):
    # Close the mailbox 
    self.imap.close()
    # End the imap connexion
    self.imap.logout()


  def check_for_spam(self) -> None:
    LOGGER.log('Getting today\'s emails', 2)
    today = datetime.today().strftime('%d-%b-%Y')
    # Get today's emails
    _, data = self.imap.uid('search', None, 'ON', today)

    LOGGER.log(f'Checking {len(data[0].split())} emails for SPAM')
    # Loop through the emails
    for id in data[0].split():
      LOGGER.log(f'Processing email {id}')
      if DB_INSTANCE.is_email_processed(id):
        LOGGER.log(f'Email {id} already processed, skipping', 2)
        continue

      message = Mail(self.imap, id)
      try :
        spam_probability = self.spam_ai.get_email_spam_probability(message)

        # Set the message as SPAM
        if spam_probability > int(os.getenv('SPAM_THRESHOLD', DEFAULT_SPAM_THRESHOLD)):
          LOGGER.log(f'Email {message.subject[:LOGGER_SUBJECT_MAX_LENGTH]} is SPAM with a probability of {spam_probability}/10')
          message.mark_as_spam()
        else:
          LOGGER.log(f'Email {message.subject[:LOGGER_SUBJECT_MAX_LENGTH]} is not SPAM with a probability of {spam_probability}/10')
      except Exception as e:
        LOGGER.log(e)
      finally:
        message.mark_as_unread()
        DB_INSTANCE.email_processed(id)
