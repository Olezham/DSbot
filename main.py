
import sql
import discord
from discord import ButtonStyle
from discord.ext import commands
from discord.ui import View, Button 
from config import TOKEN

import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

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
    print(f'Bot ready!')

@bot.command()
async def get_users(ctx):
    guild = ctx.guild
    for member in guild.members:
        print(member.name)  


@bot.command()
async def warns(ctx):
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
            await handle_button_click(interaction)  # Обработка нажатия кнопки
        except:
            pass

async def handle_button_click(interaction):
    if interaction.component.label == "Выдать варн":
        await give_warn(interaction)
    elif interaction.component.label == "Снять варн":
        await remove_warn(interaction)
    elif interaction.component.label == "Обновить список":
        await update_list(interaction)

async def give_warn(interaction):
    await interaction.response.send_message("Вы нажали кнопку 'Выдать варн'.")

async def remove_warn(interaction):
    await interaction.response.send_message("Вы нажали кнопку 'Снять варн'.")

async def update_list(interaction):
    await interaction.response.send_message("Вы нажали кнопку 'Обновить список'.")


@bot.command()
async def textall(ctx, *, message: str):
    # Удаляем сообщение с командой
    await ctx.message.delete()

    # Список ID разрешенных ролей
    allowed_role_ids = [1220028330666098710, 1220031850270031912, 1220029066535501845]

 
    if any(role.id in allowed_role_ids for role in ctx.author.roles):
      
        members = ctx.guild.members

  
        excluded_users = []

      
        for member in members:
            if any(role.id in allowed_role_ids for role in member.roles) and member.name not in excluded_users:
                try:    
                    user = await bot.fetch_user(member.id)
                    channel = await user.create_dm()
                    await channel.send(message)
                    await asyncio.sleep(0.5)
                except discord.Forbidden:
                    # Если не удается отправить сообщение пользователю, например, из-за его настроек конфиденциальности
                    print(f"Cannot send message to {user.name}#{user.discriminator} - Direct messages disabled.")
                except Exception as e:
                    print(f"Error sending message to {user.name}#{user.discriminator}: {e}")

        await ctx.send("Message sent to all allowed users on the server.")
    else:
        await ctx.send("You don't have permission to use this command.")



    



bot.run(TOKEN)