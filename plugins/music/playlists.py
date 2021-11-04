import math
import discord
from discord.ext import commands

import DiscordUtils

from requests import get
from youtube_dl import YoutubeDL

YTDL_OPTIONS = {
  'format': 'bestaudio/best',
  'extractaudio': True,
  'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
  'restrictfilenames': True,
  'noplaylist': True,
  'nocheckcertificate': True,
  'ignoreerrors': False,
  'logtostderr': False,
  'quiet': True,
  'no_warnings': True,
  'default_search': 'auto',
  'source_address': '0.0.0.0',
}

def search(arg):
    with YoutubeDL(YTDL_OPTIONS) as ydl:
        try:
            get(arg) 
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)

    return video

colours = {
  'RED': discord.Colour.red(),
  'ORANGE': discord.Colour.orange(),
  'YELLOW': discord.Colour.gold(),
  'GREEN': discord.Colour.green(),
  'BLUE': discord.Colour.blue(),
  'INDIGO': discord.Colour.blurple(),
  'VIOLET': discord.Colour.purple()
}

class PlaylistExistsError(Exception):
  def __init__(self, name: str):
    self.msg = f"Playlist of name '{name}' already exists."

  def __repr__(self):
    return self.msg


class InvalidNameError(Exception):
  def __init__(self, name: str):
    self.msg = f"Playlist of name '{name}' doesn't exist."

  def __repr__(self):
    return self.msg

class InvalidAttributeError(Exception):
  def __init__(self, name: str):
    self.msg = f"Attrbute of name '{name}' doesn't exist."

  def __repr__(self):
    return self.msg

class Playlists(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot=bot
    self.name="Playlist category:"

  @commands.command(
    name="create-playlist",
    aliases = [
      'mp'
    ],
    brief="Creates a playlist.",
    description="Creates a playlist with a given name.",
    usage="<playlist name>"
  )
  async def _create_playlist(self, ctx, *, name):
    if bool(self.db_exec(f"SELECT EXISTS(SELECT 1 FROM playlists WHERE u_tag={name.upper()});")):
      raise PLaylistExistsError(name)

    cname = name
    name = name.upper()

    msg = await ctx.send("Please input a description for your playlist:")

    description = await self.bot.wait_for('message', check = lambda message: message.channel == ctx.channel and message.author == ctx.author, timeout=60)


    while True:
      msg = await ctx.send("Please attach the icon you would like to use for this playlist below. Do not delete the message you send or the icon may not work in the future.")

      image = await self.bot.wait_for('message', check = lambda message: message.channel == ctx.channel and message.author == ctx.author, timeout=60)

      if image.attachments == []:
        continue

      else:
        break


    while True:
      msg = await ctx.send("Please send the colour you would like to use for this playlist. Options are Red, Orange, Yellow, Green, Blue, Indigo, and Violet")

      colour = await self.bot.wait_for('message', check = lambda message: message.channel == ctx.channel and message.author == ctx.author, timeout=60)

      if colour.content.upper() not in colours:
        continue

      else:
        colour = colours[colour.content.upper()]
        break


    self.db_exec(f"INSERT INTO playlists VALUES ({name}, {cname}, {image.attachments[0].url}, {ctx.author.name}, {ctx.author.mention}, {ctx.author.id}, {ctx.author.avatar_url})")

    await ctx.send(
      embed = discord.Embed(
        title=cname,
        description=description.content,
        color = colour
      ).set_image(
        url=image.attachments[0].url
      ).set_author(
        name=ctx.author.name,
        icon_url=ctx.author.avatar_url
      )
    )

  @commands.command(
    name="edit-playlist",
    aliases=[
      'ep'
    ],
    brief="Allows you to edit an attribute of a playlist",
    description="Allows you to edit a given attribute of a playlist.\nAvailable attributes:\nname: The systematic name of the playlist.\ncname: the cannonical name of the playlist.\ndescription: the description of the playlist\nimage: the icon of the playlist\ncolour: The colour of the playlist",
    usage="<playlist_name> <attr>"
  )
  async def _edit_playlist(self, ctx, attribute, *, playlist_name):
    attribute = attribute.upper()

    if bool(self.db_exec(f"SELECT EXISTS(SELECT 1 FROM playlists WHERE u_tag={name.upper()});")) == False:
      raise InvalidNameError(name)

    playlists = db_exec("SELECT * FROM playlists;")
    
    attrs = [
      "NAME",
      "CNAME",
      "DESCRIPTION",
      "IMAGE",
      "COLOUR",
      "COLOR" # dirty american support
    ]

    if attribute not in attrs:
      raise InvalidAttributeError(attribute)

    if attribute == "NAME":
      while True:
        msg = await ctx.send("Input a new name for your playlist below:")

        name = await self.bot.wait_for('message', check = lambda message: message.channel == ctx.channel and message.author == ctx.author, timeout=60)

        if name.content.upper() in self.bot.db:
          await ctx.send("That name is already a playlist name. Please input another.")

        else:
          break


      cname = name
      name = name.upper()

      self.bot.db[name] = self.bot.db[playlist_name.upper()]
      self.bot.db[name]['name'] = cname

      del self.bot.db[playlist_name.upper()]

    elif attribute == "CNAME":
      while True:
        msg = await ctx.send("Input a new name for your playlist below:")

        name = await self.bot.wait_for('message', check = lambda message: message.channel == ctx.channel and message.author == ctx.author, timeout=60)

        if name.content.upper() != playlist_name.upper():
          await ctx.send("The CName must only be different from the systematic name in case.")
        else:
          break


      self.bot.db[playlist_name.upper()]['name'] = name.content

    elif attribute == "DESCRIPTION":
      while True:
        msg = await ctx.send("Input a new description for your playlist below:")

        description = await self.bot.wait_for('message', check = lambda message: message.channel == ctx.channel and message.author == ctx.author, timeout=60)

        break


      self.bot.db[playlist_name.upper()]['description'] = description.content

    elif attribute == "IMAGE":
      while True:
        msg = await ctx.send("Attach a new image for your playlist below:")

        image = await self.bot.wait_for('message', check = lambda message: message.channel == ctx.channel and message.author == ctx.author, timeout=60)

        if image.attachments == []:
          await ctx.send("You must attach a new icon for your playlist.")
        else:
          break

      self.bot.db[playlist_name.upper()]['image'] = image.attachments[0].url

    elif attribute == "COLOUR" or attribute == "COLOR":
      while True:
        msg = await ctx.send("Input a new color for your playlist below:")

        colour = await self.bot.wait_for('message', check = lambda message: message.channel == ctx.channel and message.author == ctx.author, timeout=60)

        if colour.content.upper() not in colours:
          await ctx.send("That is not a valid color choice.")
        else:
          break

      self.bot.db[playlist_name.upper()]['colour'] = colours[colour.content.upper()]

  @commands.command(
    name="add-to-playlist",
    aliases=['add', 'atp'],
    brief="Adds a song to a playlist.",
    description="Adds a song to a playlist by name or url.",
    usage="<playlist_name> <query>"
  )
  async def _add(self, ctx, name, *, query):
    name = name.upper()
    
    if str(ctx.author.id) != str(self.bot.db[name.upper()]['author']['id']):
      return

    if name not in self.bot.db:
      raise InvalidNameError(name)
    video = search(query)
    self.bot.db[name]['songs'][query.upper()] = {}
    self.bot.db[name]['songs'][query.upper()]['name'] = query
    self.bot.db[name]['songs'][query.upper()]['url'] = video['url']


    await ctx.send("Song added to playlist.")

  @commands.command(
    name="remove-from-playlist",
    aliases=['rfp', 'r'],
    brief="Removes a song from a playlist.",
    description="Removes a song from a playlist at given index.",
    usage="<name> <song_name>"
  )
  async def _remove_from_playlist(self, ctx, name, *, song_name):

    if name.upper() not in self.bot.db:
      raise InvalidNameError(name)

    if str(ctx.author.id) != str(self.bot.db[name.upper()]['author']['id']):
      return

    del self.bot.db[name.upper()]['songs'][song_name.upper()]

    await ctx.send("Removed song from playlist.")

  @commands.command(
    name="playlist",
    aliases=['pl'],
    brief="Returns a playlist's info.",
    description="Returns important information about a playlist.",
    usage="<name>"
  )
  async def _playlist(self, ctx, *, name):
    if name.upper() not in self.bot.db:
      raise InvalidNameError(name)

    name = name.upper()

    embed = discord.Embed(
        title=self.bot.db[name]['name'],
        description=self.bot.db[name]['description'],
        color = int(self.bot.db[name]['colour'].replace("#", "0x"), base=16)
      ).set_image(
        url=self.bot.db[name]['image']
      ).set_author(
        name=self.bot.db[name]['author']['name'],
        icon_url=self.bot.db[name]['author']['avatar_url']
    )

    songs = []
    i = 0
    n = 0
    embeds = []
    for song in self.bot.db[name]['songs']:
      i += 1
      n += 1
      if i == 5:
        embed.add_field(name=f"``{n}.``", value = f"{self.bot.db[name]['songs'][song]['name']}", inline=False)
        embeds.append(embed)
        embed = discord.Embed(
            title=self.bot.db[name]['name'],
            description=self.bot.db[name]['description'],
            color = int(self.bot.db[name]['colour'].replace("#", "0x"), base=16)
          ).set_image(
            url=self.bot.db[name]['image']
          ).set_author(
            name=self.bot.db[name]['author']['name'],
            icon_url=self.bot.db[name]['author']['avatar_url']
        )
        i = 0
        continue
      embed.add_field(name=f"``{n}.``", value = f"{self.bot.db[name]['songs'][song]['name']}", inline=False)
      continue

    if i!=5 or i!=0:
      embeds.append(embed)


    paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
    await paginator.run(embeds)

def setup(bot: commands.Bot):
  bot.add_cog(Playlists(bot))
