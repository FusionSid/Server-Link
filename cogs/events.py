import discord
from discord.ext import commands
from utils import update_db, get_db, Log

log = Log("./databases/log.txt")

async def create_guild_db(guild):
    db = {
        "guild_id" : guild.id,
        "channel" : None,
        "on" : False,
        "public" : False,
        "banned_users" : {},
        "threads" : {}
    }
    data = await get_db()
    data.append(db)

    update = await update_db(data)

    if update:
        print("Success")
    else:
        print("Failed")

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        em = discord.Embed(title="Thanks for inviting me!", description="Use `;help` for help")
        
        try:
            await guild.system_channel.send(embed=em)
        except:
            for i in guild.text_channels:
                try:
                    e = await i.send(embed=em)
                    print(e)
                except:
                    pass

        await create_guild_db(guild)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        log.log_error(error)
        if isinstance(error, commands.CommandOnCooldown):
            async def better_time(cd: int):
                time = f"{cd}s"
                if cd > 60:
                    minutes = cd - (cd % 60)
                    seconds = cd - minutes
                    minutes = int(minutes / 60)
                    time = f"{minutes}min {seconds}s"
                    if minutes > 60:
                        hoursglad = minutes - (minutes % 60)
                        hours = int(hoursglad / 60)
                        minutes = minutes - (hours*60)
                        time = f"{hours}h {minutes}min {seconds}s"
                return time
                
            cd = round(error.retry_after)
            if cd == 0:
                cd = 1
            retry_after = await better_time(cd)
            em = discord.Embed(
                title="Wow buddy, Slow it down\nThis command is on cooldown",
                description=f"Try again in **{retry_after}**",
            )
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(
                title="Missing a requred value/arg",
                description="You haven't passed in all value/arg",
            )
            await ctx.send(embed=em)

        elif isinstance(error, commands.MissingPermissions):
            em = discord.Embed(
                title="Missing permissions",
                description="You don't have permissions to use this commands",
            )
            await ctx.send(embed=em)

def setup(client):
    client.add_cog(Events(client))