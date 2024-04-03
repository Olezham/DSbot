
import sql
import discord
from discord import ButtonStyle
from discord.ext import commands
from discord.ui import View, Button 
from config import TOKEN

import asyncio
import datetime

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ready!')

# @bot.command()
# async def get_users(ctx):
#     guild = ctx.guild
#     for member in guild.members:
#         print(member.name)  

'''
@bot.command()
async def warns(ctx):
    for guild in bot.guilds:
        guild_id = guild.id
        
        for member in guild.members:
            if member.bot:
                continue 
            user_id = member.id
            username = member.name
            nickname = member.nick
            if(sql.user_exist(user_id,guild_id)):
                continue
            sql.add_user(username,nickname,user_id,guild_id)
    server_id = ctx.guild.id
    embed = discord.Embed(
        title='Список игроков - варнов',
        color=discord.Color.blue()
    )
    data = sql.get_all_server_users(server_id)
    x = 0
    for i in data:
        x += 1
        embed.add_field(name=i['nickname'], value=str(x) + '. Варнов: ' + str(i['warn']), inline=False)

    view = View()
    Buttons = [
        Button(style=ButtonStyle.red, label="Выдать варн", emoji='👊🏻'),
        Button(style=ButtonStyle.green, label="Снять варн", emoji='🙌🏻'),
        Button(style=ButtonStyle.grey, label="Обновить список", emoji='💫')
    ]
    for i in Buttons:
        view.add_item(i)

    message = await ctx.send(embed=embed, view=view)

    while True:
        try:
            interaction = await bot.wait_for("button_click", timeout=60.0, check=lambda inter: inter.message.id == message.id)
        except:
            pass
'''


@bot.command()
async def textall(ctx, *, message: str):
    # Удаляем сообщение с командой
    await ctx.message.delete()

    # Список ID разрешенных ролей
    allowed_role_ids = [1139465593507020822,1220028330666098710,1224079725341970575,1224079912542142565]

 
    if any(role.id in allowed_role_ids for role in ctx.author.roles):
      
        members = ctx.guild.members

  
        excluded_users = ['x.dinozavrik']

        sended = 0
        notsended = 0
        send_to = [1225084229495423048,1220160995184476170,1224333887203971156,1224079112872656987,1224079912542142565,1224079725341970575,1220028330666098710]
        for member in members:
            if any(role.id in send_to for role in member.roles) and member.name not in excluded_users:
                try:    
                    user = await bot.fetch_user(member.id)
                    channel = await user.create_dm()
                    print(user)
                    await channel.send(message)
                    sended += 1
                    await asyncio.sleep(0.05)
                except discord.Forbidden:
                    print(f"Cannot send message to {user.name}#{user.discriminator} - Direct messages disabled.")
                    notsended += 1
                except Exception as e:
                    print(f"Error sending message to {user.name}#{user.discriminator}: {e}")
                    notsended += 1

        await ctx.send(f"Message sent to 🟢 {sended} users | Not sended to 🔴 {notsended}")

        try:
            print(f'{datetime.datetime.now} - {ctx.author.nick} sendet message to {sended} users')
        except:
            print(f'{datetime.datetime.now} - {ctx.author.name} sendet message to {sended} users')
        
    else:
        await ctx.send("You don't have permission to use this command.")
 
bot.run(TOKEN)

