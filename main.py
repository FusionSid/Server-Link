import discord
import os
from discord.ext import commands
import discord.ui
from os import listdir
from os.path import isfile, join
import dotenv
from utils import update_db, get_db

dotenv.load_dotenv()
TOKEN = os.environ['TOKEN']

intents = discord.Intents.all()
client = commands.Bot(command_prefix=";", intents=intents, help_command=None, owner_id=624076054969188363,case_insensitive=True)

async def cross_server(message):
    other_guild, other_guild_data = None,  None
    data = await get_db()

    try:
        for i in data:
            if i['guild_id'] == message.guild.id:
                guild_data = i
        
        for key, value in guild_data['threads'].items():
            if value == message.channel.id:
                other_guild = int(key)
                the_thread = int(value)

        for i in data:
            if i['guild_id'] == other_guild:
                other_guild_data = i

        for key, value in other_guild_data['threads'].items():
            if int(key) == message.guild.id:
        
                em = discord.Embed(description=message.content)
                em.set_author(name=message.author.name, url=message.author.avatar.url)

                guild = await client.fetch_guild(other_guild_data["guild_id"])
                print(guild.id, the_thread)
                send_channel = guild.get_thread(the_thread)

                return await send_channel.send(embed=em)
    except Exception as e:
        print(e)


@client.event
async def on_ready():
    print("=======================\nConnected\n=========")


@client.event
async def on_message(message):
    await cross_server(message)
    await client.process_commands(message)

def start_bot(client):
    
    lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
    no_py = [s.replace('.py', '') for s in lst]
    startup_extensions = ["cogs." + no_py for no_py in no_py]
    try:
        for cogs in startup_extensions:
            client.load_extension(cogs)

            print(f"Loaded {cogs}")

        print("\nAll Cogs Loaded\n===============\nLogging into Discord...")
        
        client.run(TOKEN)

    except Exception as e:
        print(f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")


if __name__ == '__main__':
    start_bot(client)
