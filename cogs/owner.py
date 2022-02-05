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

def setup(client):
    client.add_cog(Owner(client))