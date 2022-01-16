# mirai
Discord bot that simply counts down from a set number of days. My first Python discord bot! and also my first application command bot smh

This project was birthed in a mix of wanting to learn Python and (trying) to automate my daily countdown. For a while, I've been manually setting my status from a certain day and updating it daily downwards as the days pass. The reasoning behind it is it merely acts as a way to keep me in check and productive to my pre-determined goal within that timeframe. Was this effective? Well, yes and no. I find it does help having a timer that progressively decreases; keeps yourself accountable. On the other hand, it's such a hassle to have to update my discord status every single day.

You may be asking, why suffer through that and just find an actual product that specialises in countdowns? Well that's definitely the sensible choice, the better choice which will yield better productivity even but I'm not sure if it'll work for me. I'm a big believer that motivation comes easiest when it's convenient. And since I basically have discord open all the time and I like building discord bots; why not automate that with a bot with a new learnt language: Python

<div align="center"><img width=600 src="https://user-images.githubusercontent.com/42207245/149668588-0e495c18-89f6-4fc5-be4a-94e6048c10eb.png" /></div>
<div align="center"><img width=600 src="https://user-images.githubusercontent.com/42207245/149668605-b54d8c9a-8617-494e-8a20-0aa16cf85ef3.png" /></div>
<div align="center"><img width=600 src="https://user-images.githubusercontent.com/42207245/149668595-17488ebc-5190-443b-97a3-c45d01c700f1.png" /></div>



## Tech Stack
- [Pycord](https://github.com/Pycord-Development/pycord) - Python wrapper for the Discord API
- [Sqlite3](https://docs.python.org/3/library/sqlite3.html) - lightweight database to store countdown data

## How to use
With Discord's upcoming change on message intents, verified discord bots will no longer be able to read messages from users after April 2022. This would mean a user can't call a bot using a prefix with a command but instead have to use the built-in application or more commonly known as slash commands `/`. Personally I don't mind this change but I can see why a lot of the bigger bot developers push back with this change. It's the main reason why discord.py is shutting down support as the dev doesn't agree on the change. I welcome change so it's fine albeit maybe my first experience with slash commands should have been with a language that I'm already familiar with :aoba_sweat:

1. [Invite mirai] to any of your discord servers
2. Once invited, type slash with any of the commands below!

## Commands List
- `about` - information hub of mirai
- `countdown` - creates a countdown channel with a set nunber of days

![image](https://user-images.githubusercontent.com/42207245/149668129-05af3d94-ac8c-40dc-82a7-2706e39abf19.png)

## Todos for future me:
- Wrap async functions with a try..except
- Refactor asyncio functions; there definitely is a better way in doing this
- Finish the intermidiate python course in codecademy and apply learnings here
- Maybe add motivational text on each ping; maybe we can check out an AI who can generate this

## Useful Links
- [Notes on Python Codecademy Course](https://shizuka.notion.site/Python-08e08a73f1ab4f908f148cae13baf394)
- [Pycord API Reference](https://docs.pycord.dev/en/master/api.html)
- [Support Server Link](https://discord.gg/msMqA4HQuR)
