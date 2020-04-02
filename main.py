import discord
import json
from collections import OrderedDict
import re
import datetime

keys = {}
with open('./keys.json', 'r') as f:
    keys = json.load(f)

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('午'):
        result = re.search('\d{2,3}', message.content)
        if result:
            await message.channel.send(result.group())
        else:
            await message.channel.send('error: The price is invalid.')
    return


client.run(keys['token'])
