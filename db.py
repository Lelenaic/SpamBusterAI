from pysondb import PysonDB
from constants import DB_FILE_NAME

class DB:
  def __init__(self):
    self.db = PysonDB(DB_FILE_NAME)
  
  def email_processed(self, email_id: int) -> None:
    print(type(email_id), email_id)
    self.db.add({
      'email_id': email_id,
    })
  
  def is_email_processed(self, email_id: int) -> bool:
    print(email_id)
    return self.db.get_by_query(lambda x: x['email_id'] == email_id) != {}

DB_INSTANCE = DB()
