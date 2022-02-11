from discord import ApplicationContext
from discord.ext import commands
import markovify
import asyncio

class Markov(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.model_text = open('model.json', 'r', encoding='utf8').read()
        self.model = markovify.Text.from_json(self.model_text)
    
    @commands.slash_command(name='make', description='文章を生成します')
    async def make(self, ctx: ApplicationContext):
        text = self.model.make_sentence(tries=100).replace(' ', '')
        await ctx.interaction.response.send_message(text)

def setup(bot):
    bot.add_cog(Markov(bot))