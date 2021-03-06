import discord
import os
import platform
from discord.ext import commands
import psutil


def get_lines():
    lines = 0
    files = []
    for i in os.listdir():
        if i.endswith(".py"):
            files.append(i)
    for i in os.listdir("cogs/"):
        if i.endswith(".py"):
            files.append(f"cogs/{i}")
    for i in os.listdir("utils/"):
        if i.endswith(".py"):
            files.append(f"utils/{i}")
    for i in files:
        count = 0
        with open(i, 'r') as f:
            for line in f:
                count += 1
        lines += count
    return lines


class Utilities(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bot', 'invite'])
    async def botinvite(self, ctx):
        await ctx.send(embed=discord.Embed(title="Invite **Server Link** to your server:", description="https://discord.com/api/oauth2/authorize?client_id=896932646846885898&permissions=8&scope=bot%20applications.commands"))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! jk\n{round(self.client.latency * 1000)}ms")

    @commands.command()
    async def botinfo(self, ctx):
        em = discord.Embed(title='Server Link')
        em.add_field(inline=True, name="Server Count",value=f"{len(self.client.guilds)}")
        em.add_field(inline=True, name="User Count", value=len(list(self.client.get_all_members())))
        em.add_field(inline=True, name="Command Count",value=f"{len(self.client.commands)} commands")
        em.add_field(inline=True, name="Ping",value=f"{round(self.client.latency * 1000)}ms")
        em.set_footer(text="Made by FusionSid#3645")
        em.add_field(name='CPU Usage',value=f'{psutil.cpu_percent()}%', inline=True)
        em.add_field(name='Memory Usage',value=f'{psutil.virtual_memory().percent}% of ({round((psutil.virtual_memory().total/1073741824), 2)}GB)', inline=True)
        em.add_field(name='Available Memory',value=f'{round(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%', inline=True)
        em.add_field(inline=True, name="Python version",value=f"{platform.python_version()}")
        em.add_field(inline=True, name="Running on",value=f"{platform.system()} {platform.release()}")
        em.add_field(name="Python code", value=f"{get_lines()} of code")
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Utilities(client))
