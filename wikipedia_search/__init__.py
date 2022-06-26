from .wiki import Wikipedia

def setup(bot):
    bot.add_cog(Wikipedia(bot))