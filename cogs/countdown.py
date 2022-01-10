from discord.commands import slash_command, Option;
from discord.ext import commands;

class Countdown(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot;

  @slash_command(guild_ids=[929426428003483720], description="Starts a countdown from a set number of days")
  async def countdown(self, ctx, days: Option(int, "Enter number of days!", required=False)):
    if not days:
      return await ctx.respond('Countdown information!');
      
    return await ctx.respond(f'Coundown with {days} days!');
      

def setup(bot: commands.Bot):
  bot.add_cog(Countdown(bot));
