import discord
import wikipedia

from redbot.core import commands

class Wikipedia(commands.Cog):
    """Browse wikipedia on Discord!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wikipedia(self , ctx , * , term: str = None):
        '''Search wikipedia from discord.'''
        if term is None:
            await ctx.send('`term` is a required parameter which is missing.\n```\n[p]wikipedia <term>\n```')
            return

        s = wikipedia.search(term)
        page = wikipedia.page(term)

        em = discord.Embed(title=str(page.title) , description=str(wikipedia.summary(term)) , url=str(page.url) , color=discord.Color.green())
        await ctx.send(embed=em)