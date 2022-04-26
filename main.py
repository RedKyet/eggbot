import os
import asyncio
import discord
import random
import json
distoken = os.environ['token']

client=discord.Client()
join_message_sent = False
join_list={}
game_start=False
b_phase=1

@client.event
async def on_ready():
  print('Logged in as ', client.user)

@client.event
async def on_message(message):
  global join_message_sent
  global join_list
  global game_start
  global who_said_hai
  global b_phase
  
  if message.author == client.user:
    return
    
  elif message.content == '&ciocnitoua' and join_message_sent==False:
    await message.channel.send('**Show your :egg: to join the egg fight**')
    join_message_sent = True
    await asyncio.sleep(15)
    if len(join_list)>1:
      await message.channel.send('*Joining closed. {} joined \n To start a battle type* <:egg: Hristos a inviat>'.format(', '.join(x.mention for x in join_list)))
      # print(join_list.items())
      game_start=True
      b_phase=1
      while len(join_list)>1: await asyncio.sleep(5)
      game_start=False
      for x in join_list: winner=x.name
      await message.channel.send('**Game has ended. {} won**'.format(' '.join(x.mention for x in join_list)))
      with open("leaderboard.json", "r+") as lb:
        data = json.load(lb)
        if winner not in data:
          data.update({winner:1})
        else:
          data[winner]+=1
        marklist = sorted(data.items(), key=lambda x:x[1], reverse=True)
        sortdict= dict(marklist)
        # print(sortdict)
        lb.seek(0)
        json.dump(sortdict,lb)
      join_message_sent=False
      join_list={}
    else: 
      await message.channel.send('Nobody joined :(')
      join_message_sent = False
      join_list={}
    
  elif message.content == '🥚' and join_message_sent==True and message.author not in join_list:   
    join_list[message.author] = random.randint(1,5)
    who_said_hai=message.author

  elif message.content == "🥚 Hristos a inviat" or message.content == "🥚Hristos a inviat" or message.content == "🥚 Hristos a înviat" or message.content == "🥚Hristos a înviat" and game_start==True and b_phase==1 and message.author in join_list:
    # print(message.content)
    who_said_hai=message.author
    b_phase=2
    
  elif message.content == "🥚 Adevarat a inviat" or message.content == "🥚Adevarat a inviat" or message.content == "🥚 Adevărat a înviat" or message.content == "🥚Adevărat a înviat" and game_start==True and b_phase==2 and message.author in join_list:
    # print(message.content)
    if join_list[message.author] > join_list[who_said_hai]:
      await message.channel.send("{}'s egg brakes :(".format(who_said_hai.mention))
      join_list.pop(who_said_hai)
    elif join_list[message.author] < join_list[who_said_hai]:
      await message.channel.send("{}'s egg brakes :(".format(message.author.mention))
      join_list.pop(message.author)
    else:
      who_said_hai=random.choice([who_said_hai, message.author])
      await message.channel.send("{}'s egg brakes :(".format(who_said_hai.mention))
      join_list.pop(who_said_hai)
    b_phase=1
  elif message.content == "&help":
    await message.channel.send("""*&ciocnitoua* pentru a initia un lobby
Botul va astepta 15 secunde pentru mesaje "🥚"
Ca sa te lupti cu cineva trebuie sa dai comanda *"🥚 Hristos a inviat"* apoi astepti ca cineva sa iti raspunda cu *"🥚 Adevarat a inviat"* ca sa ciocniti oul. 
Oul are o duritate random de la 1 la 5 aleasa la inceputul jocului. Daca se ciocnesc 2 oua cu aceeasi duritate atunci rezultatul va fi random.
Ultimul jucator va fi castigatorul.
Tehnic te poti bate cu tine insuti dar va fi o sansa random sa te sinucizi.""")
  elif message.content == "&leaderboard":
    with open("leaderboard.json", "r") as lb:
      leaderboard=json.load(lb)
      embedVar = discord.Embed(title="Leaderboard - oua colectate", color=0x00ff00)
      for x in leaderboard:
        embedVar.add_field(name=x, value=leaderboard[x], inline=False)
      await message.channel.send(embed=embedVar)
client.run(distoken)

