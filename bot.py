import os
import discord
from discord.ext import commands
from replit import Database

_db = Database("")

class MusicBot(commands.Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.db = _db

bot = MusicBot(
  command_prefix = "-",
  intents = discord.Intents.default(),
  help_command=None,
  case_insensitive=True,
  strip_after_whitespace=True
)

COGS = [
  'plugins.core.errors.on_command_error', #error handler
  'plugins.core.startup.login',
  'plugins.core.help.help',
  'plugins.music.playlists',
  'plugins.music.music'
]

for cog in COGS:
  bot.load_extension(cog)

@bot.command()
@commands.is_owner()
async def wipe_db(ctx):
  for key in _db.keys():
    del _db[key]

  await ctx.send("Database wiped.")


bot.run("")
