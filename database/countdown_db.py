import sqlite3;

from helpers import Helpers;

class CountdownDatabase():
  def __init__(self, countdown_data=None):
    if countdown_data:
      self.uuid = Helpers().generate_uuid();
      self.user = countdown_data and countdown_data["user"];
      self.guild = countdown_data and countdown_data["guild"];
      self.category_channel = countdown_data["category_channel"];
      self.channel = countdown_data["channel"];
      self.days = countdown_data["days"];
    self.create_database();

  # Initialises connection with database
  # Creates one if it doesn't exist
  def connect_database(self):
    connection = sqlite3.connect('database/mirai.db');
    return connection;

  def create_database(self):
    mirai_database = self.connect_database();
    cursor = mirai_database.cursor();
    create_table = """
      CREATE TABLE IF NOT EXISTS
      Countdown(uuid TEXT NOT NULL PRIMARY KEY, days INTEGER NOT NULL, user_name TEXT NOT NULL, user_id INTEGER NOT NULL, guild_name TEXT NOT NULL, guild_id INTEGER NOT NULL, category_channel_id INTEGER NOT NULL, channel_id INTEGER NOT NULL)
    """
    return cursor.execute(create_table);
    
  def create_countdown(self):
    mirai_database = self.connect_database();
    cursor = mirai_database.cursor();
    insert_countdown = f"""
      INSERT INTO
      Countdown VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insert_countdown, (self.uuid, self.days, self.user.name, self.user.id, self.guild.name, self.guild.id, self.category_channel.id, self.channel.id));
    
    return mirai_database.commit();
    
    
    

    

  