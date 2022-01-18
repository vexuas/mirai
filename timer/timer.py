import datetime;
import asyncio
import discord;

from discord.ui import Button, View
from database.countdown_db import CountdownDatabase;

from helpers import Helpers;

# All things timer related
# Out of all the things, this was probably the toughest to implement
# The recurring timer itself isn't much of an issue, more on the Python approach of things
# With javascript slapping a setInterval is good enough, here I found out isn't as straightforward
# Ended up using asyncio since it's far easier to use instead of Timer
# Although not really sure if I'm using it right; if it works it works *shrug*
# TODO: Figure out how to properly cancel existing asyncio sleep tasks when stopping countdown
class Timer():
  # Timer initialisation
  # channel: discord TextChannel - for sending purposes
  # user: discord User - for pinging purposes
  # countdown: countdown instance from our database
  # type: if timer should use days or minutes; latter more on testing but could be an additional feature in the future
  def __init__(self, bot, channel, user, countdown, type="day"):
    self.bot = bot;
    self.date_now = datetime.datetime.now();
    self.started_at = Helpers().format_to_datetime(countdown["started_at"]);
    self.ends_at = Helpers().format_to_datetime(countdown["ends_at"]);
    self.days = countdown["days"];
    self.countdown_uuid = countdown["uuid"];
    self.user = user;
    self.channel = channel;
    self.type = type;

    # Sets up timer pointers based on days or minutes
    if self.type == 'day':
      self.passed_time = (self.date_now - self.started_at).days;
      self.current_time = self.days - self.passed_time;
      self.next_date = self.started_at + datetime.timedelta(days=self.passed_time + 1);
    if self.type == 'minute':
      self.ends_at = self.started_at + datetime.timedelta(minutes=countdown["days"]);
      self.passed_time = ((self.date_now - self.started_at).seconds // 60) % 60;
      self.current_time = self.days - self.passed_time;
      self.next_date = self.started_at + datetime.timedelta(minutes=self.passed_time + 1);

  # Starts timer
  # In essence, the whole timer works as a bundle of individual day timers
  # This means that after a timer is done for the day, we create a new timer for the next day after
  # In order to do this, this start function calls itself after it finishes the day timer
  # This continues until the current time is after the end date; which in turn would send the end countdown message
  async def start(self):
    if(self.date_now < self.ends_at):
      difference = (self.next_date - self.date_now).seconds # seconds between current time and the time when day should be passed over
      await self.start_day_timer(self.user, self.channel, difference, self.current_time); # start individual day timer
      # Deletes existing countdown message
      # This is so we can properly ping the user in a new message when the day timer gets called again
      countdown = CountdownDatabase().get_countdown(uuid=self.countdown_uuid);

      # Wrapping the next timer calls in a countdown existence conditional
      # I'll admit this is a ghetto alternative
      # The proper way is to clear the existing asyncio tasks when we stop a countdown
      # However, I'm not too versed with the module yet
      # As the timer task isn't cleared, it will continue and finish leading to the methods below
      # It will run into an error when trying to get the message as countdown doesn't exist anymore
      # Hence to prevent that, this condition is made. Told you it was ghetto, maybe I'll refactor in the future
      if countdown:
        message = self.channel.get_partial_message(countdown["message_id"]);
        await message.delete();

        await asyncio.sleep(3); # Buffer time; perhaps there's a better way of going about this
        self.update_next_timer(); # Updates timer pointers for the next day
        return await self.start(); # Calls itself
    else:
      # Send end of countdown message
      embed = self.generate_end_countdown_embed();
      view = self.generate_button();
      await self.channel.edit(name=f"{self.user.name}-end"); # channel edit rate limit is 2 per 10 minutes
      end_message = await self.channel.send(f'{self.user.mention}', embed=embed, view=view);
      return CountdownDatabase().update_countdown_message(end_message.id, self.countdown_uuid);
    
  # Updates timer pointers for next day
  # Important to keep the timer flowing
  def update_next_timer(self):
    self.date_now = datetime.datetime.now();
    if self.type == 'day':
      self.passed_time = (self.date_now - self.started_at).days;
      self.current_time = self.days - self.passed_time;
      self.next_date = self.started_at + datetime.timedelta(days=self.passed_time + 1);
    if self.type == 'minute':
      self.passed_time = ((self.date_now - self.started_at).seconds // 60) % 60;
      self.current_time = self.days - self.passed_time;
      self.next_date = self.started_at + datetime.timedelta(minutes=self.passed_time + 1);

  # Individual day timer
  # Sends a message to the countdown channel with the current day counter
  # Then waits until the time when the day should be passed over
  # user: discord User
  # channel: discord TextChannel
  # difference: seconds between current time and the time when day should be passed over
  # current: the current day the countdown is in
  # Maybe refactor this to not use passed in arguments
  async def start_day_timer(self, user, channel, difference, current):  
    async def start_countdown():
      countdown_content = f"{user.mention} Day {current}! Good luck :D" if current == self.days else f"{user.mention} Day {current}"
      current != self.days and await self.channel.edit(name=f"{self.user.name}-day-{current}"); # channel edit rate limit is 2 per 10 minutes
      countdown_message = await channel.send(countdown_content);

      CountdownDatabase().update_countdown_message(countdown_message.id, self.countdown_uuid);

      return await asyncio.sleep(difference);

    return await start_countdown()

  # Generates embed for the end countdown message
  def generate_end_countdown_embed(self):
    embed = Helpers().generate_embed();
    embed.title = "Day 0";
    embed.description = "End Reached!\n\nI hope you got close to your goal! :D\n\nTo close this channel, click the button below";
    
    return embed;

  # Generates close button for end countdown message
  def generate_button(self):
    close_button = Button(label="Close", style=discord.ButtonStyle.secondary);
    view = View();
    view.add_item(close_button);
    close_button.callback = self.handle_on_close;
    
    return view;

  # Interaction handler when user clicks on close button
  # Deletes countdown instance from our database
  # Then deletes the countdown category and channel
  async def handle_on_close(self, interaction):
    try:
      CountdownDatabase().delete_countdown(self.countdown_uuid);
      await interaction.channel.category.delete();
      return await interaction.channel.delete();
    except Exception as e:
      error_embed = Helpers().generate_error_embed("Oops something went wrong! D:\n\n I've notified the owner about the problem, feel free to delete this channel!");
      await interaction.response.edit_message(embed=error_embed, view=None);
      return await Helpers().send_error_log(self.bot, e);
