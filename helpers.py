import discord;
import uuid;
import datetime;

class Helpers():
  def __init__(self) -> None:
    pass

  # Function to generate a default embed
  def generate_embed(self):
    embed = discord.Embed();
    embed.colour = discord.Colour(10699547);
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/248430185463021569/929419612234321950/mirai.jpg");

    return embed;

  # Generates a UUID
  def generate_uuid(self):
    return str(uuid.uuid4());

  def format_to_datetime(self, date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f');

  async def send_error_log(self, bot, error):
    dev_channel = bot.get_channel(933016043310440519);
    return await dev_channel.send(str(error));

  def generate_error_embed(self, message):
    embed = discord.Embed();
    embed.color = discord.Colour(16711680);
    embed.description = message;
    
    return embed;
