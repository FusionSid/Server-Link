import discord
from discord.ext import commands

class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def settings(self, ctx):
        pass


    @commands.group()
    async def request(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        else:
            pass # help


    @request.command()
    async def accept(self, ctx):
        pass


    @request.command()
    async def deny(self, ctx):
        pass


def setup(client):
    client.add_cog(Settings(client))