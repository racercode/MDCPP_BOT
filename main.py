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
import random
import re
import html
bot=commands.Bot(command_prefix='-')
slash=InteractionClient(bot)


def cleanhtml (string) :
    #print(string)
    string=html.unescape(string)
    string = re.sub(r'<.*?>', '', string)
    string = string.replace('&lt;','<')
    string = string.replace('&gt;','>')
    string = string.replace('&amp;','&')
    string = string.replace('&quot;','\"\"')
    return string
    #return string.replace('<p>','').replace('</p>','').replace('<br />','\n')

dic={}
id_pos={}

#global id_pos, tid_pos, dic, tdic

@bot.command()
async def rank (ctx) :
    global id_pos, dic
    recv=rq.get('http://mdcpp.mingdao.edu.tw/api/user_rank?offset=0&limit=10&rule=ACM')
    dic=json.loads(recv.text)
    shortdic=dic['data']['results']
    embed=dc.Embed(
        title='MDCPP 排行榜',
        description=f"目前第一名：{shortdic[0]['user']['username']}",
        colour=dc.Colour(0XE5E242)
    )
    string='http://mdcpp.mingdao.edu.tw/'+shortdic[0]['avatar']
    embed.set_thumbnail(url=string)
    for i in range(10) :
        embed.add_field(name=shortdic[i]['user']['username'],value=f"AC : {shortdic[i]['accepted_number']}",inline=False)
    mg = await ctx.send(embed=embed)
    id_pos[mg.id]=[0,mg,shortdic[0]['user']['username'],string]
    em1 = '⬅️'
    em2 = '➡️'
    await mg.add_reaction(em1)
    await mg.add_reaction(em2)
@bot.command()
async def get (ctx) :
    
    recv=rq.get(f'http://mdcpp.mingdao.edu.tw/api/problem?paging=true&offset=0&limit=200&page=1')
    tdic=json.loads(recv.text)
    n = random.randint(0,tdic['data']['total']-1)
    shortdic=tdic['data']['results'][n]
    embed=dc.Embed(
        title='編號 : '+shortdic['_id'],
        description=shortdic['title'],
        url='http://mdcpp.mingdao.edu.tw/problem/'+shortdic['_id'],
        colour=dc.Colour(0XE5E242)
    )
    rp = await ctx.send(embed=embed,components=[
        SelectMenu(
            placeholder='請選擇細部資訊',
            max_values=7,
            options=[
                SelectOption('Description','1'),
                SelectOption('Input Description','2'),
                SelectOption('Output Description','3'),
                SelectOption('Sample Input & Output','4'),
                SelectOption('Time Limit','5'),
                SelectOption('Memory Limit','6'),
                SelectOption('Difficulty','7')
            ]
        )
    ])
    inter = await rp.wait_for_dropdown()
    labels = [option.label for option in inter.select_menu.selected_options]
        
    newembed=dc.Embed(
        colour=dc.Colour(0XE5E242)
    )
    sr = shortdic['description']
    if 'img' in sr :
        ret = ''
        for i in range (sr.find('src')+5,len(sr)) :
            if sr[i]!='\"' :
                ret+=sr[i]
            else :
                break
        if ret.startswith('http') :
            newembed.set_thumbnail(url=ret)
        else :
            newembed.set_thumbnail(url='http://mdcpp.mingdao.edu.tw/'+ret)

    newembed.set_author(name=str(ctx.author),icon_url=ctx.author.avatar_url)
    for string in labels :
        if string.startswith('Des') :
            newembed.add_field(name=string,value=cleanhtml(shortdic['description']),inline=False)
        if string.startswith('Input') :
            newembed.add_field(name=string,value=cleanhtml(shortdic['input_description']),inline=False)
        if string.startswith('Output') :
            newembed.add_field(name=string,value=cleanhtml(shortdic['output_description']),inline=False)
        if string.startswith('Sample') :
            
            for i in range (len(shortdic['samples'])) :
                 newembed.add_field(name='Sample Input '+str(i+1),value=shortdic['samples'][i]['input'],inline=False)
                 newembed.add_field(name='Sample Output '+str(i+1),value=shortdic['samples'][i]['output'],inline=True)
        if string.startswith('Time') :
            newembed.add_field(name=string,value=str(shortdic['time_limit'])+' ms',inline=False)
        if string.startswith('Memory') :
            newembed.add_field(name=string,value=str(shortdic['memory_limit'])+' MB',inline=False)
        if string.startswith('Diff') :
            newembed.add_field(name=string,value=shortdic['difficulty'],inline=False)
    await inter.reply(embed=newembed)

@bot.command()
async def tag (ctx, *, args) :
     
    string = args
    recv=rq.get(f'http://mdcpp.mingdao.edu.tw/api/problem?paging=true&offset=0&limit=1000&tag={args}&page=1')
    tdic=json.loads(recv.text)
    n = random.randint(0,tdic['data']['total']-1)
    shortdic=tdic['data']['results'][n]
    embed=dc.Embed(
        title='編號 : '+shortdic['_id'],
        description=shortdic['title'],
        url='http://mdcpp.mingdao.edu.tw/problem/'+shortdic['_id'],
        colour=dc.Colour(0XE5E242)
    )
    rp = await ctx.send(embed=embed,components=[
        SelectMenu(
            placeholder='請選擇細部資訊',
            max_values=7,
            options=[
                SelectOption('Description','1'),
                SelectOption('Input Description','2'),
                SelectOption('Output Description','3'),
                SelectOption('Sample Input & Output','4'),
                SelectOption('Time Limit','5'),
                SelectOption('Memory Limit','6'),
                SelectOption('Difficulty','7')
            ]
        )
    ])
    inter = await rp.wait_for_dropdown()
    labels = [option.label for option in inter.select_menu.selected_options]
        
    newembed=dc.Embed(
        colour=dc.Colour(0XE5E242)
            
    )
    newembed.set_author(name=str(ctx.author),icon_url=ctx.author.avatar_url)
    for string in labels :
        if string.startswith('Des') :
            newembed.add_field(name=string,value=cleanhtml(shortdic['description']),inline=False)
        if string.startswith('Input') :
            newembed.add_field(name=string,value=cleanhtml(shortdic['input_description']),inline=False)
        if string.startswith('Output') :
            newembed.add_field(name=string,value=cleanhtml(shortdic['output_description']),inline=False)
        if string.startswith('Sample') :
            
            for i in range (len(shortdic['samples'])) :
                 newembed.add_field(name='Sample Input '+str(i+1),value=shortdic['samples'][i]['input'],inline=False)
                 newembed.add_field(name='Sample Output '+str(i+1),value=shortdic['samples'][i]['output'],inline=True)
        if string.startswith('Time') :
            newembed.add_field(name=string,value=str(shortdic['time_limit'])+' ms',inline=False)
        if string.startswith('Memory') :
            newembed.add_field(name=string,value=str(shortdic['memory_limit'])+' MB',inline=False)
        if string.startswith('Diff') :
            newembed.add_field(name=string,value=shortdic['difficulty'],inline=False)
    await inter.reply(embed=newembed)

    


@bot.event
async def on_reaction_add(reaction,user) :
    
    if user.id == 885537928028229642 :
        return
    ID=reaction.message.id
    if ID not in id_pos :
        return
    if reaction.emoji == '⬅️':
        id_pos[ID][0]-=10
    else :
        id_pos[ID][0]+=10
    recv=rq.get(f'http://mdcpp.mingdao.edu.tw/api/user_rank?offset={id_pos[ID][0]}&limit=10&rule=ACM')
    dic=json.loads(recv.text)
    shortdic=dic['data']['results'] 
    embed=dc.Embed(
        title='MDCPP 排行榜',
        description='目前第一名：'+id_pos[ID][2]
    )
    embed.set_thumbnail(url=id_pos[ID][3])
    for i in range(10) :
        embed.add_field(name=shortdic[i]['user']['username'],value=f"AC : {shortdic[i]['accepted_number']}",inline=False)
    await reaction.remove(user)
    await id_pos[ID][1].edit(embed=embed)

    

load_dotenv()

bot.run(os.getenv('TOKEN'))


