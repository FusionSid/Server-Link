import discord
from discord.ext import commands
import json

async def create_guild_db(guild):
    pass

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        em = discord.Embed(title="Thanks for inviting me!", description="Use `;help` for help")
        await guild.system_channel.send(embed=em)

        await create_guild_db(guild)


def setup(client):
    client.add_cog(Events(client))