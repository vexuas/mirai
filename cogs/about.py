from discord.commands import slash_command;
from discord.ext import commands;
from helpers import generate_about_embed;

class About(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot;

  @slash_command(guild_ids=[929426428003483720], description="Displays information about Mirai")
  async def about(self, ctx):
    embed = generate_about_embed(self.bot);
    return await ctx.respond(embed=embed);
  

def setup(bot: commands.Bot):
  bot.add_cog(About(bot));
