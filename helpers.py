import discord;

def generate_about_embed():
  embed = discord.Embed();
  embed.title = "About";
  embed.description = "Hi there! I'm Mirai and I'm a simple bot that counts down from a set number of days!\n\nMy creator made me as it helps him stay focused and keep him in check with his personal goals.\n\nI hope I can help you as much as I've helped him!";
  embed.colour = discord.Colour(10699547);
  embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/248430185463021569/929419612234321950/mirai.jpg");

  return embed;
