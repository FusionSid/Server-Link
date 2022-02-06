import discord
import os
from discord.ext import commands, tasks
import discord.ui
from os import listdir
from os.path import isfile, join
import dotenv
from utils import update_db, get_db, Log
import asyncio

dotenv.load_dotenv()
TOKEN = os.environ['TOKEN']

log = Log(path="databases/log.txt")

intents = discord.Intents.all()
client = commands.Bot(command_prefix=">", intents=intents, help_command=None, owner_id=624076054969188363,case_insensitive=True)

@tasks.loop(hours=12.0)
async def threads_keep_alive():
    threads = {}
    data = await get_db()
    for i in data:
        if i['threads']:
            for key, value in i['threads'].items():
                threads[value] = i['channel']
    for key,value in threads.items():
        cha = int(key)
        thr = int(value)
        try:
            thread = await client.fetch_channel(cha)
            #thread = channel.get_thread(thr)
            msg = await thread.send("** **")
            await asyncio.sleep(1)
            await msg.delete()
        except Exception as e:
            print(e)

async def cross_server(message):
    try:
        guild1 = message.guild.id

        guild_1_data, guild_2_data, guild2 = None, None, None

        data = await get_db()

        for i in data:
            if i['guild_id'] == guild1:
                if i['channel'] is None:
                    return
                if i['threads'] == False:
                    return
                guild_1_data = i

        for key, value in guild_1_data['threads'].items():
            if value == message.channel.id:
                guild2 = int(key)
        
        for i in data:
            if i['guild_id'] == guild2:
                guild_2_data = i
                channel = i['channel']
                if i['threads'] == False:
                    return
                if channel is None:
                    return

        for key, value in guild_2_data['threads'].items():
            if int(key) == guild1:
                thread = int(value)
                em = discord.Embed(description=message.content)
                if message.author.avatar is not None:
                    em.set_author(name=message.author.name, url=message.author.avatar.url)
                else:
                    em.set_author(name=message.author.name, url=message.author.default_avatar)

                channel = await client.fetch_channel(channel)
                thread = channel.get_thread(thread)

                return await thread.send(embed=em)
    except Exception as e:
        pass

@client.event
async def on_ready():
    print("=======================\nConnected\n=========")
    log.log_message("Bot is connected to discord")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id == 938913496442212392:
        return
    await cross_server(message)
    await client.process_commands(message)

def start_bot(client):
    log.log_message("Starting up bot")
    threads_keep_alive.start()
    lst = [f for f in listdir("cogs/") if isfile(join("cogs/", f))]
    no_py = [s.replace('.py', '') for s in lst]
    startup_extensions = ["cogs." + no_py for no_py in no_py]
    try:
        for cogs in startup_extensions:
            client.load_extension(cogs)

            print(f"Loaded {cogs}")

        print("\nAll Cogs Loaded\n===============\nLogging into Discord...")
        log.log_message("All Cogs Loaded - Logging into Discord")
        
        client.run(TOKEN)

    except Exception as e:
        print(f"\n###################\nPOSSIBLE FATAL ERROR:\n{e}\nTHIS MEANS THE BOT HAS NOT STARTED CORRECTLY!")


if __name__ == '__main__':
    start_bot(client)
