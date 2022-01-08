import discord;
import json;

bot = discord.Bot();

with open("config/mirai.json") as file:
  config = json.load(file);
  
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[929426428003483720])
async def hello(ctx):
    await ctx.respond("Hello!")

bot.run(config["token"]);
