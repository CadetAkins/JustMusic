import discord, DiscordUtils; from discord.ext import commands

class InvalidCommandError(Exception):
  def __init__(self, command_name: str):
    self.output = "The command, {} ,you attempted to get information on does not exist.".format(command_name)

  def __str__(self):
    return self.output

class Help(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot=bot
    self.name="Help category:"

  @commands.command(
    name="help",
    aliases=[
      'h'
    ],
    brief="Displays information about the bot commands",
    description="Displays information about the bot commands or a specific command",
    usage="<command: optional>"
  )
  async def _help(self, ctx, command=None):
    prefix = "-"
    if command == None:
      embed_array = [] 
      for cog in self.bot.cogs:
        cog = self.bot.get_cog(cog)
        if len(cog.get_commands()) < 1:
          continue
        embed = discord.Embed(
          title=cog.name,
          color=discord.Colour.dark_blue()
        ).set_footer(
          text="For more information on a specific command run {}help <command>".format(prefix)
        )
        #iterate through commands
        for command in cog.get_commands():
          embed.add_field(
            name=f"**{command.name}**",
            value=command.brief,
            inline=False
            )
        embed_array.append(embed)
      paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
      await paginator.run(embed_array)
    else:
      command = command.upper()
      commands = {}
      for command_obj in self.bot.commands:
        commands[command_obj.name] = command_obj
        for alias in command_obj.aliases:
          commands[alias] = command_obj
          
      if command.lower() not in commands:
        raise InvalidCommandError(command)
      else:
        command_obj = commands[command.lower()]
        await ctx.send(
          embed=discord.Embed(
            color=discord.Colour.green(),
            description=command_obj.description
          ).set_author(
            name=command_obj.name
          ).add_field(
            name="Usage:",
            value="{0}{1}{2} {3}".format(
              prefix,
              command_obj.name,
              command_obj.aliases,
              command_obj.usage
            ),
            inline=False
          )

        )

def setup(bot):
  bot.add_cog(Help(bot))
