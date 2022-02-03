import discord
import os
from discord.ext import commands, tasks
import discord.ui
from os import listdir
from os.path import isfile, join
import dotenv

dotenv.load_dotenv()
TOKEN = os.environ['TOKEN']

intents = discord.Intents.all()
client = commands.Bot(command_prefix=";", intents=intents, help_command=None, owner_id=624076054969188363,case_insensitive=True)

@client.event
async def on_ready():
    print("=======================\nConnected\n=========")


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
