from discord.ext import commands
import config
import traceback, glob

bot = commands.Bot(command_prefix='hm.')

startedFlag = False

@bot.event
async def on_ready():
    global startedFlag
    if startedFlag:
        return

    bot.load_extension('jishaku')
    bot.remove_command('help')
    for cog in sorted(glob.glob('cogs/*.py')+glob.glob('cogs/*/*.py')+glob.glob('cogs/*/*/*.py')):
        name = cog[5:-3].replace('/', '.')
        try:
            bot.load_extension(f'cogs.{name}')
        except Exception as e:
            print('Failed to load extension: cogs.'+name)
            print(traceback.format_exc())

    await bot.sync_commands()

    print('Bot ready')

# pre-load cogs
for cog in sorted(glob.glob('preload_cogs/*.py')+glob.glob('preload_cogs/*/*.py')+glob.glob('preload_cogs/*/*/*.py')):
    name = cog[13:-3].replace('/', '.')
    try:
        bot.load_extension(f'preload_cogs.{name}')
    except Exception as e:
        print('Failed to load extension: preload_cogs.'+name)
        print(traceback.format_exc())

bot.run(config.TOKEN)