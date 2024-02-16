from pysondb import PysonDB
from src.constants import DB_FILE_NAME

class DB:
  def __init__(self):
    self.db = PysonDB(DB_FILE_NAME)
  
  def email_processed(self, email_id: bytes) -> None:
    self.db.add({
      'email_id': email_id.decode(),
    })
  
  def is_email_processed(self, email_id: bytes) -> bool:
    print(email_id)
    return self.db.get_by_query(lambda x: x['email_id'] == email_id.decode()) != {}

DB_INSTANCE = DB()
