import os
from email.header import decode_header
from email import message_from_bytes

GMAIL_IMAP_SERVER = 'imap.gmail.com'


class Mail:
  def __init__(self, imap, id):
    self.imap = imap
    self.id = id
    
    # We get the status here because we wanna know if the email was unread before we read it
    _, self.initial_status = self.imap.fetch(self.id, '(FLAGS)')
    _, msg_data = self.imap.fetch(id, '(RFC822)')
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
          self.sender = self.raw_email["From"]

          # Get the sender email address
          self.sender_email = self.raw_email["Return-Path"]


  def mark_as_unread(self) -> None:
    # Because we read the email to get the subject and body, if it was unread, mark it as unread, 
    if b'\\Seen' not in self.initial_status[0]:
      self.imap.store(self.id, '-FLAGS', '\\Seen')


  def get_subject(self) -> str:
    subject = decode_header(self.raw_email["Subject"])[0][0]
    if isinstance(subject, bytes):
      subject = subject.decode(decode_header(self.raw_email["Subject"])[0][1])
    
    return subject


  def get_body(self) -> str:
    if self.raw_email.is_multipart():
      for part in self.raw_email.walk():
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition"))
        try:
          body = part.get_payload(decode=True).decode()
        except:
          pass
        if content_type == "text/plain" and "attachment" not in content_disposition:
          message_content = body
    else:
      content_type = self.raw_email.get_content_type()
      body = self.raw_email.get_payload(decode=True).decode()
      if content_type == "text/plain":
        message_content = body
    
    return message_content


  def mark_as_spam(self) -> None:
    if os.getenv('HOST') == GMAIL_IMAP_SERVER:
      self.imap.store(self.id, '+X-GM-LABELS', '\\Spam')

    # Move the email in spam folder
    self.imap.copy(self.id, 'Spam')
    self.imap.store(self.id, '+FLAGS', '\\Deleted')
    self.imap.expunge()
