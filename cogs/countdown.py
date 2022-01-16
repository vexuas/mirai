import discord;
import json;

from discord.commands import slash_command, Option;
from discord.ext import commands;
from discord.ui import Button, View;
from database.countdown_db import CountdownDatabase;

from helpers import Helpers
from timer.timer import Timer;

with open("config/mirai.json") as file:
  config = json.load(file);
  
class Countdown(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot;
      
  # Generates embed going to be sent for the default countdown command    
  def generate_countdown_information_embed(self):
    embed = Helpers().generate_embed();
    embed.title = "Countdown | Help";
    embed.description = "The Countdown command, as the name suggests, counts down from a specified number of days.\n\nWhen prompted, I will create a separate channel to keep track of the remaining days and will ping you there daily until the end!\n\nTo use this command, simply add your desired days after `/countdown`";

    return embed;     

  # Generates embed going to be sent when confirming the countdown command
  # This is shown when the user uses the countdown command with the days argument
  # days: number of days - int
  def generate_countdown_confirmation_embed(self, days):
    embed = Helpers().generate_embed();
    embed.title = "Countdown | Confirmation";
    embed.description = f"You've created a countdown of {days} days.\n\nBy confirming below, I'll create a separate channel where I'll ping you daily on the number of days left\n\nGood luck with your goal! :D"

    return embed;

  # Generates the buttons view
  # Components need to be inside a View for them to properly work; View can be taken as a container
  # Buttons are inserted and pushed to the right with subsequent additions
  # A tad bit frustrating as there's currently no option to make them float right; Messages look off with buttons and a long length embed
  # Maybe check if components can be inserted inside an embed
  def generate_buttons(self):
    confirm_button = Button(label="Let's go!", style=discord.ButtonStyle.success);
    cancel_button = Button(label="Cancel", style=discord.ButtonStyle.secondary);

    view = View();
    view.add_item(cancel_button);
    view.add_item(confirm_button);

    confirm_button.callback = self.handle_on_confirm;
    cancel_button.callback = self.handle_on_cancel;
    
    return view;

  # Handler when a user clicks the Cancel Button
  # Edits the original message with a new embed and clears buttons
  async def handle_on_cancel(self, interaction):
    embed = discord.Embed();
    embed.color = discord.Colour(16711680);
    embed.description = "Cancelled Countdown";

    return await interaction.response.edit_message(embed=embed, view=None);

  # Handler when a user clicks the Let's go Button
  # 4 parts:
  # - Creates a new channel under a new category
  # - Creates a countdown instance in our database
  # - Edits the original interaction message with a success message with a link to the newly created channel
  # - Finally starts the countdown timer
  # I initially wanted to move the user to the text channel but seems discord doesn't support that; only voice channel movement. 
  # I guess it's hard to keep track and merits probably doesn't outweight the implementation
  async def handle_on_confirm(self, interaction):
    # Creates a new channel under a new category
    current_guild = await self.bot.fetch_guild(interaction.guild_id);
    countdown_category = await current_guild.create_category('Mirai Countdown');
    countdown_channel = await countdown_category.create_text_channel(f'{interaction.user.name}-day-{self.days}');

    # Creates a countdown instance in our database
    # More information in countdown_db
    CountdownDatabase({
      "user": interaction.user,
      "guild": current_guild,
      "category_channel": countdown_category,
      "channel": countdown_channel,
      "days": self.days      
    }).create_countdown();

    # Edits original interaction message with link to new channel
    embed = discord.Embed();
    embed.color = discord.Colour(3066993);
    embed.description = f"Countdown successfully set in {countdown_channel.mention}!";
    await interaction.response.edit_message(embed=embed, view=None);

    # Calls the start_countdown function to start timer
    return await self.start_countdown(interaction.user.id, interaction.guild.id);

  # Starts countdown timer
  # Retrieves countdown instance from our database 
  # Also retrieves user and channel data from discord; this is so we can properly send messages and mention the user
  # Finally calls the Timer class to start timer; more information in timer.py
  # user_id: id of user who started the countdown
  # guild_id: id of guild where countdown was started
  async def start_countdown(self, user_id, guild_id):
    countdown = CountdownDatabase().get_countdown(user_id, guild_id);
    countdown_channel = self.bot.get_channel(countdown["channel_id"]);
    user = await self.bot.fetch_user(countdown["user_id"]);

    return await Timer(countdown_channel, user, countdown).start();

  # Register slash command and main handler for initialisation
  @slash_command(description="Starts a countdown from a set number of days")
  async def countdown(self, ctx, days: Option(int, "Enter number of days!", required=False), stop: Option(discord.TextChannel, "Stops an existing countdown", required=False)):
    # If no options are passed, we show the command information
    if not days and not stop:
      embed = self.generate_countdown_information_embed();
      return await ctx.respond(embed=embed);

    # Checks if the user has an existing countdown within the guild  
    user_countdown = CountdownDatabase().get_countdown(ctx.user.id, ctx.guild.id);

    # Stop option handler
    # If user has a countdown in the guild and selects the countdown channel
    # - We delete the category channel and the countdown channel
    # - We then delete the countdown instance in our database
    # - Finally we end an appropriate embed message
    # If user doesn't have a countdown nor selected an existing countdown channel
    # - Send a warning message that there's no countdown linked to the user
    if stop:
      embed = discord.Embed();
      if user_countdown and stop.id == user_countdown["channel_id"]:
        countdown_channel = self.bot.get_channel(user_countdown["channel_id"]);
        CountdownDatabase().delete_countdown(user_countdown["uuid"]);
        await countdown_channel.category.delete();
        await countdown_channel.delete();
        embed.color = discord.Colour(16711680);
        embed.description = f"Stopped Countdown";
        return await ctx.respond(embed=embed);

      embed.color = discord.Colour(16776960);
      embed.description = "Selected channel doesn't have a countdown linked to user";
      return await ctx.respond(embed=embed);

    # Days option handler
    # If the user has an existing countdown
    # - We send a warning with a link to the existing countdown channel
    # Else we send the countdown confirmation message
    if user_countdown:
      countdown_channel = self.bot.get_channel(user_countdown["channel_id"]);
      embed = discord.Embed();
      embed.color = discord.Colour(16776960);
      embed.description = f'You already have a countdown set in {countdown_channel.mention}';
      
      return await ctx.respond(embed=embed);
      
    self.days = days;
    actions_view = self.generate_buttons();
    embed = self.generate_countdown_confirmation_embed(days);

    return await ctx.respond(embed=embed, view=actions_view);


def setup(bot: commands.Bot):
  bot.add_cog(Countdown(bot));
