#-*- coding:utf-8 -*-

#================================

import discord
import asyncio
import emoji
import sys
import time
import os
import json
import random as rdm
from discord.utils import get
from discord.ext import commands
from dictionnaires import *
from csts import *
from datetime import datetime


os.chdir(os.path.dirname(__file__))


client = commands.Bot(command_prefix=".")
client.remove_command("help")

"""
TO-DO:

Tester une game avec nouveau système
(Fix les bugs)
Finir le README


"""

@client.event
async def on_ready():

    await client.wait_until_ready()
    await client.change_presence(activity=discord.Game(name="🐺 | .help"))
    print('Bot connecté {0.user}'.format(client))

    online = client.get_channel(742095974033260611)
    updates = client.get_channel(746375690043130057)
    await online.send('✅ **{0.user}** connecté à ``{1}``'.format(client, datetime.now().strftime("%H:%M:%S")))

    # Checking guild
    guildsIds = [str(guild.id) for guild in client.guilds]

    with open('data/guilds.json', encoding='utf-8') as f: 
        data = json.load(f)

    for idg in guildsIds:
        if idg not in data:
            data.update({idg:{"channels":[], "in_game": False, "mdj": None, "valuepf": 25, "language": 'english'}})
            await updates.send("⬆️ LG Bot a **rejoint** le serveur {} ({})".format(client.get_guild(int(idg)), idg))

    for ids in list(data):
        if ids not in guildsIds:
            if client.get_guild(int(ids)) == None:
                await updates.send("⬇️ LG Bot a **quitté** le serveur {}".format(ids))
            else:
                await updates.send("⬇️ LG Bot a **quitté** le serveur {} ({})".format(client.get_guild(int(ids)), ids))
            data.pop(ids, None)

    with open('data/guilds.json', 'w', encoding='utf-8') as f: 
        json.dump(data, f, indent=4, ensure_ascii=False)


@client.event
async def on_guild_join(guild):

    gid = str(guild.id)
    updates = client.get_channel(746375690043130057)

    with open('data/guilds.json', encoding='utf-8') as f: 
        data = json.load(f)

    data.update({gid:{"channels":[], "in_game": False, "mdj": None, "valuepf": 25, "language": 'english'}})

    with open('data/guilds.json', 'w', encoding='utf-8') as f: 
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    await updates.send("⬆️ LG Bot a **rejoint** le serveur {} ({})".format(guild, gid))

    try:
        await guild.create_role(name="LG Host", colour=discord.Color.from_rgb(255,65,65))
    except:
        pass

@client.event
async def on_guild_remove(guild):

    gid = str(guild.id)
    updates = client.get_channel(746375690043130057)

    with open('data/guilds.json', encoding='utf-8') as f: 
        data = json.load(f)

    await updates.send("⬇️ LG Bot a **quitté** le serveur {} ({})".format(guild, gid))
    data.pop(gid, None)

    with open('data/guilds.json', 'w', encoding='utf-8') as f: 
        json.dump(data, f, indent=4, ensure_ascii=False)
  

@client.event
async def on_guild_channel_create(channel):
    
    if channel.name == "lg-announcements":

        embed = discord.Embed(
            colour = discord.Color.from_rgb(100,10,10),
            title = "Thanks for adding LG Bot to {}".format(channel.guild.name),
            description = "From now on, updates and announcements will be sent in this channel."
        )
        embed.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )
        embed.add_field(
            name = "📌 Useful links",
            value = "[Invite the bot](https://www.google.fr/) - [Support server](https://www.google.fr/) - [French server](https://discord.gg/nuUpb7U)",
            inline = False
        )
        embed.add_field(
            name = "Bot Usage",
            value = "To start using the bot, an admin needs to enter the `.setup` command. That will create all the channels needed to play the game. \n \nTo host a game you need to have the `LG Host` role that the bot creates when it joins a server. \n \nUse the `.lsetting` command to change the language of the bot (english by default). Available languages are **french** and **english**. \n \nUse the `.help` command to get more informations about the game and commands.",
            inline = False
        )

        await channel.send(embed=embed)

@client.event
async def on_message(ctx):

    try:
        gid = str(ctx.guild.id)

        with open('data/guilds.json', encoding='utf-8') as f:
            data = json.load(f)

        channels = [client.get_channel(k) for k in data[gid]["channels"]]
        aid = data[gid]["mdj"]
        mdj = client.get_user(aid)
        
        with open('data/games.json', encoding='utf-8') as gf:
            gdata = json.load(gf)

        lang = data[gid]["language"]
        with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
            ldata = json.load(lf)

        game_started = gdata[aid]["game_started"]
        day = gdata[aid]["day"]
        Lroles_dispo = gdata[aid]["Lroles"]
        cpt_jour = gdata[aid]["cpt_jour"]
        can_vote = gdata[aid]["can_vote"]
        Lp = gdata[aid]["Lp"]

    except:
        pass

    author = ctx.author
    rolemdj = 'Maître du Jeu'
    rolebot = 'LG Bot'
    is_okmsg = True


    try:
        if game_started == True:

            # Cas où channel privé
            if ctx.channel.type is discord.ChannelType.private:
                if author.bot:
                    pass

                else:
                    if can_vote == False:
                        is_okmsg = False
                        await ctx.author.send(ldata["voteCannotSendMsg"])

                    elif can_vote == True and Lp[str(ctx.author.id)][10] == 'Non':
                        await ctx.author.send(ldata["voteAlreadyVoted"])

                    elif can_vote == True and Lp[str(ctx.author.id)][10] == 'Oui':
                        vote = str(ctx.content)

                        if vote == 'blanc' or vote == 'Blanc':

                            embedv = discord.Embed(
                                colour = discord.Color.from_rgb(255,255,255)
                            )
                            embedv.set_author(
                                name = "LG Bot",
                                icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                            )
                            embedv.add_field(
                                name = ldata["voteEmbedName"],
                                value = ldata["voteEmbedValue"],
                                inline = False
                            )

                        else:
                            try:
                                member_name, member_discriminator = vote.split('#')
                            except ValueError:
                                await ctx.channel.send(ldata["voteValueError"])
                            else:
                                
                                aut_name, aut_disc = str(ctx.author).split('#')
                                is_author = False

                                for userid in dicop_id_to_emoji:
                                    user = client.get_user(int(userid))
                                    if (user.name, user.discriminator) == (member_name, member_discriminator):

                                        if (user.name, user.discriminator) == (aut_name, aut_disc):
                                            
                                            if 'Ange' in Lroles_dispo:
                                                is_author = True

                                        if is_author == False:
                                            Lp[str(ctx.author.id)][10] = 'Non'

                                            embedv = discord.Embed(
                                                colour = discord.Color.green(),
                                            )
                                            embedv.set_author(
                                                name = ctx.author.name,
                                                icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.author)
                                            )
                                            embedv.add_field(
                                                name = ldata["voteEmbedName"],
                                                value = ldata["voteEmbedChoice"].format(user),
                                                inline = False
                                            )
                                            embedv.set_thumbnail(
                                                url = user.avatar_url
                                            )

                                            await ctx.author.send(embed=embedv)
                                            await channels[0].send(embed=embedv)
                                            break

                                        else:
                                            await ctx.author.send(ldata["voteVoteYourself"])
                                            break
                                
                                if Lp[str(ctx.author.id)][10] == 'Oui' and is_author == False:
                                    await ctx.author.send(ldata["votePlayerNameNotValid"])

                                else:
                                    await ctx.author.send(ldata["voteUserDone"])


            # Cas où auteur = bot ou mdj
            try:
                role_author = [role.name for role in author.roles]
                if rolemdj in role_author or ctx.author.bot:
                    is_okmsg = False
            except:
                pass
            
            
            # Cas où il faut crypter un message
            if is_okmsg == True:

                #Cryptage du message
                msg = ctx.content
                strm = [c for c in msg]
                # 1/4 chance qu'une lettre de fasse remplacer par un des symboles ci-dessous (par défaut, dépend de valuepf)
                for i in range(len(strm)-1):
                    if strm[i] != ' ':
                        replace = rdm.randint(1,100)
                        if replace <= valuepf:
                            strm[i] = rdm.choice(['#','?','$','%','@','§'])

                # Cas de la PF qui reçoit les msg des LG (pas LGB ni IPDL)          
                if ctx.channel == channels[8]:
                    if day == False:     
                        await channels[9].send(''.join(strm))

                    if 'Oeil' in Lroles_dispo and cpt_jour == 1:
                        await channels[23].send("({}) ".format(ctx.channel.name) + ''.join(strm))
                
                # Cas du Chaman qui reçoit le salon des morts
                elif ctx.channel == channels[3]:
                    await channels[20].send(''.join(strm))
                    
                    if 'Oeil' in Lroles_dispo and cpt_jour == 1:
                        await channels[23].send("({}) ".format(ctx.channel.name) + ''.join(strm))

                # Cas du Jaloux qui reçoit le salon du couple
                elif ctx.channel == channels[6]:
                    if day == True:
                        await channels[21].send(''.join(strm))
                    
                    if 'Oeil' in Lroles_dispo and cpt_jour == 1:
                        await channels[23].send("({}) ".format(ctx.channel.name) + ''.join(strm))

                # Cas du 3e Oeil
                elif ctx.channel in channels:
                    if ctx.channel.name == 'commandes-bot' or ctx.channel.name == 'roles-de-la-game' or ctx.channel.name == 'place-du-village' or ctx.channel.name == '3e-oeil' or ctx.channel.name == 'chaman' or ctx.channel.name == 'petite-fille' or ctx.channel.name == 'jaloux':
                        pass
                    else:
                        if 'Oeil' in Lroles_dispo and cpt_jour == 1:
                            await channels[23].send("({}) ".format(ctx.channel.name) + ''.join(strm))

    except:
        pass

    await client.process_commands(ctx)

@client.event
async def on_command_error(ctx, error):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
            data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send(ldata["errorMissingArg"].format(ctx.author))
    
    if isinstance(error, commands.MissingAnyRole):
        await ctx.channel.send(ldata["errorPermissionMissing"])

    if isinstance(error, commands.MissingPermissions):
        await ctx.channel.send(ldata["errorPermissionMissing"])

@client.command()
async def update(ctx, atype, *, text):

    gid = str(ctx.guild.id)
    updates = client.get_channel(746375690043130057)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    if ctx.author.id == 157588494460518400:
        
        L = text.split('|')

        if atype == "annonce":
            ecolor = discord.Color.from_rgb(100,10,10)
        elif atype == "update":
            ecolor = discord.Color.green()
        elif atype == "test":
            ecolor = discord.Color.gold()

        embed = discord.Embed(
            colour = ecolor,
            title = ldata["updateTitle"]
        )
        embed.set_author(
            name = ctx.author,
            icon_url = ctx.author.avatar_url
        )

        for i in range(0, len(L), 2):
            embed.add_field(
                name = L[i],
                value = L[i+1],
                inline = False
            )

        if atype == 'test':
            await updates.send('**ANNOUNCEMENT TEST**')
            await updates.send(embed=embed)
            
        else:
            for guild in client.guilds:
                print(guild.name)
                channel = discord.utils.get(guild.text_channels, name='lg-announcements')
                if channel == None:
                    await updates.send("``{}`` n'a pas de channel lg-announcements".format(guild.name))
                else:
                    await channel.send(embed=embed)
    
    else:
        await ctx.channel.send(ldata["errorPermissionMissing"])


@client.command()
async def help(ctx):
#Commande d'aide utilisateur


    if ctx.channel.type is discord.ChannelType.private:
        pass

    else:
        gid = str(ctx.guild.id)

        with open('data/guilds.json', encoding='utf-8') as f:
            data = json.load(f)

        lang = data[gid]["language"]
        with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
            ldata = json.load(lf)

        author = ctx.author

        embed0 = discord.Embed(
            colour = discord.Color.from_rgb(123,23,43),
            title = ldata["helpPage0Title"],
            description = ldata["helpPage0Desc"]
        )
        embed0.add_field(
            name = ldata["helpPage0Field1Name"],
            value = ldata["helpPage0Field1Value"],
            inline = False
        )
        embed0.add_field(
            name = ldata["helpPage0Field2Name"],
            value = ldata["helpPage0Field2Value"],
            inline = False
        )
        embed0.add_field(
            name = ldata["helpPage0Field3Name"],
            value = ldata["helpPage0Field3Value"],
            inline = True
        )
        embed0.add_field(
            name = ldata["helpPage0Field4Name"],
            value = ldata["helpPage0Field4Value"],
            inline = True
        )
        embed0.add_field(
            name = ldata["helpPage0Field5Name"],
            value = ldata["helpPage0Field5Value"],
            inline = True   
        )
        embed0.add_field(
            name = ldata["helpPage0Field6Name"],
            value = ldata["helpPage0Field6Value"],
            inline = False
        )
        embed0.set_footer(
            text = 'Page 1/5 • {0.name}'.format(author)
        )


        embed1 = discord.Embed(
            colour = discord.Color.red(),
        )

        embed1.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )

        embed1.set_thumbnail(
            url='https://www.loups-garous-en-ligne.com/jeu/assets/images/carte2.png'
        )

        embed1.add_field(
            name = ldata["helpPage1Field2Name"],
            value = ldata["helpPage1Field2Value"],
            inline = False
        )

        embed1.set_footer(
            text = 'Page 2/5 • {0.name}'.format(author)
        )

        embed2 = discord.Embed(
            colour = discord.Color.from_rgb(0,0,100),
            title = ldata["helpPage2Title"]
        )
        embed2.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )
        embed2.set_thumbnail(
            url='https://www.loups-garous-en-ligne.com/jeu/assets/images/carte2.png'
        )
        embed2.add_field(
            name = ldata["helpPage2Field1Name"],
            value = ldata["helpPage2Field1Value"],
            inline = False
        )
        embed2.add_field(
            name = ldata["helpPage2Field2Name"],
            value = ldata["helpPage2Field2Value"],
            inline = False
        )
        embed2.add_field(
            name = ldata["helpPage2Field3Name"],
            value = ldata["helpPage2Field3Value"],
            inline = False
        )
        embed2.set_footer(
            text = 'Page 3/5 • {0.name}'.format(author)
        )

        embed3 = discord.Embed(
            colour = discord.Color.gold(),
            title = ldata["helpPage3Title"]
        )

        embed3.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )
        embed3.set_thumbnail(
            url='https://www.loups-garous-en-ligne.com/jeu/assets/images/carte2.png'
        )
        embed3.add_field(
            name = ldata["helpPage3Field1Name"],
            value = ldata["helpPage3Field1Value"],
            inline = False
        )
        embed3.set_footer(
            text = 'Page 4/5 • {0.name}'.format(author)
        )

        embed4 = discord.Embed(
            colour = discord.Color.green(),
            title = ldata["helpPage4Title"]
        )
        embed4.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )
        embed4.set_thumbnail(
            url='https://www.loups-garous-en-ligne.com/jeu/assets/images/carte2.png'
        )
        embed4.add_field(
            name = ldata["helpPage4Field1Name"],
            value = ldata["helpPage4Field1Value"],
            inline = False
        )
        embed4.set_footer(
            text = 'Page 5/5 • {0.name}'.format(author)
        )

        #await ctx.channel.send(ldata["helpNoticeUser"].format(author))
        panel = await ctx.channel.send(embed=embed0)
        page = 0
        d = {0: embed0, 1: embed1, 2: embed2, 3: embed3, 4: embed4}
        await panel.add_reaction(left)
        await panel.add_reaction(right)

        def checkHelp(reaction, user):
            return (user == author) and (panel.id == reaction.message.id) and (str(reaction.emoji) == left or str(reaction.emoji) == right)
        
        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", check=checkHelp, timeout=120.0)
                if str(reaction.emoji) == right:
                    if page < 4:
                        page += 1
                    else:
                        page = 0
                    await panel.edit(embed=d[page])
                elif str(reaction.emoji) == left:
                    if page > 0:
                        page -= 1
                    else:
                        page = 4
                    await panel.edit(embed=d[page])
            except asyncio.TimeoutError:
                break



@client.command()
@commands.has_any_role("Maître du Jeu")
async def test(ctx):

    with open('data/games.json', encoding='utf-8') as f:
        data = json.load(f)

    await ctx.channel.send(', '.join(data[str(ctx.author.id)]["Lroles"]))


@client.command()
async def lsetting(ctx, langs):

    gid = str(ctx.guild.id)
    with open("data/guilds.json", encoding='utf-8') as f:
        data = json.load(f)
    

    if langs == 'french' or langs == 'english':
        data[gid]["language"] = langs
        with open("data/guilds.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        if ctx.author.guild_permissions.administrator:
        
            lang = data[gid]["language"]
            with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
                ldata = json.load(lf)
            await ctx.channel.send(ldata["lsettingsConfirmation"].format(langs))

        else:
            await ctx.channel.send(ldata["errorPermissionMissing"])

    else:
        await ctx.channel.send(ldata["lsettingsError"])


@client.command()
async def setup(ctx):

    author = ctx.author
    print("Commande .setup exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), author))

    gid = str(ctx.guild.id)
    with open("data/guilds.json", encoding='utf-8') as f:
        d = json.load(f)
    
    lang = d[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    if lang == 'french':
        chans = chans_fr
    elif lang == 'english':
        chans = chans_en

    if ctx.author.guild_permissions.administrator:

        try:
            if len(d[gid]["channels"]) > 0:
                await ctx.channel.send(ldata["setupAlreadyExecuted"])
                d[gid]["in_game"] = False
                d[gid]["mdj"] = None
                with open("data/guilds.json", 'w', encoding='utf-8') as f:
                    json.dump(d, f, indent=4, ensure_ascii=False)
        except:
            d.update({gid:{"channels":[], "in_game": False, "mdj": None, "valuepf": 25}})
            with open("data/guilds.json", 'w', encoding='utf-8') as f:
                json.dump(d, f, indent=4, ensure_ascii=False)

        if len(d[gid]["channels"]) == 0:

            guild = ctx.guild
            text_channel_list = []
            channels = []

            embed = discord.Embed(
                    colour = discord.Color.red(),
                    title = ldata["setupErrorEmbedTitle"]
                )

            name = ldata["categoryName"]
            category = discord.utils.get(ctx.guild.categories, name=name)

            is_categ = False

            for categorie in guild.categories:
                if str(categorie) == name:
                    is_categ = True
                    break

            if is_categ == False:
                await guild.create_category(name)

            print(is_categ)
            category = discord.utils.get(ctx.guild.categories, name=name)


            for channel in guild.text_channels:
                if str(channel.category) == name:
                    text_channel_list.append(str(channel.name))


            print(text_channel_list)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False, mention_everyone=False, attach_files=False, embed_links=False)
            }
            overwrites_pdv = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, read_message_history=True, mention_everyone=False, attach_files=False, embed_links=False)
            }

            for i in range(0,30):

                if chans[i] in text_channel_list:
                    print('{} déjà créée'.format(chans[i]))
        
                else:
                    if i == 1 or i == 2:
                        await guild.create_text_channel(chans[i], category=category, overwrites=overwrites_pdv) 
                    else:
                        await guild.create_text_channel(chans[i], category=category, overwrites=overwrites)
                    print('{} OK'.format(chans[i]))

                try:
                    channels.append((discord.utils.get(guild.text_channels, name=chans[i])).id)
                except:
                    pass
            
            with open('data/guilds.json', encoding='utf-8') as json_file: 
                data = json.load(json_file) 

            data[gid]["channels"] = channels

            with open('data/guilds.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent = 4, ensure_ascii=False)
            
            channels = [client.get_channel(idc) for idc in channels]
            print(channels)

            await channels[0].send(ldata["setupOver"])

    else:
        await ctx.channel.send(ldata["errorPermissionMissing"])


@client.command()
async def delete(ctx):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    if ctx.author.guild_permissions.administrator:

        channels = [client.get_channel(k) for k in data[gid]["channels"]]
        print(data[gid]["channels"])
        if len(data[gid]["channels"]) == 0:
            
            await ctx.channel.send(ldata["deleteError"].format(non))

        else:

            embed = discord.Embed(
                colour = discord.Color.from_rgb(85,0,25)
            )

            embed.set_author(
                name = "LG Bot",
                icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
            )

            embed.add_field(
                name = ldata["deleteName"],
                value = ldata["deleteValue"].format(ok, non),
                inline = False
            )

            panel = await ctx.channel.send(embed=embed)
            await panel.add_reaction(ok)
            await panel.add_reaction(non)

            def checkDelete(reaction, user):
                return (user == ctx.author) and (str(reaction.emoji) == ok or str(reaction.emoji) == non) and (reaction.message.id == panel.id)

            try:
                reaction, user = await client.wait_for("reaction_add", check=checkDelete, timeout=30.0)
            except:
                pass
            else:
                if str(reaction.emoji) == ok:
                    name = ldata["categoryName"]
                    category = discord.utils.get(ctx.guild.categories, name=name)
                    for channel in ctx.guild.text_channels:
                        if str(channel.category) == name:
                            await channel.delete()
                    
                    await category.delete()

                    data[gid]["channels"] = []

                    with open("data/guilds.json", 'w', encoding='utf-8') as jf:
                        json.dump(data, jf, indent=4, ensure_ascii=False)
                else:
                    await panel.delete()
    
    else:
        await ctx.channel.send(ldata["errorPermissionMissing"])

"""
@client.command()
async def hcreate(ctx):

    if ctx.channel.type is discord.ChannelType.private:
        pass
    else:
        gid = str(ctx.guild.id)

        with open('data/guilds.json', encoding='utf-8') as f:
            data = json.load(f)

        lang = data[gid]["language"]
        with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
            ldata = json.load(lf)

        if lang == 'french':
            liste_roles = liste_roles_fr
        elif lang == 'english':
            liste_roles = liste_roles_en

        embed = discord.Embed(
            colour = discord.Color.from_rgb(0,0,120),
            title = ldata["helpCreateTitle"]
        )

        embed.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )

        embed.add_field(
            name = ldata["helpCreateField1Name"],
            value = ldata["helpCreateField1Value"],
            inline = False
        )


        embed.add_field(
            name = ldata["helpCreateField2Name"],
            value = ldata["helpCreateField2Value"],
            inline = False
        )


        embed.add_field(
            name = ldata["helpCreateField2Name"],
            value = ', '.join(liste_roles) + ldata["helpCreateField3Value"],
            inline = False
        )


        await ctx.channel.send(ldata["helpCreateNoticeUser"].format(ctx.author))

        await ctx.author.send(embed=embed)
"""

@client.command()
@commands.has_any_role("LG Host")
async def create(ctx):
    
    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    if lang == 'french':
        liste_roles = liste_roles_fr
    elif lang == 'english':
        liste_roles = liste_roles_en

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    in_game = data[gid]["in_game"]

    if len(channels) != 0:

        embed = discord.Embed(
            colour = discord.Color.from_rgb(0,0,100)
        )

        embed.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )

        embed.add_field(
            name = ldata["createWaitForName1"],
            value = ldata["createWaitForValue"],
            inline = False
        )
        st = ', '.join(liste_roles)
        embed.add_field(
            name = ldata["createWaitForName2"],
            value = "```{}```".format(st),
            inline = False
        )

        panel = await ctx.channel.send(embed=embed)

        def checkCreate(message):
            return message.author == ctx.author and ctx.channel == message.channel

        try:
            message = await client.wait_for("message", check=checkCreate, timeout=60.0)
        except asyncioTimeoutError:
            pass
        else:
            await panel.delete()
            Lroles_dispo = []
            ok_roles = True
            Lroles = message.content.split(", ")
            for role in Lroles:
                if role not in liste_roles:
                    print(role)
                    await ctx.channel.send(ldata["createRoleNotValidEmbedValue"].format(role))
                    ok_roles = False
                    break
                else:
                    Lroles_dispo.append(role)

            if lang == "french":

                if ('Voleur' in Lroles_dispo and 'Sectaire' in Lroles_dispo) or ('Voleur' in Lroles_dispo and 'JDF' in Lroles_dispo) or ('Voleur' in Lroles_dispo and 'Imposteur' in Lroles_dispo) or ('Voleur' in Lroles_dispo and 'Traitre' in Lroles_dispo):
                    await ctx.channel.send("❌ Une combinaison de rôle est incompatible. Le **Voleur** n'est pas compatible avec: ``Sectaire, Joueur de Flûte, Imposteur, Traître``")
                    ok_roles = False

                if ('Imposteur' in Lroles_dispo and 'Traitre' in Lroles_dispo):
                    await ctx.channel.send("❌ Impossible d'avoir un Imposteur et un Traître dans la même partie.")
                    ok_roles = False
                
                oneRoles = ['Voyante','Chasseur','Jaloux','Ancien','Sorcière','PF','Bouc','Idiot','Corbeau','Chaman','Renard','Ours','Chevalier','Salvateur','LGA','IPDL','LGB','Cupidon','JDF','Ange','Enfant','Voleur','Sectaire','Juge','Confesseur','Chaperon','Ankou','Dictateur','Noctambule','Oeil','Traitre','Imposteur','Faucheur','Servante','Assassin','Devin']
                for role in oneRoles:
                    if Lroles_dispo.count(role) > 1:
                        await ctx.channel.send("❌ Impossible d'avoir plusieurs **{}** dans la même partie.".format(role))
                        ok_roles = False
                        break

                if 'Chaperon' in Lroles_dispo and 'Chasseur' not in Lroles_dispo:
                    await ctx.channel.send("❌ Impossible d'avoir un Chaperon Rouge sans Chasseur")
                    ok_roles = False
            
            elif lang == "english":

                if ('Thief' in Lroles_dispo and 'Sectairian' in Lroles_dispo) or ('Thief' in Lroles_dispo and 'PP' in Lroles_dispo) or ('Thief' in Lroles_dispo and 'Impostor' in Lroles_dispo) or ('Thief' in Lroles_dispo and 'Traitor' in Lroles_dispo):
                    await ctx.channel.send("❌ A role combination is not allowed. A **Thief** can't be in the same roster as: ``Sectarian, Pied Piper, Impostor, Traitor``")
                    ok_roles = False

                if ('Impostor' in Lroles_dispo and 'Traitor' in Lroles_dispo):
                    await ctx.channel.send("❌ A role combination is not allowed: A **Traitor** and an **Impostor** cannot be in the same game.")
                    ok_roles = False
                
                oneRoles = ['Oracle','Hunter','Jealous','Ancient','Witch','Girl','Scapegoat','Idiot','Crow','Shaman','Fox','Bear','Knight','Guard','AW','WF','WW','Cupid','PP','Angel','Child','Thief','Sectarian','Juge','Confessor','RRH','Ankou','Dictator','Owl','Eye','Traitor','Impostor','Reaper','Servant','Assassin','Diviner']
                for role in oneRoles:
                    if Lroles_dispo.count(role) > 1:
                        await ctx.channel.send("❌ You cannot have multiple **{}** in the game.".format(role))
                        ok_roles = False
                        break

                if 'RRH' in Lroles_dispo and 'Hunter' not in Lroles_dispo:
                    await ctx.channel.send("❌ You cannot have a **Red Riding Hood** in the game without a **Hunter**")
                    ok_roles = False
                
            if ok_roles == True:

                if len(Lroles_dispo) != 0:

                    if 'Voleur' in Lroles_dispo or 'Imposteur' in Lroles_dispo or 'Traitre' in Lroles_dispo or 'Chaman' in Lroles_dispo or 'IPDL' in Lroles_dispo or 'Thief' in Lroles_dispo or 'Impostor' in Lroles_dispo or 'Traitor' in Lroles_dispo or 'Shaman' in Lroles_dispo or 'WF' in Lroles_dispo:
                        evalue = ldata["createVisibilityValueHidden"]
                    else:
                        evalue = ldata["createVisibilityValueVisible"]
                    
                    embed = discord.Embed(
                        colour = discord.Color.from_rgb(0,0,100),
                        description = "Composition: {}".format(', '.join(Lroles_dispo))
                    )

                    embed.add_field(
                        name = ldata["createVisibilityName"],
                        value = evalue,
                        inline = False
                    )
    
                    embed.set_author(
                        name = "LG Bot",
                        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                    )

                    panel2 = await ctx.channel.send(embed=embed)
                    await panel2.add_reaction('👁️')
                    if 'Voleur' in Lroles_dispo or 'Imposteur' in Lroles_dispo or 'Traitre' in Lroles_dispo or 'Chaman' in Lroles_dispo or 'IPDL' in Lroles_dispo or 'Thief' in Lroles_dispo or 'Impostor' in Lroles_dispo or 'Traitor' in Lroles_dispo or 'Shaman' in Lroles_dispo or 'WF' in Lroles_dispo:
                        pass
                    else:
                        await panel2.add_reaction(non)

                    def checkCreate2(reaction, user):
                        return (user == ctx.author) and (reaction.message.id == panel2.id) and (str(reaction.emoji) == '👁️' or str(reaction.emoji) == non)

                    try:
                        reaction, user = await client.wait_for("reaction_add", check=checkCreate2, timeout=30.0)
                    except asyncioTimeoutError:
                        pass
                    else:

                        await channels[1].purge(limit=50)

                        if str(reaction.emoji) == '👁️':
                            compo = ldata["compoVisible"]
                            is_compo = True

                        else:
                            compo = ldata["compoHidden"]
                            await channels[1].send(ldata["compoIsHidden"])
                            is_compo = False

                        await panel2.delete()

                        if in_game == False:
                            with open('data/games.json', encoding='utf-8') as json_file: 
                                data = json.load(json_file) 
                            data.update({str(ctx.author.id):{"guild":ctx.guild.id, "Lp": {}, "Lroles": [], "idtoemoji": {}, "dictemoji": {}, "is_compo": is_compo, "game_started": False, "day": True, "is_enfant": False, "ancien_dead": False, "check_couple": False, "cpt_jour": 0, "can_vote": False}})
                            with open('data/games.json', 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent = 4, ensure_ascii=False)

                        with open('data/games.json', encoding='utf-8') as jf:
                            gdata = json.load(jf)

                        gdata[str(ctx.author.id)]["Lroles"] = Lroles_dispo
                        
                        if compo == ldata["compoVisible"]:
                            gdata[str(ctx.author.id)]["is_compo"] = True
                        else:
                            gdata[str(ctx.author.id)]["is_compo"] = False

                        with open('data/games.json', 'w', encoding='utf-8') as f:
                            json.dump(gdata, f, indent=4, ensure_ascii=False)

                        with open('data/guilds.json', encoding='utf-8') as json_file:
                            data = json.load(json_file)
                        
                        data[gid]["in_game"] = True
                        data[gid]["mdj"] = ctx.author.id

                        with open('data/guilds.json', 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=4, ensure_ascii=False)


                        embedc = discord.Embed(
                            colour = discord.Color.from_rgb(0,0,100),
                            title = ldata["createConfrimTitle"]
                        )

                        Lr = ["{}".format(k) for k in Lroles_dispo]
                        st = ", ".join(Lr)

                        embedc.add_field(
                            name = ldata["createConfrimField1Name"],
                            value = "```{}```".format(st),
                            inline = False
                        )

                        embedc.add_field(
                            name = ldata["createConfrimField2Name"],
                            value = ldata["createConfrimField2Value"].format(compo),
                            inline = False
                        )

                        embedc.set_author(
                            name = "LG Bot",
                            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                        )

                        await ctx.channel.send(ldata["createGameCreated"].format(ctx.author))
                        await ctx.channel.send(embed=embedc)
                        if compo == ldata["compoVisible"]:
                            await channels[1].send(embed=embedc)
                        await channels[1].send(ldata["createGameMaster"].format(ctx.author))

    else: 
        await ctx.channel.send(ldata["createSetupErrorValue"])
        await ctx.send(embed=embed)


@client.command()
@commands.has_any_role("LG Host")
async def sign(ctx, action = 'create'):
    # Permet d'inscrire automatiquement tout le monde à la partie.

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    in_game = data[gid]["in_game"]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    if action == "create":
                    
        gdata[aid]["idtoemoji"] = {}
        gdata[aid]["dictemoji"] = {}

        with open('data/games.json', 'w', encoding='utf-8') as jf:
            json.dump(gdata, jf, indent=4, ensure_ascii=False)

    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    dicop_emoji = gdata[aid]["dictemoji"]

    print("Commande .sign {} exécutée à {} par {}.".format(action, datetime.now().strftime("%H:%M:%S"), ctx.author))


    embed = discord.Embed(
        colour = discord.Color.red(),
        title = ldata["inscriptionErrorTitle"]
    )

    embed.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    try:
        author = ctx.author
        channel = author.voice.channel
        members = channel.members
    except:
        embed.add_field(
            name = ldata["inscriptionVoiceErrorName"],
            value = ldata["inscriptionVoiceErrorValue"],
            inline = False
        )

        await ctx.channel.send(ldata["errorNotice"].format(ctx.author.id))
        await ctx.channel.send(embed=embed)
    
    else:

        if len(channels) > 0:

            if in_game == True:

                if action == "create":
                    
                    gdata[aid]["idtoemoji"] = {}
                    gdata[aid]["dictemoji"] = {}

                    with open('data/games.json', 'w', encoding='utf-8') as jf:
                        json.dump(gdata, jf, indent=4, ensure_ascii=False)

                    print(dicop_id_to_emoji)

                    Lj = [member for member in members if str(member.id) not in dicop_id_to_emoji and str(member) != str(author)]
                    recap = ["``{}``: {} \n".format(member, dicop_id_to_emoji[str(member.id)]) for member in members if str(member.id) in dicop_id_to_emoji]

                    insc_loading = await ctx.channel.send(ldata["inscriptionLoading"])

                    print("create")

                    is_there_banned = False
                    # ex_liste = ['◽','🥇','🥈','🐝','🚙','🛏️','😎','😆','😔','👏']

                    while True:
                        eliste = rdm.sample(list(emoji.UNICODE_EMOJI), len(Lj))
                        #eliste = rdm.sample(ex_liste, len(Lj))
                        print(eliste)
                        banned_emojis = ['✅','❌','❎','⬜','🌫️','◻️','▫️','◽','🥇','🥈',"🐺", "🔪", "👒", "🔇", "🔊", "🌙", "🧒", "❤️", "💤", "🕵️", "🎺", "🌞","1️⃣","2️⃣","3️⃣","🛑","⏱️","📔"]
                        for bem in banned_emojis:
                            if bem in eliste:
                                is_there_banned = True
                                break
                        print(is_there_banned)
                        if is_there_banned == False:
                            break
                        else:
                            is_there_banned = False
                        

                    print(eliste)

                    for member in Lj:

                        await channels[1].set_permissions(member, overwrite=can_see)
                        await channels[2].set_permissions(member, overwrite=can_talk)
                        print(member)
                        if str(member) != str(author):

                            for i in range(3,30):
                                await channels[i].set_permissions(member, overwrite=cant_talk)
                            #Enlève les permissions de tous les salons pour tous les joueurs

                        print("OK perm {}".format(member))

                        emoji_p = rdm.choice(eliste)
                        eliste.remove(emoji_p)

                        print(member, emoji_p)

                        gdata[aid]["idtoemoji"][str(member.id)] = emoji_p
                        gdata[aid]["dictemoji"][emoji_p] = member.id


                        with open('data/games.json', 'w', encoding='utf-8') as jf:
                            json.dump(gdata, jf, indent=4, ensure_ascii=False)


                        await member.add_roles(get(member.guild.roles, name="Joueurs Thiercelieux"))

                        await channels[0].send(ldata["inscriptionPlayerEmoji"].format(member,emoji_p))

                        recap.append("``{}``: {} \n".format(member, emoji_p))

                    await ctx.channel.send(ldata["inscriptionDone"])

                    await insc_loading.delete()

                    embedi = discord.Embed(
                        colour = discord.Color.gold(),
                        title = ldata["inscriptionRecapTitle"]
                    )
                    embedi.add_field(
                        name = ldata["inscriptionRecapName"],
                        value = ''.join(recap),
                        inline = False
                    )
                    embedi.set_author(
                        name = "LG Bot",
                        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                    )
                    embedi.set_footer(
                        text = ldata["inscriptionRecapFooter"]
                    )

                    await ctx.channel.send(embed=embedi)

                
                elif action == 'clear':

                    print("clear")

                    if len(dicop_id_to_emoji) == 0:
                        await ctx.channel.send(ldata["inscriptionNoSignedUp"])

                    else:
                        gdata[aid]["idtoemoji"] = {}
                        gdata[aid]["dictemoji"] = {}

                        with open('data/games.json', 'w', encoding='utf-8') as jf:
                            json.dump(gdata, jf, indent=4, ensure_ascii=False)

                        await ctx.channel.send(ldata["inscriptionClearDone"])
                    

                else:
                    embed.add_field(
                        name ='✏️ Erreur: Argument invalide', 
                        value = "L'argument est invalide. Veuillez vérifier que l'argument est soit 'create' ou 'clear'.", 
                        inline = False
                    )

                    await ctx.channel.send(ldata["errorNotice"].format(ctx.author.id))
                    await ctx.send(embed=embed)

            else:
                embed.add_field(
                    name = ldata["inscriptionNoGameName"],
                    value = ldata["inscriptionNoGameValue"],
                    inline = False
                )
                
                await ctx.channel.send(ldata["errorNotice"].format(ctx.author.id))
                await ctx.channel.send(embed=embed)

        else:
            embed.add_field(
                name = ldata["inscriptionNoSetupName"],
                value = ldata["inscriptionNoSetupValue"],
                inline = False
            )

            await ctx.channel.send(ldata["errorNotice"].format(ctx.author.id))
            await ctx.channel.send(embed=embed)
    


@client.command()
@commands.has_any_role("LG Host")
async def remove(ctx, *, member : discord.User):
    
    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    dicop_emoji = gdata[aid]["dictemoji"]

    member_name, member_discriminator = member.split('#')

    rrecap = []
    user_del = None

    for userid in dicop_id_to_emoji:
        user = client.get_user(int(userid))

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            user_del = user
            print("ok")

        else:
            rrecap.append("``{}``: {} \n".format(user, dicop_id_to_emoji[str(userid)]))

    del gdata[aid]["dictemoji"][dicop_id_to_emoji[str(user_del.id)]]
    del gdata[aid]["idtoemoji"][str(user_del.id)]
    await ctx.channel.send(ldata["removePlayerNotice"].format(user_del))
    print("ok")

    embed = discord.Embed(
        colour = discord.Color.gold(),
        title = ldata["inscriptionRecapTitle"]
    )
    embed.add_field(
        name = ldata["inscriptionRecapName"],
        value = ''.join(rrecap),
        inline = False
    )
    embed.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )


    if user_del == None:
        ctx.channel.send(ldata["removePlayerNotValid"])

    else:
        await ctx.channel.send(embed=embed)


@client.command()
@commands.has_any_role("LG Host")
async def players(ctx):
#Affiche la liste de tous les rôles

    print("Commande .liste exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), ctx.author))

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)
    
    dicop_id_to_emoji = gdata[aid]["idtoemoji"]

    recap = []
    if len(dicop_id_to_emoji) == 0:
        await ctx.channel.send(ldata["playersNoSigned"])
    else:
        print("ok joueurs aff")
        if len(Lp) != 0:
            for nameid in dicop_id_to_emoji:
                fiche_player = Lp[nameid]
                rolep = fiche_player[1]
                if str(rolep) == 'Mort':
                    pass
                else:
                    recap.append("``{}``: {} \n".format(client.get_user(int(nameid)), dicop_id_to_emoji[nameid]))
        
        else:
            for nameid in dicop_id_to_emoji:
                recap.append("``{}``: {} \n".format(client.get_user(int(nameid)), dicop_id_to_emoji[nameid]))
    
        embed = discord.Embed(
            colour = discord.Color.orange(),
            title = ldata["playersEmbedName"]
        )
        embed.add_field(
            name = ldata["playersEmbedValue"],
            value = ''.join(recap),
            inline = False
        )
        embed.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )

        await ctx.channel.send(embed=embed)


@client.command()
async def roles(ctx):
#Permet d'afficher la liste des rôles (envoyé en MP)

    if ctx.channel.type is discord.ChannelType.private:
        pass

    else:
        gid = str(ctx.guild.id)

        with open('data/guilds.json', encoding='utf-8') as f:
                data = json.load(f)

        lang = data[gid]["language"]
        with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
            ldata = json.load(lf)

        if lang == 'french':
            LrVillage = LrVillage_fr
            LrLG = LrLG_fr
            LrSolo = LrSolo_fr
            LrAutre = LrAutre_fr
            trad_roles = trad_roles_fr
            desc_roles = desc_roles_fr
        elif lang == 'english':
            LrVillage = LrVillage_en
            LrLG = LrLG_en
            LrSolo = LrSolo_en
            LrAutre = LrAutre_en
            trad_roles = trad_roles_en
            desc_roles = desc_roles_en

        def Ldivide(L,n):

            for i in range(0, len(L), n):  
                yield L[i:i + n]

        LrV = list(Ldivide(LrVillage,(len(LrVillage)//2)+1))
        LrG = list(Ldivide(LrLG, len(LrLG)))
        LrS = list(Ldivide(LrSolo, len(LrSolo)))
        LrA = list(Ldivide(LrAutre, len(LrAutre)))

        Lall = [LrV,LrG,LrS,LrA]

        d = {}
        cpt = 0
        author = ctx.author

        for Lgr in Lall:

            for L in Lgr:

                if Lgr == LrV:
                    ecolour = discord.Color.green()
                    etitle = ldata["rolesVillage"]

                elif Lgr == LrG:
                    ecolour = discord.Color.red()
                    etitle = ldata["rolesWerewolves"]

                elif Lgr == LrS:
                    ecolour = discord.Color.default()
                    etitle = ldata["rolesSolo"]

                elif Lgr == LrA:
                    ecolour = discord.Color.from_rgb(254,254,254)
                    etitle = ldata["rolesOthers"]

                embed = discord.Embed(
                    colour = ecolour,
                    title = etitle
                )
                
                embed.set_author(
                    name = "LG Bot",
                    icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                )

                for i in range(len(L)):

                    if L[i] in trad_roles:
                        ename = "{} ({})".format(trad_roles[L[i]], L[i])
                    else:
                        ename = L[i]

                    embed.add_field(
                        name = ename,
                        value = "```{}```".format(desc_roles[L[i]]),
                        inline = False
                    )

                #await ctx.channel.send(embed=embed)

                
                d[cpt] = embed
                cpt += 1

        page = 0
        panel = await ctx.channel.send(embed=d[page])
        await panel.add_reaction(left)
        await panel.add_reaction(right)

        def checkRoles(reaction, user):
            return (user == author) and (panel.id == reaction.message.id) and (str(reaction.emoji) == left or str(reaction.emoji) == right)
        
        while True:
            try:
                reaction, user = await client.wait_for("reaction_add", check=checkRoles, timeout=120.0)
                if str(reaction.emoji) == right:
                    if page < len(list(d))-1:
                        page += 1
                    else:
                        page = 0
                    await panel.edit(embed=d[page])
                elif str(reaction.emoji) == left:
                    if page > 0:
                        page -= 1
                    else:
                        page = len(list(d))-1
                    await panel.edit(embed=d[page])
            except asyncio.TimeoutError:
                break
                

@client.command()
@commands.has_any_role("LG Host")
async def start(ctx, state_couple = 'non'):
#Commande de départ

    gid = str(ctx.guild.id)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    if lang == 'french':
        liste_roles = liste_roles_fr
        liste_LG = liste_LG_fr
        liste_village = liste_village_fr
        desc_roles = desc_roles_fr
        dicoroles = dicoroles_fr
        trad_roles = trad_roles_fr
    elif lang == 'english':
        liste_roles = liste_roles_en
        liste_LG = liste_LG_en
        liste_village = liste_village_en
        desc_roles = desc_roles_en
        dicoroles = dicoroles_en
        trad_roles = trad_roles_fr

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    in_game = data[gid]["in_game"]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    Lroles_dispo = gdata[aid]["Lroles"]
    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    is_compo = gdata[aid]["is_compo"]
    Lp = gdata[aid]["Lp"]
    game_started = gdata[aid]["game_started"]

    
    print("[{}] Commande .start {} exécutée par {}".format(datetime.now().strftime("%H:%M:%S"), state_couple, ctx.author))

    annoncef = []
    is_sect = False
    ecolour = discord.Color.red()

    if len(channels) == 0:
        channels_check = '❌'
    else:
        channels_check = '✅'

    if in_game == True:
        create_check = '✅'
    else:
        create_check = '❌'

    if len(dicop_id_to_emoji) == 0:
        ins_check = '❌'
    else:
        ins_check = '✅'

    if len(dicop_id_to_emoji) == len(Lroles_dispo):
        roles_check = '✅'
    else:
        roles_check = '❌'

    if state_couple == 'couple' or state_couple == 'non' or state_couple == 'lovers':
        c_check = '✅'
    else:
        c_check = '❌'

    if roles_check == '✅' and ins_check == '✅' and create_check == '✅' and channels_check == '✅' and c_check == '✅':
        ecolour = discord.Color.green()

    embed_check = discord.Embed(
        title = ldata["startEmbedVerificationTitle"],
        colour = ecolour
    )

    embed_check.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed_check.add_field(
        name = ldata["startEmbedVerificationName"],
        value = ldata["startEmbedVerificationValue"].format(channels_check, create_check, ins_check, roles_check, len(Lroles_dispo), len(dicop_id_to_emoji), c_check, state_couple),
        inline = False
    )

    print("ok")

    await ctx.channel.send(embed=embed_check)

    if roles_check == '✅' and ins_check == '✅' and create_check == '✅' and channels_check == '✅' and c_check == '✅' and game_started == False:
        
        print("ok")

        await channels[1].purge(limit=50)
        #On doit faire int parce que nbplayers est un string

        #Check si on a bien entrer le bon nombre de rôles

        author = str(ctx.author)

        channel = ctx.author.voice.channel
        members = channel.members

        members = [user for user in members if str(user) != author]
        #Enlève le MJ de la liste des joueurs

        start_time = time.time()


        await channels[1].purge(limit=50)
        await channels[2].purge(limit=50)
        

        print("Partie commencée")
        #ldata["startGameStarted"]
        await ctx.channel.send(ldata["startGameStarted"])

        if is_compo == False:
            await channels[1].send(ldata["startCompositionHidden"])
        else:
            await channels[1].send(ldata["startCompositionShow"])

            embedaf = discord.Embed(
                title = ldata["startEmbedRolesTitle"],
                colour = discord.Color.default()
            )
        
            Lroles_final = list(dict.fromkeys(Lroles_dispo))
            Laff = ["``{}`` ({}) \n".format(trad_roles[k], Lroles_dispo.count(k)) if k in trad_roles else "``{}`` ({}) \n".format(k, Lroles_dispo.count(k)) for k in Lroles_final]


            if state_couple == "couple" or state_couple == "Couple":
                Laff.append(ldata["startRandomCouple"])
            elif 'Cupidon' in Lroles_dispo:
                Laff.append(ldata["startCouple"])
        

            embedaf.add_field(
                name = ldata["startEmbedRolesName"],
                value = ''.join(Laff),
                inline = False
            )
            embedaf.set_author(
                name = "LG Bot",
                icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
            )

            print("ok")

            await channels[1].send(embed=embedaf)

        await ctx.channel.send(ldata["startStartingMessage"].format(author))

        Lroles_game = [k for k in Lroles_dispo]

        for member in members:
            
            if str(member) != str(author):

                print(Lroles_game)
                role_given = rdm.choice(Lroles_game)
                Lroles_game.remove(role_given)

                
                if role_given in trad_roles:
                    await ctx.channel.send(ldata["startPlayerHasRole"].format(member, trad_roles[role_given]))
                else:
                    await ctx.channel.send(ldata["startPlayerHasRole"].format(member, role_given))

                if role_given in dicoroles:
                    if role_given == "PF" or role_given == "Chaman" or role_given == "Jaloux" or role_given == "Oeil":
                        await channels[dicoroles[role_given]].set_permissions(member, overwrite=can_see)
                    else:
                        await channels[dicoroles[role_given]].set_permissions(member, overwrite=can_talk)

                    if role_given == "IPDL" or role_given == 'LGB':
                        await channels[8].set_permissions(member, overwrite=can_talk)
                
                embedr = discord.Embed(
                    title = "Disctribution des rôles",
                    colour = discord.Color.red()
                )

                try:
                    if role_given in trad_roles:
                        ename = ldata["startYourRoleIs"].format(trad_roles[role_given])
                        print("{} a le rôle {}".format(member, trad_roles[role_given]))

                    else:
                        ename = "Ton rôle est: __{}__".format(role_given)
                        print("{} a le rôle {}".format(member, role_given))

                    embedr.add_field(
                        name = ename,
                        value = "``{}``".format(desc_roles[role_given]),
                        inline = False
                    )

                    embedr.set_author(
                        name = str(member),
                        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(member)
                    )

                    await member.send(embed=embedr)

                except:
                    ctx.channel.send(ldata["startPlayerHasNotOpenDM"].format(member))

                annoncef.append(ldata["startPlayerHasRoleAnnounce"].format(member, dicop_id_to_emoji[str(member.id)], role_given))


                gdata[aid]["Lp"][str(member.id)] = [str(member), role_given, 'Non', 'Non', 'Non', 'Non', 'Non', 'Non', 'Non', 'Non', 'Non', dicop_id_to_emoji[str(member.id)], role_given]
                # 0: joueur # 1: rôle # 2: couple # 3: maitre/enfant # 4: charmé # 5: secte # 6: infecté # 7: imposteur # 8: rôle imposteur (LG) # 9: rôle traître # 10: peut voter # 11: emoji joueur # 12: role backup revive command

                if role_given == 'Sectaire' or role_given == 'Sectarian':
                    membersect = member

                if role_given == 'Traitre' or role_given == 'Traitor':
                    membertraitre = member

                if role_given == 'Imposteur' or role_given == 'Impostor':
                    memberimp = member


                print('Terminé {}'.format(member))


        if 'Traitre' in Lroles_dispo or 'Traitor' in Lroles_dispo:
            
            Lroles_traitre = [k for k in liste_roles if (k in liste_village and k not in Lroles_dispo)]
            print(Lroles_traitre)
            role_traitre = rdm.choice(Lroles_traitre)

            argr = role_traitre
            if role_traitre in trad_roles:
                argr = trad_roles[role_traitre]
            await membertraitre.send(ldata["startSendRoleTraitor"].format(argr))
            await ctx.channel.send(ldata["startTraitorRole"].format(membertraitre, argr))
            annoncef.append(ldata["startTraitorRoleAnnounce"].format(membertraitre, argr))

            if role_traitre in dicoroles:
                await channels[dicoroles[role_traitre]].set_permissions(member, overwrite=can_talk)

            gdata[aid]["Lp"][str(membertraitre.id)][9] = role_traitre


        if 'Imposteur' in Lroles_dispo or 'Impostor' in Lroles_dispo:

            Lroles_imp = [k for k in liste_roles if (k not in Lroles_dispo) or (k == 'Jaloux' and state_couple == 'couple')]

            Lrimp = rdm.sample(Lroles_imp, 2)
            role_imp1,role_imp2 = Lrimp[0],Lrimp[1]

            print(role_imp1,role_imp2)

            embed_panel = discord.Embed(
                colour = discord.Color.red()
            )

            print('création panel')

            dicoimp = {}
            dicoimp['🥇'] = role_imp1
            dicoimp['🥈'] = role_imp2

            arg1 = role_imp1
            arg2 = role_imp2
            if role_imp1 in trad_roles:
                arg1 = trad_roles[role_imp1]
            if role_imp2 in trad_roles:
                arg2 = trad_roles[role_imp2]

            embed_panel.set_author(name = ldata["startImpostorEmbedAuthor"])
            embed_panel.add_field(
                name =ldata["startImpostorEmbedName"],
                value = ldata["startImpostorEmbedValue"].format(arg1,arg2),
                inline = False)
            current_panel = await memberimp.send(embed=embed_panel)

            await current_panel.add_reaction('🥇')
            await current_panel.add_reaction('🥈')
            
            def checkImp(reaction, user):
                return (user == memberimp) and (str(reaction.emoji) == '🥇' or str(reaction.emoji) == '🥈') and (reaction.message.id == current_panel.id)

            try:
                reaction, user = await client.wait_for("reaction_add", check=checkImp, timeout=30.0)
                roleimp = dicoimp[reaction.emoji]
                argrole = roleimp
                if roleimp in trad_roles:
                    argrole = trad_roles[roleimp]
                await memberimp.send(ldata["startImposteurRoleChosen"].format(argrole))
            except asyncio.TimeoutError:
                roleimp = rdm.choice(list(dicoimp.values()))
                argrole = roleimp
                if roleimp in trad_roles:
                    argrole = trad_roles[roleimp]
                await memberimp.send(ldata["startImpostorRandomRole"].format(argrole))
            finally:
                await channels[0].send(ldata["startImposterRole"].format(roleimp))
                annoncef.append(ldata["startImposterRoleAnnounce"].format(memberimp, roleimp))
                if roleimp in dicoroles:
                    await channels[dicoroles[roleimp]].set_permissions(memberimp, overwrite=can_talk)
                    if roleimp in liste_LG:
                        gdata[aid]["Lp"][str(memberimp.id)][8] = 'LG'
                        if roleimp == 'LGB' or roleimp == 'Infect':
                            await channels[8].set_permissions(memberimp, overwrite=can_talk)
                await reaction.message.delete()


        if "Sectaire" in Lroles_dispo or 'Sectarian' in Lroles_dispo:
            Ltemps = [k for k in list(gdata[aid]["Lp"].keys()) if str(gdata[aid]["Lp"][k][1]) != 'Sectaire']
            pop_sect = int(nbp/2)
            sect = rdm.sample(Ltemps, pop_sect)
            for ids in sect:
                gdata[aid]["Lp"][ids][5] = "Secte"
            
            sect = [client.get_user(int(i)) for i in sect]

            await ctx.channel.send(ldata["startCultList"].format(', '.join(sect)))
            await membersect.send(ldata["startCultListPlayer"].format(', '.join(sect)))

            annoncef.append(ldata["startCultListAnnounce"].format(', '.join(sect)))


        if state_couple == 'couple' or state_couple == 'lovers':

            L = [k for k in members if str(k) != str(author) or str(gdata[aid]["Lp"][str(k.id)][1]) != 'Jaloux']
            
            i1 = rdm.randint(0,len(L)-1)
            if str(L[i1]) != author:
                amant1 = L[i1]
                gdata[aid]["Lp"][str(L[i1].id)][2] = 'Oui'
                L.pop(i1)

            i2 = rdm.randint(0,len(L)-1)
            if str(L[i2]) != author:
                amant2 = L[i2]
                gdata[aid]["Lp"][str(L[i2].id)][2] = 'Oui'
                L.pop(i2)

            await channels[6].set_permissions(amant1, overwrite=can_see)
            await channels[6].set_permissions(amant2, overwrite=can_see)
            await amant1.send(ldata["startLover"].format(amant2))
            await amant2.send(ldata["startLover"].format(amant1))
            print("Amant 1: {}, Amant 2: {}".format(amant1,amant2))
            await ctx.channel.send(ldata["startLovers"].format(amant1,amant2))

            annoncef.append(ldata["startLoversAnnounce"].format(amant1, amant2))


        embed = discord.Embed(
            colour = discord.Color.gold(),
            title = ldata["startEmbedEndTitle"]
        )
        embed.add_field(
            name = ldata["startEmbedEndName"],
            value = ''.join(annoncef),
            inline = False
        )
        embed.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )
        
        await ctx.channel.send("Lancement de la partie terminé.")
        await ctx.channel.send(embed=embed)

        gdata[aid]["game_started"] = True

        with open('data/games.json', 'w', encoding='utf-8') as f:
            json.dump(gdata, f, indent=4, ensure_ascii=False)

        await menu(ctx)

    
    else:

        embede = discord.Embed(
            colour = discord.Color.default(),
            title = ldata["startEmbedErrorTitle"]
        )

        embede.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )

        embede.add_field(
            name =ldata["startEmbedErrorName"], 
            value = ldata["startEmbedErrorValue"], 
            inline = False)

        await ctx.channel.send(embed=embede)


@client.command()
@commands.has_any_role("LG Host")
async def fmenu(ctx):
    await menu(ctx)

# Commande pour forcer l'apparition du menu en cas de bug

async def menu(ctx):

    print("ok")

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)
    
    aid = str(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    game_started = gdata[aid]["game_started"]
    day = gdata[aid]["day"]
    Lroles_dispo = gdata[aid]["Lroles"]

    panel = discord.Embed(
            colour = discord.Color.green()
        ) 
    
    print("ok")

    emojis_action = ["🐺", "🔪", "👒", "🔇", "🔊", "🌙", "🧒", "❤️", "💤", "🕵️", "🎺", "🌞","🛑","📔"]

    if game_started == False:    # ATTENTION NE PAS OUBLIER DE CHANGER EN FALSE

        await ctx.channel.send(ldata["menuGameHasNotStarted"])

    else:

        print("ok")

        if day == True:
            panel.set_author(
                name=ldata["menuPanelAuthorDay"]
            )
            panel.add_field(
                name=ldata["menuPanelKillName"],
                value=ldata["menuPanelKillNValue"],
                inline=False
            )
            if 'IPDL' in Lroles_dispo:
                panel.add_field(
                    name=ldata["menuPanelInfectName"],
                    value=ldata["menuPanelInfectValue"],
                    inline=False
                )

            if 'Servante' in Lroles_dispo:
                panel.add_field(
                    name=ldata["menuPanelServanteName"],
                    value=ldata["menuPanelServanteValue"],
                    inline=False
                )

            panel.add_field(
                name=ldata["menuPanelMuteName"],
                value=ldata["menuPanelMuteValue"],
                inline=False
            )

            panel.add_field(
                name=ldata["menuPanelUnmuteName"],
                value=ldata["menuPanelUnmuteValue"],
                inline=False
            )

            panel.add_field(
                name=ldata["menuPanelNightName"],
                value=ldata["menuPanelNightValue"],
                inline=False
            )

            panel.add_field(
                name=ldata["menuPanelVoteName"],
                value=ldata["menuPanelVoteValue"],
                inline=False
            )

            panel.add_field(
                name=ldata["menuPanelResetName"],
                value=ldata["menuPanelResetValue"],
                inline=False
            )

            msg = await ctx.channel.send(embed=panel)

            await msg.add_reaction("🔪")
            if 'IPDL' in Lroles_dispo:
                await msg.add_reaction("🐺")
            if 'Servante' in Lroles_dispo:
                await msg.add_reaction("👒")
            await msg.add_reaction("🔇")
            await msg.add_reaction("🔊")
            await msg.add_reaction("🌙")
            await msg.add_reaction("📔")
            await msg.add_reaction("🛑")

        
        else:
            panel.set_author(
                name=ldata["menuPanelAuthorNight"]
            )
            if 'Enfant' in Lroles_dispo:
                panel.add_field(
                    name=ldata["menuPanelEnfantName"],
                    value=ldata["menuPanelEnfantValue"],
                    inline=False
                )
            if 'Cupidon' in Lroles_dispo:    
                panel.add_field(
                    name=ldata["menuPanelCupiName"],
                    value=ldata["menuPanelCupiValue"],
                    inline=False
                )
            if 'Noctambule' in Lroles_dispo: 
                panel.add_field(
                    name=ldata["menuPanelNoctName"],
                    value=ldata["menuPanelNoctValue"],
                    inline=False
                )
            if 'Voleur' in Lroles_dispo:
                panel.add_field(
                    name=ldata["menuPanelVoleurName"],
                    value=ldata["menuPanelVoleurValue"],
                    inline=False
                )
            if 'JDF' in Lroles_dispo:
                panel.add_field(
                    name=ldata["menuPanelJDFName"],
                    value=ldata["menuPanelJDFValue"],
                    inline=False
                )

            panel.add_field(
                name=ldata["menuPanelDayName"],
                value=ldata["menuPanelDayValue"],
                inline=False
            )

            msg = await ctx.channel.send(embed=panel)


            if 'Enfant' in Lroles_dispo:
                await msg.add_reaction("🧒")
            if 'Cupidon' in Lroles_dispo:
                await msg.add_reaction("❤️")
            if 'Noctambule' in Lroles_dispo:
                await msg.add_reaction("💤")
            if 'Voleur' in Lroles_dispo:
                await msg.add_reaction("🕵️")
            if 'JDF' in Lroles_dispo:
                await msg.add_reaction("🎺")
            await msg.add_reaction("🌞")

        def checkMenu(reaction, user):
            return (user == mdj) and (reaction.message.id == msg.id) and (str(reaction.emoji) in emojis_action)
        
        reaction, user = await client.wait_for("reaction_add", check=checkMenu)
        await reaction.message.delete()

        d = {"🧒": 'Enfant', "🕵️": 'Voleur', "🐺": 'Infect', "👒": 'Servante', "💤": 'Noctambule', "🔪": 'Kill'}


        if reaction.emoji == "❤️":
            await cupidon_panel(reaction.message)
        
        elif reaction.emoji == "🎺":
            await charm_panel(reaction.message)
        
        elif reaction.emoji in d:
            await action_panel(reaction.message, d[reaction.emoji])

        elif reaction.emoji == "🔇":
            await mute(reaction.message, "mute")

        elif reaction.emoji == "🔊":
            await mute(reaction.message, "unmute")

        elif reaction.emoji == "🌙":
            await jour(reaction.message, "nuit")

        elif reaction.emoji == "🌞":
            await jour(reaction.message, "jour")

        elif reaction.emoji == "🛑":
            await reset_panel(reaction.message)

        elif reaction.emoji == "📔":
            await vote_panel(reaction.message)


async def jour(ctx, dtime):

    channel = author.voice.channel
    members = channel.members

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    game_started = gdata[aid]["game_started"]
    cpt_jour = gdata[aid]["cpt_jour"]
    day = gdata[aid]["day"]
    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    Lp = gdata[aid]["Lp"]

    is_cover = False
    is_devin = False


    if game_started == True:

        if dtime == 'nuit':

            if day == True:

                gdata[aid]["cpt_jour"] += 1
                gdata[aid]["day"] = False
         
                for memberid in dicop_id_to_emoji:

                    member = client.get_user(int(memberid))

                    await member.edit(mute=True)
                    await channels[2].set_permissions(member, overwrite=can_see) 

                    rol = Lp[str(memberid)][1]
                    statusc = Lp[str(memberid)][2]
                    status_infect = Lp[str(memberid)][8]
                    status_impost = Lp[str(memberid)][9]
                    
                    if rol == 'LG' or rol == 'LGB' or rol == 'IPDL' or rol == 'LGA' or (rol == 'Enfant' and is_enfant == True) or status_infect == 'Infecté' or (rol == 'Imposteur' and status_impost == 'LG'):
                        await channels[8].set_permissions(member, overwrite=can_talk)
                        print("{} OK a été demute de LG".format(str(member)))
                    if statusc == 'Oui':
                        await channels[6].set_permissions(member, overwrite=can_see)
                        print("{} OK a été mute de couple".format(str(member)))

                while is_cover == False:
                    if 'LGA' in Lroles_dispo:
                        imember = rdm.choice(list(dicop_id_to_emoji.keys()))
                        await channels[8].send(ldata["jourCoverLGA"].format(Lp[imember][1]))
                        await channels[0].send(ldata["jourCoverLGA"].format(Lp[imember][1]))
                        if cpt_jour == 1 and 'Oeil' in Lroles_dispo:
                            await channels[23].send(ldata["jourCoverLGA"].format(Lp[imember][1]))
                        is_cover = True
                    else:
                        is_cover = True 
                

                while is_devin == False:
                    if "Devin" in Lroles_dispo:
                        imember = rdm.choice(list(dicop_id_to_emoji.keys()))
                        if Lp[imember][1] == 'Devin':
                            pass
                        else:
                            await channels[29].send(ldata["jourGuessDevin"].format(str(imember)))
                            await channels[0].send(ldata["jourGuessDevin2"].format(str(imember),Lp[imember][1]))
                            if cpt_jour == 1 and 'Oeil' in Lroles_dispo:
                                await channels[23].send(ldata["jourGuessDevin3"].format(str(imember)))
                            is_devin = True
                    else:
                        break
                
                embedn = discord.Embed(
                    title = ldata["jourEmbedSleepTitle"],
                    description = ldata["jourEmbedSleepDesc"].format(cpt_jour),
                    colour = discord.Color.dark_blue()
                )

                embedn.set_author(
                    name = "LG Bot",
                    icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                )

                await channels[2].send(embed=embedn)
                Laffichage_day = [ldata["jourAffichage"].format(client.get_user(int(idm)), dicop_id_to_emoji[idm], Lp[idm][1]) for idm in dicop_id_to_emoji]

                embed = discord.Embed(
                    title = ldata["jourEmbedInfoTitle"],
                    colour = discord.Color.gold()
                )

                embed.add_field(
                    name = ldata["jourEmbedInfoName"],
                    value = ''.join(Laffichage_day),
                    inline = False
                )
                embed.set_author(
                    name = "LG Bot",
                    icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                )

                await channels[0].send(embed=embed)


        if dtime == 'jour':
            if day == False:
 
                gdata[aid]["day"] = True
                
                for memberid in dicop_id_to_emoji:

                    member = client.get_user(int(memberid))

                    await member.edit(mute=False)
                    await channels[2].set_permissions(member, overwrite=can_talk)

                    rol = Lp[str(memberid)][1]
                    statusc = Lp[str(memberid)][2]
                    status_infect = Lp[str(memberid)][8]
                    status_impost = Lp[str(memberid)][9]

                    check_LG = False
                    if rol == 'LG' or rol == 'LGB' or rol == 'IPDL' or rol == 'LGA' or (rol == 'Enfant' and is_enfant == True) or status_infect == 'Infecté' or (rol == 'Imposteur' and status_impost == 'LG'):
                        check_LG = True

                    if check_LG == True:
                        await channels[8].set_permissions(member, overwrite=can_see)
                        print("{} OK a été mute de LG".format(str(member)))
                    if rol == 'LGB' or rol == 'IPDL':
                        await channels[dicoroles[rol]].set_permissions(member, overwrite=can_talk)
                        print("{} OK a été demute de LGB/IPDL (cas où noctambule)".format(str(member)))
                    else: 
                        if rol in dicoroles and check_LG == False:
                            if rol == "PF" or rol == "Chaman" or rol == "Jaloux" or rol == "Oeil":
                                await channels[dicoroles[rol]].set_permissions(member, overwrite=can_see)
                            else:
                                await channels[dicoroles[rol]].set_permissions(member, overwrite=can_talk)
                            print("{} OK a été demute de {} (cas où noctambule)".format(member, channels[dicoroles[rol]]))

                    if statusc == 'Oui':
                        await channels[6].set_permissions(member, overwrite=can_talk)
                        print("{} OK a été demute de couple".format(str(member)))


                embedj = discord.Embed(
                    title = ldata["jourEmbedWakeUpTitle"],
                    description = ldata["jourEmbedWakeUpDesc"].format(cpt_jour),
                    colour = discord.Color.dark_gold()
                )

                embedj.set_author(
                    name = "LG Bot",
                    icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                )

                await channels[2].send(embed=embedj)

                Laffichage_day = [ldata["jourAffichage"].format(client.get_user(int(idm)), dicop_id_to_emoji[idm], Lp[idm][1]) for idm in dicop_id_to_emoji]

                embed = discord.Embed(
                    title = ldata["jourEmbedInfoTitle"],
                    colour = discord.Color.gold()
                )

                embed.add_field(
                    name = ldata["jourEmbedInfoName"],
                    value = ''.join(Laffichage_day),
                    inline = False
                )
                embed.set_author(
                    name = "LG Bot",
                    icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                )

                await channels[0].send(embed=embed)

    with open('data/games.json', 'w', encoding='utf-8') as f:
        json.dump(gdata, f, indent=4, ensure_ascii=False)

    await menu(ctx)


async def action_panel(ctx, action):
    # Actions: Enfant, Voleur, Infect, Kill, Noctambule, Servante

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    dicop_emoji = gdata[aid]["dictemoji"]

    d = ldata["actionPanelRolesDecs"]

    embed_panel = discord.Embed(
        colour = discord.Color.green()
    )

    embed_panel.set_author(
        name = ldata["actionPanelAuthor"].format(action),
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed_panel.add_field(
        name =ldata["actionPanelName"], 
        value = ldata["actionPanelValue"].format(d[action]), 
        inline = False
    )

    panel = await ctx.channel.send(embed=embed_panel)

    print(action)

    for nameid in dicop_id_to_emoji:
        name = client.get_user(int(nameid))
        print(name)
        fiche_player = Lp[nameid]
        print(fiche_player[1])
        if action == 'Enfant' and str(fiche_player[1]) == 'Enfant':
            print("ok e")
            n_enfant = nameid
        elif action == 'Voleur' and str(fiche_player[1]) == 'Voleur':
            n_voleur = nameid
        elif (action == 'Infect') and (str(fiche_player[1]) == 'LG' or str(fiche_player[1]) == 'LGA' or str(fiche_player[1]) == 'LGB' or str(fiche_player[1]) == 'IPDL' or str(fiche_player[1]) == 'GML' or fiche_player[9] == 'Infecté' or (str(fiche_player[1]) == 'Enfant' and is_enfant == True)):
            pass
        elif (action == "Noctambule") and (str(fiche_player[1]) == 'Noctambule' or fiche_player[8] == 'Noctambule' or fiche_player[9] == 'Noctambule'):
            n_noctambule = nameid
        elif (action == 'Servante') and (str(fiche_player[1]) == 'Servante' or fiche_player[8] == 'Servante' or fiche_player[9] == 'Servante'):
            n_servante = nameid
        else:
            print("ok")
            await panel.add_reaction(dicop_id_to_emoji[nameid])
    await panel.add_reaction("❌")


    def check(reaction, user):
        return (user == mdj) and ((str(reaction.emoji) in dicop_emoji) or str(reaction.emoji) == non) and (reaction.message.id == panel.id)

    try:
        reaction, user = await client.wait_for("reaction_add", check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.channel.send(ldata["actionPanelTimedOut"])
        await panel.delete()
        await menu(ctx)
    else:
        if str(reaction.emoji) == non:
            await ctx.channel.send(ldata["actionPanelCommandCancelled"])
            await reaction.message.delete()
            await menu(ctx)
        else:
            if action == 'Enfant':
                await enfant_action(reaction.message, str(dicop_emoji[reaction.emoji]), n_enfant, auth)
            elif action == 'Voleur':
                await voleur_action(reaction.message, str(dicop_emoji[reaction.emoji]), n_voleur, 'Voleur', auth)
            elif action == 'Infect':
                await infect_action(reaction.message, str(dicop_emoji[reaction.emoji]), auth)
            elif action == 'Kill':
                await kill_action(reaction.message, str(dicop_emoji[reaction.emoji]), 'Kill', auth)
            elif action == 'Noctambule':
                await noctambule_action(reaction.message, str(dicop_emoji[reaction.emoji]), n_noctambule, auth)
            elif action == 'Servante':
                await voleur_action(reaction.message, str(dicop_emoji[reaction.emoji]), n_servante, 'Servante', auth)
                await kill_action(reaction.message, str(dicop_emoji[reaction.emoji]), 'Servante', auth)


async def cupidon_panel(ctx):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    dicop_emoji = gdata[aid]["dictemoji"]

    lc = []

    embed_panel = discord.Embed(
        colour = discord.Color.from_rgb(255,0,70)
    )

    embed_panel.set_author(
        name = ldata["cupidonPanelAuthor"],
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed_panel.add_field(
        name =ldata["actionPanelName"], 
        value = ldata["cupidonPanelValue"], 
        inline = False
    )

    await ctx.channel.send("Veuillez choisir le 1e amant")
    current_panel = await ctx.channel.send(embed=embed_panel)

    for nameid in dicop_id_to_emoji:
        await current_panel.add_reaction(dicop_id_to_emoji[nameid])
    await current_panel.add_reaction("❌")

    def checkCupi(reaction, user):
        return (user == mdj) and ((str(reaction.emoji) in dicop_emoji) or str(reaction.emoji) == non) and (reaction.message.id == current_panel.id)

    try:
        reaction, user = await client.wait_for("reaction_add", check=checkCupi, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.channel.send(ldata["actionPanelTimedOut"])
        await current_panel.delete()
        await menu(ctx)
    else:
        if str(reaction.emoji) == non:
            await ctx.channel.send(ldata["actionPanelCommandCancelled"])
            await reaction.message.delete()
            await menu(ctx)
        else:
            lc.append(dicop_emoji[reaction.emoji])
            reaction.message.delete()
            await ctx.channel.send(ldata["cupidonPanelChoose2ndLover"])
            panel2 = await ctx.channel.send(embed=embed_panel)
            for nameid in dicop_id_to_emoji:
                if nameid not in lc:
                    await panel2.add_reaction(dicop_id_to_emoji[nameid])

            def checkCupi2(reaction, user):
                return (user == mdj) and ((str(reaction.emoji) in dicop_emoji) or str(reaction.emoji) == non) and (reaction.message.id == panel2.id)

            try:
                reaction, user = await client.wait_for("reaction_add", check=checkCupi2, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.channel.send(ldata["actionPanelTimedOut"])
                await panel2.delete()
                await menu(ctx)
            else:
                lc.append(dicop_emoji[reaction.emoji])
                await cupidon_action(reaction.message, lc)



async def cupidon_action(ctx, liste_couple):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    dicop_emoji = gdata[aid]["dictemoji"]
    Lp = gdata[aid]["Lp"]

    cpl1 = liste_couple[0]
    cpl2 = liste_couple[1]

    gdata[aid]["Lp"][str(cpl1)][2] = 'Couple'
    gdata[aid]["Lp"][str(cpl2)][2] = 'Couple'

    await channels[6].set_permissions(cpl1, overwrite=can_see)
    await channels[6].set_permissions(cpl2, overwrite=can_see)
    await client.get_user(cpl1).send(ldata["cupidonDMLovers"].format(cpl2))
    await client.get_user(cpl2).send(ldata["cupidonDMLovers"].format(cpl1))
    await ctx.channel.send(ldata["cupidonLoversList"].format(cpl1,cpl2))
    await ctx.delete()

    with open('data/games.json', 'w', encoding='utf-8') as f:
        json.dump(gdata, f, indent=4, ensure_ascii=False)
    await menu(ctx)


async def enfant_action(ctx, maitreid, enfantid):

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    Lp = gdata[aid]["Lp"]

    gdata[aid]["Lp"][maitreid][3] = 'Maitre'
    gdata[aid]["Lp"][enfantid][3] = 'Enfant'

    await ctx.channel.send(ldata["enfantMaster"].format(client.get_user(int(maitreid)), client.get_user(int(enfantid))))
    await ctx.delete()

    with open('data/games.json', 'w', encoding='utf-8') as jf:
        json.dump(gdata, jf, indent=4, ensure_ascii=False)

    await menu(ctx)


async def voleur_action(ctx, stolenid, voleurid, step):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    if lang == 'french':
        dicoroles = dicoroles_fr
    elif lang == 'english':
        dicoroles = dicoroles_en

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    Lp = gdata[aid]["Lp"]

    fiche_stolen = Lp[stolenid]
    role_stolen = fiche_stolen[1]

    fiche_voleur = Lp[voleurid]
    role_voleur = fiche_voleur[1]

    gdata[aid]["Lp"][stolenid][1],gdata[aid]["Lp"][voleurid][1] = role_voleur,role_stolen

    if role_stolen == 'Enfant':
        gdata[aid]["Lp"][voleurid][3] = 'Enfant'
        gdata[aid]["Lp"][stolenid][3] = 'Non'

    voleur_name = client.get_user(int(voleurid))
    stolen_name = client.get_user(int(stolenid))

    if role_stolen in dicoroles:
        print(role_stolen, "voleur dicoroles")
        await channels[dicoroles[role_stolen]].set_permissions(voleur_name, overwrite=can_talk)
        await channels[dicoroles[role_stolen]].set_permissions(stolen_name, overwrite=cant_talk)
        if role_stolen == 'LGB' or role_stolen == 'IPDL' or (role_stolen == 'Enfant' and is_enfant == True) or fiche_stolen[9] == 'Infecté':
            await channels[8].set_permissions(stolen_name, overwrite=cant_talk)
            await channels[8].set_permissions(voleur_name, overwrite=can_talk)
    await channels[dicoroles[role_voleur]].set_permissions(voleur_name, overwrite=cant_talk)
    await channels[dicoroles[role_voleur]].set_permissions(stolen_name, overwrite=can_talk)

    await stolen_name.send(ldata["voleurVoleur"])
    await voleur_name.send(ldata["voleurStolen"].format(str(role_stolen)))
    await ctx.channel.send(ldata["voleurSummary"].format(str(voleur_name),str(stolen_name),str(role_stolen)))
    await ctx.delete()

    with open('data/games.json', 'w', encoding='utf-8') as jf:
        json.dump(gdata, jf, indent=4, ensure_ascii=False)

    if step == 'Voleur':
        await menu(ctx)


async def infect_action(ctx, infectid):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    Lp = gdata[aid]["Lp"]
    day = gdata[aid]["day"]

    infect_name = client.get_user("infectid")

    if day == True:
        await channels[8].set_permissions(infect_name, overwrite=can_see)
    elif day == False:
        await channels[8].set_permissions(infect_name, overwrite=can_talk)

    gdata[aid]["Lp"][infectid][6] = 'Infecté'

    await infect_name.send(ldata["infectInfect"])
    await ctx.channel.send(ldata["infectSummary"].format(str(infect_name)))
    await ctx.delete()

    with open('data/games.json', 'w', encoding='utf-8') as jf:
        json.dump(gdata, jf, indent=4, ensure_ascii=False)

    await menu(ctx)


async def charm_panel(ctx):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    Lp = gdata[aid]["Lp"]
    dicop_id_to_emoji = gdata[aid]["idtoemoji"]

    lc = []

    embed_panel = discord.Embed(
        colour = discord.Color.from_rgb(255,30,100)
    )

    embed_panel.set_author(
        name = ldata["charmPanelAuthor"],
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed_panel.add_field(
        name =ldata["actionPanelName"], 
        value = ldata["charmPanelValue"], 
        inline = False
    )

    current_panel = await ctx.channel.send(embed=embed_panel)

    for nameid in dicop_id_to_emoji:
        fiche_player = Lp[nameid]
        if str(fiche_player[1]) == 'JDF' or fiche_player[4] == 'Charmé':
            pass      
        else:
            await current_panel.add_reaction(dicop_id_to_emoji[nameid])
    await current_panel.add_reaction("❌")

    def checkCharm(reaction, user):
        return (user == mdj) and ((str(reaction.emoji) in dicop_emoji) or str(reaction.emoji) == non) and (reaction.message.id == current_panel.id)

    try:
        reaction, user = await client.wait_for("reaction_add", check=checkCharm, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.channel.send(ldata["actionPanelTimedOut"])
        await current_panel.delete()
        await menu(ctx)
    else:
        if str(reaction.emoji) == non:
            await ctx.channel.send(ldata["actionPanelCommandCancelled"])
            await reaction.message.delete()
            await menu(ctx)
        else:
            lc.append(dicop_emoji[reaction.emoji])
            await reaction.message.delete()
            await ctx.channel.send(ldata["charmPanelOnlyOne"])
            panel2 = await ctx.channel.send(embed=embed_panel)
            for nameid in dicop_id_to_emoji:
                fiche_player = Lp[nameid]
                if str(fiche_player[1]) == 'JDF' or fiche_player[4] == 'Charmé':
                    pass  
                elif int(nameid) in lc:
                    pass
                else:
                    await panel2.add_reaction(dicop_id_to_emoji[nameid])
            await panel2.add_reaction("❌")

            def checkCharm2(reaction, user):
                return (user == mdj) and ((str(reaction.emoji) in dicop_emoji) or str(reaction.emoji) == non) and (reaction.message.id == panel2.id)

            try:
                reaction, user = await client.wait_for("reaction_add", check=checkCharm2, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.channel.send(ldata["actionPanelTimedOut"])
                await panel2.delete()
                await menu(ctx)
            else:
                if reaction.emoji in dicop_emoji:
                    lc.append(dicop_emoji[reaction.emoji])
                await charm_action(reaction.message, lc)


async def charm_action(ctx, liste_charm):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    Lp = gdata[aid]["Lp"]

    for memberid in liste_charm:
        gdata[aid]["Lp"][str(memberid)][4] = 'Charmé'
        await channels[4].set_permissions(member, overwrite=can_see)
        await member.send(ldata["charmTarget"])
        await ctx.channel.send(ldata["charmSummary"].format(str(member)))

    await ctx.delete()
    with open('data/games.json', 'w', encoding='utf-8') as jf:
        json.dump(gdata, jf, indent=4, ensure_ascii=False)
    await menu(ctx)


async def kill_action(ctx, killedid, step):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    if lang == 'french':
        dicoroles = dicoroles_fr
        trad_roles = trad_roles_fr
    elif lang == 'english':
        dicoroles = dicoroles_en
        trad_roles = trad_roles_en

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    Lp = gdata[aid]["Lp"]
    ancien_dead = gdata[aid]["ancien_dead"]
    is_enfant = gdata[aid]["is_enfant"]
    check_couple = gdata[aid]["check_couple"]

    channel = mdj.voice.channel
    members = channel.members

    members = [k for k in members if str(k) != str(author)]

    killed_name = client.get_user(int(killedid))

    pla = Lp[killedid]
    rolep = pla[1]
    status_couple = pla[2]
    status_maitre = pla[3]
    status_infect = pla[6]
    status_impost = pla[8]

    member = killed_name
    
    if rolep == 'Ancien' and ancien_dead == False:
        gdata[aid]["ancien_dead"] = True
        await ctx.channel.send(ldata["killAncienKill"])

    else:
        try:
            print("{0.name} couple: {1}".format(member,status_couple))
            print("{0.name} enfant/maitre: {1}".format(member,status_maitre))
        except:
            pass
        
        if rolep in dicoroles:
            await channels[dicoroles[rolep]].set_permissions(member, overwrite=cant_talk)
            print('OK dicoroles')

        if rolep == "IPDL" or rolep == 'LGB':
            await channels[8].set_permissions(member, overwrite=cant_talk)
            print('OK LGB/IPDL')

        if rolep == 'Enfant' and is_enfant == True:
            await channels[8].set_permissions(member, overwrite=cant_talk)
            print('OK Enfant')

        if status_couple == 'Oui':
            await ctx.channel.send(ldata["killDoNotForget"])  
            await channels[6].set_permissions(member, overwrite=cant_talk)  
            gdata[aid]["check_couple"] = False

        if status_infect == 'Infecté':
            await channels[8].set_permissions(member, overwrite=cant_talk)
            print("OK infect")

        if status_impost == 'LG':
            await channels[8].set_permissions(member, overwrite=cant_talk)
            print ('OK Impost LG')

        if status_maitre == 'Maitre' and is_enfant == False:
            print("OK Maitre")
            gdata[aid]["is_enfant"] = True
            for memberenf in members:
                pla_en = Lp[str(memberenf.id)]
                status_enfant = pla_en[5]
                print(memberenf, pla_en)
                if status_enfant == 'Enfant':
                    await channels[8].set_permissions(memberenf, overwrite=can_talk)
                    await channels[26].set_permissions(memberenf, overwrite=cant_talk)
                    await ctx.channel.send(ldata["killIsNowLG"].format(memberenf))
                    break

        await channels[3].set_permissions(member, overwrite=can_talk)
        await channels[2].set_permissions(member, overwrite=can_see)

        embed = discord.Embed(
            colour = discord.Color.default(),
            title = ldata["killDeadTitle"]
        )

        embed.set_thumbnail(
            url = member.avatar_url
        )

        embed.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )

        if rolep in trad_roles:
            evalue = ldata["killDeadRole"].format(trad_roles[rolep])

        else:
            evalue = ldata["killDeadRole"].format(rolep)

        embed.add_field(
            name = ldata["killDeadName"].format(member),
            value = evalue,
            inline = False
        )

        await channels[2].send(embed=embed)
        await ctx.channel.send(embed=embed)

        try:
            await member.edit(mute=True)
        except: 
            pass

        gdata[aid]["Lp"][str(member.id)][1] = 'Mort'
        del gdata[aid]["dictemoji"][dicop_id_to_emoji[str(member.id)]]
        del gdata[aid]["idtoemoji"][str(member.id)]
        

        print('OK {} est mort, il était {}'.format(str(member), rolep))

        if is_compo == True:
            
            gdata[aid]["Lroles"] = [k for k in Lroles_dispo if str(k) != str(rolep)]

            await channels[1].purge(limit=50)          
            
            embedaf = discord.Embed(
                colour = discord.Color.default(),
                title = ldata["killInfoGame"]
            )

            Lroles_final = list(dict.fromkeys(Lroles_dispo))
            Laff = ["``{}`` ({}) \n".format(trad_roles[k], Lroles_dispo.count(k)) if k in trad_roles else "``{}`` ({}) \n".format(k, Lroles_dispo.count(k)) for k in Lroles_final]

            if check_couple == True:
                await Laff.append(ldata["killCouple"])
            
            embedaf.add_field(
                name = ldata["killEmbedName"],
                value = ''.join(Laff),
                inline = False
            )

            embedaf.set_author(
                name = "LG Bot",
                icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
            )

            await channels[1].send(embed=embedaf)
    
        else:
            gdata[aid]["Lroles"] = [k for k in Lroles_dispo if str(k) != str(rolep)]

    await ctx.delete()

    with open('data/games.json', 'w', encoding='utf-8') as jf:
        json.dump(gdata, jf, indent=4, ensure_ascii=False)

    await menu(ctx)


@client.command()
async def revive(ctx, pid):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    try:
        temp = int(pid)
    except ValueError:
        await ctx.channel.send(ldata["reviveValueError"])
    else:

        channels = [client.get_channel(k) for k in data[gid]["channels"]]
        aid = str(data[gid]["mdj"])
        mdj = client.get_user(data[gid]["mdj"])

        with open('data/games.json', encoding='utf-8') as gf:
            gdata = json.load(gf)

        Lp = gdata[aid]["Lp"]
        Lroles_dispo = gdata[aid]["Lroles"]

        if pid in list(Lp):

            if gdata[aid]["Lp"][str(member.id)][1] == 'Mort':

                gdata[aid]["Lp"][str(member.id)][1] = gdata[aid]["Lp"][str(member.id)][12]
                gdata[aid]["idtoemoji"][str(member.id)] = gdata[aid]["Lp"][str(member.id)][11]
                gdata[aid]["dictemoji"][gdata[aid]["Lp"][str(member.id)][11]] = str(member.id)
                gdata[aid]["Lroles"].append(gdata[aid]["Lp"][str(member.id)][12])

                with open("games.json", 'w', encoding='utf-8') as jf:
                    json.dump(gdata, jf, ensure_ascii=False)

                await ctx.channel.send(ldata["reviveSucceeded"].format(client.get_user(int(pid))))
            
            else:
                await ctx.channel.send(ldata["reviveNotDead"])

        else:
            await ctx.channel.send(ldata["reviveIDNotValid"])


async def noctambule_action(ctx, victimeid, noctambuleid):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    Lp = gdata[aid]['Lp']
    is_enfant = gdata[aid]["is_enfant"]

    victime_name = client.get_user(int(victimeid))
    noctambule_name = client.get_user(int(noctambuleid))

    member = victime_name

    print("{} couple: {}".format(str(member),Lp[victimeid][4]))
    print("{} enfant/maitre: {}".format(str(member),Lp[victimeid][5]))
    
    if Lp[victimeid][1] in dicoroles:
        await channels[dicoroles[Lp[victimeid][1]]].set_permissions(member, overwrite=cant_talk)
        print('OK dicoroles')
    if Lp[victimeid][1] == "IPDL" or Lp[victimeid][1] == 'LGB' or (Lp[victimeid][1] == 'Enfant' and is_enfant == True) or Lp[victimeid][6] == 'Infecté' or Lp[victimeid][8] == 'LG':
        await channels[8].set_permissions(member, overwrite=cant_talk)
        print('OK LG')

    await victime_name.send(ldata["noctambuleVictim"].format(noctambule_name))
    await ctx.channel.send(ldata["noctambuleSummary"].format(victime_name, Lp[victimeid][1], noctambule_name))
    await ctx.delete()

    with open('data/games.json', 'w', encoding='utf-8') as jf:
        json.dump(gdata, jf, indent=4, ensure_ascii=False)

    await menu(ctx)


async def vote_panel(ctx):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    channel = author.voice.channel
    members = [member for member in channel.members if member is not author and str(Lp[str(member.id)][1]) != 'Mort']

    for member in members:
        try:
            await member.send(ldata["voteWillStart"])
        except:
            await ctx.channel.send(ldata["voteCanNotBeSend"].format(member))


    embed = discord.Embed(
        colour = discord.Color.green()
    )

    embed.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed.add_field(
        name = ldata["votePanelName"],
        value = ldata["votePanelValue"],
        inline = False
    )

    embed_vote = await ctx.channel.send(embed=embed)

    await embed_vote.add_reaction('⏱️')
    await embed_vote.add_reaction('✅')
    await embed_vote.add_reaction('❌')

    # A finir


async def mute(ctx, state):

    try:
        gid = str(ctx.guild.id)

        with open('data/guilds.json', encoding='utf-8') as f:
            data = json.load(f)

        lang = data[gid]["language"]
        with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
            ldata = json.load(lf)

        aid = str(data[gid]["mdj"])
        mdj = client.get_user(data[gid]["mdj"])

        channel = author.voice.channel
        members = channel.members

        for member in members:
            if str(member) == str(author):
                pass
            else:
                if state == 'mute':
                    await member.edit(mute=True)
                elif state == 'unmute':
                    await member.edit(mute=False)

        await menu(ctx)
    except:
        pass


@client.command()
async def purge(ctx, limit):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    if ctx.author.guild_permissions.administrator:

        await ctx.channel.purge(limit=int(limit))

    else:
        await ctx.channel.send(ldata["errorPermissionMissing"])

@client.command()
async def crypt(ctx, pourcentage):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    if ctx.author.guild_permissions.administrator:

        channels = [client.get_channel(k) for k in data[gid]["channels"]]
        aid = str(data[gid]["mdj"])
        mdj = client.get_user(data[gid]["mdj"])

        embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande crypt"
        )
        
        embed.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )


        if int(pourcentage) > 100:

            embed.add_field(
                name ='.crypt <value>', 
                value = ldata["cryptEmbedValue"], 
                inline = False
            )

        
            await ctx.send(embed=embed)

        else:
            data[gid]["valuepf"] = int(pourcentage)
            await ctx.channel.send(ldata["cryptChanged"].format(data[gid]["valuepf"]))

            with open("data/guilds.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False )

    else:
        await ctx.channel.send(ldata["errorPermissionMissing"])

@client.command()
async def breport(ctx, *, bug):

    with open('data/guilds.json', encoding='utf-8') as f:
        gdata = json.load(f)

    lang = gdata[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    with open("data/blocklist.json", encoding='utf-8') as f:
        data = json.load(f)

    if str(ctx.author.id) in data:
        await ctx.author.send(ldata["reportBanned"])
    
    else:
    
        embed = discord.Embed(
            title = "Bug report",
            colour = discord.Color.from_rgb(0,0,100)
        )

        embed.set_author(
            name = str(ctx.author),
            icon_url = ctx.author.avatar_url
        )

        embed.add_field(
            name = "🔎 {} ({}) a reporté le bug suivant :".format(ctx.author, ctx.author.id),
            value = "```{}```".format(bug, non),
            inline = False
        )

        await client.get_channel(746291001043320834).send(embed=embed)
        await ctx.channel.send(ldata["reportSent"])


@client.command()
async def rban(ctx, idb, *, reason = None):

    if ctx.author.id == 157588494460518400:

        gid = str(ctx.guild.id)

        with open('data/guilds.json', encoding='utf-8') as f:
            gdata = json.load(f)

        lang = gdata[gid]["language"]
        with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
            ldata = json.load(lf)

        with open("data/blocklist.json", encoding='utf-8') as f:
            data = json.load(f)

        if idb in data:
            await ctx.channel.send("❌ Cet utilisateur ({}) est déjà banni.".format(idb))

        else:
            data.update({idb:{"name": str(client.get_user(int(idb))), "reason": reason}})

            with open("data/blocklist.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            await ctx.channel.send("🔨 {} a été banni, il ne peut plus envoyer des reports de bugs. \nRaison: ``{}``".format(client.get_user(int(idb)), reason))
            
            embed = discord.Embed(
                title = ldata["banYouAreBanned"],
                colour = discord.Color.default()
            )
        
            embed.set_footer(
                text = str(client.get_user(int(idb))),
                icon_url = client.get_user(int(idb)).avatar_url
            )

            embed.add_field(
                name = ldata["banForbidden"],
                value = "```{}```".format(reason),
                inline = False
            )
            embed.set_author(
                name = str(ctx.author),
                icon_url = ctx.author.avatar_url
            )

            await client.get_user(int(idb)).send(embed=embed)



@client.command()
async def unban(ctx, idb):       

    if ctx.author.id == 157588494460518400:

        gid = str(ctx.guild.id)

        with open('data/guilds.json', encoding='utf-8') as f:
            gdata = json.load(f)

        lang = gdata[gid]["language"]
        with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
            ldata = json.load(lf)

        with open("data/blocklist.json", encoding='utf-8') as f:
            data = json.load(f)
            

        if idb in data:
            data.pop(idb, None)

            with open("data/blocklist.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            await ctx.channel.send("✅ Cet utilisateur ({}) a été débanni".format(idb))

        else:
            await ctx.channel.send("❌ Cet utilisateur ({}) n'est pas dans la liste des bannis".format(idb))

@client.command()
async def banlist(ctx):       

    if ctx.author.id == 157588494460518400:

        gid = str(ctx.guild.id)

        with open('data/guilds.json', encoding='utf-8') as f:
            gdata = json.load(f)

        lang = gdata[gid]["language"]
        with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
            ldata = json.load(lf)

        with open("data/blocklist.json", encoding='utf-8') as f:
            data = json.load(f)
        
        Lb = ["**{}** *({})* \nRaison: ``{}``\n \n".format(data[elm]["name"], elm, data[elm]["reason"]) for elm in data]

        await ctx.channel.send(''.join(Lb))
            


@client.command()
@commands.has_any_role("LG Host")
async def freset(ctx):
# Reset de force
    await reset(ctx, ctx.author)


async def reset_panel(ctx, auth):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    embed = discord.Embed(
        colour = discord.Color.from_rgb(85,0,25),
        title = ldata["resetEmbedTitle"]
    )

    embed.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed.add_field(
        name = ldata["resetWarningName"],
        value = ldata["resetWarningValue"],
        inline = False
    )

    panel = await ctx.channel.send(embed=embed)

    await panel.add_reaction("✅")
    await panel.add_reaction("❌")

    def checkReset(reaction, user):
        print(panel.id, reaction.message.id)
        return (user == mdj) and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌") and (reaction.message.id == panel.id)

    try:
        reaction, user = await client.wait_for("reaction_add", check=checkReset, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.channel.send(ldata["actionPanelTimedOut"])
        await panel.delete()
        await menu(ctx)
    else:
        if str(reaction.emoji) == "❌":
            await ctx.channel.send(ldata["actionPanelCommandCancelled"])
            await reaction.message.delete()
            await menu(ctx)
        else:
            await reset(ctx)


async def reset(ctx):
#Commande d'arrêt du jeu

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])
    in_game = gdata[aid]["in_game"]

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    try:
        author = auth
        channel = author.voice.channel
        members = channel.members
    except:
        members = []

    if in_game == True:

        for member in members:
            await channels[2].set_permissions(member, overwrite=can_talk)
            await channels[3].set_permissions(member, overwrite=cant_talk)
            print("OK, {}".format(member))

        data[gid]["in_game"] = False
        data[gid]["mdj"] = None

        with open('data/guilds.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        gdata.update({aid:{"guild":ctx.guild.id,"Lp": [], "Lroles": [], "idtoemoji": {},"dictemoji": {},"is_compo": is_compo,"game_started": False,"day": False,"is_enfant": False,"ancien_dead": False,"check_couple": False,"cpt_jour": 0,"can_vote": False}})
                    
        with open('data/games.json', 'w', encoding='utf-8') as f:
            json.dump(gdata, f, indent = 4, ensure_ascii=False)

        await ctx.channel.send(ldata["resetGameStopped"])

    else:
        await ctx.channel.send(ldata["resetNoGame"])

        for member in members:
            await channels[2].set_permissions(member, overwrite=can_talk)
            await channels[3].set_permissions(member, overwrite=cant_talk)
            print("OK, {}".format(member))


client.run(TOKEN)