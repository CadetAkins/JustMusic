import os
import discord
from discord.ext import commands
from replit import Database

_db = Database("https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsImlzcyI6ImNvbm1hbiIsImtpZCI6InByb2Q6MSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb25tYW4iLCJleHAiOjE2MzU0Nzc0NDUsImlhdCI6MTYzNTM2NTg0NSwiZGF0YWJhc2VfaWQiOiJjMDAxOTVkOS01M2Y5LTQ3OTctYmViOC1mOTIyNmU1NzQ2OTQifQ.TNoK4QS02sxsxBFTi6-KwYcEBDbCSrtzyeD4-gr8kWBk3bM6vUl1YOwgCM3y26o1DyInBXGy8us1_GeP1irN3w")

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


bot.run("OTAyMzgzOTgzMzk0OTcxNjg4.YXdokw.22zMVbdAZC7qdkmqugL774H53kc")
