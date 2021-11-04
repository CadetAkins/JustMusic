import os
import discord
from discord.ext import commands
import sqlite3

class MusicBot(commands.Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # initialize database
    self._db = sqlite3.connect(os.getenv("DATABASE_PATH"))
    self._db.execute("CREATE table IF NOT EXISTS table_name (name, cname, playlist_description, playlist_image_url, author_name, author_mention, author_avatar, author_id);")
    self._db.close()
    
  def db_exec(self, call: str):
    self._db = sqlite3.connect(os.getenv("DATABASE_PATH"))
    self._db.execute(call)
    self._db.close()

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

bot.run(os.getenv("TOKEN"))
