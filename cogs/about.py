from discord.commands import slash_command;
from discord.ext import commands;

class About(commands.Cog):
  """Displays information about Mirai"""

  def __init__(self, bot: commands.Bot):
    self.bot = bot;

  slash_command(guild_ids=[929426428003483720])
  async def about(self, ctx):
    await ctx.respond('Hello!');


def setup(bot: commands.Bot):
  bot.add_cog(About(bot));
