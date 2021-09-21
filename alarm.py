import json
import os
from dislash import SelectMenu, SelectOption, InteractionClient
import discord as dc
from discord.utils import get
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
import time
import requests as rq
bot=commands.Bot(command_prefix='/')
slash=InteractionClient(bot)

dic=['陳彥廷','黃承傑','黃冠穎','李俊翰','謝侑哲','陳茗佑','邱繼叡']

@bot.event
async def on_ready() :
    alarm.start()
@bot.event
async def on_message(message) :
    string = message.content
    user=message.author
    if message.channel.id != 867413719217602560:
        return
    if string.startswith('每') and user==885499476918300732:
        await message.channel.send('可以停了嗎')
    elif string.startswith('每') or len(string)>=15 :
        if user.id==885537928028229642 or user.id==795258895622340619:
            print('GOOD')
        else :
            await message.channel.send('請不要附和那個 bot')
p=6
@tasks.loop(seconds=60)
async def alarm():
    
    global p
    result=time.strftime('%M',time.localtime())
    if result[0]=='0':
        result=result[1:]
    print(result)
    if eval(result)%6!=5:
        return 
    channel=bot.get_channel(867413719217602560)
    msg = await channel.send(f'大家一起膜拜{dic[p]}大電神!')
    emoji = bot.get_emoji(886951701318348841)
    await msg.add_reaction(emoji)
    
    p+=1
    
    if(p>=len(dic)) :
        p-=len(dic)


load_dotenv()

bot.run(os.getenv('TOKEN'))


