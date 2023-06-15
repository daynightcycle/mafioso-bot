

# Imports
import ast
import asyncio
from collections import Counter
import discord
from discord.ext import commands
from discord.utils import get
import os
from os import environ
from os.path import exists
import random


# Intents
intents = discord.Intents.all()
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix='m!', intents=intents)


# Permission Checks


# Checks if the command message's author is an owner of the command message's guild.
# https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html#checks
def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)


# Checks if the command message's author has the host role designated for their guild.
# https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html#checks
# https://discordpy.readthedocs.io/en/stable/api.html#discord.Guild.id
def is_host():
    def predicate(ctx):
        host_role_id = get_guild_value(ctx, 'role_host')  # This gets the ID for the server's host role.
        for role in ctx.author.roles:  # Each role the command message's author has is checked. If they have the host role, the module predicate() returns True.
            if role.id == host_role_id:
                return True
    return commands.check(predicate)


# ID and File Search


# Returns a Discord ID for a channel or role saved to the guide file. This module should NOT be used to get a guild's game file; use get_game_file() instead.
# https://stackabuse.com/python-remove-the-prefix-and-suffix-from-a-string/
def get_guild_value(ctx, target):
    guild_file = 'guild' + str(ctx.message.guild.id) + '.txt'  # Uses the command message's guild ID to construct the guild file path.
    if exists(guild_file):  # Checks if the guild file path exists.
        with open(guild_file, 'r') as fp:  # Reads the guild file into the contents[] list.
            contents = fp.readlines()
            if get_guild_index(target) < 16:
                return int(contents[get_guild_index(target)][len(get_guild_prefix(target)):].strip('\n'))  # Removes the prefix and line breaks from the target guild ID. The guild ID is converted to an integer and returned.
            else:
                return contents[19][len('Game Open: '):].strip('\n')  # Removes the prefix and line breaks from the target game file. The game file is returned as a string.
    else:
        await ctx.channel.send('Guild file not found.')
        return None  # None is returned if no guild file has been created yet.


#  Returns a game value saved to a guild's game file.
# https://stackabuse.com/python-remove-the-prefix-and-suffix-from-a-string/
def get_game_value(ctx, target):
    game_file = get_guild_value(ctx, 'game_open')
    if exists(game_file):  # Checks if the game file path exists.
        with open(game_file, 'r') as fp:  # Reads the game file into the contents[] list.
            contents = fp.readlines()
            if get_guild_index(target) == 1:
                return int(contents[1][len('Time: '):].strip('\n'))  # Removes the prefix and line breaks from the time value. The time value is returned as a string.
            else:
                return ast.literal_eval(contents[get_game_index(target)][len(get_game_prefix(target)):].strip('\n'))  # Removes the prefix and line breaks from the target game value. The game value is returned as a list.
    else:
        await ctx.channel.send('Guild file not found.')
        return None  # None is returned if no game file has been created yet.


# Guild File Shortcuts


# Returns a target guild file index.
def get_guild_index(target):
    if target == 'chan_ann':
        return 1
    if target == 'chan_bot':
        return 2
    if target == 'chan_coven':
        return 3
    if target == 'chan_data':
        return 4
    if target == 'chan_day':
        return 5
    if target == 'chan_dead':
        return 6
    if target == 'role_dead':
        return 7
    if target == 'chan_end':
        return 8
    if target == 'user_ex':
        return 9
    if target == 'chan_host':
        return 10
    if target == 'role_host':
        return 11
    if target == 'chan_interest':
        return 12
    if target == 'chan_mafia':
        return 13
    if target == 'role_player':
        return 14
    if target == 'chan_vote':
        return 15
    if target == 'game_open':
        return 16


# Returns a target guild file prefix.
def get_guild_prefix(target):
    if target == 'chan_ann':
        return 'Announcement Channel: '
    if target == 'chan_bot':
        return 'Bot Log Channel: '
    if target == 'chan_coven':
        return 'Coven Channel: '
    if target == 'chan_data':
        return 'Data Channel: '
    if target == 'chan_day':
        return 'Day Phase Channel: '
    if target == 'chan_dead':
        return 'Dead Channel: '
    if target == 'role_dead':
        return 'Dead Role: '
    if target == 'chan_end':
        return 'End Channel: '
    if target == 'user_ex':
        return 'Example User: '
    if target == 'chan_host':
        return 'Host Channel: '
    if target == 'role_host':
        return 'Host Role: '
    if target == 'chan_interest':
        return 'Interest Check Channel: '
    if target == 'chan_mafia':
        return 'Mafia Channel: '
    if target == 'role_player':
        return 'Player Role: '
    if target == 'chan_vote':
        return 'Voting Channel: '
    if target == 'game_open':
        return 'Game Open: '


# Game File Shortcuts


# Returns a target game file index.
def get_game_index(target):
    if target == 'time':
        return 1
    if target == 'hosts':
        return 2
    if target == 'host_names':
        return 3
    if target == 'host_mentions':
        return 4
    if target == 'alive':
        return 5
    if target == 'alive_names':
        return 6
    if target == 'alive_mentions':
        return 7
    if target == 'emotes':
        return 8
    if target == 'dead':
        return 9
    if target == 'dead_names':
        return 10
    if target == 'dead_mentions':
        return 11
    if target == 'votes':
        return 12
    if target == 'vote_names':
        return 13
    if target == 'vote_mentions':
        return 14
    if target == 'voters':
        return 15
    if target == 'voter_names':
        return 16
    if target == 'voter_mentions':
        return 17
    if target == 'early_voters':
        return 18
    if target == 'early_voter_names':
        return 19
    if target == 'early_voter_mentions':
        return 20
    if target == 'medium':
        return 21
    if target == 'medium_names':
        return 22
    if target == 'medium_mentions':
        return 23
    if target == 'seances':
        return 24
    if target == 'mafia':
        return 25
    if target == 'mafia_names':
        return 26
    if target == 'mafia_mentions':
        return 27
    if target == 'coven':
        return 28
    if target == 'coven_names':
        return 29
    if target == 'coven_mentions':
        return 30


# Returns a target game file prefix.
def get_game_prefix(target):
    if target == 'time':
        return 'Time: '
    if target == 'hosts':
        return 'Hosts: '
    if target == 'host_names':
        return 'Host Names: '
    if target == 'host_mentions':
        return 'Host Mentions: '
    if target == 'alive':
        return 'Alive: '
    if target == 'alive_names':
        return 'Alive Names: '
    if target == 'alive_mentions':
        return 'Alive Mentions: '
    if target == 'emotes':
        return 'Emotes: '
    if target == 'dead':
        return 'Dead: '
    if target == 'dead_names':
        return 'Dead Names: '
    if target == 'dead_mentions':
        return 'Dead Mentions: '
    if target == 'votes':
        return 'Votes: '
    if target == 'vote_names':
        return 'Vote Names: '
    if target == 'vote_mentions':
        return 'Vote Mentions: '
    if target == 'voters':
        return 'Voters: '
    if target == 'voter_names':
        return 'Voter Names: '
    if target == 'voter_mentions':
        return 'Voter Mentions: '
    if target == 'early_voters':
        return 'Early Voters: '
    if target == 'early_voter_names':
        return 'Early Voter Names: '
    if target == 'early_voter_mentions':
        return 'Early Voter Mentions: '
    if target == 'medium':
        return 'Mediums: '
    if target == 'medium_names':
        return 'Medium Names: '
    if target == 'medium_mentions':
        return 'Medium Mentions: '
    if target == 'seances':
        return 'Seances: '
    if target == 'mafia':
        return 'Mafia: '
    if target == 'mafia_names':
        return 'Mafia Names: '
    if target == 'mafia_mentions':
        return 'Mafia Mentions: '
    if target == 'coven':
        return 'Coven: '
    if target == 'coven_names':
        return 'Coven Names: '
    if target == 'coven_mentions':
        return 'Coven Mentions: '


# Setup


# Sets up a guild file for a guild if there is no guild file already created.
@bot.command()
@commands.check_any(is_guild_owner(), commands.is_owner())  # This command may only be used by guild admins or MafiosoBot's owner.
async def server_setup(ctx):
    guild_file = 'guild' + str(ctx.message.guild.id) + '.txt'  # Uses the command message's guild ID to construct the guild file path.
    if not exists(guild_file):  # Checks if the game file path exists.
        with open(guild_file, 'w') as fp:  # Creates and writes to guild file.
            fp.write(ctx.message.guild.name + '\nAnnouncement Channel: \nBot Log Channel: \nCoven Channel: \nD2M Channel: \nData Channel: \nDay Phase Channel: \nDead Channel: \nDead Role: \nEnd Channel: \nExample User: \nHost Channel: \nHost Role: \nInterest Check Channel: \nM2D Channel: \nMafia Channel: \nPlayer Role: \nSeance Channel: \nVoting Channel: \nGame Open: None\n')
        await ctx.channel.send(guild_file + ' has been created for **' + ctx.message.guild.name + '.**')
    else:
        await ctx.channel.send('This server has already been set up.')  # This is returned is a guild file already exists.


# Designates a given role to be the host role.
@bot.command()
@commands.check_any(is_guild_owner(), commands.is_owner())  # This command may only be used by guild admins or MafiosoBot's owner.
async def hosts(ctx, in_role):
    guild_file = 'guild' + str(ctx.message.guild.id) + '.txt'  # Uses the command message's guild ID to construct the guild file path.
    with open(guild_file, 'r') as fp:  # Reads the guild file into the contents[] list.
        contents = fp.readlines()
    if in_role.isdigit():  # First, this module checks if the user input a raw role ID.
        for role in ctx.message.guild.roles:
            if role.id == in_role:
                role_name = role.name
                contents[11] = 'Host Role: ' + str(role.id) + '\n'  # A role that has the input ID is designated the host role.
    elif in_role.startswith('<@&'):  # Secondly, this module checks if the user input a role mention.
        role_id = int(in_role[len('<@&'):len('>')])  # The mention is stripped of its prefix and suffix.
        for role in ctx.message.guild.roles:
            if role.id == role_id:
                role_name = role.name
                contents[11] = 'Host Role: ' + str(role.id) + '\n'  # A role that has the resulting ID is designated the host role.
    else:  # Finally, this module checks if the user input a role name string.
        for role in ctx.message.guild.roles:
            if role.name == in_role:
                role_name = role.name
                contents[11] = 'Host Role: ' + str(role.id) + '\n'  # A role that has the same name as the input string is designated the host role.
    with open(guild_file, 'w') as fp:  # Writes the updated contents[] list to the guild file.
        fp.writelines(contents)
    await ctx.channel.send('**' + role_name + '**' + ' is now the Host Role.')


# Creates a game file for a guild if there is no game file already created.
@bot.command()
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
async def create_game(ctx):
    guild = ctx.message.guild  # Writes the command message's guild ID to a variable.
    if get_guild_value(ctx, 'game_open') == 'None':  # If there is no game file associated with the guild, a game file is created.
        hosts_list = [member.id for member in get_guild_value(ctx, 'role_host')]  # The IDs of members with the designated host role are added to this list.
        host_names_list = [member.name for member in get_guild_value(ctx, 'role_host')]  # The names of members with the designated host role are added to this list.
        host_mentions_list = [member.mention for member in get_guild_value(ctx, 'role_host')]  # The mention strings of members with the designated host role are added to this list.
        alive_list = [member.id for member in get_guild_value(ctx, 'role_player')]  # The IDs of members with the designated player role are added to this list.
        alive_names_list = [member.name for member in get_guild_value(ctx, 'role_player')]  # The names of members with the designated player role are added to this list.
        alive_mentions_list = [member.mention for member in get_guild_value(ctx, 'role_player')]  # The mention strings of members with the designated player role are added to this list.
        emotes = []
        unused_emotes = ['❤', '🍎', '📙', '🔥', '⭐', '🌻', '🌖', '🟢', '🌲', '🔷', '🎵', '🌊', '🟪', '☂', '🌈', '☁', '⚙', '⚽', '📷', '🔑']
        for _ in range(len(alive)):  # Random emojis are assigned to players; these are used to voting with role reactions.
            user_emote = random.choice(unused_emotes)
            unused_emotes.remove(user_emote)
            emotes.append(user_emote)
        dead_list = [member.id for member in get_guild_value(ctx, 'role_dead')]  # The IDs of members with the designated dead role are added to this list.
        dead_names_list = [member.name for member in get_guild_value(ctx, 'role_dead')]  # The names of members with the designated dead role are added to this list.
        dead_mentions_list = [member.mention for member in get_guild_value(ctx, 'role_dead')]  # The mention strings of members with the designated dead role are added to this list.
        with open('game_count.txt', 'w+') as fp:  # Opens game count file for reading and writing, adding 1 to the game count.
            contents = fp.readlines()
            game_id = int(contents[0]) + 1
            fp.writelines(str(game_id))
        game_file = 'game' + str(game_id) + '.txt'
        with open(game_file, 'w') as fp:  # Creates and writes to game file.
            fp.write('ID: ' + str(game_id) + '\nTime: 0\nHosts: ' + str(hosts_list) + '\nHost Names: ' + str(host_names_list) + '\nHost Mentions: ' + str(host_mentions_list) + '\nAlive: ' + str(alive_list) + '\nAlive Names: ' + str(alive_names_list) + '\nAlive Mentions: ' + str(alive_mentions_list) + '\nEmotes: ' + str(emotes) + '\nDead: ' + str(dead_list) + '\nDead Names: ' + str(dead_names_list) + '\nDead Mentions: ' + str(dead_mentions_list) + '\nVotes: []\nVote Names: []\nVote Mentions: []\nVoters: []\nVoter Names: []\nVoter Mentions: []\nEarly Voters: []\nEarly Voter Names: []\nEarly Voter Mentions: []\nMediums: []\nMedium Names: []\nMedium Mentions: []\nSeances: []\nMafia: []\nMafia Names: []\nMafia Mentions: []\nCoven: []\nCoven Names: []\nCoven Mentions: []')
        with open('guild' + str(guild.id) + '.txt', 'w+'):  # Uses the command message's guild ID to construct the guild file path, read the guild file into the contents[] list, and update the game file value.
            contents = fp.readlines()
            contents[16] = 'Game Open: ' + game_file
            fp.writelines(contents)
        await ctx.channel.send(game_file + ' has been created for **' + guild.name + '.**')
        # Role and Channel IDs are written to variables to set permissions.
        role_player = get(guild.roles, id=get_guild_value(ctx, 'role_player'))
        role_dead = get(guild.roles, id=get_guild_value(ctx, 'role_dead'))
        chan_ann = bot.get_channel(get_guild_value(ctx, 'chan_ann'))
        chan_bot = bot.get_channel(get_guild_value(ctx, 'chan_bot'))
        chan_coven = bot.get_channel(get_guild_value(ctx, 'chan_coven'))
        chan_data = bot.get_channel(get_guild_value(ctx, 'chan_data'))
        chan_day = bot.get_channel(get_guild_value(ctx, 'chan_day'))
        chan_dead = bot.get_channel(get_guild_value(ctx, 'chan_dead'))
        chan_end = bot.get_channel(get_guild_value(ctx, 'chan_end'))
        chan_host = bot.get_channel(get_guild_value(ctx, 'chan_host'))
        chan_mafia = bot.get_channel(get_guild_value(ctx, 'chan_mafia'))
        chan_vote = bot.get_channel(get_guild_value(ctx, 'chan_vote'))
        # Players and dead are not allowed to change nicknames; this is to avoid confusion during voting or deduction.
        await role_player.edit(permissions=discord.Permissions(change_nickname=False))
        await role_dead.edit(permissions=discord.Permissions(change_nickname=False))
        # Permissions to channels based on role are set.
        await chan_ann.set_permissions(role_player, read_messages=True, send_messages=False, add_reactions=False)
        await chan_ann.set_permissions(role_dead, read_messages=True, send_messages=False, add_reactions=False)
        await chan_bot.set_permissions(role_player, read_messages=False, send_messages=False, add_reactions=False)
        await chan_bot.set_permissions(role_dead, read_messages=False, send_messages=False, add_reactions=False)
        await chan_coven.set_permissions(role_player, read_messages=False, send_messages=False, add_reactions=False)
        await chan_coven.set_permissions(role_dead, read_messages=False, send_messages=False, add_reactions=False)
        await chan_data.set_permissions(role_player, read_messages=False, send_messages=False, add_reactions=False)
        await chan_data.set_permissions(role_dead, read_messages=False, send_messages=False, add_reactions=False)
        await chan_day.set_permissions(role_player, read_messages=True, send_messages=False, add_reactions=False)
        await chan_day.set_permissions(role_dead, read_messages=True, send_messages=False, add_reactions=False)
        await chan_dead.set_permissions(role_player, read_messages=False, send_messages=False, add_reactions=False)
        await chan_dead.set_permissions(role_dead, read_messages=True, send_messages=True, add_reactions=True)
        await chan_end.set_permissions(role_player, read_messages=True, send_messages=False, add_reactions=False)
        await chan_end.set_permissions(role_dead, read_messages=True, send_messages=False, add_reactions=False)
        await chan_host.set_permissions(role_player, read_messages=False, send_messages=False, add_reactions=False)
        await chan_host.set_permissions(role_dead, read_messages=False, send_messages=False, add_reactions=False)
        await chan_mafia.set_permissions(role_player, read_messages=False, send_messages=False, add_reactions=False)
        await chan_mafia.set_permissions(role_dead, read_messages=False, send_messages=False, add_reactions=False)
        await chan_vote.set_permissions(role_player, read_messages=True, send_messages=False, add_reactions=False)
        await chan_vote.set_permissions(role_dead, read_messages=True, send_messages=False, add_reactions=False)
        await ctx.channel.send('Permissions have been assigned.')
    else:
        await ctx.channel.send('There is already an active game in this server.')  # This is returned is a game file for a guild already exists.


# unedited


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


# Permissions: Hosts


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
async def addcov(ctx, in_user):
    guild = ctx.message.guild
    if exists(mafiguildvalue(guild, 'gameopen')):
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
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
async def addexuser(ctx, in_user):
    guild = ctx.message.guild
    guild_file = 'guild' + str(guild.id) + '.txt'  # Uses the command message's guild ID to construct the guild file path.
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
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
async def addmaf(ctx, in_user):
    guild = ctx.message.guild
    if exists(mafiguildvalue(guild, 'gameopen')):
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
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
async def addmed(ctx, in_user):
    guild = ctx.message.guild
    if exists(mafiguildvalue(guild, 'gameopen')):
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
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
async def caste(ctx, type, in_role):
    guild = ctx.message.guild
    guild_file = 'guild' + str(guild.id) + '.txt'  # Uses the command message's guild ID to construct the guild file path.
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
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
async def chan(ctx, type):
    guild = ctx.message.guild
    guild_file = 'guild' + str(guild.id) + '.txt'  # Uses the command message's guild ID to construct the guild file path.
    with open(guild_file, 'r') as fp:
        contents = fp.readlines()
    contents[mafiguildindex('chan' + type)] = mafiguildprefix('chan' + type) + str(ctx.message.channel.id) + '\n'
    with open(guild_file, 'w') as fp:
        fp.writelines(contents)
    fp.close()
    await ctx.channel.send(ctx.message.channel.mention + ' is now the ' + mafiguildprefix('chan' + type).strip(': ') + '.')


@bot.command()
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
async def removecov(ctx, in_user):
    guild = ctx.message.guild
    if exists(mafiguildvalue(guild, 'gameopen')):
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
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
async def removemaf(ctx, in_user):
    guild = ctx.message.guild
    if exists(mafiguildvalue(guild, 'gameopen')):
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
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
async def removemed(ctx, in_user):
    guild = ctx.message.guild
    if exists(mafiguildvalue(guild, 'gameopen')):
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
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
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
            if exists(user_file):
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
                if exists(user_file):
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
@commands.check_any(is_guild_owner(), is_host(), commands.is_owner())  # This command may only be used by guild admins, guild members with the designated host role, or MafiosoBot's owner.
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
        guild_file = 'guild' + str(guild.id) + '.txt'  # Uses the command message's guild ID to construct the guild file path.
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
        if first_day == True:
            if not mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven') == []:
                for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven'))):
                    await coven_chat.set_permissions(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')[i]), read_messages=True, send_messages=True, add_reactions=True)
                await coven_chat.send('**Coven Chat is open the first day!**')
            if not mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia') == []:
                for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia'))):
                    await mafia_chat.set_permissions(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia')[i]), read_messages=True, send_messages=True, add_reactions=True)
                await mafia_chat.send('**Mafia Chat is open the first day!**')
        else:
            if not mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven') == []:
                for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven'))):
                    await coven_chat.set_permissions(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')[i]), read_messages=True, send_messages=False, add_reactions=False)
                await coven_chat.send('**Coven Chat is closed!**')
            if not mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia') == []:
                for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia'))):
                    await mafia_chat.set_permissions(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia')[i]), read_messages=True, send_messages=False, add_reactions=False)
                await mafia_chat.send('**Mafia Chat is closed!**')
        ann_chat_start_message = 'Day Phase has begun. Voting will be closed for the first 12 hours of Day Phase or until all players have used the `m!early` command. **' + str(majority(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')))) + ' votes** are needed to end the day.'
        await ann_chat.send(ann_chat_start_message)
        await day_chat.send('**Day Phase has begun!**')
        counter = 0
        while True:
            await asyncio.sleep(1)
            counter += 1
            if 10 <= counter or len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'earlyvoters')) == len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')):
                with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                    contents = fp.readlines()
                contents[mafigameindex('time')] = mafigameprefix('time') + '2' + '\n'
                with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                    fp.writelines(contents)
                fp.close()
                break
        voting_message = 'Voting has begun! Use `m!votes` to see a condensed voting record.\n\n*No one has voted yet.*\n\n**Majority: **' + str(majority(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive'))))
        for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'emotes'))):
            voting_message = voting_message + '\n' + mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alivementions')[i] + ': ' + mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'emotes')[i]
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
                await day_chat.send('**Day Phase is closed!**')
                await ann_chat.send('**The day has ended. Please wait for a host.**')
                if not mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven') == []:
                    for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven'))):
                        await coven_chat.set_permissions(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'coven')[i]), read_messages=True, send_messages=True, add_reactions=True)
                    await coven_chat.send('**Coven Chat is open!**')
                if not mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia') == []:
                    for i in range(len(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia'))):
                        await mafia_chat.set_permissions(guild.get_member(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'mafia')[i]), read_messages=True, send_messages=True, add_reactions=True)
                    await mafia_chat.send('**Mafia Chat is open!**')
                with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                    contents = fp.readlines()
                contents[mafigameindex('time')] = mafigameprefix('time') + '3' + '\n'
                contents[mafigameindex('votes')] = mafigameprefix('votes') + '[]' + '\n'
                contents[mafigameindex('votenames')] = mafigameprefix('votenames') + '[]' + '\n'
                contents[mafigameindex('votementions')] = mafigameprefix('votementions') + '[]' + '\n'
                contents[mafigameindex('voters')] = mafigameprefix('voters') + '[]' + '\n'
                contents[mafigameindex('voternames')] = mafigameprefix('voternames') + '[]' + '\n'
                contents[mafigameindex('votermentions')] = mafigameprefix('votermentions') + '[]' + '\n'
                contents[mafigameindex('earlyvoters')] = mafigameprefix('earlyvoters') + '[]' + '\n'
                contents[mafigameindex('earlyvoternames')] = mafigameprefix('earlyvoternames') + '[]' + '\n'
                contents[mafigameindex('earlyvotermentions')] = mafigameprefix('earlyvotermentions') + '[]' + '\n'
                with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                    fp.writelines(contents)
                fp.close()
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


@bot.command()
async def votes(ctx):
    guild = ctx.message.guild
    message_string = ''
    votes = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votes')
    voted = list(set(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votes')))
    votedmentions = list(set(mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votementions')))
    votermentions = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votermentions')
    for i in range(len(voted)):
        lynchers = []
        vote_amount = 0
        for j in range(len(votes)):
            if votes[j] == voted[i]:
                lynchers.append(votermentions[j])
                vote_amount += 1
        message_string = message_string + '\n\n' + votedmentions[i] + ' has **' + str(vote_amount) + ' votes** from:\n'
        for k in range(len(lynchers)):
            message_string = message_string + lynchers[k] + ' '
    embedVotes = discord.Embed(title='Votes', description=message_string, color=0xdd020b)
    await ctx.channel.send(embed=embedVotes)


# Other Non-Commands


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


# make this time dependent
@bot.event
async def on_message(message):
    guild = message.channel.guild
    try:
        if not message.author.id == 991436402652893235:
            if exists(mafiguildvalue(guild, 'gameopen')):
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
    except FileNotFoundError:
        pass
    await bot.process_commands(message)


@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    try:
        if exists(mafiguildvalue(guild, 'gameopen')):
            if payload.channel_id == mafiguildvalue(guild, 'chanvote'):
                if not payload.member.id == 991436402652893235:
                    if message.author.id == 991436402652893235:
                        alive = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alive')
                        alivenames = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alivenames')
                        alivementions = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'alivementions')
                        if payload.member.id in alive:
                            votes = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votes')
                            votenames = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votenames')
                            votementions = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votementions')
                            voters = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'voters')
                            voternames = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'voternames')
                            votermentions = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'votermentions')
                            emotes = mafigamevalue(mafiguildvalue(guild, 'gameopen'), 'emotes')
                            voting_message = message.content
                            voting_action = 'None'
                            day_chat = bot.get_channel(mafiguildvalue(guild, 'chanday'))
                            if payload.member.id not in voters:
                                if payload.emoji.name == '✅' or payload.emoji.name == '❌':
                                    if payload.emoji.name == '✅':
                                        votes.append('None')
                                        votenames.append('None')
                                        votementions.append('None')
                                        voters.append(payload.member.id)
                                        voternames.append(payload.member.name)
                                        votermentions.append(payload.member.mention)
                                        voting_action = payload.member.mention + ' has no-voted.'
                                        voting_receipt = '**' + payload.member.display_name + '** has no-voted.'
                                        await day_chat.send(voting_receipt)
                                        if voting_message.startswith('Voting has begun! Use `m!votes` to see a condensed voting record.\n\n*No one has voted yet.*\n'):
                                            voting_message = voting_message.replace('*No one has voted yet.*', voting_action)
                                        else:
                                            voting_message = voting_message.replace('\n\n**Majority: **', '\n\n' + voting_action + '\n\n**Majority: **')
                                        await message.remove_reaction(payload.emoji, payload.member)
                                    elif payload.emoji.name == '❌':
                                        await message.remove_reaction(payload.emoji, payload.member)
                                else:
                                    if not payload.member.id == alive[emotes.index(payload.emoji.name)]:
                                        votes.append(alive[emotes.index(payload.emoji.name)])
                                        votenames.append(alivenames[emotes.index(payload.emoji.name)])
                                        votementions.append(alivementions[emotes.index(payload.emoji.name)])
                                        voters.append(payload.member.id)
                                        voternames.append(payload.member.name)
                                        votermentions.append(payload.member.mention)
                                        voting_action = payload.member.mention + ' has voted for ' + '**' + guild.get_member(alive[emotes.index(payload.emoji.name)]).display_name + '**.'
                                        voting_receipt = '**' + payload.member.display_name + '** has voted for ' + '**' + guild.get_member(alive[emotes.index(payload.emoji.name)]).display_name + '**.'
                                        await day_chat.send(voting_receipt)
                                        print('A')
                                        if voting_message.startswith('Voting has begun! Use `m!votes` to see a condensed voting record.\n\n*No one has voted yet.*\n'):
                                            voting_message = voting_message.replace('*No one has voted yet.*', voting_action)
                                        else:
                                            print(voting_action)
                                            print(voting_message.replace('\n\n**Majority: **', '\n\n' + voting_action + '\n\n**Majority: **'))
                                            voting_message = voting_message.replace('\n\n**Majority: **', '\n\n' + voting_action + '\n\n**Majority: **')
                                            print('B')
                                        await message.remove_reaction(payload.emoji, payload.member)
                                    else:
                                        await message.remove_reaction(payload.emoji, payload.member)
                            else:  # players who have already voted
                                if payload.emoji.name == '✅' or payload.emoji.name == '❌':
                                    if payload.emoji.name == '✅':
                                        if not votes[voters.index(payload.member.id)] == 'None':
                                            votes[voters.index(payload.member.id)] = 'None'
                                            votenames[voters.index(payload.member.id)] = 'None'
                                            votementions[voters.index(payload.member.id)] = 'None'
                                            voting_action = payload.member.mention + ' has no-voted.'
                                            voting_receipt = '**' + payload.member.display_name + '** has no-voted.'
                                            await day_chat.send(voting_receipt)
                                            if voting_message.startswith('Voting has begun! Use `m!votes` to see a condensed voting record.\n\n*No one has voted yet.*\n'):
                                                voting_message = voting_message.replace('*No one has voted yet.*', voting_action)
                                            else:
                                                voting_message = voting_message.replace('\n\n**Majority: **', '\n\n' + voting_action + '\n\n**Majority: **')
                                            await message.remove_reaction(payload.emoji, payload.member)
                                        else:
                                            await message.remove_reaction(payload.emoji, payload.member)
                                    elif payload.emoji.name == '❌':
                                        votes.pop(voters.index(payload.member.id))
                                        votenames.pop(voters.index(payload.member.id))
                                        votementions.pop(voters.index(payload.member.id))
                                        voters.remove(payload.member.id)
                                        voternames.remove(payload.member.name)
                                        votermentions.remove(payload.member.mention)
                                        voting_action = payload.member.mention + ' changed their mind.'
                                        voting_receipt = '**' + payload.member.display_name + '** changed their mind.'
                                        await day_chat.send(voting_receipt)
                                        if voting_message.startswith('Voting has begun! Use `m!votes` to see a condensed voting record.\n\n*No one has voted yet.*\n'):
                                            voting_message = voting_message.replace('*No one has voted yet.*', voting_action)
                                        else:
                                            voting_message = voting_message.replace('\n\n**Majority: **', '\n\n' + voting_action + '\n\n**Majority: **')
                                        await message.remove_reaction(payload.emoji, payload.member)
                                else:
                                    if not payload.member.id == alive[emotes.index(payload.emoji.name)]:
                                        if not votes[voters.index(payload.member.id)] == alive[emotes.index(payload.emoji.name)]:
                                            votes[voters.index(payload.member.id)] = alive[emotes.index(payload.emoji.name)]
                                            votenames[voters.index(payload.member.id)] = alivenames[emotes.index(payload.emoji.name)]
                                            votementions[voters.index(payload.member.id)] = alivementions[emotes.index(payload.emoji.name)]
                                            voting_action = payload.member.mention + ' has voted for ' + '**' + guild.get_member(alive[emotes.index(payload.emoji.name)]).display_name + '**.'
                                            voting_receipt = '**' + payload.member.display_name + '** has voted for ' + '**' + guild.get_member(alive[emotes.index(payload.emoji.name)]).display_name + '**.'
                                            await day_chat.send(voting_receipt)
                                            if voting_message.startswith('**Voting has begun! Use `m!votes` to see a condensed voting record.**\n\n*No one has voted yet.*\n'):
                                                voting_message = voting_message.replace('*No one has voted yet.*', voting_action)
                                            else:
                                                voting_message = voting_message.replace('\n\n**Majority: **', '\n\n' + voting_action + '\n\n**Majority: **')
                                            await message.remove_reaction(payload.emoji, payload.member)
                                        else:
                                            await message.remove_reaction(payload.emoji, payload.member)
                                    else:
                                        await message.remove_reaction(payload.emoji, payload.member)
                            print('C')
                            with open(mafiguildvalue(guild, 'gameopen'), 'r') as fp:
                                contents = fp.readlines()
                            contents[mafigameindex('votes')] = mafigameprefix('votes') + str(votes) + '\n'
                            contents[mafigameindex('votenames')] = mafigameprefix('votenames') + str(votenames) + '\n'
                            contents[mafigameindex('votementions')] = mafigameprefix('votementions') + str(votementions) + '\n'
                            contents[mafigameindex('voters')] = mafigameprefix('voters') + str(voters) + '\n'
                            contents[mafigameindex('voternames')] = mafigameprefix('voternames') + str(voternames) + '\n'
                            contents[mafigameindex('votermentions')] = mafigameprefix('votermentions') + str(votermentions) + '\n'
                            with open(mafiguildvalue(guild, 'gameopen'), 'w') as fp:
                                fp.writelines(contents)
                            fp.close()
                            print('D')
                            try:
                                print(voting_message)
                                await message.edit(content=voting_message)
                                print('E')
                            except:
                                print('F')
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
    except FileNotFoundError:
        pass


bot.run(os.getenv('TOKEN'))
