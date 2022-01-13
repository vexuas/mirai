import sqlite3;
import datetime;

from helpers import Helpers
from timer.day_timer import DayTimer;

# All things countdown data related
# Getting the hang of classes pog
class CountdownDatabase():
  def __init__(self, countdown_data=None):
    # We only want to keep track of data if it's passed in
    if countdown_data:
      self.uuid = Helpers().generate_uuid();
      self.user = countdown_data and countdown_data["user"];
      self.guild = countdown_data and countdown_data["guild"];
      self.category_channel = countdown_data["category_channel"];
      self.channel = countdown_data["channel"];
      self.days = countdown_data["days"];
      self.started_at = datetime.datetime.now();
      self.ends_at = datetime.datetime.now() + datetime.timedelta(days=countdown_data["days"]);
    self.create_database(); # creates database with table if it doesn't exist every time class is called

  # Initialises connection with database
  # Creates one if it doesn't exist
  def connect_database(self):
    connection = sqlite3.connect('database/mirai.db');
    return connection;

  # Creates main table with relevant columns
  # I stringified uuid since seems too much to create an adapter to make uuid types to work
  # TODO: Add date created and date ending for countdown
  def create_database(self):
    mirai_database = self.connect_database();
    cursor = mirai_database.cursor();
    create_table = """
      CREATE TABLE IF NOT EXISTS
      Countdown(uuid TEXT NOT NULL PRIMARY KEY, days INTEGER NOT NULL, started_at DATE NOT NULL, ends_at DATE NOT NULL, user_name TEXT NOT NULL, user_id INTEGER NOT NULL, guild_name TEXT NOT NULL, guild_id INTEGER NOT NULL, category_channel_id INTEGER NOT NULL, channel_id INTEGER NOT NULL)
    """
    return cursor.execute(create_table);
    
  # Inserts new countdown to our database
  # There might be a better way to insert data; settled with this qmark style since it's straightforward albeit constrained 
  def create_countdown(self):
    mirai_database = self.connect_database();
    cursor = mirai_database.cursor();
    insert_countdown = f"""
      INSERT INTO
      Countdown VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insert_countdown, (self.uuid, self.days, self.started_at, self.ends_at, self.user.name, self.user.id, self.guild.name, self.guild.id, self.category_channel.id, self.channel.id));
    
    return mirai_database.commit();
    
  # Retrieves a countdown from our database
  # By default, the data returned would be in a tuple
  # To change this, I've made a factory below that transforms the data into a dictionary  
  # Found a better way to link variables in a sql statement; will keep both patterns for learnings
  # user_id: id of user who initialised command
  # guild_id: id of guild where command was initialised
  def get_countdown(self, user_id, guild_id):
    mirai_database = self.connect_database();
    mirai_database.row_factory = self.dict_factory # Tells the database to transform data into a dictionary
    cursor = mirai_database.cursor();
    get_countdown = f"""
      SELECT * FROM Countdown WHERE user_id=:user_id AND guild_id=:guild_id
    """

    cursor.execute(get_countdown, {"user_id" : user_id, "guild_id": guild_id});
    countdown = cursor.fetchone();
    DayTimer(countdown);
    return countdown;
    
  # Deletes a countdown from our database  
  # uuid: unique identifier of countdown
  def delete_countdown(self, uuid):
    mirai_database = self.connect_database();
    cursor = mirai_database.cursor();
    delete_countdown = f"""
      DELETE FROM Countdown WHERE uuid=:uuid
    """

    cursor.execute(delete_countdown, {"uuid": uuid});
    return mirai_database.commit();
    
  # Changes data into a dictionary  
  def dict_factory(self, cursor, row):
    d = {};
    for index, col in enumerate(cursor.description):
      d[col[0]] = row[index];
    return d;
