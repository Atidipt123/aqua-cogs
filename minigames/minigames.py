from redbot.core import commands

import discord
import requests
import random
import datetime
import asyncio

class MiniGames(commands.Cog):
    """Mini Games on Discord!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trivia(self , ctx):
        '''
        Random Trivia Question
        '''
        r = requests.get('https://opentdb.com/api.php?amount=1&category=17&difficulty=easy&type=multiple').json()
        opt: list = r['results'][0]['incorrect_answers']
        opt.append(r['results'][0]['correct_answer'])
        random.shuffle(opt)

        options = {
            'a': opt[0],
            'b': opt[1],
            'c': opt[2],
            'd': opt[3]
        }

        s = f'''
A: {opt[0]}
B: {opt[1]}
C: {opt[2]}
D: {opt[3]}
        '''
        em = discord.Embed(title=r['results'][0]['question'] , description=s , color=discord.Color.green()).set_author(name=ctx.author.name , icon_url=str(ctx.author.avatar_url)).add_field(name="Category" , value=r['results'][0]['category'])
        await ctx.send(embed=em)
        del s

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            m = await self.bot.wait_for('message' , check=check , timeout=20)
            if options[m.content.lower()] == r['results'][0]['correct_answer']:
                await m.reply(embed=discord.Embed(description="Correct Answer!" , color=discord.Color.green()))
            else:
                await m.reply(f"Wrong answer!\nCorrect Option: [{r['results'][0]['correct_answer']}]")
        except TimeoutError:
            await ctx.send("Timed Out")

    @commands.command()
    async def rps(self , ctx , choice: str = None):
        '''
        Rock Paper Scissors!
        '''

        if choice is None or choice.lower() not in ['rock' , 'paper' , 'scissors']:
            await ctx.send('Missing required parameter `choice`.\n```\n[p]rps <choice Rock|Paper|Scissors>\n```')
            return

        choice = choice.lower()
        comp = random.choice(['rock' , 'paper' , 'scissors'])

        if choice == comp:
            em = discord.Embed(title="Rock Paper Scissors!" , description="Its a Tie." , color=discord.Colour.gold() , timestamp=datetime.datetime.now())
            em.add_field(name="You" , value=choice , inline=False)
            em.add_field(name="Computer" , value=comp , inline=False)
            await ctx.send(embed=em)

        elif choice == 'rock' and comp == 'paper':
            em = discord.Embed(title="Rock Paper Scissors!" , description="You Lose!" , color=discord.Colour.red() , timestamp=datetime.datetime.now())
            em.add_field(name="You" , value=choice , inline=False)
            em.add_field(name="Computer" , value=comp , inline=False)
            await ctx.send(embed=em)

        elif choice == 'scissors' and comp == 'rock':
            em = discord.Embed(title="Rock Paper Scissors!" , description="You Lose!" , color=discord.Colour.red() , timestamp=datetime.datetime.now())
            em.add_field(name="You" , value=choice , inline=False)
            em.add_field(name="Computer" , value=comp , inline=False)
            await ctx.send(embed=em)

        elif choice == 'paper' and comp == 'scissors':
            em = discord.Embed(title="Rock Paper Scissors!" , description="You Lose!" , color=discord.Colour.red() , timestamp=datetime.datetime.now())
            em.add_field(name="You" , value=choice , inline=False)
            em.add_field(name="Computer" , value=comp , inline=False)
            await ctx.send(embed=em)

        elif choice == 'rock' and comp == 'scissors':
            em = discord.Embed(title="Rock Paper Scissors!" , description="You Win!" , color=discord.Colour.green() , timestamp=datetime.datetime.now())
            em.add_field(name="You" , value=choice , inline=False)
            em.add_field(name="Computer" , value=comp , inline=False)
            await ctx.send(embed=em)

        elif choice == 'scissors' and comp == 'paper':
            em = discord.Embed(title="Rock Paper Scissors!" , description="You Win!" , color=discord.Colour.green() , timestamp=datetime.datetime.now())
            em.add_field(name="You" , value=choice , inline=False)
            em.add_field(name="Computer" , value=comp , inline=False)
            await ctx.send(embed=em)

        elif choice == 'paper' and comp == 'rock':
            em = discord.Embed(title="Rock Paper Scissors!" , description="You Win!" , color=discord.Colour.green() , timestamp=datetime.datetime.now())
            em.add_field(name="You" , value=choice , inline=False)
            em.add_field(name="Computer" , value=comp , inline=False)
            await ctx.send(embed=em)

    @commands.command()
    async def gtn(self , ctx):
        '''Guess The Number!'''

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        number = random.randint(1, 10)
        await ctx.send("You have 3 chances to guess the number! The number lies between 1 and 10, including both endpoints.")

        for i in range(0, 3):
            await ctx.send(f'Send a number. You have `{3-i}` chances left.')
            try:
                response = await self.bot.wait_for('message' , check = check , timeout = 30)
            except asyncio.TimeoutError:
                await ctx.send("You didnt reply on time!")
                
            guess = int(response.content)

            if guess > number:
                await ctx.send('Wrong Number!\nHint-__Your number is bigger than the answer__')
                continue
            
            elif guess < number:
                await ctx.send('Wrong Number!\nHint-__Your number is smaller than the answer__')
                continue

            else:
                await ctx.send('You guessed the number!')
                break

    @commands.command()
    async def coinflip(self , ctx , side: str = None):
        '''
        Guess where the coin will land!
        '''
        if side is None or side.lower() not in ['heads' , 'tails']:
            await ctx.send("Missing required parameter `side`.\n```\n[p]coinflip <side Heads|Tails>\n```")
            return

        x = random.choice(['heads' , 'tails'])

        if side.lower() == x:
            await ctx.send(f'You guessed it right! The coin landed on __{x}__.')
        else:
            await ctx.send(f'You guessed it wrong! The coin landed on __{x}__.')