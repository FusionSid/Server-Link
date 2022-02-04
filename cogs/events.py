import discord
from discord.ext import commands
from utils import update_db, get_db

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


def setup(client):
    client.add_cog(Events(client))