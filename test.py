#from dotenv import load_dotenv
#load_dotenv()

import os
token = os.environ.get("saliva_token")
owner_role_id = int(os.environ.get("owner_role_id"))

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(token)