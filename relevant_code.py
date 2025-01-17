import discord
from discord import user
import json, random, os
import DB, time
from keep_alive import keep_alive #Used on replit, to keep bot alive
from discord.ext import commands
import asyncio


## Configure Bots
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
token = os.environ['DISCORD_TOKEN']
client.run(token)


## If the bot is ready, on_read() will be triggered
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    
## Once user is typing, bot can detect "which channel, which user, and when" and following will be triggered
# @client.event
# async def on_typing(channel, user, when):
#     print("send DM to typing user")
#     await user.send('''  Send before you think twice.
#     {}
#     {}
#     '''.format(channel.name, when))


## If the bot is ready, on_read() will be triggered
async def send_join_msg(member) :
    start_msg = '''
Hello, This is Brina's Bot testing channel

```diff
- Discord red text
```

```css
[Discord orange-red text]
```
Include emoji :watermelon:
GIF : 
https://tenor.com/view/wtf-huh-what-the-heck-puppy-cute-gif-17738058
    '''
    embed = discord.Embed(
        color= discord.Colour.dark_teal() # or any color you want
    )
    embed.add_field(name='If you wish to know more please go to following link,' ,value='[Getting started Link](https://discord.com/channels/741527808400031854/849631605660057630/849631816557133874)', inline=False)
    embed.add_field(name='Second things you need to know' ,value='[Go to another Channel](https://discord.com/channels/741527808400031854/848522274528034837/849646113140768788)', inline=False)
    embed.add_field(name='VIdeo ' ,value='[VIdeo](https://www.youtube.com/watch?v=EphQsR3-_-U&ab_channel=CeeCee)', inline=False)

    await member.send(content = start_msg ,embed=embed)

def get_all_users():
    # guiId = 741527808400031858
    user_list = []
    all_members = client.get_all_members()
    for member in all_members:
        user_list.append(member)
    
    return user_list
    
    
## Such message prepare the interactive template for introduction bot
async def join_verify(ctx):
    ## Join page
    Welcome_page = discord.Embed(
        title = "Welcome join this Discord Channel",
        description = "Please answer the following answer to verify your role",
        colour = discord.Colour.orange()
    )
    message = await ctx.author.send(embed = Welcome_page)

    await message.add_reaction("\U0001F44D")
    await message.add_reaction("\U0001F44E")
    accept = False



    while True:
        # However, in the DM, user is the bot
        reaction, user = await client.wait_for('reaction_add', check = check)
        if str(reaction) =="\U0001F44D":
            accept = True
            break
        else:
            await user.send("Sorry you cannot join us!")
            break

    await message.delete()

    ## Degree select page
    degree_page = discord.Embed(
        title = "Please select wheter you're bachelor, master, phd",
        description = "Select bat if you're bachelor, horse if you're master, select duck if you're doctor",
        colour = discord.Colour.orange()
    )
    message = await ctx.author.send(embed = degree_page)
    def check(reaction, user):
        return user != message.author

    bachelor= "🦇"
    master = "🐴"
    doc="🦆"
    await message.add_reaction(bachelor)
    await message.add_reaction(master)
    await message.add_reaction(doc)
    status = -1
    role_name = 'TEST_users'
    while True:
            # However, in the DM, user is the bot
            reaction, user = await client.wait_for('reaction_add', check = check)
            if str(reaction) =="🦇":
                print("user {} is a bachelor".format(user))
                role_name = "bachelor"
                break
            elif str(reaction) =="🐴":
                print('user {} is master'.format(user))
                status = 1
                role_name = "master"
                break

            elif str(reaction) =="🦆":
                print('user {} is doctor'.format(user))
                role_name = "phd"
                status = 2
                break
    await asyncio.sleep(5)

    # KEY, add_role 要是 member
    # need extra find member, now 
    await add_role(ctx.author, role_name)
    await message.delete()
    # According status to give user role


    ## Add school page
    



async def interaction(ctx):
    if not hasattr(interaction, "result"):
        interaction.result = {}

    page1 = discord.Embed(
        title = "Invitation to xxx presentaion",
        description = "This event is hosted by xxxx, and xxxx is going to share his/her experience in finding xxx job. PLease let us know whether your interested! NOTE: PLEASE select the following two emoji to join or not",
        colour = discord.Colour.orange()
    )
    page2 = discord.Embed(
        title = "Sorry to see that you declined our invitation",
        description = "Hope we can see you next time!",
        colour = discord.Colour.orange()
    )
    page3 = discord.Embed(
        title = "Glad you choose to accept!",
        description = "Looking forward to seeing you in person!",
        colour = discord.Colour.orange()
    )
    pages = [page1, page2, page3]

    # all_users = get_all_users()
    message = await ctx.channel.send(embed = page1)
    # message = await ctx.author.send(embed = page1)
    # all_users = [user for user in all_users if user.name != "LuisHsu" and user.name !="Token_Bot_test"]

    # message = await user.send(embed = page1)

    await message.add_reaction("\U0001F44D")
    await message.add_reaction("\U0001F44E")

    # print(message)
    # print(user)
    i = 0
    reaction = None
    def check(reaction, user):
        return user != message.author

        # print(user, ctx.author, message.author)
        ## KEY, If in the public channel, the user will be the ctx.author (the person typein $interaction)
        # return user == ctx.author 

        ## KEY, If in the private(DM) channel, the user wiil become the bot, so we need to check 
        # return user == message.author

    while True:
        try:
            # KEY, for the same reason, in the public channel, the user will be the actual person
            # However, in the DM, user is the bot
            reaction, user = await client.wait_for('reaction_add', timeout= 10.0, check = check)
            if str(reaction) =="\U0001F44E":
                i = 1
                print('DECLINED')
                # await message.edit(embed = pages[i])
            elif str(reaction) == "\U0001F44D":
                i = 2
                print('ACCEPT')
                # await message.edit(embed = pages[i])

            interaction.result[user.name] = i

            # clarify who's user, owner
            # print(reaction, user, message.author, ctx.author)
            print(interaction.result)
            # await message.remove_reaction(reaction, user)

            # Private channel
            # await message.remove_reaction(reaction, ctx.author)

        except Exception as e:
            print(e)
            break

    print(interaction.result)
    # print(user_feedback)
    await ctx.channel.send(interaction.result)
    # Than we can base on user's decision to Update inforamtion to DB
    # await message.clear_reactions()
    await message.delete()
    # await message.clear_reactions()


## **Important, Bot will detect users' message, and it can further detect the response of users
## Can be used to mimic command
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    author = message.author
    msg = message.content

    if msg.startswith('$hello'):
        # await message.channel.send(start_msg)
        await send_join_msg(message.author)

    if msg.startswith('$createUser'):
        DB.create_user(author.id,author.name)
        await message.channel.send("Successful create USER {}".format(author.name))

    if msg.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))


    if msg.startswith("$all_users"):
        all_users = get_all_users()
        all_users = [user for user in all_users if user.name != "LuisHsu" and user.name !="Token_Bot_test"]
        for user in all_users:
            print(user)
            print(user.name)
            print(type(user))

            await user.send("Hi")
        # for member in message.guild.members:
        #     channel = await member.create_dm()
        #     await channel.send('Messages successfully sent!')

    if msg.startswith("$join_verify"):
        await join_verify(message)

    # Test DM function
    if msg.startswith("$DM"):
        await message.author.send("HI")

    if msg.startswith("$whoami"):
        res = '''
        id: {}
        name :{}
        guild: {}
        status: {}
        role: {}
        '''.format(author.id, author.name, author.guild, author.status, author.roles)
        await author.send(res)

    if msg.startswith('$roles'):
        role_name = [role.name for role in author.roles]
        res = '''
        role_names : {}
        '''.format(role_name)

        if 'manager' in role_name:
            res +="\n You're a fucking manger!!"
        await message.channel.send(res)

    if msg.startswith('$add'):
        user_id = author.id
        token = msg.split(' ')[1]
        res_messsage = DB.add_token(user_id, token)
        await message.channel.send(res_messsage)

    if msg.startswith('$tokens'):
        user_id = author.id
        tokens = DB.select_token(user_id)
        await message.author.send('''>>> ```markdown
        Hi you still have ##{}
        ```
        '''.format(tokens))

    if msg.startswith('$interaction'):
        await interaction(message)

    if msg.startswith('$verify'):
        print("Add role to user")
        member = author
        role_ID = 849863921765842954 # verify Chat channel
        verifiedRole = discord.utils.get(member.guild.roles, id = role_ID)
        await member.add_roles(verifiedRole)

    if msg.startswith('$remove_role'):
        await remove_role(author)


@commands.has_role('TEST_users')
async def remove_role(member: discord.Member):
    role = discord.utils.get(member.guild.roles, name = 'TEST_users')
    await member.remove_roles(role)
    time.sleep(3)
    await member.send("You already remove 'TEST_users' role")


## Add role to certain user
async def add_role(member: discord.member, role_name):
    role = discord.utils.get(member.guild.roles, name = role_name)
    await member.add_roles(role)
    time.sleep(3)
    await member.send("You've already been added '{}' role".format(role_name))

 
## If there are member join this channel, such function will be triggered
@client.event
async def on_member_join(member):
    print("new member join")
    await send_join_msg(member)
    time.sleep(10)   #The parameter is in seconds, so it'll wait for 30 seconds
    # #this role is for Verification Channel
    # role_ID = 849863921765842954 # verify chat channel
    role_ID = 848537536716734474 # TEST users

    verifiedRole = discord.utils.get(member.guild.roles, id = role_ID)
    await member.add_roles(verifiedRole)

keep_alive()
