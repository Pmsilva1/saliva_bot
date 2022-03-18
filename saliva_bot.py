from dotenv import load_dotenv
load_dotenv()

import os
token = os.environ.get("saliva_token")
owner_role_id = int(os.environ.get("owner_role_id"))
import discord

import json

#def make_embed(message):
    #msg_json = json.loads(message)
    #content = msg_json["content"]
    #embed = msg_json["embed"]

    #embedVar = discord.Embed(title=embed["title"], description=embed["description"], color=embed["color"])
    #embedVar.set_author()
    #embedVar.set_footer()
    #embedVar.set_image()
    #embedVar.set_thumbnail()
    #embedVar.add_field(name="Field1", value="hi", inline=False)


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    role = discord.utils.find(lambda r: r.id == owner_role_id, message.guild.roles)

    if role in message.author.roles:
        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        if message.content.startswith('!!hello'):
            with open('example.json', 'r') as help_file:
                help_commands = json.load(help_file)
                help_embed = discord.Embed.from_dict(help_commands)
                await message.channel.send(embed=help_embed)

        if message.content.startswith('!!embedmsg'):
            await message.channel.send('Where do you want to send this embeded message?')
            msg = await client.wait_for('message')
            #await message.channel.send(f"You said this? {msg.content}")
            test = json.loads(msg.content)
            embedVar = discord.Embed.from_dict(test)
            print(embedVar)
            await message.channel.send(embed=embedVar)
client.run(token)