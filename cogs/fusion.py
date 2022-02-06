import discord
from utils import get_db
import os
import json
from discord.ext import commands
import dotenv
from utils import is_it_me, Log
from subprocess import run
import time
from os import listdir
from os.path import isfile, join

log = Log("./database/log.txt", timestamp=True)

dotenv.load_dotenv()


class Fusion(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(is_it_me)
    async def reload(self, ctx, extension):
        self.client.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
        await ctx.send(embed=embed)

    @commands.group()
    @commands.check(is_it_me)
    async def git(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        else:
            return await ctx.send(embed=discord.Embed(title=f"Git Commands", description="?git pull\n?git status\n?git add\n?git commit\n?git push"))

    @git.command()
    @commands.check(is_it_me)
    async def pull(self, ctx):
        output = run(["git", "pull"], capture_output=True).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.check(is_it_me)
    async def status(self, ctx):
        output = run(["git", "status"], capture_output=True).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.check(is_it_me)
    async def add(self, ctx):
        output = run(["git", "add", "."], capture_output=True).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.check(is_it_me)
    async def commit(self, ctx):
        output = run(["git", "commit", "-m", "'Updated File'"],
                     capture_output=True).stdout

        await ctx.send(output.decode())

    @git.command()
    @commands.check(is_it_me)
    async def push(self, ctx):
        output = run(["git", "push"], capture_output=True).stdout

        await ctx.send(output.decode())

    @commands.command()
    @commands.check(is_it_me)
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Load', description=f'{extension} successfully loaded', color=0xff00c8)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(is_it_me)
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title='Unload', description=f'{extension} successfully unloaded', color=0xff00c8)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(is_it_me)
    async def serverlist(self, ctx):
        servers = list(self.client.guilds)
        await ctx.send(f"Connected on {str(len(servers))} servers:")
        await ctx.send('\n'.join(guild.name for guild in servers))

    @commands.command()
    @commands.check(is_it_me)
    async def message_servers(self, ctx, *, message):
        data = await get_db()
        for guild in self.client.guilds:
            for i in data:
                if i['guild_id'] == guild.id:
                    if i['channel'] is None:
                        break
                    else:
                        try:
                            channel = await self.client.fetch_channel(i["channel"])
                            await channel.send(message)
                            break
                        except:
                            break

    @commands.command(aliases=['dmr'])
    @commands.check(is_it_me)
    async def dmreply(self, ctx, *, msg=None):
        if ctx.message.reference is None:
            return
        else:
            await ctx.message.delete()
            id = ctx.message.reference.message_id
            id = await ctx.channel.fetch_message(id)
            await id.reply(msg)
            id = int(id.content)
        person = await self.client.fetch_user(id)

        if msg is None:
            pass
        else:
            await person.send(msg)

        if ctx.message.attachments is None:
            return
        else:
            for i in ctx.message.attachments:
                em = discord.Embed()
                em.set_image(url=i.url)
                await person.send(embed=em)

    @commands.command()
    @commands.check(is_it_me)
    async def logs(self, ctx):
        file = discord.File("./database/log.txt")
        await ctx.author.send(file=file)

    @commands.command()
    @commands.check(is_it_me)
    async def reloadall(self, ctx):
        lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
        no_py = [s.replace('.py', '') for s in lst]
        startup_extensions = ["cogs." + no_py for no_py in no_py]
        startup_extensions.remove("cogs.Leveling")

        try:
            for cogs in startup_extensions:
                self.client.reload_extension(cogs)

            await ctx.send("All Reloaded")

        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if isinstance(message.channel, discord.DMChannel):

            cha = await self.client.fetch_channel(926232260166975508)
            em = discord.Embed(
                title="New DM", description=f"From {message.author.name}")

            if message.content != "":
                em.add_field(name="Content", value=f"{message.content}")
            await cha.send(content=f"{message.author.id}", embed=em)

            if message.attachments is not None:
                for attachment in message.attachments:
                    em = discord.Embed(title="** **")
                    em.set_image(url=attachment.url)
                    await cha.send(embed=em)


def setup(client):
    client.add_cog(Fusion(client))
