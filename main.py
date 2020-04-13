import discord
import json
from collections import OrderedDict
import re
import datetime
import os
import graph

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
    
    if message.content.startswith('全部見せて'):
        res = re.search('[1-9][0-9]*', message.content)
        if res:
            weeksago = (int)(res.group())
        graph.graph(weeksago)
        await message.channel.send(file=discord.File('./img/a.png'))


client.run(keys['token'])
