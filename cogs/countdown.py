import discord;
import json;
from discord.commands import slash_command, Option;
from discord.ext import commands
from discord.ui import Button, View

from helpers import generate_embed;

with open("config/mirai.json") as file:
  config = json.load(file);
  
class Countdown(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot;
      
  # Generates the embed going to be sent for the default countdown command    
  def generate_countdown_information_embed(self):
     embed = generate_embed();
     embed.title = "Countdown | Help";
     embed.description = "The Countdown command, as the name suggests, counts down from a specified number of days.\n\nWhen prompted, I will create a separate channel to keep track of the remaining days and will ping you there daily until the end!\n\nTo use this command, simply add your desired days after `/countdown`";

     return embed;     

  def generate_buttons(self):
    confirm_button = Button(label="Let's go!", style=discord.ButtonStyle.success);
    cancel_button = Button(label="Cancel", style=discord.ButtonStyle.secondary);

    view = View();
    view.add_item(cancel_button);
    view.add_item(confirm_button);

    return view;

  # Registering slash command
  @slash_command(guild_ids=config["guildIDs"], description="Starts a countdown from a set number of days")
  async def countdown(self, ctx, days: Option(int, "Enter number of days!", required=False)):
    if not days:
      embed = self.generate_countdown_information_embed();
      return await ctx.respond(embed=embed);

    actions_view = self.generate_buttons();

    return await ctx.respond(f'Coundown with {days} days!', view=actions_view);


def setup(bot: commands.Bot):
  bot.add_cog(Countdown(bot));
