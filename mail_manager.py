import os
from mail import Mail
from datetime import datetime
from imaplib import IMAP4_SSL
from spam_ai import SpamAI

class MailManager:

  def __init__(self):
    self.spam_ai = SpamAI()


  def __enter__(self):
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
    today = datetime.today().strftime('%d-%b-%Y')
    # Get today's emails
    _, data = self.imap.search(None, 'ON', today)

    # Loop through the emails
    for id in data[0].split():
      message = Mail(self.imap, id)
      spam_probability = self.get_email_spam_probability(message)

      # Set the message as SPAM
      if spam_probability > int(os.getenv('SPAM_THRESHOLD', 8)):
        message.mark_as_spam()



  def get_email_spam_probability(self, mail: Mail) -> int:
    return self.spam_ai.get_email_spam_probability(mail)


  
