import sqlite3
from sqlite3 import Error

DB_FILE_PATH = "./db.sqlite"
db = sqlite3.connect(DB_FILE_PATH)
db.row_factory = sqlite3.Row


def upload_mutuals_suggestions(suggestions):
  pass

def get_messages():
  query = "SELECT * FROM message"
  return list(db.execute(query))
    