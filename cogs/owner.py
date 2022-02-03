import discord
from discord.ext import commands
from utils import is_it_me
import json

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.check(is_it_me)
    async def blacklist(self, ctx):
        pass


    @commands.command()
    @commands.check(is_it_me)
    async def whitelist(self, ctx):
        pass
    

    @commands.command()
    @commands.check(is_it_me)
    async def reload(self, ctx, extension):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.check(is_it_me)
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(title='Load', description=f'{extension} successfully loaded', color=0xff00c8)
        await ctx.send(embed=embed)
    

    @commands.command()
    @commands.check(is_it_me)
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        embed = discord.Embed(title='Unload', description=f'{extension} successfully unloaded', color=0xff00c8)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Owner(client))