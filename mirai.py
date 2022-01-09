import discord;
import json;

mirai = discord.Bot();

# Reads config json file
with open("config/mirai.json") as file:
  config = json.load(file);
  
# Event handlers  
@mirai.event
# Function that fires when mirai boots up and successfully logs in
async def on_ready():
    dev_channel = mirai.get_channel(929427727033982986);
    print(f"We have logged in as {mirai.user}");
    await dev_channel.send("I'm booting up! (◕ᴗ◕✿)");

# Loads cogs into the mirai
# TODO: Make it a loop of the whole cogs folder
mirai.load_extension('cogs.about');

mirai.run(config["token"]);
