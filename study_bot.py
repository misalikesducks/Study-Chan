import discord #import the discord package 
from discord.ext import commands, tasks
import pandas as pd #pandas is a framework that works with tables and databases 
import random
import datetime
import sched
import time 
#client for the bot 
client = commands.Bot(command_prefix='study ')

@client.command()
async def helpme(context): #context holds context on how this was called   help embed 
    myEmbed = discord.Embed(title="help you?", description="i cant help you", color=0xCC7178)
    myEmbed.set_thumbnail(url='https://i.pinimg.com/564x/1c/c6/1b/1cc61b959292039e4b3ca0fd8b30bcba.jpg')
    myEmbed.set_author(name='Commands', icon_url='https://cdn.discordapp.com/attachments/774840217865158688/774884501163737128/image0.jpg')
    myEmbed.add_field(name="Log your Days:", value="study clockin (clock, cl, clo)", inline=False)
    myEmbed.add_field(name="Magic 8Ball:", value="study 8ball (eightball)", inline=False)
    myEmbed.add_field(name="Motivation:", value="study motivation (lazy)", inline=False)
    
    await context.message.channel.send(embed=myEmbed)


@client.command() #timer
async def timer(ctx, time: int):
    await ctx.send("Starting timer")
    def check(message):
        return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
    try:
        m = await client.wait_for("message", check=check, timeout=time)
        await ctx.send("Countdown cancelled")
    except:
        await ctx.send(f"{ctx.author} no more studying")

#check in
@client.command(aliases=['clock', 'cl', 'clo'])
async def clockin(context):
    #df = pd.DataFrame({"Name":["hello", "test"]}) 
    #df.to_csv('/Users/connie/Desktop/Discord Bot/output.csv')
    df = pd.read_csv('output.csv', index_col=0) 
    user = context.message.author
    duplicate = False
    index = 0
    for i in df.index: 
        if df.loc[i].User == str(user):
            num = df.loc[i].Streaks 
            df.at[i, "Streaks"] = num + 1
            duplicate = True
            df.to_csv('output.csv')
            index = i
            break

    if not duplicate: 
        df = df.append({"User": str(user),"Streaks": 1}, ignore_index=True)
        df.to_csv('output.csv')
    #df.at[i, "Streaks"] 
    myEmbed = discord.Embed(description="this is how you've been studying", color=0xCC7178)
    myEmbed.set_author(name=str(user), icon_url=user.avatar_url)
    myEmbed.add_field(name="Days of Torture:", value=df.loc[index].Streaks, inline=False)
    myEmbed.set_thumbnail(url=user.avatar_url)
    await context.message.channel.send(embed=myEmbed)

@client.command(aliases=['8ball', 'eightball'])
async def _8ball(context, *, question):
    responses = ['no u dum', 'yes', 'fates are in your favour', 'maybe', 'nope', 'go study', 'no', 'seems likely', 'perhaps',
                'dont count on it', 'my nonexistent braincells say no', 'cannot predict now', 'oops idk', 'try again?'
                'signs point to yes', 'most likely', 'sure']
    await context.message.channel.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

#mcdonalds
@client.command(aliases=['motivate', 'lazy'])
async def motivation(context):
    responses = ['https://careers.mcdonalds.com/main/jobs/75357003-71BF-4B02-9050-A9BD013A90F7?lang=en-us',
                'https://careers.mcdonalds.com/main/jobs/51F5D22A-3CF7-4DF9-8C72-A6BB0179D88D?lang=en-us',
                'https://www.indeed.com/viewjob?cmp=Montco--Rooter-of-Montgomery,-Chester,-Delaware,-Berks,-Bucks-and-Lehigh-Counties&t=Experience+Plumber+Sewer+Drain+Cleaner&jk=4b78ab747f512900&sjdu=QwrRXKrqZ3CNX5W-O9jEvfWeEUhkAr3amPxUm5TO9U6RdXsVLxSVASkojNKm8V0HGL3JRNsWCjseMglbvu2zJ7mSBgNigDRBaUkVi6bq0tCFWZi7J6T5dsAdCDdWjO2u&tk=1emitgas534nb000&adid=361019449&ad=-6NYlbfkN0D4ojF2GkQhVGZdjtHMfJzC0g8XVl8_qh2SsMp0Uts_8p8RToJ3I4ryxCRPLd2IxTLuLV69Wpm8et1I0Ecdxt93-unJF1Y90H00qHH2q__FbbUksht5qHQih8M-C5eAhiJ8Y99GrUFwG8lhEbXM2V_7vtBDQ4WmBU4Tj3SCywc-G8OuCUSCm7oP98UZQviY8WmAkFTuINol83Wyn2bYh9EFpMn5h-_f-m0do4CIWYc-7RAmFRVFpyRJrOFzSOJ4-QlvrKqtqS7DHn5-hW3gB5OGYpBnmgySKaSpnVaMiFuEuQomIjKum6rfJN1TtnjtYnk64aQZpFZfB738U65nIH00&pub=4a1b367933fd867b19b072952f68dceb&vjs=3',
                'https://www.simplyhired.com/job/ysJa3CVKw2hqGEy_9xHRPiyTf-7LRL2Ev85rnHfL92zGx91khsgM6w?isp=1&sjdu=cnx0XGv_IhRgPmexAqJH77xfXIh50tCaD6N0YSs5xxol7_T3JjVL2i47IZsI2WvM1foGwFy0cw4-ZiSeawSz3020uYrXcLNyuHkB_sm5WpPVw4qeChl0URcxu0lJf_NE7fq9erz_8jnam2qQEuJWUOg10g&advNum=1071146325689980&q=vomit+cleaner',
                'https://www.indeed.com/viewjob?cmp=DoodyCalls---Central-Jersey&t=Pooper+Scooper&jk=44ea8479ca800379&sjdu=QwrRXKrqZ3CNX5W-O9jEvfL5Z989XHr2tDhrH0FUmcC2oZAzX2y4YI5AeKVxDA8n1fzC1lgHxnXH1bEa0f7En3MXPbjNQnbtC4kUdGsQSi4&tk=1emits9vl34nb000&adid=329724429&ad=-6NYlbfkN0AsBQcbsuNMq7_Pd5WiFPsuRq_2eGkX1lcVGQzgkDJxvi_2jcvJeha7vApRUJVKsTtYpKCzuly3y3c2tuFayIoGehp66wrwMT0Z_LCW1wgMKvLaXEtRi20Px5WLHyJxoaH5zlSnjzI9WZnVJSidn0krcQ_OQPj6yrIDOXXsej3JANjGQawBIwUkcPx7A-u4acm2ul6mCyDsNlXQVpo0-ZWvQJ_dN1B5QNepvRL0buStDO3c4crwKmGpws4G6et6UhF2fmF--vRo4tPifty_b3BpdtEw8G9mEvd_yFikkVCOxzgsXYuRjJcn5oSg2pfQmZX2M9_9y4XeBg-vXfcTmIgB&pub=4a1b367933fd867b19b072952f68dceb&vjs=3',
                'https://www.indeed.com/viewjob?cmp=Family-Counseling-Center-of-the-CSRA&t=Urine+Drug+Screen+Collector+Observer&jk=3c36cd5e860cfae4&q=Urine+Drug+Specimen+Collector&vjs=3',
                'idk man, life struggle struggly and then you gurgle gurgle',
                "when life gives you lemons you eat poo"]
    await context.message.channel.send(f'You have a bright future ahead:\n{random.choice(responses)}')

#error
@client.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandNotFound):
        await context.message.channel.send('lol thats not a command')

#error for 8ball
@_8ball.error
async def _8ball_error(context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await context.message.channel.send('u didnt ask me a question')

#sends msg to general whesn bot joins server
@client.event
async def on_connect():
    #retrieving the channel we want access to
    text_channel = []
    for guild in client.guilds:
        for channel in guild.text_channels: 
            text_channel.append(client.get_channel(channel.id))
            
    general = text_channel[0]
    await general.send('im here, oWo')

#sets the status of bot when it's online
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name="you study"))

#run the client on the server 
client.run('Nzc0Njg1NjYyMzcyMTY3NzQx.X6bYPg.kdrmOHN7C0_hDiqsYGFt2uqMhgI') #takes in the token that allows to connect from bot that we coded to the server 