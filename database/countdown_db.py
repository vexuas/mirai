import sqlite3;
import uuid;

class CountdownDatabase():
  def __init__(self, countdown_data):
    self.user = countdown_data["user"];
    self.guild = countdown_data["guild"];
    self.category_channel = countdown_data["category_channel"];
    self.channel = countdown_data["channel"];
    self.days = countdown_data["days"];

  # Initialises connection with database
  # Creates one if it doesn't exist
  def connect_database(self):
    connection = sqlite3.connect('database/mirai.db');
    return connection;

  def create_countdown(self):
    cursor = self.connect_database().cursor();
    cursor.execute("CREATE TABLE IF NOT EXISTS Countdown(uuid)")
    mirai_database = self.connect_database();
    

  