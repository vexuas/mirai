import discord;
import json;

bot = discord.Bot();

with open("config/mirai.json") as file:
  config = json.load(file);
  
@bot.event
async def on_ready():
    dev_channel = bot.get_channel(929427727033982986);
    print(f"We have logged in as {bot.user}");
    await dev_channel.send("I'm booting up! (◕ᴗ◕✿)");

bot.load_extension('cogs.about');

bot.run(config["token"]);
