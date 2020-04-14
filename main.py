import discord
import json
from collections import OrderedDict
import re
import datetime
import os
import graph
import datetime
import time

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
        nums = []
        nums.extend(re.findall('\D[1-9][0-9]*', message.content))
        for i in range(len(nums)):
            nums[i] = (int)(re.search('[1-9][0-9]*', nums[i]).group())
        today = datetime.date.today()
        if len(nums) == 3:
            today = datetime.date(nums[0], nums[1], nums[2])
            today += datetime.timedelta(days=(5 - today.weekday()) % 7)
        if len(nums) == 2:
            today = datetime.date(datetime.date.today().year, nums[0], nums[1])
            today += datetime.timedelta(days=(5 - today.weekday()) % 7)
        graph.graph(today)
        await message.channel.send(file=discord.File('./img/a.png'))
    
    if re.match(r'^.*(玉音放送|gyokuon|itumizu|学位|大場|おおば).*$', message.content):
        await gyokuon()
    
    if client.get_user(keys['i']) in message.mentions:
        await gyokuon()

@client.event
async def on_raw_reaction_add(reaction):
    if reaction.emoji.name == "gyokuon":
        await gyokuon()

async def gyokuon():
    await client.change_presence(activity=discord.Game(name='玉音放送'))
    voice = await discord.VoiceChannel.connect(client.get_channel(keys['gyokuon']))
    voice.play(discord.FFmpegPCMAudio('gyokuon.mp3'))
    time.sleep(40)
    await voice.disconnect()
    await client.change_presence(activity=None)

client.run(keys['token'])
