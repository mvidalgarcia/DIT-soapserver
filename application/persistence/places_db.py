#!/usr/bin/python
import MySQLdb

class PlacesDB:
  # DB constructor
  def __init__(self):
    # Database connection.
    self.db = MySQLdb.connect("localhost", user="dit", passwd="dit", db="dit")
    # Cursor object to execute queries.
    self.cur= self.db.cursor()
    self.result = {}
  
  # DB functions
  def get_categories(self):
    # Query categories
    self.cur.execute("SELECT * FROM category")
  
    # Store in a dictonary. {id: 'category', ...} 
    for row in self.cur.fetchall():
      self.result[row[0]] = row[1]
    return self.result

