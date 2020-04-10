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
    
    if message.content.startswith('午') or message.content.startswith('買値'):
        ampm = ''
        if message.content.startswith('午前') or message.content.startswith('買値'):
            ampm = 'am'
        elif message.content.startswith('午後'):
            ampm = 'pm'
        else:
            return
        result = re.search('[1-9][0-9]{1,2}', message.content)
        price = None
        if result:
            price = (int)(result.group())
            today = (str)(datetime.date.today())
            data = {}
            datapath = './data/' + today + '.json'
            if os.path.exists(datapath):
                with open(datapath, 'r') as f:
                    data = json.load(f)
            data['day'] = datetime.date.today().weekday()
            if message.author.name in data:
                data[message.author.name][ampm] = price
            else:
                data[message.author.name] = {ampm : price}
            with open(datapath, 'w') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            await message.channel.send('おｋ')
        else:
            await message.channel.send('ダメです')
    
    if message.content.startswith('グラフ'):
        graph.graph()
        await message.channel.send(file=discord.File('./img/a.png'))


client.run(keys['token'])
