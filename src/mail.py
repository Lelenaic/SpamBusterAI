import os
from email.header import decode_header
from email import message_from_bytes
from bs4 import BeautifulSoup
import html2text
from src.logger import LOGGER
from src.constants import GMAIL_IMAP_SERVER, LOGGER_SUBJECT_MAX_LENGTH

class Mail:
  def __init__(self, imap, id):
    self.imap = imap
    self.id = id
    
    LOGGER.log(f'Getting email {self.id} from IMAP server')
    # We get the status here because we wanna know if the email was unread before we read it
    _, self.initial_status = self.imap.uid('fetch', self.id, '(FLAGS)')
    _, msg_data = self.imap.uid('fetch', self.id, '(RFC822)')
    # We use a for and if because the python imap library
    # returns multiple parts for an email, only the tuple part is the email
    # other parts are the email flags or metadata
    for response_part in msg_data:
      if isinstance(response_part, tuple):
          # Decode the bytes to get the message
          self.raw_email = message_from_bytes(response_part[1])

          # Get the email subject
          self.subject = self.get_subject()
          
          # Get the email body
          self.body = self.get_body()

          # Get the sender name
          self.sender = self.raw_email['From']

          # Get the sender email address
          self.sender_email = self.raw_email['Return-Path']


  def mark_as_unread(self) -> None:
    # Because we read the email to get the subject and body, if it was unread, mark it as unread, 
    if b'\\Seen' not in self.initial_status[0]:
      self.imap.uid('store', self.id, '-FLAGS', '\\Seen')


  def get_subject(self) -> str:
    header = decode_header(self.raw_email['Subject'])[0]
    subject = header[0]
    encoding = header[1]

    if isinstance(subject, bytes):
        if encoding is None or encoding.lower() == 'unknown-8bit':
            encoding = 'utf-8'
        subject = subject.decode(encoding)
    
    return subject


  def get_body(self) -> str:
    if self.raw_email.is_multipart():
      # The mail is in multiple parts
      for part in self.raw_email.walk():
        content_type = part.get_content_type()
        content_disposition = str(part.get('Content-Disposition'))
        try:
          body = part.get_payload(decode=True).decode()
        except:
          pass
        if content_type == 'text/plain' and 'attachment' not in content_disposition:
          message_content = body
        elif content_type == 'text/html' and 'attachment' not in content_disposition:
          message_content = self.html_to_text(body)
    else:
      # The mail is only one part, so decode it and get the text
      content_type = self.raw_email.get_content_type()
      body = self.raw_email.get_payload(decode=True).decode()
      # If it's only text, juste get it
      if content_type == 'text/plain':
        message_content = body
      # It's HTML, so transform it into text
      elif content_type == 'text/html':
        message_content = self.html_to_text(body)
    
    return message_content

  def html_to_text(self, html: str) -> str:
    h = html2text.HTML2Text()
    h.ignore_links = False
    return h.handle(html)
    # soup = BeautifulSoup(html, 'lxml')
    # return soup.get_text()

  def mark_as_spam(self) -> None:
    LOGGER.log(f'Marking email {self.subject[:LOGGER_SUBJECT_MAX_LENGTH]} as SPAM', 2)
    if os.getenv('HOST') == GMAIL_IMAP_SERVER:
      self.imap.uid('store', self.id, '+X-GM-LABELS', '\\Spam')

    # Move the email in spam folder
    self.imap.uid('copy', self.id, 'Spam')
    self.imap.uid('store', self.id, '+FLAGS', '\\Deleted')
    self.imap.expunge()
    LOGGER.log(f'Done marking email {self.subject[:LOGGER_SUBJECT_MAX_LENGTH]} as SPAM', 3)
