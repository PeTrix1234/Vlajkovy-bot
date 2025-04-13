
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

FLAG_EMOJIS = {
    "🇨🇿": "CZ", "🇸🇰": "SK", "🇩🇪": "DE", "🇫🇷": "FR",
    "🇮🇹": "IT", "🇵🇱": "PL", "🇺🇸": "US", "🇬🇧": "UK",
    "🇪🇸": "ES", "🇷🇺": "RU", "🇺🇦": "UA", "🇯🇵": "JP",
    "🇰🇷": "KR", "🇨🇳": "CN", "🇧🇷": "BR", "🇮🇳": "IN",
    "🇨🇦": "CA", "🇦🇺": "AU"
}

TARGET_MESSAGE_ID = int(os.getenv('TARGET_MESSAGE_ID', 0))

@bot.event
async def on_ready():
    print(f'Bot je online jako {bot.user}')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != TARGET_MESSAGE_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None or member.bot:
        return

    emoji = str(payload.emoji)
    if emoji not in FLAG_EMOJIS:
        return

    new_nick = member.nick or member.name
    for flag in FLAG_EMOJIS:
        if flag in new_nick:
            new_nick = new_nick.replace(f" {flag}", "").replace(flag, "")
    new_nick = f"{new_nick} {emoji}"

    try:
        await member.edit(nick=new_nick)
    except discord.Forbidden:
        print(f"Nemám oprávnění změnit přezdívku pro {member.name}.")
    except Exception as e:
        print(f"Chyba při změně přezdívky: {e}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != TARGET_MESSAGE_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    member = guild.get_member(payload.user_id)
    if member is None or member.bot:
        return

    emoji = str(payload.emoji)
    if emoji not in FLAG_EMOJIS:
        return

    new_nick = member.nick or member.name
    new_nick = new_nick.replace(f" {emoji}", "").replace(emoji, "")

    try:
        await member.edit(nick=new_nick)
    except discord.Forbidden:
        print(f"Nemám oprávnění změnit přezdívku pro {member.name}.")
    except Exception as e:
        print(f"Chyba při změně přezdívky: {e}")

bot.run(os.getenv('TOKEN'))
