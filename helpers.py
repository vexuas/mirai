import discord;
import uuid;

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
