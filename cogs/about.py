import json;
from discord.commands import slash_command;
from discord.ext import commands;

from helpers import Helpers;

# Reads package.json file; mostly to retrieve bot version
with open("package.json") as file:
  package = json.load(file);
  
with open("config/mirai.json") as file:
  config = json.load(file);

class About(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot;

  # Generates the embed going to be sent for the about command
  # client: initialising discord client
  def generate_about_embed(self):
    embed = Helpers().generate_embed();
    embed.title = "About";
    embed.description = "Hi there! I'm Mirai and I'm a simple bot that counts down from a set number of days!\n\nMy creator made me as it helps him stay focused and keep him in check with his personal goals. Also because he wanted to create his first Python Project!\n\nI hope I can help you as much as I've helped him! (◕ᴗ◕✿)";

    embed.add_field(name="Creator", value="Vexuas#8141", inline=True);
    embed.add_field(name="Date Created", value=self.bot.user.created_at.strftime('%d-%b-%Y'), inline=True);
    embed.add_field(name="Version", value=package["version"], inline=True);
    embed.add_field(name="Library", value="Pycord", inline=True);
    embed.add_field(name="Last Update", value="24-Jan-2022", inline=True);
    embed.add_field(name="Source Code", value="[Github](https://github.com/vexuas/mirai)", inline=True);

    return embed;

  # Register slash command and main handler for initialisation
  @slash_command(description="Displays information about Mirai")
  async def about(self, ctx):
    try:
      embed = self.generate_about_embed();
      return await ctx.respond(embed=embed);
    except Exception as error:
      error_embed = Helpers().generate_error_embed("Oops something went wrong! D: Try again in a bit!");
      await ctx.respond(embed=error_embed);
      return await Helpers().send_error_log(self.bot, ctx, error, "About Command");


def setup(bot: commands.Bot):
  bot.add_cog(About(bot));
