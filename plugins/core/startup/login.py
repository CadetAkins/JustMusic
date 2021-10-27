import discord
from discord.ext import commands

class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as: {self.bot.user.name}, {self.bot.user.id}")
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name="to user requested music!"
            )
        )


def setup(bot):
    bot.add_cog(Login(bot))
