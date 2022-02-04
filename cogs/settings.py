import discord
from discord.ext import commands
from utils import get_db, update_db

class GuildRequest(discord.ui.View):
    def __init__(self, guild, ctx, channel):
        super().__init__(timeout=100)
        self.guild = guild
        self.ctx = ctx
        self.channel = channel
    

    @discord.ui.button(style=discord.ButtonStyle.green, label="Accept", custom_id="accept")
    async def accept(self, button, interaction):
        for i in self.children:
            i.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Accepted")

        thread = None
        thread2 = None

        async for message in self.channel.history(limit=1):
                thread = await message.create_thread(name=self.ctx.guild.name)
                break

        data = await get_db()

        for i in data:
            if i['guild_id'] == self.ctx.guild.id:
                channel2 = i['channel']
        
        if channel2 is None:
            em = discord.Embed(
                title = "Request Failed",
                description = "Server does not have a channel set\nAsk server owner or admin to use `;setchannel`"
            )
            return await self.ctx.send(embed=em)
    
        try:
            channel2 = await self.ctx.guild.fetch_channel(channel2)
        except:
            em = discord.Embed(
                title = "Request Failed",
                description = "Server does not have a channel set\nAsk server owner or admin to use `;setchannel`"
            )
            return await self.ctx.send(embed=em)

        async for message in channel2.history(limit=1):
                thread2 = await message.create_thread(name=self.guild.name)
                break

        for i in data:
            if i["guild_id"] == self.guild.id:
                i["threads"][self.ctx.guild.id] = thread.id
        
        for i in data:
            if i["guild_id"] == self.ctx.guild.id:
                i["threads"][self.guild.id] = thread2.id

        await thread.send(embed=discord.Embed(title='Server Link!', description="Created"))
        await thread2.send(embed=discord.Embed(title='Server Link!', description="Created"))

        update = await update_db(data)

        if update:
            print("Success")
        else:
            print("Failed")

    @discord.ui.button(style=discord.ButtonStyle.red, label="Deny", custom_id="deny")
    async def deny(self, button, interaction):
        for i in self.children:
            i.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Denied")
        data = await get_db()

        for i in data:
            if i['guild_id'] == self.ctx.guild.id:
                channel = i['channel']
        await self.ctx.guild.fetch_channel(channel)
        em = discord.Embed(
                title = "Request Denied",
                description = "The server decided to deny your request"
            )
        await channel.send(embed=em)



async def send_request(guild, ctx):
    data = await get_db()

    for i in data:
        if i['guild_id'] == guild.id:
            channel = i['channel']
    
    if channel is None:
        em = discord.Embed(
            title = "Request Failed",
            description = "Server does not have a channel set\nAsk server owner or admin to use `;setchannel`"
        )
        return await ctx.send(embed=em)
    
    try:
        channel = await guild.fetch_channel(channel)
    except:
        em = discord.Embed(
            title = "Request Failed",
            description = "Server does not have a channel set\nAsk server owner or admin to use `;setchannel`"
        )
        return await ctx.send(embed=em)
    
    request_em = discord.Embed(
        title = "New Guild Request", 
        description = f"Guild: {guild.name}, ID: {guild.id}"
    )

    update = await update_db(data)

    if update:
        print("Success")
    else:
        print("Failed")

    view = GuildRequest(guild, ctx, channel)
    await channel.send(embed=request_em, view=view)


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def settings(self, ctx):
        pass


    @commands.command()
    async def setchannel(self, ctx, channel:discord.TextChannel):
        data = await get_db()
        for guild in data:
            if guild['guild_id'] == ctx.guild.id:
                guild['channel'] = channel.id
        
        update = await update_db(data)

        if update:
            print("Success")
        else:
            print("Failed")


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

    
    @request.command()
    async def send(self, ctx, guild:int):
        guild_ids = []
        for i in self.client.guilds:
            guild_ids.append(i.id)
        
        if guild not in guild_ids:
            em = discord.Embed(
                title = "Request Failed",
                description = "Server either doesn't exist or doesn't have this bot on it.\nFor the bot to work it must be on both servers"
            )
            return await ctx.send(embed=em)

        guild = await self.client.fetch_guild(guild)

        await send_request(guild, ctx)
            


def setup(client):
    client.add_cog(Settings(client))