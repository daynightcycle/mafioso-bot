

# Imports
import ast
import asyncio
from collections import Counter
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import neverSleep
import os
import random


# Intents
intents = discord.Intents.all()
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix='m!', intents=intents)


# Permission Checks


def is_owner():
    def predicate(ctx):
        return 635543231895044107 == ctx.author.id
    return commands.check(predicate)


def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)


def is_host():
    def predicate(ctx):
        guild = ctx.message.guild
        guild_file = 'guild' + str(guild.id) + '.txt'
        with open(guild_file, 'r') as fp:
            contents = fp.readlines()
        stripped_in_id = contents[12].strip('\n')
        raw_in_id = stripped_in_id[len('Host Role: '):]
        for role in ctx.author.roles:
            if role.id == raw_in_id:
                return role.id == raw_in_id
    return commands.check(predicate)


# Guild Shortcuts


def mafiguildindex(target):
    if target == 'chanann':
        return 1
    if target == 'chanbot':
        return 2
    if target == 'chancoven':
        return 3
    if target == 'chand2m':
        return 4
    if target == 'chandata':
        return 5
    if target == 'chanday':
        return 6
    if target == 'chandead':
        return 7
    if target == 'roledead':
        return 8
    if target == 'chanend':
        return 9
    if target == 'exuser':
        return 10
    if target == 'chanhost':
        return 11
    if target == 'rolehost':
        return 12
    if target == 'chaninter':
        return 13
    if target == 'chanm2d':
        return 14
    if target == 'chanmafia':
        return 15
    if target == 'roleplayer':
        return 16
    if target == 'chanseance':
        return 17
    if target == 'chanvote':
        return 18
    if target == 'gameopen':
        return 19


def mafiguildprefix(target):
    if target == 'chanann':
        return 'Announcement Channel: '
    if target == 'chanbot':
        return 'Bot Log Channel: '
    if target == 'chancoven':
        return 'Coven Channel: '
    if target == 'chand2m':
        return 'D2M Channel: '
    if target == 'chandata':
        return 'Data Channel: '
    if target == 'chanday':
        return 'Day Phase Channel: '
    if target == 'chandead':
        return 'Dead Channel: '
    if target == 'roledead':
        return 'Dead Role: '
    if target == 'chanend':
        return 'End Channel: '
    if target == 'exuser':
        return 'Example User: '
    if target == 'chanhost':
        return 'Host Channel: '
    if target == 'rolehost':
        return 'Host Role: '
    if target == 'chaninter':
        return 'Interest Check Channel: '
    if target == 'chanm2d':
        return 'M2D Channel: '
    if target == 'chanmafia':
        return 'Mafia Channel: '
    if target == 'roleplayer':
        return 'Player Role: '
    if target == 'chanseance':
        return 'Seance Channel: '
    if target == 'chanvote':
        return 'Voting Channel: '
    if target == 'gameopen':
        return 'Game Open: '


def mafiguildvalue(guild, target):
    guild_file = 'guild' + str(guild.id) + '.txt'
    with open(guild_file, 'r') as fp:
        contents = fp.readlines()
    if 1 <= mafiguildindex(target) <= 18:
        stripped_target = contents[mafiguildindex(target)].strip('\n')
        fp.close()
        return int(stripped_target[len(mafiguildprefix(target)):])
    elif 19 == mafiguildindex(target):
        stripped_target = contents[19].strip('\n')
        fp.close()
        return stripped_target[len('Game Open: '):]
    else:
        print('You stepped on a lego: Index not found in mafiaguildvalue().')


# Game Shortcuts


def mafigameindex(target):
    if target == 'time':
        return 1
    if target == 'hosts':
        return 2
    if target == 'hostnames':
        return 3
    if target == 'hostmentions':
        return 4
    if target == 'alive':
        return 5
    if target == 'alivenames':
        return 6
    if target == 'alivementions':
        return 7
    if target == 'dead':
        return 8
    if target == 'deadnames':
        return 9
    if target == 'deadmentions':
        return 10
    if target == 'votes':
        return 11
    if target == 'votenames':
        return 12
    if target == 'votementions':
        return 13
    if target == 'voters':
        return 14
    if target == 'voternames':
        return 15
    if target == 'votermentions':
        return 16
    if target == 'earlyvoters':
        return 17
    if target == 'earlyvoternames':
        return 18
    if target == 'earlyvotermentions':
        return 19
    if target == 'mediums':
        return 20
    if target == 'mediumnames':
        return 21
    if target == 'mediummentions':
        return 22
    if target == 'seances':
        return 23
    if target == 'mafia':
        return 24
    if target == 'mafianames':
        return 25
    if target == 'mafiamentions':
        return 26
    if target == 'coven':
        return 27
    if target == 'covennames':
        return 28
    if target == 'covenmentions':
        return 29
    if target == 'emotes':
        return 30


def mafigameprefix(target):
    if target == 'time':
        return 'Time: '
    if target == 'hosts':
        return 'Hosts: '
    if target == 'hostnames':
        return 'Host Names: '
    if target == 'hostmentions':
        return 'Host Mentions: '
    if target == 'alive':
        return 'Alive: '
    if target == 'alivenames':
        return 'Alive Names: '
    if target == 'alivementions':
        return 'Alive Mentions: '
    if target == 'dead':
        return 'Dead: '
    if target == 'deadnames':
        return 'Dead Names: '
    if target == 'deadmentions':
        return 'Dead Mentions: '
    if target == 'votes':
        return 'Votes: '
    if target == 'votenames':
        return 'Vote Names: '
    if target == 'votementions':
        return 'Vote Mentions: '
    if target == 'voters':
        return 'Voters: '
    if target == 'voternames':
        return 'Voter Names: '
    if target == 'votermentions':
        return 'Voter Mentions: '
    if target == 'earlyvoters':
        return 'Early Voters: '
    if target == 'earlyvoternames':
        return 'Early Voter Names: '
    if target == 'earlyvotermentions':
        return 'Early Voter Mentions: '
    if target == 'mediums':
        return 'Mediums: '
    if target == 'mediumnames':
        return 'Medium Names: '
    if target == 'mediummentions':
        return 'Medium Mentions: '
    if target == 'seances':
        return 'Seances: '
    if target == 'mafia':
        return 'Mafia: '
    if target == 'mafianames':
        return 'Mafia Names: '
    if target == 'mafiamentions':
        return 'Mafia Mentions: '
    if target == 'coven':
        return 'Coven: '
    if target == 'covennames':
        return 'Coven Names: '
    if target == 'covenmentions':
        return 'Coven Mentions: '
    if target == 'emotes':
        return 'Emotes: '


def mafigamevalue(in_file, target):
    with open(in_file, 'r') as fp:
        contents = fp.readlines()
    if 1 == mafigameindex(target):
        stripped_target = contents[1].strip('\n')
        fp.close()
        return int(stripped_target[len('Time: '):])
    elif 2 <= mafigameindex(target) <= 30:
        stripped_target = contents[mafigameindex(target)].strip('\n')
        fp.close()
        return ast.literal_eval(stripped_target[len(mafigameprefix(target)):])
    else:
        print('You stepped on a lego: Index not found in mafiagamevalue().')


# User Shortcuts


def mafiuserchan(guild, user_id):
    user_file = 'user' + str(user_id) + '_' + str(guild.id) + '.txt'
    with open(user_file, 'r') as fp:
        contents = fp.readlines()
    user_list = ast.literal_eval(contents[0])
    return user_list[2]


# Math


def majority(number):
    if number in [0, 1, 2]:
        return 'None'
    else:
        if (number % 2) == 0:
            return int(number / 2 + 1)
        else:
            return int(number / 2 + 0.5)


def majority_vote(guild):
    if len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votes')) > 0:
        if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votes').count(most_common(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votes'))) >= majority(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive'))):
            return True
        else:
            return False
    else:
        return False


def most_common(in_list):
    data = Counter(in_list)
    return data.most_common(1)[0][0]



# Permissions: Bot Owner and Server Owners


@bot.command()
@commands.check_any(is_guild_owner(), is_owner())
async def hosts(ctx, in_role):
    guild = ctx.message.guild
    guild_file = 'guild' + str(guild.id) + '.txt'
    with open(guild_file, 'r') as fp:
        contents = fp.readlines()
    if in_role.startswith('<@&'):
        stripped_in_role = in_role.strip('>')
        raw_in_role = int(stripped_in_role[len('<@&'):])
        for role in guild.roles:
            if role.id == raw_in_role:
                role_name = role.name
                contents[12] = 'Host Role: ' + str(role.id) + '\n'
        with open(guild_file, 'w') as fp:
            fp.writelines(contents)
        fp.close()
        await ctx.channel.send('**' + role_name + '**' + ' is now the Host Role.')
        return
    if in_role.isdigit():
        for role in guild.roles:
            if role.id == int(in_role):
                role_name = role.name
                contents[12] = 'Host Role: ' + str(role.id) + '\n'
        with open(guild_file, 'w') as fp:
            fp.writelines(contents)
        fp.close()
        await ctx.channel.send('**' + role_name + '**' + ' is now the Host Role.')
        return
    for role in guild.roles:
        if role.name == in_role:
            role_name = role.name
            contents[12] = 'Host Role: ' + str(role.id) + '\n'
    with open(guild_file, 'w') as fp:
        fp.writelines(contents)
    fp.close()
    await ctx.channel.send('**' + role_name + '**' + ' is now the Host Role.')


@bot.command()
@commands.check_any(is_guild_owner(), is_owner())
async def setup(ctx):
    guild_file = 'guild' + str(ctx.message.guild.id) + '.txt'
    if not os.path.exists(guild_file):
        with open(guild_file, 'w') as fp:
            fp.write(ctx.message.guild.name + '\nAnnouncement Channel: \nBot Log Channel: \nCoven Channel: \nD2M Channel: \nData Channel: \nDay Phase Channel: \nDead Channel: \nDead Role: \nEnd Channel: \nExample User: \nHost Channel: \nHost Role: \nInterest Check Channel: \nM2D Channel: \nMafia Channel: \nPlayer Role: \nSeance Channel: \nVoting Channel: \nGame Open: None\n')
        fp.close()
        await ctx.channel.send(guild_file + ' has been created for **' + ctx.message.guild.name + '.**')
    else:
        await ctx.channel.send('This server has already been set up.')


# Permissions: Hosts


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def addcov(ctx, in_user):
    guild = ctx.message.guild
    if os.path.exists(mafiguildvalue(guild, 'gameopen')):
        coven = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')
        covennames = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'covennames')
        covenmentions = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'covenmentions')
        coven_chat = bot.get_channel(mafiguildvalue(guild, 'chancoven'))
        if in_user.startswith('<@') or in_user.isdigit():
            if in_user.startswith('<@'):
                in_user = in_user.strip('>')
                in_user = int(in_user[len('<@'):])
            else:
                in_user = int(in_user)
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')[i] == in_user:
                    if not (in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediums') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')):
                        coven.append(in_user)
                        await coven_chat.set_permissions(guild.get_member(in_user), read_messages=True)
                        covennames.append(guild.get_member(in_user).name)
                        covenmentions.append(guild.get_member(in_user).mention)
                        with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                            contents = fp.readlines()
                        contents[mafigameindex('coven')] = mafigameprefix('coven') + str(coven) + '\n'
                        contents[mafigameindex('covennames')] = mafigameprefix('covennames') + str(covennames) + '\n'
                        contents[mafigameindex('covenmentions')] = mafigameprefix('covenmentions') + str(covenmentions) + '\n'
                        with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                            fp.writelines(contents)
                        fp.close()
                        await ctx.channel.send('**' + covennames[len(covennames)-1] + '** is now a member of the Coven.')
                        return
                    else:
                        await ctx.channel.send('This user is already a member of the Coven, or is a member of an opposing faction (such as the Mafia).')
                        return
            else:
                await ctx.channel.send('This user is not a Player and cannot be added to the Coven.')
        else:
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alivenames'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alivenames')[i] == in_user:
                    if not (in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediumnames') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafianames') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'covennames')):
                        coven.append(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')[i]).id)
                        await coven_chat.set_permissions(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')[i]), read_messages=True)
                        covennames.append(in_user)
                        covenmentions.append(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')[i]).mention)
                        with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                            contents = fp.readlines()
                        contents[mafigameindex('coven')] = mafigameprefix('coven') + str(coven) + '\n'
                        contents[mafigameindex('covennames')] = mafigameprefix('covennames') + str(covennames) + '\n'
                        contents[mafigameindex('covenmentions')] = mafigameprefix('covenmentions') + str(covenmentions) + '\n'
                        with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                            fp.writelines(contents)
                        fp.close()
                        await ctx.channel.send('**' + covennames[len(covennames)-1] + '** is now a member of the Coven.')
                        return
                    else:
                        await ctx.channel.send('This user is already a member of the Coven, or is a member of an opposing faction (such as the Mafia).')
                        return
            else:
                await ctx.channel.send('This user is not a Player and cannot be added to the Coven.')
    else:
        await ctx.channel.send('There is no game open on this server.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def addexuser(ctx, in_user):
    guild = ctx.message.guild
    guild_file = 'guild' + str(guild.id) + '.txt'
    with open(guild_file, 'r') as fp:
        contents = fp.readlines()
    if in_user.startswith('<@') or in_user.isdigit():
            if in_user.startswith('<@'):
                in_user = in_user.strip('>')
                in_user = int(in_user[len('<@'):])
            else:
                in_user = int(in_user)
            try:
                contents[10] = 'Example User: ' + str(guild.get_member(in_user).id) + '\n'
                found = True
                with open(guild_file, 'w') as fp:
                    fp.writelines(contents)
                fp.close()
                await ctx.channel.send('**' + guild.get_member(in_user).name + '**' + ' is now the example user.')
            except:
                await ctx.channel.send('This is not a real user.')
    else:
        for member in guild.members:
            found = False
            if in_user == member.name:
                found = True
                contents[10] = 'Example User: ' + str(member.id) + '\n'
                with open(guild_file, 'w') as fp:
                    fp.writelines(contents)
                fp.close()
                await ctx.channel.send('**' + in_user + '**' + ' is now the example user.')
                return
        if found == False:
            await ctx.channel.send('This is not a real user.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def addmaf(ctx, in_user):
    guild = ctx.message.guild
    if os.path.exists(mafiguildvalue(guild, 'gameopen')):
        mafia = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia')
        mafianames = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafianames')
        mafiamentions = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafiamentions')
        mafia_chat = bot.get_channel(mafiguildvalue(guild, 'chanmafia'))
        if in_user.startswith('<@') or in_user.isdigit():
            if in_user.startswith('<@'):
                in_user = in_user.strip('>')
                in_user = int(in_user[len('<@'):])
            else:
                in_user = int(in_user)
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')[i] == in_user:
                    if not (in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediums') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')):
                        mafia.append(in_user)
                        await mafia_chat.set_permissions(guild.get_member(in_user), read_messages=True)
                        mafianames.append(guild.get_member(in_user).name)
                        mafiamentions.append(guild.get_member(in_user).mention)
                        with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                            contents = fp.readlines()
                        contents[mafigameindex('mafia')] = mafigameprefix('mafia') + str(mafia) + '\n'
                        contents[mafigameindex('mafianames')] = mafigameprefix('mafianames') + str(mafianames) + '\n'
                        contents[mafigameindex('mafiamentions')] = mafigameprefix('mafiamentions') + str(mafiamentions) + '\n'
                        with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                            fp.writelines(contents)
                        fp.close()
                        await ctx.channel.send('**' + mafianames[len(mafianames)-1] + '** is now a member of the Mafia.')
                        return
                    else:
                        await ctx.channel.send('This user is already a member of the Mafia, or is a member of an opposing faction (such as the Coven).')
                        return
            else:
                await ctx.channel.send('This user is not a Player and cannot be added to the Mafia.')
        else:
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alivenames'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alivenames')[i] == in_user:
                    if not (in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediumnames') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafianames') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'covennames')):
                        mafia.append(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')[i]).id)
                        await mafia_chat.set_permissions(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')[i]), read_messages=True)
                        mafianames.append(in_user)
                        mafiamentions.append(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')[i]).mention)
                        with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                            contents = fp.readlines()
                        contents[mafigameindex('mafia')] = mafigameprefix('mafia') + str(mafia) + '\n'
                        contents[mafigameindex('mafianames')] = mafigameprefix('mafianames') + str(mafianames) + '\n'
                        contents[mafigameindex('mafiamentions')] = mafigameprefix('mafiamentions') + str(mafiamentions) + '\n'
                        with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                            fp.writelines(contents)
                        fp.close()
                        await ctx.channel.send('**' + mafianames[len(mafianames)-1] + '** is now a member of the Mafia.')
                        return
                    else:
                        await ctx.channel.send('This user is already a member of the Mafia, or is a member of an opposing faction (such as the Coven).')
                        return
            else:
                await ctx.channel.send('This user is not a Player and cannot be added to the Mafia.')
    else:
        await ctx.channel.send('There is no game open on this server.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def addmed(ctx, in_user):
    guild = ctx.message.guild
    if os.path.exists(mafiguildvalue(guild, 'gameopen')):
        mediums = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediums')
        mediumnames = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediumnames')
        mediummentions = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediummentions')
        seances = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'seances')
        if in_user.startswith('<@') or in_user.isdigit():
            if in_user.startswith('<@'):
                in_user = in_user.strip('>')
                in_user = int(in_user[len('<@'):])
            else:
                in_user = int(in_user)
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')[i] == in_user:
                    if not (in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediums') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')):
                        mediums.append(in_user)
                        mediumnames.append(guild.get_member(in_user).name)
                        mediummentions.append(guild.get_member(in_user).mention)
                        seances.append(1)
                        with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                            contents = fp.readlines()
                        contents[mafigameindex('mediums')] = mafigameprefix('mediums') + str(mediums) + '\n'
                        contents[mafigameindex('mediumnames')] = mafigameprefix('mediumnames') + str(mediumnames) + '\n'
                        contents[mafigameindex('mediummentions')] = mafigameprefix('mediummentions') + str(mediummentions) + '\n'
                        contents[mafigameindex('seances')] = mafigameprefix('seances') + str(seances) + '\n'
                        with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                            fp.writelines(contents)
                        fp.close()
                        await ctx.channel.send('**' + mediumnames[len(mediumnames)-1] + '** is now a Medium.')
                        return
                    else:
                        await ctx.channel.send('This user was already assigned this role or cannot become a medium.')
                        return
            else:
                await ctx.channel.send('This user is not a Player and cannot be assigned this role.')
        else:
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alivenames'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alivenames')[i] == in_user:
                    if not (in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediumnames') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafianames') or in_user in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'covennames')):
                        mediums.append(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')[i]).id)
                        mediumnames.append(in_user)
                        mediummentions.append(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')[i]).mention)
                        seances.append(1)
                        with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                            contents = fp.readlines()
                        contents[mafigameindex('mediums')] = mafigameprefix('mediums') + str(mediums) + '\n'
                        contents[mafigameindex('mediumnames')] = mafigameprefix('mediumnames') + str(mediumnames) + '\n'
                        contents[mafigameindex('mediummentions')] = mafigameprefix('mediummentions') + str(mediummentions) + '\n'
                        contents[mafigameindex('seances')] = mafigameprefix('seances') + str(seances) + '\n'
                        with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                            fp.writelines(contents)
                        fp.close()
                        await ctx.channel.send('**' + mediumnames[len(mediumnames)-1] + '** is now a Medium.')
                        return
                    else:
                        await ctx.channel.send('This user was already assigned this role or cannot become a medium.')
                        return
            else:
                await ctx.channel.send('This user is not a Player and cannot be assigned this role.')
    else:
        await ctx.channel.send('There is no game open on this server.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def caste(ctx, type, in_role):
    guild = ctx.message.guild
    guild_file = 'guild' + str(guild.id) + '.txt'
    with open(guild_file, 'r') as fp:
        contents = fp.readlines()
    found = False
    if in_role.startswith('<@&') or in_role.isdigit():
        if in_role.startswith('<@&'):
            in_role = in_role.strip('>')
            in_role = int(in_role[len('<@&'):])
        else:
            in_role = int(in_role)
        try:
            contents[mafiguildindex('role' + type)] = mafiguildprefix('role' + type) + str(get(guild.roles, id=in_role).id) + '\n'
            found = True
            if not in_role == mafiguildvalue(guild, 'rolehost'):
                with open(guild_file, 'w') as fp:
                    fp.writelines(contents)
                fp.close()
                await ctx.channel.send('**' + get(guild.roles, id=in_role).name + '**' + ' is now the ' + mafiguildprefix('role' + type).strip(': ') + '.')
            else:
                await ctx.channel.send('You cannot change the Host Role with the `caste` command. You must use the `hosts` command.')
        except:
            await ctx.channel.send('This is not a real role.')
    else:
        for role in guild.roles:
            found = False
            if in_role == role.name:
                found = True
                if not role.id == mafiguildvalue(guild, 'rolehost'):
                    contents[mafiguildindex('role' + type)] = mafiguildprefix('role' + type) + str(get(guild.roles, id=role.id)) + '\n'
                    with open(guild_file, 'w') as fp:
                        fp.writelines(contents)
                    fp.close()
                    await ctx.channel.send('**' + get(guild.roles, id=role.id).name + '**' + ' is now the ' + mafiguildprefix('role' + type).strip(': ') + '.')
                    return
    if found == False:
        await ctx.channel.send('This is not a real role.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def chan(ctx, type):
    guild = ctx.message.guild
    guild_file = 'guild' + str(guild.id) + '.txt'
    with open(guild_file, 'r') as fp:
        contents = fp.readlines()
    contents[mafiguildindex('chan' + type)] = mafiguildprefix('chan' + type) + str(ctx.message.channel.id) + '\n'
    with open(guild_file, 'w') as fp:
        fp.writelines(contents)
    fp.close()
    await ctx.channel.send(ctx.message.channel.mention + ' is now the ' + mafiguildprefix('chan' + type).strip(': ') + '.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def creategame(ctx):
    hosts = []
    host_names = []
    host_mentions = []
    alive = []
    alive_names = []
    alive_mentions = []
    unused_emotes = ['❤', '🍎', '📙', '🔥', '⭐', '🌻', '🌖', '🟢', '🌲', '🔷', '🎵', '🌊', '🟪', '☂', '🌈', '☁', '⚙', '⚽', '📷', '➕']
    emotes = []
    guild = ctx.message.guild
    day_chat = bot.get_channel(mafiguildvalue(guild, 'chanday'))
    vote_chat = bot.get_channel(mafiguildvalue(guild, 'chanvote'))
    coven_chat = bot.get_channel(mafiguildvalue(guild, 'chancoven'))
    mafia_chat = bot.get_channel(mafiguildvalue(guild, 'chanmafia'))
    end_chat = bot.get_channel(mafiguildvalue(guild, 'chanend'))
    dead_chat = bot.get_channel(mafiguildvalue(guild, 'chandead'))
    data_chat = bot.get_channel(mafiguildvalue(guild, 'chandata'))
    host_chat = bot.get_channel(mafiguildvalue(guild, 'chanhost'))
    players = get(guild.roles, id=mafiguildvalue(guild, 'roleplayer'))
    dead = get(guild.roles, id=mafiguildvalue(guild, 'roledead'))
    for member in guild.members:
        for role in member.roles:
            if role.id == mafiguildvalue(guild, 'roledead'):
                await ctx.channel.send('Remove the Dead Role from all users before starting a new game.')
                return
            if role.id == mafiguildvalue(guild, 'rolehost'):
                hosts.append(member.id)
                host_names.append(member.name)
                host_mentions.append(member.mention)
            if role.id == mafiguildvalue(guild, 'roleplayer'):
                alive.append(member.id)
                alive_names.append(member.name)
                alive_mentions.append(member.mention)
                user_emote = random.choice(unused_emotes)
                unused_emotes.remove(user_emote)
                emotes.append(user_emote)
                await day_chat.set_permissions(member, read_messages=None, send_messages=None, add_reactions=None)
                await vote_chat.set_permissions(member, read_messages=None, send_messages=None, add_reactions=None)
                await coven_chat.set_permissions(member, read_messages=None, send_messages=None, add_reactions=None)
                await mafia_chat.set_permissions(member, read_messages=None, send_messages=None, add_reactions=None)
                await end_chat.set_permissions(member, read_messages=None, send_messages=None, add_reactions=None)
                await dead_chat.set_permissions(member, read_messages=None, send_messages=None, add_reactions=None)
                await data_chat.set_permissions(member, read_messages=None, send_messages=None, add_reactions=None)
                await host_chat.set_permissions(member, read_messages=None, send_messages=None, add_reactions=None)
    if mafiguildvalue(guild, 'gameopen') == 'None':
        with open('gamecount.txt', 'r') as fp:
            contents = fp.readlines()
        game_id = int(contents[0]) + 1
        with open('gamecount.txt', 'w') as fp:
            fp.writelines(str(game_id))
        fp.close()
        game_file = 'game' + str(game_id) + '.txt'
        with open(game_file, 'w+') as fp:
            fp.write('ID: ' + str(game_id) + '\n' + 'Time: 0' + '\n' + 'Hosts: ' + str(hosts) + '\n' + 'Host Names: ' + str(host_names) + '\n' + 'Host Mentions: ' + str(host_mentions) + '\n' + 'Alive: ' + str(alive) + '\n' + 'Alive Names: ' + str(alive_names) + '\n' + 'Alive Mentions: ' + str(alive_mentions) + '\n' + 'Dead: []\nDead Names: []\nDead Mentions: []\nVotes: []\nVote Names: []\nVote Mentions: []\nVoters: []\nVoter Names: []\nVoter Mentions: []\nEarly Voters: []\nEarly Voter Names: []\nEarly Voter Mentions: []\nMediums: []\nMedium Names: []\nMedium Mentions: []\nSeances: []\nMafia: []\nMafia Names: []\nMafia Mentions: []\nCoven: []\nCoven Names: []\nCoven Mentions: []\nEmotes: ' + str(emotes) + '\n')
            fp.close()
        guild_file = 'guild' + str(guild.id) + '.txt'
        with open(guild_file, 'r') as fp:
            contents = fp.readlines()
        contents[mafiguildindex('gameopen')] = mafiguildprefix('gameopen') + game_file + '\n'
        with open(guild_file, 'w') as fp:
            fp.writelines(contents)
        fp.close()
        await players.edit(permissions=discord.Permissions(change_nickname=False))
        await dead.edit(permissions=discord.Permissions(change_nickname=False))
        await day_chat.set_permissions(players, read_messages=True, send_messages=False, add_reactions=False)
        await day_chat.set_permissions(dead, read_messages=True, send_messages=False, add_reactions=False)
        await vote_chat.set_permissions(players, read_messages=True, send_messages=False, add_reactions=False)
        await vote_chat.set_permissions(dead, read_messages=True, send_messages=False, add_reactions=False)
        await coven_chat.set_permissions(players, read_messages=False, send_messages=False, add_reactions=False)
        await coven_chat.set_permissions(dead, read_messages=False, send_messages=False, add_reactions=False)
        await mafia_chat.set_permissions(players, read_messages=False, send_messages=False, add_reactions=False)
        await mafia_chat.set_permissions(dead, read_messages=False, send_messages=False, add_reactions=False)
        await end_chat.set_permissions(players, read_messages=True, send_messages=False, add_reactions=False)
        await end_chat.set_permissions(dead, read_messages=True, send_messages=False, add_reactions=False)
        await dead_chat.set_permissions(players, read_messages=False, send_messages=False, add_reactions=False)
        await dead_chat.set_permissions(dead, read_messages=True, send_messages=True, add_reactions=True)
        await data_chat.set_permissions(players, read_messages=False, send_messages=False, add_reactions=False)
        await data_chat.set_permissions(dead, read_messages=False, send_messages=False, add_reactions=False)
        await host_chat.set_permissions(players, read_messages=False, send_messages=False, add_reactions=False)
        await host_chat.set_permissions(dead, read_messages=False, send_messages=False, add_reactions=False)
        await ctx.channel.send(game_file + ' has been created for **' + ctx.message.guild.name + '.**')
    else:
        await ctx.channel.send('There is already an active game in this server.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def removecov(ctx, in_user):
    guild = ctx.message.guild
    if os.path.exists(mafiguildvalue(guild, 'gameopen')):
        coven = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')
        covennames = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'covennames')
        covenmentions = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'covenmentions')
        coven_chat = bot.get_channel(mafiguildvalue(guild, 'chancoven'))
        if in_user.startswith('<@') or in_user.isdigit():
            if in_user.startswith('<@'):
                in_user = in_user.strip('>')
                in_user = int(in_user[len('<@'):])
            else:
                in_user = int(in_user)
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')[i] == in_user:
                    await coven_chat.set_permissions(guild.get_member(in_user), read_messages=False)
                    covennames.pop(coven.index(in_user))
                    covenmentions.pop(coven.index(in_user))
                    coven.pop(coven.index(in_user))
                    with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                        contents = fp.readlines()
                    contents[mafigameindex('coven')] = mafigameprefix('coven') + str(coven) + '\n'
                    contents[mafigameindex('covennames')] = mafigameprefix('covennames') + str(covennames) + '\n'
                    contents[mafigameindex('covenmentions')] = mafigameprefix('covenmentions') + str(covenmentions) + '\n'
                    with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                        fp.writelines(contents)
                    fp.close()
                    await ctx.channel.send('This user is no longer a member of the Coven.')
                    return
            else:
                await ctx.channel.send('This user is not a member of the Coven and cannot be removed.')
        else:
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'covennames'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'covennames')[i] == in_user:
                    await coven_chat.set_permissions(guild.get_member(coven[i]), read_messages=False)
                    coven.pop(covennames.index(in_user))
                    covenmentions.pop(covennames.index(in_user))
                    covennames.pop(covennames.index(in_user))
                    with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                        contents = fp.readlines()
                    contents[mafigameindex('coven')] = mafigameprefix('coven') + str(coven) + '\n'
                    contents[mafigameindex('covennames')] = mafigameprefix('covennames') + str(covennames) + '\n'
                    contents[mafigameindex('covenmentions')] = mafigameprefix('covenmentions') + str(covenmentions) + '\n'
                    with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                        fp.writelines(contents)
                    fp.close()
                    await ctx.channel.send('This user is no longer a member of the Coven.')
                    return
            else:
                await ctx.channel.send('This user is not a member of the Coven and cannot be removed.')
    else:
        await ctx.channel.send('There is no game open on this server.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def removemaf(ctx, in_user):
    guild = ctx.message.guild
    if os.path.exists(mafiguildvalue(guild, 'gameopen')):
        mafia = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia')
        mafianames = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafianames')
        mafiamentions = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafiamentions')
        mafia_chat = bot.get_channel(mafiguildvalue(guild, 'chanmafia'))
        if in_user.startswith('<@') or in_user.isdigit():
            if in_user.startswith('<@'):
                in_user = in_user.strip('>')
                in_user = int(in_user[len('<@'):])
            else:
                in_user = int(in_user)
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia')[i] == in_user:
                    await mafia_chat.set_permissions(guild.get_member(in_user), read_messages=False)
                    mafianames.pop(mafia.index(in_user))
                    mafiamentions.pop(mafia.index(in_user))
                    mafia.pop(mafia.index(in_user))
                    with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                        contents = fp.readlines()
                    contents[mafigameindex('mafia')] = mafigameprefix('mafia') + str(mafia) + '\n'
                    contents[mafigameindex('mafianames')] = mafigameprefix('mafianames') + str(mafianames) + '\n'
                    contents[mafigameindex('mafiamentions')] = mafigameprefix('mafiamentions') + str(mafiamentions) + '\n'
                    with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                        fp.writelines(contents)
                    fp.close()
                    await ctx.channel.send('This user is no longer a member of the Mafia.')
                    return
            else:
                await ctx.channel.send('This user is not a member of the Mafia and cannot be removed.')
        else:
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafianames'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafianames')[i] == in_user:
                    await mafia_chat.set_permissions(guild.get_member(mafia[i]), read_messages=False)
                    mafia.pop(mafianames.index(in_user))
                    mafiamentions.pop(mafianames.index(in_user))
                    mafianames.pop(mafianames.index(in_user))
                    with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                        contents = fp.readlines()
                    contents[mafigameindex('mafia')] = mafigameprefix('mafia') + str(mafia) + '\n'
                    contents[mafigameindex('mafianames')] = mafigameprefix('mafianames') + str(mafianames) + '\n'
                    contents[mafigameindex('mafiamentions')] = mafigameprefix('mafiamentions') + str(mafiamentions) + '\n'
                    with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                        fp.writelines(contents)
                    fp.close()
                    await ctx.channel.send('This user is no longer a member of the Mafia.')
                    return
            else:
                await ctx.channel.send('This user is not a member of the Mafia and cannot be removed.')
    else:
        await ctx.channel.send('There is no game open on this server.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def removemed(ctx, in_user):
    guild = ctx.message.guild
    if os.path.exists(mafiguildvalue(guild, 'gameopen')):
        mediums = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediums')
        mediumnames = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediumnames')
        mediummentions = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediummentions')
        seances = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'seances')
        if in_user.startswith('<@') or in_user.isdigit():
            if in_user.startswith('<@'):
                in_user = in_user.strip('>')
                in_user = int(in_user[len('<@'):])
            else:
                in_user = int(in_user)
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediums'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediums')[i] == in_user:
                    mediumnames.pop(mediums.index(in_user))
                    mediummentions.pop(mediums.index(in_user))
                    seances.pop(mediums.index(in_user))
                    mediums.pop(mediums.index(in_user))
                    with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                        contents = fp.readlines()
                    contents[mafigameindex('mediums')] = mafigameprefix('mediums') + str(mediums) + '\n'
                    contents[mafigameindex('mediumnames')] = mafigameprefix('mediumnames') + str(mediumnames) + '\n'
                    contents[mafigameindex('mediummentions')] = mafigameprefix('mediummentions') + str(mediummentions) + '\n'
                    contents[mafigameindex('seances')] = mafigameprefix('seances') + str(seances) + '\n'
                    with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                        fp.writelines(contents)
                    fp.close()
                    await ctx.channel.send('This user is no longer a Medium.')
                    return
            else:
                await ctx.channel.send('This user could not be removed from the Medium list as they were not in the list.')
        else:
            for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediumnames'))):
                if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediumnames')[i] == in_user:
                    mediums.pop(mediumnames.index(in_user))
                    mediummentions.pop(mediumnames.index(in_user))
                    seances.pop(mediumnames.index(in_user))
                    mediumnames.pop(mediumnames.index(in_user))
                    with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                        contents = fp.readlines()
                    contents[mafigameindex('mediums')] = mafigameprefix('mediums') + str(mediums) + '\n'
                    contents[mafigameindex('mediumnames')] = mafigameprefix('mediumnames') + str(mediumnames) + '\n'
                    contents[mafigameindex('mediummentions')] = mafigameprefix('mediummentions') + str(mediummentions) + '\n'
                    contents[mafigameindex('seances')] = mafigameprefix('seances') + str(seances) + '\n'
                    with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                        fp.writelines(contents)
                    fp.close()
                    await ctx.channel.send('This user is no longer a Medium.')
                    return
            else:
                await ctx.channel.send('This user could not be removed from the Medium list as they were not in the list.')
    else:
        await ctx.channel.send('There is no game open on this server.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def route(ctx, in_user):
    guild = ctx.message.guild
    user_list = []
    if in_user.startswith('<@') or in_user.isdigit():
        if in_user.startswith('<@'):
            in_user = in_user.strip('>')
            in_user = int(in_user[len('<@'):])
        else:
            in_user = int(in_user)
        if guild.get_member(in_user) in guild.members:
            user_list.append(guild.get_member(in_user).name)
            user_list.append(in_user)
            user_list.append(ctx.message.channel.id)
            user_file = 'user' + str(in_user) + '_' + str(guild.id) + '.txt'
            contents = []
            if os.path.exists(user_file):
                with open (user_file, 'r') as fp:
                    contents = fp.readlines()
                contents[0] = str(user_list)
                with open(user_file, 'w') as fp:
                    fp.writelines(contents)
                fp.close()
                await ctx.channel.send('**' + guild.get_member(in_user).name + '** route file has been updated.')
                return
            else:
                contents.append(str(user_list))
                with open(user_file, 'w') as fp:
                    fp.writelines(contents)
                fp.close()
                await ctx.channel.send('**' + guild.get_member(in_user).name + '** route file has been created.')
                return
    else:
        for member in guild.members:
            if in_user == member.name:
                user_list.append(in_user)
                user_list.append(member.id)
                user_list.append(ctx.message.channel.id)
                user_file = 'user' + str(member.id) + '_' + str(guild.id) + '.txt'
                contents = []
                if os.path.exists(user_file):
                    with open (user_file, 'r') as fp:
                        contents = fp.readlines()
                    contents[0] = str(user_list)
                    with open(user_file, 'w') as fp:
                        fp.writelines(contents)
                    fp.close()
                    await ctx.channel.send('**' + in_user + '** route file has been updated.')
                    return
                else:
                    contents.append(str(user_list))
                    with open(user_file, 'w') as fp:
                        fp.writelines(contents)
                    fp.close()
                    await ctx.channel.send('**' + in_user + '** route file has been created.')
                    return
    await ctx.channel.send('This user is not a member of this server.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), is_owner())
async def startday(ctx):
    guild = ctx.message.guild
    if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'time') in [1, 2]:
        await ctx.channel.send('The day has already been started.')
        return
    if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'time') in [0, 3]:
        if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'time') == 0:
            first_day = True
        else:
            first_day = False
        guild_file = 'guild' + str(guild.id) + '.txt'
        ann_chat = bot.get_channel(mafiguildvalue(guild, 'chanann'))
        day_chat = bot.get_channel(mafiguildvalue(guild, 'chanday'))
        vote_chat = bot.get_channel(mafiguildvalue(guild, 'chanvote'))
        coven_chat = bot.get_channel(mafiguildvalue(guild, 'chancoven'))
        mafia_chat = bot.get_channel(mafiguildvalue(guild, 'chanmafia'))
        dead_chat = bot.get_channel(mafiguildvalue(guild, 'chandead'))
        players = get(guild.roles, id=mafiguildvalue(guild, 'roleplayer'))
        dead = get(guild.roles, id=mafiguildvalue(guild, 'roledead'))
        with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
            contents = fp.readlines()
        contents[mafigameindex('time')] = mafigameprefix('time') + '1' + '\n'
        with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
            fp.writelines(contents)
        fp.close()
        await day_chat.set_permissions(players, send_messages=True, add_reactions=True)
        for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia'))):
            if first_day == True:
                await mafia_chat.set_permissions(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia')[i], send_messages=True, add_reactions=True)
            else:
                await mafia_chat.set_permissions(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia')[i], send_messages=False, add_reactions=False)
        for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven'))):
            if first_day == True:
                await coven_chat.set_permissions(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')[i]), send_messages=True, add_reactions=True)
            else:
                await coven_chat.set_permissions(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')[i]), send_messages=False, add_reactions=False)
        await ann_chat.send('Day Phase has begun. Voting will be closed for the first 12 hours of Day Phase or until all players have used the `m!early` command.')
        await day_chat.send('**Day Phase has begun!**')
        if first_day == True:
            if not mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia') == []:
                await mafia_chat.send('**Mafia chat is open on the first day!**')
            if not mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven') == []:
                await coven_chat.send('**Coven chat is open on the first day!**')
        counter = 0
        while True:
            await asyncio.sleep(1)
            counter += 1
            if 43200 <= counter or len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'earlyvoters')) == len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')):
                with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                    contents = fp.readlines()
                contents[mafigameindex('time')] = mafigameprefix('time') + '2' + '\n'
                with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                    fp.writelines(contents)
                fp.close()
                break
        voting_message = '**Voting has begun!**\n\n*No one has voted yet.*\n'
        for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'emotes'))):
            voting_message = voting_message + '\n' + mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alivementions')[i] + ': ' + mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'emotes')[i]
        voting_message = voting_message + '\n' + 'No vote: ' + '✅' + '\n' + 'Unvote: ' + '❌'
        moji = await vote_chat.send(voting_message)
        ballot = vote_chat.last_message
        for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'emotes'))):
            await moji.add_reaction(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'emotes')[i])
        await moji.add_reaction('✅')
        await moji.add_reaction('❌')
        while True:
            await asyncio.sleep(1)
            counter += 1
            if 172800 <= counter or majority_vote(guild):
                await ballot.clear_reactions()
                await day_chat.set_permissions(players, send_messages=False, add_reactions=False)
                for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia'))):
                    await mafia_chat.set_permissions(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia')[i], send_messages=True, add_reactions=True)
                for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven'))):
                    await coven_chat.set_permissions(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')[i], send_messages=True, add_reactions=True)
                with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                    contents = fp.readlines()
                contents[mafigameindex('time')] = mafigameprefix('time') + '3' + '\n'
                contents[mafigameindex('votes')] = mafigameprefix('votes') + '\n'
                contents[mafigameindex('voters')] = mafigameprefix('voters') + '\n'
                contents[mafigameindex('earlyvoters')] = mafigameprefix('earlyvoters') + '\n'
                contents[mafigameindex('earlyvoternames')] = mafigameprefix('earlyvoternames') + '\n'
                contents[mafigameindex('earlyvotermentions')] = mafigameprefix('earlyvotermentions') + '\n'
                with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                    fp.writelines(contents)
                fp.close()
                await day_chat.send('**The day has ended. Please wait for a host.**')
                break


# Permissions: Everyone


@bot.command()
async def alive(ctx):
    guild = ctx.message.guild
    alive = []
    for member in guild.members:
        for role in member.roles:
            if role.id == mafiguildvalue(guild, 'roleplayer'):
                alive.append(member.display_name)
    if alive == []:
        message_string = 'No one is alive.'
    else:
        alive.sort(key=str.lower)
        for i in range(len(alive)):
            for member in guild.members:
                if alive[i] == member.display_name:
                    alive[i] = member.mention
        message_string = '\n' + '\n'.join(alive)
    embedAlive = discord.Embed(title='Alive', description=message_string, color=0x81c2f8)
    await ctx.channel.send(embed=embedAlive)


@bot.command()
async def dead(ctx):
    guild = ctx.message.guild
    dead = []
    for member in guild.members:
        for role in member.roles:
            if role.id == mafiguildvalue(guild, 'roledead'):
                dead.append(member.display_name)
    if dead == []:
        message_string = 'No one is dead.'
    else:
        dead.sort(key=str.lower)
        for i in range(len(dead)):
            for member in guild.members:
                if dead[i] == member.display_name:
                    dead[i] = member.mention
        message_string = '\n' + '\n'.join(dead)
    embedDead = discord.Embed(title='Dead', description=message_string, color=0x6b77bb)
    await ctx.channel.send(embed=embedDead)


@bot.command()
async def early(ctx):
    guild = ctx.message.guild
    earlyvoters = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'earlyvoters')
    earlyvoternames = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'earlyvoternames')
    earlyvotermentions = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'earlyvotermentions')
    if not ctx.author.id in mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'earlyvoters'):
        earlyvoters.append(ctx.author.id)
        earlyvoternames.append(ctx.author.name)
        earlyvotermentions.append(ctx.author.mention)
        with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
            contents = fp.readlines()
        contents[mafigameindex('earlyvoters')] = mafigameprefix('earlyvoters') + str(earlyvoters) + '\n'
        contents[mafigameindex('earlyvoternames')] = mafigameprefix('earlyvoternames') + str(earlyvoternames) + '\n'
        contents[mafigameindex('earlyvotermentions')] = mafigameprefix('earlyvotermentions') + str(earlyvotermentions) + '\n'
        with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
            fp.writelines(contents)
        fp.close()
        await ctx.channel.send('**' + ctx.author.display_name + '** has opted to vote early.')


@bot.command()
async def hello(ctx):
    await ctx.channel.send('Hello!')


# Other Non-Commands


@commands.cooldown(1, 30, commands.BucketType.user)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    guild = message.channel.guild
    if not message.author.id == 991436402652893235:
        if os.path.exists(mafiguildvalue(guild, 'gameopen')):
            if mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'time') == 3:
                if not mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediums') == []:
                    if message.channel.id == mafiguildvalue(guild, 'chandead'):
                        for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediums'))):
                            personal_chat = bot.get_channel(mafiuserchan(guild, mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mediums')[i]))
                            output = '**' + message.author.display_name + ':** ' + message.content
                            if not message.attachments == []:
                                for i in range(len(message.attachments)):
                                    output = output + '\n' + str(message.attachments[i])
                            await personal_chat.send(output)
    await bot.process_commands(message)


@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if os.path.exists(mafiguildvalue(guild, 'gameopen')):
        if payload.channel_id == mafiguildvalue(guild, 'chanvote'):
            if not payload.member.id == 991436402652893235:
                if message.author.id == 991436402652893235:
                    alive = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')
                    if payload.member.id in alive:
                        votes = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votes')
                        voters = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'voters')
                        emotes = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'emotes')
                        voting_message = message.content
                        voting_action = 'None'
                        if payload.member.id not in voters:
                            if payload.emoji.name == '✅' or payload.emoji.name == '❌':
                                if payload.emoji.name == '✅':
                                    votes.append('None')
                                    voters.append(payload.member.id)
                                    voting_action = '**' + payload.member.display_name + '** has no-voted.'
                                    if voting_message.startswith('**Voting has begun!**\n\n*No one has voted yet.*\n'):
                                        voting_message = voting_message.replace('*No one has voted yet.*', voting_action)
                                    else:
                                        voting_message = voting_message.replace('\n\n<', '\n\n' + voting_action + '\n\n<')
                                    await message.remove_reaction(payload.emoji, payload.member)
                                elif payload.emoji.name == '❌':
                                    await message.remove_reaction(payload.emoji, payload.member)
                            else:
                                if not payload.member.id == alive[emotes.index(payload.emoji.name)]:
                                    votes.append(alive[emotes.index(payload.emoji.name)])
                                    voters.append(payload.member.id)
                                    voting_action = '**' + payload.member.display_name + '** has voted for ' + '**' + guild.get_member(alive[emotes.index(payload.emoji.name)]).display_name + '**.'
                                    if voting_message.startswith('**Voting has begun!**\n\n*No one has voted yet.*\n'):
                                        voting_message = voting_message.replace('*No one has voted yet.*', voting_action)
                                    else:
                                        voting_message = voting_message.replace('\n\n<', '\n\n' + voting_action + '\n\n<')
                                    await message.remove_reaction(payload.emoji, payload.member)
                                else:
                                    await message.remove_reaction(payload.emoji, payload.member)
                        else: # players who have already voted
                            if payload.emoji.name == '✅' or payload.emoji.name == '❌':
                                if payload.emoji.name == '✅':
                                    if not votes[voters.index(payload.member.id)] == 'None':
                                        votes[voters.index(payload.member.id)] = 'None'
                                        voting_action = '**' + payload.member.display_name + '** has no-voted.'
                                        if voting_message.startswith('**Voting has begun!**\n\n*No one has voted yet.*\n'):
                                            voting_message = voting_message.replace('*No one has voted yet.*', voting_action)
                                        else:
                                            voting_message = voting_message.replace('\n\n<', '\n\n' + voting_action + '\n\n<')
                                        await message.remove_reaction(payload.emoji, payload.member)
                                    else:
                                        await message.remove_reaction(payload.emoji, payload.member)
                                elif payload.emoji.name == '❌':
                                    votes.pop(voters.index(payload.member.id))
                                    voters.remove(payload.member.id)
                                    voting_action = '**' + payload.member.display_name + '** changed their mind.'
                                    if voting_message.startswith('**Voting has begun!**\n\n*No one has voted yet.*\n'):
                                        voting_message = voting_message.replace('*No one has voted yet.*', voting_action)
                                    else:
                                        voting_message = voting_message.replace('\n\n<', '\n\n' + voting_action + '\n\n<')
                                    await message.remove_reaction(payload.emoji, payload.member)
                            else:
                                if not payload.member.id == alive[emotes.index(payload.emoji.name)]:
                                    if not votes[voters.index(payload.member.id)] == alive[emotes.index(payload.emoji.name)]:
                                        votes[voters.index(payload.member.id)] = alive[emotes.index(payload.emoji.name)]
                                        voting_action = '**' + payload.member.display_name + '** has voted for ' + '**' + guild.get_member(alive[emotes.index(payload.emoji.name)]).display_name + '**.'
                                        if voting_message.startswith('**Voting has begun!**\n\n*No one has voted yet.*\n'):
                                            voting_message = voting_message.replace('*No one has voted yet.*', voting_action)
                                        else:
                                            voting_message = voting_message.replace('\n\n<', '\n\n' + voting_action + '\n\n<')
                                        await message.remove_reaction(payload.emoji, payload.member)
                                    else:
                                        await message.remove_reaction(payload.emoji, payload.member)
                                else:
                                    await message.remove_reaction(payload.emoji, payload.member)
                        with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                            contents = fp.readlines()
                        contents[mafigameindex('votes')] = mafigameprefix('votes') + str(votes) + '\n'
                        contents[mafigameindex('voters')] = mafigameprefix('voters') + str(voters) + '\n'
                        with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                            fp.writelines(contents)
                        fp.close()
                        try:
                            await message.edit(content=voting_message)
                        except:
                            if channel.last_message_id == message.id:
                                if not voting_action == 'None':
                                    await channel.send('Ballot too long!\n\n' + voting_action)
                            else:
                                last_message = await channel.fetch_message(channel.last_message_id)
                                if not voting_action == 'None':
                                    new_content = last_message.content + '\n\n' + voting_action
                                    try:
                                        await last_message.edit(content=new_content)
                                    except:
                                        await channel.send('Ballot too long!\n\n' + voting_action)
                    else:
                        await message.remove_reaction(payload.emoji, payload.member)


neverSleep.awake('https://MafiosoBot.daynightcycle.repl.co', False)
bot.run(os.getenv('TOKEN'))
