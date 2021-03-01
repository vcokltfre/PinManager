from templatebot import Bot
from discord.ext import commands
from discord import Embed, TextChannel, Game
from datetime import datetime
from os import getenv
from dotenv import load_dotenv

from utils.db import Database

load_dotenv()

bot = Bot(name="PinManager", command_prefix="p!", help_command=None, activity=Game(name="p!pins"))
db = Database()

@bot.group(name="pins")
@commands.has_guild_permissions(manage_guild=True)
async def pins(ctx: commands.Context):
    if not ctx.invoked_subcommand:
        await ctx.send("Usage:\n`p!pins add <channel> <archive_channel>`\n`p!pins remove <channel>`")

@pins.command(name="add", aliases=["set"])
async def pins_add(ctx: commands.Context, channel: TextChannel, archive: TextChannel):
    try:
        await db.add_channel(channel.id, archive.id)
    except:
        await ctx.send("That channel already has an archive channel, remove it to add a new one.")
    else:
        await ctx.send(f"Successfully added {archive.mention} as the archive channel for {channel.mention}")

@pins.command(name="del", aliases=["remove"])
async def pins_del(ctx: commands.Context, channel: TextChannel):
    try:
        await db.remove_channel(channel.id)
    except:
        await ctx.send("Failed to remove the channel.")
    else:
        await ctx.send(f"Removed the archive channel for {channel.mention}")

@bot.event
async def on_guild_channel_pins_update(channel: TextChannel, last: datetime):
    if not last:
        return

    delta = datetime.now() - last
    if delta.seconds > 5:
        return

    c = await db.get_channel(channel.id)
    if not c:
        return

    pins = await channel.pins()
    if len(pins) < 50:
        return

    ac = bot.get_channel(c[0])
    if not ac:
        return

    m = pins[-1]
    embed = Embed(title=f"#{channel} | Pins", colour=0x87CEEB)
    embed.description = m.content
    embed.add_field(name="​", value=f"[Jump to Message]({m.jump_url})")
    embed.set_author(name=str(m.author), icon_url=str(m.author.avatar_url))
    await ac.send(embed=embed)
    await m.unpin()

bot.run(getenv("TOKEN"))
