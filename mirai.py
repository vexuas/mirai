import discord;
import json
import datetime;

from database.countdown_db import CountdownDatabase
from helpers import Helpers
from timer.timer import Timer;

mirai = discord.Bot();

# Reads config json file
with open("config/mirai.json") as file:
  config = json.load(file);
  
# Event handlers  
@mirai.event
# Function that fires when mirai boots up and successfully logs in
async def on_ready():
  dev_channel = mirai.get_channel(929427727033982986);
  await dev_channel.send("I'm booting up! (◕ᴗ◕✿)");
  countdowns = CountdownDatabase().get_all_countdowns();
  for countdown in countdowns:
    countdown_channel = mirai.get_channel(countdown["channel_id"]);
    if datetime.datetime.now() < Helpers().format_to_datetime(countdown["ends_at"]):
      countdown_message = countdown_channel.get_partial_message(countdown["message_id"]);
      user = await mirai.fetch_user(countdown["user_id"]);
      await countdown_message.delete();
      await Timer(countdown_channel, user, countdown, type="minute").start();
    else:
      await countdown_channel.category.delete();
      await countdown_channel.delete();
      CountdownDatabase().delete_countdown(uuid=countdown["uuid"]);
      

  # TODO: Start existing countdowns
  # TODO: Delete countdowns that already have ended

# Loads cogs into mirai
# TODO: Make it a loop of the whole cogs folder
mirai.load_extension('cogs.about');
mirai.load_extension('cogs.countdown');

mirai.run(config["token"]);
