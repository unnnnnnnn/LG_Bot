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
from discord.ext import commands, tasks
from dictionnaires import *
from csts import *
from datetime import datetime


#os.chdir(os.path.dirname(__file__))


client = commands.Bot(command_prefix="lg!")
client.remove_command("help")


@client.event
async def on_ready():

    await client.wait_until_ready()
    await client.change_presence(activity=discord.Game(name="🐺 | lg!help"))

    online = client.get_channel(742095974033260611)
    updates = client.get_channel(746375690043130057)
    rapport = client.get_channel(751824930244657223)

    # Checking guild
    guildsIds = [str(guild.id) for guild in client.guilds]

    with open('data/guilds.json', encoding='utf-8') as f: 
        data = json.load(f)

    for idg in guildsIds:
        if idg not in data:
            data.update({idg:{"name": client.get_guild(int(idg)).name, "channels":[], "in_game": False, "mdj": None, "valuepf": 25, "language": 'english'}})
            categories = client.get_guild(int(idg)).categories
            for c in categories:
                if c.name == "The Werewolves of Millers Hollow" or c.name == "Les Loups Garous de Thiercelieux":
                    for channel in c.channels:
                        data[idg]["channels"].append(channel.id)
                    break

    for ids in list(data):
        if ids not in guildsIds:
            if client.get_guild(int(ids)) == None:
                await updates.send("⬇️ LG Bot a **quitté** le serveur {}".format(ids))
            else:
                await updates.send("⬇️ LG Bot a **quitté** le serveur {} ({})".format(client.get_guild(int(ids)), ids))
            data.pop(ids, None)

        else:
            if len(data[ids]["channels"]) == 0:
                categories = client.get_guild(int(ids)).categories
                for c in categories:
                    if c.name == "The Werewolves of Millers Hollow" or c.name == "Les Loups Garous de Thiercelieux":
                        for channel in c.channels:
                            data[ids]["channels"].append(channel.id)
                        break

    with open('data/guilds.json', 'w', encoding='utf-8') as f: 
        json.dump(data, f, indent=4, ensure_ascii=False)

    with open('data/guilds.json', encoding='utf-8') as f: 
        data = json.load(f)
    await rapport.send("``{}`` \nGuilds: **{}** \n \n{}".format(datetime.now().strftime("%H:%M:%S"), len(client.guilds),''.join(["__{}__: \nChannels: **{}** \n \n".format(data[idg]["name"], len(data[idg]["channels"])) for idg in data])))

    print('Bot connecté {0.user}'.format(client))
    await online.send('✅ **{0.user}** connecté à ``{1}``'.format(client, datetime.now().strftime("%H:%M:%S")))



@client.event
async def on_guild_join(guild):

    gid = str(guild.id)
    updates = client.get_channel(746375690043130057)
    
    with open('data/guilds.json', encoding='utf-8') as f: 
        data = json.load(f)

    data.update({gid:{"name": client.get_guild(int(gid)).name, "channels":[], "in_game": False, "mdj": None, "valuepf": 25, "language": 'english', "checkdone": 0}})

    with open('data/guilds.json', 'w', encoding='utf-8') as f: 
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    await updates.send("⬆️ LG Bot a **rejoint** le serveur {} ({})".format(guild, gid))

    try:
        await guild.create_role(name="LG Host", colour=discord.Color.from_rgb(255,65,65), permissions=perms)
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
            value = "[Invite the bot](https://discord.com/oauth2/authorize?client_id=683468750582054937&permissions=536734712&scope=bot) - Support Server soon - [French server](https://discord.gg/nuUpb7U)",
            inline = False
        )
        embed.add_field(
            name = "Bot Usage",
            value = "To start using the bot, an admin needs to enter the `lg!setup` command. That will create all the channels needed to play the game. \n \nTo host a game you need to have the `LG Host` role that the bot creates when it joins a server. \n \nUse the `lg!lsetting` command to change the language of the bot (english by default). Available languages are **french** and **english**. \n \nUse the `lg!help` command to get more informations about the game and commands.",
            inline = False
        )

        await channel.send(embed=embed)

@client.event
async def on_message(ctx):

    if ctx.author.bot:
        pass
    else:
        if ctx.channel.type is discord.ChannelType.private:
            
            with open('data/games.json', encoding='utf-8') as gf:
                gdata = json.load(gf)
            
            for aid in gdata:
                if str(ctx.author.id) in gdata[aid]["idtoemoji"]:
                    gid = str(gdata[aid]["guild"])
                    break
        else:
            gid = str(ctx.guild.id)


        with open('data/guilds.json', encoding='utf-8') as f:
            data = json.load(f)

        channels = [client.get_channel(k) for k in data[gid]["channels"]]
        valuepf = data[gid]["valuepf"]
        aid = str(data[gid]["mdj"])
        
        if data[gid]["mdj"]== None:
            pass
        else:
            mdj = client.get_user(int(aid))
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
            dicop_id_to_emoji = gdata[aid]["idtoemoji"]

            author = ctx.author
            rolemdj = 'Maître du Jeu'
            rolebot = 'LG Bot'
            is_okmsg = True

    try:
        if game_started == True:

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

                        if vote == 'blanc' or vote == 'Blanc' or vote == "nobody" or vote == "Nobody":

                            embedv = discord.Embed(
                                colour = discord.Color.from_rgb(254,254,254)
                            )
                            embedv.set_author(
                                name = ctx.author.name,
                                icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(ctx.author)
                            )
                            embedv.add_field(
                                name = ldata["voteEmbedName"],
                                value = ldata["voteEmbedValue"],
                                inline = False
                            )
                            await ctx.author.send(embed=embedv)
                            await channels[2].send(embed=embedv)
                            gdata[aid]["Lp"][str(ctx.author.id)][10] = 'Non'

                            with open('data/games.json', 'w', encoding='utf-8') as kf:
                                json.dump(gdata, kf, indent=4, ensure_ascii=False)

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
                                            gdata[aid]["Lp"][str(ctx.author.id)][10] = 'Non'

                                            with open('data/games.json', 'w', encoding='utf-8') as kf:
                                                json.dump(gdata, kf, indent=4, ensure_ascii=False)

                                            embedv = discord.Embed(
                                                colour = discord.Color.from_rgb(123,23,43),
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
                                            await channels[2].send(embed=embedv)
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

                    if ('Oeil' in Lroles_dispo or 'Eye' in Lroles_dispo) and cpt_jour == 1:
                        await channels[23].send("({}) ".format(ctx.channel.name) + ''.join(strm))
                
                # Cas du Chaman qui reçoit le salon des morts
                elif ctx.channel == channels[3]:
                    await channels[20].send(''.join(strm))
                    
                    if ('Oeil' in Lroles_dispo or 'Eye' in Lroles_dispo) and cpt_jour == 1:
                        await channels[23].send("({}) ".format(ctx.channel.name) + ''.join(strm))

                # Cas du Jaloux qui reçoit le salon du couple
                elif ctx.channel == channels[6]:
                    if day == True:
                        await channels[21].send(''.join(strm))
                    
                    if ('Oeil' in Lroles_dispo or 'Eye' in Lroles_dispo) and cpt_jour == 1:
                        await channels[23].send("({}) ".format(ctx.channel.name) + ''.join(strm))

                # Cas du 3e Oeil
                elif ctx.channel in channels:
                    channel = ctx.channel
                    if channel == channels[0] or channel == channels[1] or channel == channels[2] or channel == channels[3] or channel == channels[23] or channel == channels[20] or channel == channels[9] or channel == channels[21]:
                        pass
                    else:
                        if ('Oeil' in Lroles_dispo or 'Eye' in Lroles_dispo) and cpt_jour == 1:
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
            lg_host = get(guild.roles, name="LG Host")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False, mention_everyone=False, attach_files=False, embed_links=False),
                lg_host: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True, mention_everyone=True, attach_files=True, embed_links=True)
            }
            overwrites_pdv = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, read_message_history=True, mention_everyone=False, attach_files=False, embed_links=False),
                lg_host: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True, mention_everyone=True, attach_files=True, embed_links=True)
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
                    name_fr = "Les Loups Garous de Thiercelieux"
                    name_en = "The Werewolves of Millers Hollow"
                    for cat in ctx.guild.categories:
                        if cat.name == name_fr or cat.name == name_en:
                            category = cat

                    #category = discord.utils.get(ctx.guild.categories, name=name_fr)
                    #category = discord.utils.get(ctx.guild.categories, name=name_en)

                    for channel in ctx.guild.text_channels:
                        if str(channel.category) == name_fr or str(channel.category) == name_en:
                            await channel.delete()

                    try:
                        await category.delete()
                    except:
                        pass

                    data[gid]["channels"] = []

                    with open("data/guilds.json", 'w', encoding='utf-8') as jf:
                        json.dump(data, jf, indent=4, ensure_ascii=False)
                    await panel.delete()
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

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    in_game = data[gid]["in_game"]

    check_chans = False

    if lang == 'french':
        liste_roles = liste_roles_fr
        if channels[0].name == "commandes-bot":
            check_chans = True
    elif lang == 'english':
        liste_roles = liste_roles_en
        if channels[0].name == "bot-commands":
            check_chans = True

    if check_chans == True:

        if ctx.author.voice and ctx.author.voice.channel:

            if data[gid]["mdj"] == ctx.author.id or data[gid]["mdj"] == None:

                if len(channels) != 0:

                    try:
                        with open('data/games.json', encoding='utf-8') as gf:
                            gdata = json.load(gf)

                        aid = str(ctx.author.id)
                        game_started = gdata[aid]["game_started"]
                    except:
                        game_started = False
                    
                    if game_started == False:

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
                        embed.set_footer(
                            text = ldata["createWaitForFooter"]
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

                            voleurRoles = ['Sectaire', 'Sectarian', 'JDF', 'PP', 'Imposteur', 'Impostor', 'Traitor', 'Traitre']
                            if "Voleur" in Lroles_dispo or "Thief" in Lroles_dispo or "Servante" in Lroles_dispo or "Servant" in Lroles_dispo:
                                print("ok")
                                for role in voleurRoles:
                                    if role in Lroles_dispo:
                                        await ctx.channel.send(ldata["createVoleurInvalid"])
                                        ok_roles = False
                                        break
                            
                            if ('Imposteur' in Lroles_dispo and 'Traitre' in Lroles_dispo) or ('Impostor' in Lroles_dispo and 'Traitor' in Lroles_dispo):
                                await ctx.channel.send(ldata["createImpTraitre"])
                                ok_roles = False
                            
                            oneRoles = ['Voyante','Chasseur','Jaloux','Ancien','Sorcière','PF','Bouc','Idiot','Corbeau','Chaman','Renard','Ours','Chevalier','Salvateur','LGA','IPDL','LGB','Cupidon','JDF','Ange','Enfant','Voleur','Sectaire','Juge','Confesseur','Chaperon','Ankou','Dictateur','Noctambule','Oeil','Traitre','Imposteur','Faucheur','Servante','Assassin','Devin','Oracle','Hunter','Jealous','Ancient','Witch','Girl','Scapegoat','Idiot','Crow','Shaman','Fox','Bear','Knight','Guard','AW','WF','WW','Cupid','PP','Angel','Child','Thief','Sectarian','Juge','Confessor','RRH','Ankou','Dictator','Owl','Eye','Traitor','Impostor','Reaper','Servant','Assassin','Diviner']
                            for role in oneRoles:
                                if Lroles_dispo.count(role) > 1:
                                    await ctx.channel.send(ldata["createOneRole"].format(role))
                                    ok_roles = False
                                    break

                            if ('Chaperon' in Lroles_dispo and 'Chasseur' not in Lroles_dispo) or ('RRH' in Lroles_dispo and 'Hunter' not in Lroles_dispo):
                                await ctx.channel.send(ldata["createChapChasseur"])
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
                                        reaction, user = await client.wait_for("reaction_add", check=checkCreate2, timeout=60.0)
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

                                            data.update({str(ctx.author.id):{"guild":ctx.guild.id, "Lp": {}, "Lroles": [], "Ljoueurs": [], "idtoemoji": {}, "dictemoji": {}, "is_compo": is_compo, "game_started": False, "day": True, "is_enfant": False, "ancien_dead": False, "check_couple": False, "cpt_jour": 0, "can_vote": False}})
                                            
                                            #check.start()

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
                                        data[gid]["checkdone"] = len(Lroles_dispo)

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
                        await ctx.channel.send(ldata["createGameAlreadyStarted"])
                        await ctx.send(embed=embed)

                else: 
                    await ctx.channel.send(ldata["createSetupErrorValue"])
                    await ctx.send(embed=embed)

            elif data[gid]["mdj"] != None and data[gid]["mdj"] != ctx.author.id:
                await ctx.channel.send(ldata["createAlreadyGame"].format(client.get_user(int(data[gid]["mdj"])), int(data[gid]["mdj"])))

        else:
            await ctx.channel.send(ldata["createNoVoiceChannel"])

    else:
        await ctx.channel.send(ldata["createWrongLanguage"])

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

                        try:
                            await member.add_roles(get(member.guild.roles, name="Joueurs Thiercelieux"))
                        except:
                            pass

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

    print("Commande .players exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), ctx.author))

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    if data[gid]["mdj"] == None:

        aid = str(ctx.author.id)
    else:
        aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    Lp = gdata[aid]["Lp"]

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

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)
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
        trad_roles = trad_roles_en

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    in_game = data[gid]["in_game"]

    if data[gid]["mdj"] == None:
        aid = str(ctx.author.id)
    else:
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
        if state_couple == "non" and ("Jealous" in Lroles_dispo or "Jaloux" in Lroles_dispo):
            c_check = '❌'
        else:
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

    await ctx.channel.send(embed=embed_check)

    if roles_check == '✅' and ins_check == '✅' and create_check == '✅' and channels_check == '✅' and c_check == '✅' and game_started == False:

        author = str(ctx.author)
        channel = ctx.author.voice.channel

        members = channel.members
        members = [user for user in members if str(user) != author]

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
                    if role_given == "PF" or role_given == "Chaman" or role_given == "Jaloux" or role_given == "Oeil" or role_given == "Girl" or role_given == "Shaman" or role_given == "Jealous" or role_given == "Eye":
                        await channels[dicoroles[role_given]].set_permissions(member, overwrite=can_see)
                    else:
                        await channels[dicoroles[role_given]].set_permissions(member, overwrite=can_talk)

                    if role_given == "IPDL" or role_given == 'LGB' or role_given == "WF" or role_given == 'WW':
                        await channels[8].set_permissions(member, overwrite=can_talk)
                
                embedr = discord.Embed(
                    title = ldata["startRoleTitle"],
                    colour = discord.Color.red()
                )

                try:
                    if role_given in trad_roles:
                        ename = ldata["startYourRoleIs"].format(trad_roles[role_given])
                        print("{} a le rôle {}".format(member, trad_roles[role_given]))

                    else:
                        ename = ldata["startYourRoleIs"].format(role_given)
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

                gdata[aid]["Ljoueurs"].append(member.id)
                gdata[aid]["Lp"][str(member.id)] = [str(member), role_given, 'Non', 'Non', 'Non', 'Non', 'Non', 'Non', 'Non', 'Non', 'Non', dicop_id_to_emoji[str(member.id)], role_given]
                # 0: joueur # 1: rôle # 2: couple # 3: maitre/enfant # 4: charmé # 5: secte # 6: infecté # 7: rôle imposteur # 8: imposteur LG # 9: rôle traître # 10: peut voter # 11: emoji joueur # 12: role backup revive command

                if role_given == 'Sectaire' or role_given == 'Sectarian':
                    membersect = member

                if role_given == 'Traitre' or role_given == 'Traitor':
                    membertraitre = member

                if role_given == 'Imposteur' or role_given == 'Impostor':
                    memberimp = member


                print('Terminé {}'.format(member))


        if 'Traitre' in Lroles_dispo or 'Traitor' in Lroles_dispo:
            print("trait")
            LforbiddenT = ['Brother', 'Sister', 'Owl', 'Child', 'Cupid', 'Traitor', 'Impostor', 'RRH', 'Frère', 'Soeur', 'Noctambule', 'Enfant', 'Cupidon', 'Traitre', 'Imposteur', 'Chaperon', 'WF', 'IPDL', 'Voleur', 'Thief', 'Servante', 'Servant', 'Jaloux', 'Jealous']
            Lroles_traitre = []
            for k in liste_roles:
                if str(k) in Lroles_dispo or str(k) in LforbiddenT or str(k) in liste_village:
                    pass
                else:
                    Lroles_traitre.append(k)
            #Lroles_traitre = [k for k in liste_roles if (k in liste_village and k not in Lroles_dispo and k not in LforbiddenT)]
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

            print("imp")
            LforbiddenImp = ['Brother', 'Sister', 'Owl', 'Child', 'Cupid', 'Traitor', 'Impostor', 'RRH', 'Frère', 'Soeur', 'Noctambule', 'Enfant', 'Cupidon', 'Traitre', 'Imposteur', 'Chaperon', 'WF', 'IPDL', 'Voleur', 'Thief', 'Servante', 'Servant', 'Jaloux', 'Jealous']
            Lroles_imp = []
            for k in liste_roles:
                if str(k) in Lroles_dispo or str(k) in LforbiddenImp:
                    pass
                else:
                    Lroles_imp.append(k)
            #Lroles_imp = [k for k in liste_roles if (k not in Lroles_dispo) or (k == 'Jaloux' and state_couple == 'couple') or (k not in LforbiddenImp)]
            print(Lroles_imp)
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

            if lang == 'french':
                await ctx.channel.send("⚙️ En attente du choix de l'Imposteur...")
            elif lang == 'english':
                await ctx.channel.send("⚙️ Waiting for the Impostor's choice...")

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
                await current_panel.delete()


        if "Sectaire" in Lroles_dispo or 'Sectarian' in Lroles_dispo:
            Ltemps = [k for k in list(gdata[aid]["Lp"].keys()) if str(gdata[aid]["Lp"][k][1]) != 'Sectaire']
            pop_sect = int(len(Ltemps)/2)
            sect = rdm.sample(Ltemps, pop_sect)

            for ids in sect:
                gdata[aid]["Lp"][ids][5] = "Secte"

            sect = [client.get_user(int(i)) for i in sect]
            secta = [k.name for k in sect]
            await ctx.channel.send(ldata["startCultList"].format(', '.join(secta)))
            await membersect.send(ldata["startCultListPlayer"].format(', '.join(secta)))

            annoncef.append(ldata["startCultListAnnounce"].format(', '.join(secta)))


        if state_couple == 'couple' or state_couple == 'lovers':

            L = [k for k in members if str(k) != str(author) and str(gdata[aid]["Lp"][str(k.id)][1]) != 'Jaloux' and str(gdata[aid]["Lp"][str(k.id)][1]) != 'Jealous']
            print(L)
            i1 = rdm.randint(0,len(L)-1)
            if str(L[i1]) != author:
                amant1 = L[i1]
                gdata[aid]["Lp"][str(L[i1].id)][2] = 'Couple'
                L.pop(i1)

            i2 = rdm.randint(0,len(L)-1)
            if str(L[i2]) != author:
                amant2 = L[i2]
                gdata[aid]["Lp"][str(L[i2].id)][2] = 'Couple'
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

        await ctx.channel.send(embed=embed)

        gdata[aid]["game_started"] = True

        with open('data/games.json', 'w', encoding='utf-8') as f:
            json.dump(gdata, f, indent=4, ensure_ascii=False)

        await menu(ctx)

    
    else:
        print("no start")
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

    print("menu")

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
    mdj = client.get_user(data[gid]["mdj"])

    panel = discord.Embed(
        colour = discord.Color.green()
    ) 
    

    emojis_action = ["🐺", "🔪", "👒", "🔇", "🔊", "🌙", "🧒", "❤️", "💤", "🕵️", "🎺", "🌞","🛑","📔"]

    if game_started == False:    # ATTENTION NE PAS OUBLIER DE CHANGER EN FALSE

        await ctx.channel.send(ldata["menuGameHasNotStarted"])

    else:

        if day == True:
            panel.set_author(
                name = ldata["menuPanelNameDay"]
            )
            panel.add_field(
                name=ldata["menuPanelKillName"],
                value=ldata["menuPanelKillValue"],
                inline=False
            )

            if 'IPDL' in Lroles_dispo or 'WF' in Lroles_dispo:
                panel.add_field(
                    name=ldata["menuPanelInfectName"],
                    value=ldata["menuPanelInfectValue"],
                    inline=False
                )

            if 'Servante' in Lroles_dispo or "Servant" in Lroles_dispo:
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
            if 'IPDL' in Lroles_dispo or 'WF' in Lroles_dispo:
                await msg.add_reaction("🐺")
            if 'Servante' in Lroles_dispo or "Servant" in Lroles_dispo:
                await msg.add_reaction("👒")
            await msg.add_reaction("🔇")
            await msg.add_reaction("🔊")
            await msg.add_reaction("🌙")
            await msg.add_reaction("📔")
            await msg.add_reaction("🛑")

        
        else:

            panel.set_author(
                name=ldata["menuPanelNameNight"]
            )

            if 'Enfant' in Lroles_dispo or 'Child' in Lroles_dispo:
                panel.add_field(
                    name=ldata["menuPanelEnfantName"],
                    value=ldata["menuPanelEnfantValue"],
                    inline=False
                )

            if 'Cupidon' in Lroles_dispo or 'Cupid' in Lroles_dispo:    
                panel.add_field(
                    name=ldata["menuPanelCupiName"],
                    value=ldata["menuPanelCupiValue"],
                    inline=False
                )

            if 'Noctambule' in Lroles_dispo or 'Owl' in Lroles_dispo: 
                panel.add_field(
                    name=ldata["menuPanelNoctName"],
                    value=ldata["menuPanelNoctValue"],
                    inline=False
                )

            if 'Voleur' in Lroles_dispo or 'Thief' in Lroles_dispo:
                panel.add_field(
                    name=ldata["menuPanelVoleurName"],
                    value=ldata["menuPanelVoleurValue"],
                    inline=False
                )

            if 'JDF' in Lroles_dispo or 'PP' in Lroles_dispo:
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


            if 'Enfant' in Lroles_dispo or 'Child' in Lroles_dispo:
                await msg.add_reaction("🧒")
            if 'Cupidon' in Lroles_dispo or 'Cupid' in Lroles_dispo:
                await msg.add_reaction("❤️")
            if 'Noctambule' in Lroles_dispo or 'Owl' in Lroles_dispo:
                await msg.add_reaction("💤")
            if 'Voleur' in Lroles_dispo or 'Thief' in Lroles_dispo:
                await msg.add_reaction("🕵️")
            if 'JDF' in Lroles_dispo or 'PP' in Lroles_dispo:
                await msg.add_reaction("🎺")
            await msg.add_reaction("🌞")

        def checkMenu(reaction, user):
            return (user == mdj) and (reaction.message.id == msg.id) and (str(reaction.emoji) in emojis_action)
        
        reaction, user = await client.wait_for("reaction_add", check=checkMenu)
        await reaction.message.delete()

        if lang == 'french':
            d = {"🧒": 'Enfant', "🕵️": 'Voleur', "🐺": 'Infect', "👒": 'Servante', "💤": 'Noctambule', "🔪": 'Kill'}
        elif lang == 'english':
            d = {"🧒": 'Child', "🕵️": 'Thief', "🐺": 'Infect', "👒": 'Servant', "💤": 'Owl', "🔪": 'Kill'}

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

    print("jour")
    
    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    if lang == "french":
        dicoroles = dicoroles_fr
    elif lang == "english":
        dicoroles = dicoroles_en

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])


    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    game_started = gdata[aid]["game_started"]
    cpt_jour = gdata[aid]["cpt_jour"]
    day = gdata[aid]["day"]
    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    Lp = gdata[aid]["Lp"]
    Lroles_dispo = gdata[aid]["Lroles"]
    is_enfant = gdata[aid]["is_enfant"]

    is_cover = False
    is_devin = False

    print(day)

    if game_started == True:

        if dtime == 'nuit':

            if day == True:

                gdata[aid]["cpt_jour"] += 1
                with open('data/games.json', 'w', encoding='utf-8') as jf:
                    json.dump(gdata, jf, indent=4, ensure_ascii=False)
                gdata[aid]["day"] = False
         
                for memberid in dicop_id_to_emoji:

                    print(memberid)

                    member = client.get_user(int(memberid))
                    membermute = ctx.guild.get_member(int(memberid))
                    
                    try:
                        await membermute.edit(mute=True)
                    except:
                        pass
                    await channels[2].set_permissions(member, overwrite=can_see)

                    rol = Lp[str(memberid)][1]
                    statusc = Lp[str(memberid)][2]
                    status_infect = Lp[str(memberid)][8]
                    status_impost = Lp[str(memberid)][9]
                    
                    print("ok")
                    
                    if rol == 'LG' or rol == 'LGB' or rol == 'IPDL' or rol == 'LGA' or (rol == 'Enfant' and is_enfant == True) or status_infect == 'Infecté' or (rol == 'Imposteur' and status_impost == 'LG') or rol == 'Werewolf' or rol == 'WW' or rol == 'WF' or rol == 'AW' or (rol == 'Impostor' and status_impost == 'Werewolf') or (rol == 'Child' and is_enfant == True):
                        await channels[8].set_permissions(member, overwrite=can_talk)
                        print("{} OK a été demute de LG".format(str(member)))
                    if statusc == 'Couple':
                        await channels[6].set_permissions(member, overwrite=can_see)
                        print("{} OK a été mute de couple".format(str(member)))

                while is_cover == False:
                    if 'LGA' in Lroles_dispo or 'AW' in Lroles_dispo:
                        imember = rdm.choice(list(dicop_id_to_emoji.keys()))
                        await channels[8].send(ldata["jourCoverLGA"].format(Lp[imember][1]))
                        await channels[0].send(ldata["jourCoverLGA"].format(Lp[imember][1]))
                        if cpt_jour == 1 and ('Oeil' in Lroles_dispo or 'Eye' in Lroles_dispo):
                            await channels[23].send(ldata["jourCoverLGA"].format(Lp[imember][1]))
                        is_cover = True
                    else:
                        is_cover = True 

                while is_devin == False:
                    if "Devin" in Lroles_dispo or 'Diviner' in Lroles_dispo:
                        imember = rdm.choice(list(dicop_id_to_emoji.keys()))
                        if Lp[imember][1] == 'Devin' or Lp[imember][1] == 'Diviner':
                            pass
                        else:
                            await channels[29].send(ldata["jourGuessDevin"].format(str(imember)))
                            await channels[0].send(ldata["jourGuessDevin2"].format(str(imember),Lp[imember][1]))
                            if cpt_jour == 1 and ('Oeil' in Lroles_dispo or 'Eye' in Lroles_dispo):
                                await channels[23].send(ldata["jourGuessDevin3"].format(str(imember)))
                            is_devin = True
                    else:
                        break

                cpt_jour = gdata[aid]["cpt_jour"]

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

                print("ok")

        elif dtime == 'jour':
 
            gdata[aid]["day"] = True
            
            for memberid in dicop_id_to_emoji:
                
                print(memberid)

                member = client.get_user(int(memberid))
                membermute = ctx.guild.get_member(int(memberid))
                    
                try:
                    await membermute.edit(mute=False)
                except:
                    pass
                await channels[2].set_permissions(member, overwrite=can_talk)

                rol = Lp[str(memberid)][1]
                statusc = Lp[str(memberid)][2]
                status_infect = Lp[str(memberid)][8]
                status_impost = Lp[str(memberid)][9]

                check_LG = False
                if rol == 'LG' or rol == 'LGB' or rol == 'IPDL' or rol == 'LGA' or (rol == 'Enfant' and is_enfant == True) or status_infect == 'Infecté' or (rol == 'Imposteur' and status_impost == 'LG') or rol == 'Werewolf' or rol == 'WW' or rol == 'WF' or rol == 'AW' or (rol == 'Impostor' and status_impost == 'Werewolf') or (rol == 'Child' and is_enfant == True):
                    check_LG = True

                if check_LG == True:
                    await channels[8].set_permissions(member, overwrite=can_see)
                    print("{} OK a été mute de LG".format(str(member)))

                if rol == 'LGB' or rol == 'IPDL' or rol == "WW" or rol == "WF":
                    await channels[dicoroles[rol]].set_permissions(member, overwrite=can_talk)
                    print("{} OK a été demute de LGB/IPDL (cas où noctambule)".format(str(member)))

                if rol in dicoroles and check_LG == False:
                    if rol == "PF" or rol == "Chaman" or rol == "Jaloux" or rol == "Oeil" or rol == "Girl" or rol == "Shaman" or rol == "Jealous" or rol == "Eye":
                        await channels[dicoroles[rol]].set_permissions(member, overwrite=can_see)
                    else:
                        await channels[dicoroles[rol]].set_permissions(member, overwrite=can_talk)
                    print("{} OK a été demute de {} (cas où noctambule)".format(member, channels[dicoroles[rol]]))

                if statusc == 'Couple':
                    await channels[6].set_permissions(member, overwrite=can_talk)
                    print("{} OK a été demute de couple".format(str(member)))

            cpt_jour = gdata[aid]["cpt_jour"]

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

    with open('data/games.json', 'w', encoding='utf-8') as jf:
        json.dump(gdata, jf, indent=4, ensure_ascii=False)

    await menu(ctx)


async def action_panel(ctx, action):
    # Actions: Enfant, Voleur, Infect, Kill, Noctambule, Servante
    print("action")
    print(action)

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

    d = ldata["actionPanelRolesDesc"][action]

    embed_panel = discord.Embed(
        colour = discord.Color.green()
    )

    embed_panel.set_author(
        name = ldata["actionPanelAuthor"].format(action),
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed_panel.add_field(
        name = ldata["actionPanelName"], 
        value = ldata["actionPanelValue"].format(d), 
        inline = False
    )

    panel = await ctx.channel.send(embed=embed_panel)

    for nameid in dicop_id_to_emoji:
        name = client.get_user(int(nameid))
        print(name)
        fiche_player = Lp[nameid]
        print(fiche_player[1])
        if (action == 'Enfant' and str(fiche_player[1]) == 'Enfant') or (action == 'Child' and str(fiche_player[1]) == 'Child'):
            print("ok e")
            n_enfant = nameid
        elif (action == 'Voleur' and str(fiche_player[1]) == 'Voleur') or (action == 'Thief' and str(fiche_player[1]) == 'Thief'):
            n_voleur = nameid
        elif (action == 'Infect') and (str(fiche_player[1]) == 'LG' or str(fiche_player[1]) == 'LGA' or str(fiche_player[1]) == 'LGB' or str(fiche_player[1]) == 'IPDL' or str(fiche_player[1]) == 'GML' or fiche_player[9] == 'Infecté' or (str(fiche_player[1]) == 'Enfant' and is_enfant == True) or str(fiche_player[1]) == 'AW' or str(fiche_player[1]) == 'WW' or str(fiche_player[1]) == 'WF' or str(fiche_player[1]) == 'BBW' or fiche_player[9] == 'Infecté' or (str(fiche_player[1]) == 'Child' and is_enfant == True)):
            pass
        elif ((action == "Noctambule") and (str(fiche_player[1]) == 'Noctambule' or fiche_player[8] == 'Noctambule' or fiche_player[9] == 'Noctambule')) or (action == 'Owl' and (str(fiche_player[1]) == 'Owl' or fiche_player[8] == 'Owl' or fiche_player[9] == 'Owl')):
            n_noctambule = nameid
        elif (action == 'Servante' and (str(fiche_player[1]) == 'Servante' or fiche_player[8] == 'Servante' or fiche_player[9] == 'Servante')) or (action == 'Servant' and (str(fiche_player[1]) == 'Servant' or fiche_player[8] == 'Servant' or fiche_player[9] == 'Servant')):
            n_servante = nameid
        else:
            print("add")
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
            print("ok")
            if action == 'Enfant' or action == 'Child':
                await enfant_action(reaction.message, str(dicop_emoji[reaction.emoji]), n_enfant)
            elif action == 'Voleur' or action == 'Thief':
                await voleur_action(reaction.message, str(dicop_emoji[reaction.emoji]), n_voleur, 'Voleur')
            elif action == 'Infect':
                await infect_action(reaction.message, str(dicop_emoji[reaction.emoji]))
            elif action == 'Kill':
                await kill_action(reaction.message, str(dicop_emoji[reaction.emoji]), 'Kill')
            elif action == 'Noctambule' or action == 'Owl':
                await noctambule_action(reaction.message, str(dicop_emoji[reaction.emoji]), n_noctambule)
            elif action == 'Servante' or action == 'Servant':
                await voleur_action(reaction.message, str(dicop_emoji[reaction.emoji]), n_servante, 'Servante')
                await kill_action(reaction.message, str(dicop_emoji[reaction.emoji]), 'Servante')


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
    Lp = gdata[aid]["Lp"]

    lc = []

    embed_panel = discord.Embed(
        colour = discord.Color.from_rgb(255,0,70)
    )

    embed_panel.set_author(
        name = ldata["cupidonPanelAuthor"],
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed_panel.add_field(
        name = ldata["actionPanelName"], 
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
            await reaction.message.delete()
            await ctx.channel.send(ldata["cupidonPanelChoose2ndLover"])
            panel2 = await ctx.channel.send(embed=embed_panel)
            for nameid in dicop_id_to_emoji:
                if int(nameid) in lc:
                    pass
                else:
                    await panel2.add_reaction(dicop_id_to_emoji[nameid])
            await panel2.add_reaction("❌")

            def checkCupi2(reaction, user):
                return (user == mdj) and ((str(reaction.emoji) in dicop_emoji) or str(reaction.emoji) == non) and (reaction.message.id == panel2.id)

            try:
                reaction, user = await client.wait_for("reaction_add", check=checkCupi2, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.channel.send(ldata["actionPanelTimedOut"])
                await panel2.delete()
                await menu(ctx)
            else:
                if str(reaction.emoji) == non:
                    await ctx.channel.send(ldata["actionPanelCommandCancelled"])
                    await reaction.message.delete()
                    await menu(ctx)
                else:
                    lc.append(dicop_emoji[reaction.emoji])
                    await cupidon_action(reaction.message, lc)



async def cupidon_action(ctx, liste_couple):
    print(liste_couple)
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

    c1 = client.get_user(cpl1)
    c2 = client.get_user(cpl2)

    await channels[6].set_permissions(c1, overwrite=can_see)
    await channels[6].set_permissions(c2, overwrite=can_see)
    await c1.send(ldata["cupidonDMLovers"].format(c2))
    await c2.send(ldata["cupidonDMLovers"].format(c1))
    await ctx.channel.send(ldata["cupidonLoversList"].format(c1,c2))
    await ctx.delete()

    with open('data/games.json', 'w', encoding='utf-8') as f:
        json.dump(gdata, f, indent=4, ensure_ascii=False)
    await menu(ctx)


async def enfant_action(ctx, maitreid, enfantid):

    print("enfant")

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    print("ok")

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    print("ok")    

    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    print("ok")

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    print("ok")

    Lp = gdata[aid]["Lp"]

    print("ok")
    gdata[aid]["Lp"][maitreid][3] = 'Maitre'
    gdata[aid]["Lp"][enfantid][3] = 'Enfant'
    print("ok")
    await ctx.channel.send(ldata["enfantMaster"].format(client.get_user(int(maitreid)), client.get_user(int(enfantid))))
    await ctx.delete()
    print("ok")
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
    is_enfant = gdata[aid]["is_enfant"]

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
        print("ok")
        if role_stolen == 'LGB' or role_stolen == 'IPDL' or (role_stolen == 'Enfant' and is_enfant == True) or fiche_stolen[9] == 'Infecté' or role_stolen == 'WW' or role_stolen == 'WF' or (role_stolen == 'Child' and is_enfant == True):
            await channels[8].set_permissions(stolen_name, overwrite=cant_talk)
            if step == 'Voleur':
                await channels[8].set_permissions(voleur_name, overwrite=can_talk)
            elif step == 'Servante':
                await channels[8].set_permissions(voleur_name, overwrite=can_see)
    if step == "Voleur":
        await channels[dicoroles[role_voleur]].set_permissions(voleur_name, overwrite=cant_talk)
        await channels[dicoroles[role_voleur]].set_permissions(stolen_name, overwrite=can_talk)

        await stolen_name.send(ldata["voleurVoleur"])
        await ctx.channel.send(ldata["voleurSummary"].format(str(voleur_name),str(stolen_name),str(role_stolen)))
    await voleur_name.send(ldata["voleurStolen"].format(str(role_stolen)))
    await ctx.delete()

    with open('data/games.json', 'w', encoding='utf-8') as jf:
        json.dump(gdata, jf, indent=4, ensure_ascii=False)

    if step == 'Voleur':
        await menu(ctx)


async def infect_action(ctx, infectid):

    print("infect")

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    print("ok")

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)
    print("ok")
    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])
    print("ok")
    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)
    print("ok")
    Lp = gdata[aid]["Lp"]
    day = gdata[aid]["day"]
    print("ok")
    infect_name = client.get_user(int(infectid))
    print(infect_name)

    if day == True:
        await channels[8].set_permissions(infect_name, overwrite=can_see)
    elif day == False:
        await channels[8].set_permissions(infect_name, overwrite=can_talk)

    print("ok")
    gdata[aid]["Lp"][infectid][6] = 'Infecté'
    print("ok")
    await infect_name.send(ldata["infectInfect"])
    await ctx.channel.send(ldata["infectSummary"].format(str(infect_name)))
    await ctx.delete()
    print("ok")
    with open('data/games.json', 'w', encoding='utf-8') as jf:
        json.dump(gdata, jf, indent=4, ensure_ascii=False)
    print("ok")
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
    dicop_emoji = gdata[aid]["dictemoji"]

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
        if str(fiche_player[1]) == 'JDF' or fiche_player[4] == 'Charmé' or str(fiche_player[1]) == 'PP':
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
                if str(fiche_player[1]) == 'JDF' or fiche_player[4] == 'Charmé' or str(fiche_player[1]) == 'PP':
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

    print(liste_charm)
    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    print("ok")
    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])
    print("ok")
    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)
    print("ok")
    Lp = gdata[aid]["Lp"]
    print("ok")
    for memberid in liste_charm:
        print(memberid)
        member = client.get_user(int(memberid))
        gdata[aid]["Lp"][str(memberid)][4] = 'Charmé'
        await channels[4].set_permissions(member, overwrite=can_see)
        await member.send(ldata["charmTarget"])
        await ctx.channel.send(ldata["charmSummary"].format(str(member)))

    print("ok")
    await ctx.delete()
    with open('data/games.json', 'w', encoding='utf-8') as jf:
        json.dump(gdata, jf, indent=4, ensure_ascii=False)
    await menu(ctx)


async def kill_action(ctx, killedid, step):

    print("kill")

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
    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    dicop_emoji = gdata[aid]["dictemoji"]
    is_compo = gdata[aid]["is_compo"]
    Lroles_dispo = gdata[aid]["Lroles"]

    killed_name = client.get_user(int(killedid))
    killed_member = ctx.guild.get_member(int(killedid))

    pla = Lp[killedid]
    rolep = pla[1]
    status_couple = pla[2]
    status_maitre = pla[3]
    status_infect = pla[6]
    status_impost = pla[8]

    member = killed_name

    if (rolep == 'Ancien' or rolep == 'Ancient') and ancien_dead == False:
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

        if rolep == "IPDL" or rolep == 'LGB' or rolep == "WF" or rolep == 'WW':
            await channels[8].set_permissions(member, overwrite=cant_talk)
            print('OK LGB/IPDL')

        if (rolep == 'Enfant' or rolep == 'Child') and is_enfant == True:
            await channels[8].set_permissions(member, overwrite=cant_talk)
            print('OK Enfant')

        if status_couple == 'Couple':
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
            for mid in dicop_id_to_emoji:
                pla_en = Lp[mid]
                print(mid, pla_en)
                if pla_en[3] == 'Enfant':
                    enf = client.get_user(int(mid))
                    await channels[8].set_permissions(enf, overwrite=can_see)
                    await channels[26].set_permissions(enf, overwrite=cant_talk)
                    await ctx.channel.send(ldata["killIsNowLG"].format(enf))
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
            await killed_member.edit(mute=True)
        except: 
            pass

        gdata[aid]["Lp"][str(member.id)][1] = 'Mort'
        emj = dicop_id_to_emoji[str(member.id)]
        del gdata[aid]["dictemoji"][emj]
        del gdata[aid]["idtoemoji"][str(member.id)]

        print('OK {} est mort, il était {}'.format(str(member), rolep))

        if is_compo == True:

            await channels[1].purge(limit=50)          
            
            embedaf = discord.Embed(
                colour = discord.Color.default(),
                title = ldata["killInfoGame"]
            )

            Lroles_dispo.remove(rolep)
            gdata[aid]["Lroles"] = Lroles_dispo
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
            Lroles_dispo.remove(rolep)
            gdata[aid]["Lroles"] = Lroles_dispo

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

            if Lp[pid][1] == 'Mort':

                gdata[aid]["Lp"][pid][1] = gdata[aid]["Lp"][pid][12]
                gdata[aid]["idtoemoji"][pid] = gdata[aid]["Lp"][pid][11]
                gdata[aid]["dictemoji"][gdata[aid]["Lp"][pid][11]] = int(pid)
                gdata[aid]["Lroles"].append(gdata[aid]["Lp"][pid][12])

                with open("data/games.json", 'w', encoding='utf-8') as jf:
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

    if lang == 'french':
        dicoroles = dicoroles_fr
    elif lang == 'english':
        dicoroles = dicoroles_en

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

    print("vote")

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

    for mid in dicop_id_to_emoji:
        member = client.get_user(int(mid))
        gdata[aid]["Lp"][mid][10] = 'Oui'
        try:
            await member.send(ldata["voteWillStart"])
        except:
            await ctx.channel.send(ldata["voteCanNotBeSend"].format(member))

    with open('data/games.json', 'w', encoding='utf-8') as kf:
        json.dump(gdata, kf, indent=4, ensure_ascii=False)

    embed = discord.Embed(
        colour = discord.Color.default()
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

    panel = await ctx.channel.send(embed=embed)

    await panel.add_reaction('⏱️')
    await panel.add_reaction('❌')

    def checkVote(reaction, user):
        return (user == mdj) and (reaction.message.id == panel.id) and (str(reaction.emoji) == '⏱️' or str(reaction.emoji) == non)

    try:
        reaction, user = await client.wait_for("reaction_add", check=checkVote, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.channel.send(ldata["actionPanelTimedOut"])
        await panel.delete()
        await menu(ctx)
    else:
        if str(reaction.emoji) == non:
            await panel.delete()
            await menu(ctx)
        else:
            with open('data/games.json', encoding='utf-8') as gf:
                gdata = json.load(gf)
            
            gdata[aid]["can_vote"] = True

            with open('data/games.json', 'w', encoding='utf-8') as kf:
                json.dump(gdata, kf, indent=4, ensure_ascii=False)

            await panel.clear_reaction('⏱️')
            await panel.clear_reaction(non)
            await panel.add_reaction(ok)

            def checkVote2(reaction, user):
                return (user == mdj) and (reaction.message.id == panel.id) and (str(reaction.emoji) == ok )

            reaction, user = await client.wait_for("reaction_add", check=checkVote2)

            with open('data/games.json', encoding='utf-8') as gf:
                gdata = json.load(gf)

            gdata[aid]["can_vote"] = False

            with open('data/games.json', 'w', encoding='utf-8') as kf:
                json.dump(gdata, kf, indent=4, ensure_ascii=False)

            await ctx.channel.send("**Vote is over**")
            await panel.delete()
            await menu(ctx)


async def mute(ctx, state):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    aid = str(data[gid]["mdj"])
    mdj = client.get_user(int(aid))

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    Ljoueurs = gdata[aid]["Ljoueurs"]

    for mid in Ljoueurs:
        member = ctx.guild.get_member(mid)

        if state == 'mute':
            await member.edit(mute=True)
        elif state == 'unmute':
            await member.edit(mute=False)

    await menu(ctx)


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
                json.dump(data, f, indent=4, ensure_ascii=False )

    else:
        await ctx.channel.send(ldata["errorPermissionMissing"])

@client.command()
async def breport(ctx, *, bug):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    with open("data/blocklist.json", encoding='utf-8') as bf:
        data = json.load(bf)

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
    await reset_panel(ctx, ctx.author)


async def reset_panel(ctx, auth=None):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    if data[gid]["mdj"] == None:
        aid = str(auth.id)
    else:
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
        if mdj == None:
            return (user == auth) and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌") and (reaction.message.id == panel.id) 
        else:
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
            await reaction.message.delete()
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
    in_game = data[gid]["in_game"]

    with open('data/games.json', encoding='utf-8') as gf:
        gdata = json.load(gf)

    Ljoueurs = gdata[aid]["Ljoueurs"]

    if in_game == True:

        for ichannel in channels:
            for idmember in Ljoueurs:
                member = client.get_user(int(idmember))
                await ichannel.set_permissions(member, overwrite=None)

        data[gid]["in_game"] = False
        data[gid]["mdj"] = None

        with open('data/guilds.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        gdata.update({aid:{"guild":None,"Lp": {}, "Lroles": [], "Ljoueurs": [], "idtoemoji": {}, "dictemoji": {}, "is_compo": True, "game_started": False, "day": False, "is_enfant": False, "ancien_dead": False, "check_couple": False, "cpt_jour": 0, "can_vote": False}})
                    
        with open('data/games.json', 'w', encoding='utf-8') as f:
            json.dump(gdata, f, indent = 4, ensure_ascii=False)

        await ctx.channel.send(ldata["resetGameStopped"])

    else:
        await ctx.channel.send(ldata["resetNoGame"])

        for ichannel in channels:
            for idmember in dicop_id_to_emoji:
                member = client.get_user(int(idmember))
                await ichannel.set_permissions(member, overwrite=None)

        await ctx.channel.send("OK ✅")


@client.command()
async def gstop(ctx, hid):

    gid = str(ctx.guild.id)

    with open('data/guilds.json', encoding='utf-8') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    in_game = data[gid]["in_game"]

    lang = data[gid]["language"]
    with open('langages/{}.json'.format(lang), encoding='utf-8') as lf:
        ldata = json.load(lf)

    with open("data/games.json", encoding='utf-8') as gf:
        gdata = json.load(gf)

    if ctx.author.guild_permissions.administrator:

        if hid in gdata:
            
            if in_game == True:

                data[gid]["in_game"] = False
                data[gid]["mdj"] = None

                with open('data/guilds.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

                gdata.update({hid:{"guild":None,"Lp": {}, "Lroles": [], "idtoemoji": {},"dictemoji": {},"is_compo": True,"game_started": False,"day": False,"is_enfant": False,"ancien_dead": False,"check_couple": False,"cpt_jour": 0,"can_vote": False}})

                with open('data/games.json', 'w', encoding='utf-8') as f:
                    json.dump(gdata, f, indent = 4, ensure_ascii=False)

                await channels[0].send("<@{}> Un administrateur ({}) a arrêter votre partie de force.".format(int(hid), ctx.author))


client.run(TOKEN)