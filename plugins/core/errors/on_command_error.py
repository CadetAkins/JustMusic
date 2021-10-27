import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound):
      return # silence command not found errors 

    await ctx.send(
      embed=discord.Embed(
        title=str(error.__class__.__name__),
        description="```\n" + str(error) + "```",
        color=discord.Colour.red()
      )
    )

def setup(bot: commands.Bot):
  bot.add_cog(ErrorHandler(bot))
