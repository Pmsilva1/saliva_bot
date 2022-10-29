#from dotenv import load_dotenv
#load_dotenv()

#---------Imports-----------#
import os

token = os.environ.get("saliva_token")
owner_role_id = int(os.environ.get("owner_role_id"))
import discord
from discord.ext import tasks
import json
from replit import db
import time
import asyncio
import random
import math

#-------------Quart--------#
from quart import Quart

app = Quart(__name__)


@app.route('/')
async def home():
    return 'Hello I am alive!'


#-----------API data-------#
#import requests
#req = requests.get(f"https://discord.com/api/{token}")

#req.headers["X-RateLimit-Remaining"] # How many more requests you can make before `X-RateLimitReset`

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

#----


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    #update_dailies.start()
    #await client.get_channel(937361332896935976).send("bot is online")


#@tasks.loop(hours=1)
#async def update_dailies():
#  t = time.localtime(time.time())
#
#  h = t.tm_hour
#
#  asia_h = 21 - h
#  eu_h = 6 - h
#  na_h = 10 - h
#
#
#  if asia_h < 0: asia_h = 24 - abs(asia_h)
#  if eu_h < 0: eu_h = 24 - abs(eu_h)
#  if na_h < 0: na_h = 24 - abs(na_h)
#
#  await client.get_channel(963446907106111498).edit(name = f"SEA Reset: {asia_h} hours left ")
#  await client.get_channel(963446933144342548).edit(name = f"EU Reset: {eu_h} hours left ")
#  await client.get_channel(963446964882636850).edit(name = f"NA Reset: {na_h} hours left ")

#@update_dailies.before_loop
#async def update_dailies_before():
#  print("waiting...")
#  await client.wait_until_ready()


@client.event
async def on_message(message):
    role = discord.utils.find(lambda r: r.id == owner_role_id,
                              message.guild.roles)
    if message.author == client.user:
        return

    if message.author.id == 232962187532959746:
        msg = message.content.lower()
        if msg == 'hi' or msg == 'Hi':
            await message.channel.send("<a:bedge:1017279572720488489>",
                                       reference=message)
    if message.content.startswith('!!'):
        command = message.content[2:]
        content = command.split(" ")

        if content[0] == 'eval':
            if role in message.author.roles:
                try:
                    result = eval(command[len(content[0]) + 1:])
                    await message.channel.send(f"run result:\n{result}")
                except Exception as e:
                    await message.add_reaction("⚠")
                    await message.channel.send(f"Exception ocurred:\n{e}")
        elif content[0] == 'exec':
            if role in message.author.roles:
                try:
                    exec(command[len(content[0]) + 1:])
                except Exception as e:
                    await message.add_reaction("⚠")
                    await message.channel.send(f"Exception ocurred:\n{e}")

        elif content[0] == 'poll':
            if role in message.author.roles:
                new_msg = await client.get_channel(950489473471377428).send(
                    f"{command[len(content[0])+1:]} @here")
                await new_msg.add_reaction("👍")
                await new_msg.add_reaction("😐")
                await new_msg.add_reaction("👎")
                await message.delete()
        elif content[0] == 'hello':
            await message.channel.send('hello')
        elif content[0] == 'stinkybot':
            await message.channel.send('owie :(')
        elif content[0] == 'mirror':
            await message.channel.send(command[len(content[0]) + 1:])
        #elif content[0] == 'spam':
        #for item in db:
        #await message.channel.send(f"{item}")
        #await message.channel.send(f"{db[item]}")
        elif content[0] == 'ping':
            if len(content) == 1:
                await message.channel.send(f"<@{str(232962187532959746)}>")
            elif len(content) == 2:
                pings = int(content[1])

                for x in range(pings):
                    await message.channel.send(f"<@{str(232962187532959746)}>")

        elif content[0] == 'json':
            if role in message.author.roles:
                try:
                    with open('example.json', 'r') as help_file:
                        help_commands = json.load(help_file)
                        help_embed = discord.Embed.from_dict(help_commands)
                        await message.channel.send(embed=help_embed)
                except:
                    await message.add_reaction("⚠")

        elif content[0] == 'embedmsg':
            if role in message.author.roles:
                await message.channel.send(
                    'Where do you want to send this embeded message?')
                msg = await client.wait_for('message')
                #await message.channel.send(f"You said this? {msg.content}")
                test = json.loads(msg.content)
                embedVar = discord.Embed.from_dict(test)
                print(embedVar)
                await message.channel.send(embed=embedVar)

        elif content[0] == 'deathcounter':
            number = message.content[14:].strip()

            if "deathcount_silva" in db:
                current = int(db["deathcount_silva"])
            else:
                current = 0

            if number.isnumeric() == True and role in message.author.roles:
                current += int(number)
                db["deathcount_silva"] = str(current)
                await client.get_channel(958072688360947773).edit(
                    name=f"Fotter Taking L's: {current}")
            await message.channel.send(f"Current Counter:{current}")

        elif content[0] == 'getembed':
            channel = client.get_channel(int(content[1]))  # Channel ID
            msg = await channel.fetch_message(int(content[2]))  # Message ID
            embeds = msg.embeds
            for embed in embeds:
                await message.channel.send(embed.to_dict())

        elif content[0] == 'editembed':
            channel = client.get_channel(int(content[1]))  # Channel ID
            msg = await channel.fetch_message(int(content[2]))  # Message ID

            reply = ""
            newembed = discord.Embed().from_dict(reply)
            await msg.edit(embed=newembed)
            #await message.channel.send(newembed.to_dict())

        elif content[0] == 'forceheartboard':
            #try:
            channel = client.get_channel(int(content[1]))  # Channel ID
            msg = await channel.fetch_message(int(content[2]))  # Message ID
            msg_reply = None
            if len(content) > 3:
                msg_reply = await channel.fetch_message(int(content[3]))
            embed = discord.Embed()
            print(f"\n{msg}\n")
            embed.set_author(name=msg.author, icon_url=msg.author.avatar_url)
            embed.description = msg.content
            embed.timestamp = msg.created_at
            embed.colour = 16711680

            if msg.embeds:
                print(f"\n{msg.embeds[0].url}\n")
                print(f"\n{msg.embeds[0].image}\n")
                print(f"\n{msg.embeds[0].video}\n")
                print(f"\n{msg.embeds[0].video.url}\n")

                if msg.embeds[0].image:
                    embed.set_image(url=msg.embeds[0].image.url)
                elif msg.embeds[0].video:
                    urlx = msg.embeds[0].video.url

                    #urlx = "https://c.tenor.com/wy54tJC1ZiYAAAAd/venti-eating-asmr-asmr.gif"
                    print(f"I get in here\n{urlx}")
                    embed.set_image(url=urlx)
                elif msg.embeds[0].url:
                    embed.set_image(url=msg.embeds[0].url)

            if msg.attachments:
                embed.set_image(url=msg.attachments[0].url)
            if msg_reply is not None or msg.reference is not None:
                if msg.reference is not None:
                    msg_reply = await channel.fetch_message(
                        msg.reference.message_id)

                if bool(msg_reply.content):
                    embed.add_field(name=f"Replied to {msg_reply.author}",
                                    value=f"{msg_reply.content}",
                                    inline=False)
                else:
                    embed.add_field(name=f"Replied to {msg_reply.author}",
                                    value="\u200B",
                                    inline=False)

            embed.add_field(name="\u200B", value="\u200B", inline=False)
            embed.add_field(name="Message Link",
                            value=f"[Click to go to message]({msg.jump_url})",
                            inline=True)

            if msg_reply is not None or msg.reference is not None:
                embed.add_field(
                    name="Reply Link",
                    value=f"[Click to go to reply]({msg_reply.jump_url})",
                    inline=True)

            await client.get_channel(974398694541647903).send(embed=embed)
            await message.delete()
        #except Exception as e: # Error Check
        #print(e)
        elif content[0] in db:
            if len(content) == 1:
                await message.channel.send(f"{db[content[0]]}")
            elif role in message.author.roles:
                if (content[1].startswith('<https://')
                        or content[1].startswith('<http://')
                    ) and content[1][-1] == '>':
                    db[content[0]] = content[1][1:-1]
                else:
                    db[content[0]] = command[len(content[0]) + 1:]
                await message.channel.send(
                    f"{content[0]} command succesfully updated")

        elif role in message.author.roles and len(content) != 1:
            if (content[1].startswith('<https://')
                    or content[1].startswith('<http://')
                ) and content[1][-1] == '>':
                db[content[0]] = content[1][1:-1]
            else:
                db[content[0]] = command[len(content[0]) + 1:]
            await message.channel.send(
                f"{content[0]} command succesfully created")


@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji.id == 972294917642674186 and reaction.count >= 2:
        message = reaction.message
        reactions = message.reactions

        for react in reactions:
            if str(react.emoji) == '💖':
                return
        await message.add_reaction('💖')
        msg_channel = message.channel

        embed = discord.Embed()
        print(f"\n{message.content}\n")
        embed.set_author(name=message.author,
                         icon_url=message.author.avatar_url)
        embed.description = message.content
        embed.timestamp = message.created_at
        embed.colour = 16711680

        if message.embeds:
            embed.set_image(url=message.embeds[0].image.url)
        if message.attachments:
            embed.set_image(url=message.attachments[0].url)
        if message.reference is not None:
            reply_content = await msg_channel.fetch_message(
                message.reference.message_id)
            embed.add_field(name=f"Replied to {reply_content.author}",
                            value=f"{reply_content.content}",
                            inline=False)

        embed.add_field(name="\u200B", value="\u200B", inline=False)
        embed.add_field(name="Message Link",
                        value=f"[Click to go to message]({message.jump_url})",
                        inline=True)

        if message.reference is not None:
            embed.add_field(
                name="Reply Link",
                value=f"[Click to go to reply]({message.reference.jump_url})",
                inline=True)

        await client.get_channel(974398694541647903).send(embed=embed)


@client.event
async def on_message_edit(message_before, message_after):
    if not message_after.author.bot and message_before.content != message_after.content:
        num = random.random()
        if num < 0.05 or num > 0.95:
            await message_after.channel.send(
                "<:PeepoHey:940629497126989834><:Edited:974123135949479976>",
                reference=message_after)
        if num < 0.01 or num > 0.99:
            await message_after.channel.send(
                f"Edit deez nuts {message_after.author.name}")


@client.event
async def on_message_delete(message):
    async for entry in message.guild.audit_logs(
            limit=1, action=discord.AuditLogAction.message_delete):
        deleter = entry.user

    embed = discord.Embed()
    print(f"\n{message.content}\n")
    embed.set_author(name=message.author, icon_url=message.author.avatar_url)
    embed.description = message.content
    embed.timestamp = message.created_at
    embed.colour = 16711680
    embed.add_field(name=f"Deleted by {deleter}", value="\u200B", inline=False)

    if message.embeds:
        embed.set_image(url=message.embeds[0].image.url)
    if message.attachments:
        embed.set_image(url=message.attachments[0].url)

    await client.get_channel(1016697667759378432).send(embed=embed)


@client.event
async def on_member_join(member):
    await member.add_roles(937366688989610004)
    await client.create_role(member.guild, name=f"{member.name}")
    try:
        role = discord.utils.get(member.guild.roles, name=f"{member.name}")
        await member.add_roles(role)
    except:
        print("Error creating/giving new role")


loop = asyncio.get_event_loop()

try:
    #update_dailies.start()
    client.loop.create_task(app.run_task('0.0.0.0', 8080))
    client.run(token)

except:
    os.system("kill 1")
