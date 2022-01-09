import discord;
import json;

# Reads package.json file; mostly to retrieve bot version
with open("package.json") as file:
  package = json.load(file);
  
#----------
# Function to generate the embed going to be sent for the about command
# bot: initialising discord client
def generate_about_embed(bot):
  embed = discord.Embed();
  embed.title = "About";
  embed.description = "Hi there! I'm Mirai and I'm a simple bot that counts down from a set number of days!\n\nMy creator made me as it helps him stay focused and keep him in check with his personal goals. Also because he wanted to create his first Python Project!\n\nI hope I can help you as much as I've helped him! (◕ᴗ◕✿)";
  embed.colour = discord.Colour(10699547);
  embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/248430185463021569/929419612234321950/mirai.jpg");

  embed.add_field(name="Creator", value="Vexuas#8141", inline=True);
  embed.add_field(name="Date Created", value=bot.user.created_at.strftime('%d-%b-%Y'), inline=True);
  embed.add_field(name="Version", value=package["version"], inline=True);
  embed.add_field(name="Library", value="Pycord", inline=True);
  embed.add_field(name="Last Update", value="10-Jan-2022", inline=True);
  embed.add_field(name="Source Code", value="[Github](https://github.com/vexuas/mirai)", inline=True);

  return embed;
#----------
