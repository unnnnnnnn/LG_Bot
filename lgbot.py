#-*- coding:utf-8 -*-

#================================

import discord
import asyncio
import emoji
import re
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
from inspect import getsourcefile
from pprint import pprint

os.chdir(os.path.dirname(__file__))

client = commands.Bot(command_prefix=".")
client.remove_command("help")


@client.event
async def on_ready():
#Fonction initiale du bot (automatique)
#Initialisation

    
    await client.wait_until_ready()
    await client.change_presence(activity=discord.Game(name="🐺 | .help"))
    print('Bot connecté {0.user}'.format(client))

    online = client.get_channel(742095974033260611)
    await online.send('✅ **{0.user}** connecté à ``{1}``'.format(client, datetime.now().strftime("%H:%M:%S")))



@client.event
async def on_message(ctx):

    try:
        gid = str(ctx.guild.id)

        with open('guilds.json') as f:
            data = json.load(f)

        channels = [client.get_channel(k) for k in data[gid]["channels"]]
        aid = data[gid]["mdj"]
        mdj = client.get_user(aid)
        
        with open('games.json') as gf:
            gdata = json.load(gf)

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
                        await ctx.author.send("Les messages privés avec le bot ne sont pas autorisés pendant la partie, __sauf pendant le vote__.")

                    elif can_vote == True and Lp[str(ctx.author.id)][10] == 'Non':
                        await ctx.author.send("❌ Vous avez déjà voté. Vous ne pouvez pas voter à nouveau.")

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
                                name = "📔 Vous avez fait votre choix",
                                value = "Vous avez voté **Blanc** ◽",
                                inline = False
                            )

                        else:
                            try:
                                member_name, member_discriminator = vote.split('#')
                            except ValueError:
                                await ctx.channel.send("❌ Nom de joueur non valide. Veuillez vérifier que vous ne vous êtes pas trompé.")
                            else:
                                
                                aut_name, aut_disc = str(ctx.author).split('#')
                                is_author = False

                                for user in dicop_name_to_emoji:
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
                                                name = "📔 Vous avez fait votre choix",
                                                value = "Vous avez voté pour **{.name}**".format(user),
                                                inline = False
                                            )
                                            embedv.set_thumbnail(
                                                url = user.avatar_url
                                            )

                                            await ctx.author.send(embed=embedv)
                                            await channels[0].send(embed=embedv)
                                            break

                                        else:
                                            await ctx.author.send("❌ Vous ne pouvez pas voter pour vous même car il y a un Ange dans la partie.")
                                            break
                                
                                if Lp[str(ctx.author.id)][10] == 'Oui' and is_author == False:
                                    await ctx.author.send("❌ Nom de joueur non valide. Veuillez vérifier que vous ne vous êtes pas trompé.")

                                else:
                                    await ctx.author.send("✅ Votre vote a bien été pris en compte. Veuillez patienter jusqu'à la fin du vote.")


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


@client.command()
async def help(ctx):
#Commande d'aide utilisateur

    author = ctx.author
    
    embed1 = discord.Embed(
        colour = discord.Color.red(),
        title = "🐺 Bienvenue sur le menu d'aide du LG Bot !"
    )
    embed1.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )
    embed1.set_thumbnail(
        url='https://www.loups-garous-en-ligne.com/jeu/assets/images/carte2.png'
    )
    embed1.add_field(
        name = "📚 Sommaire",
        value = "``Page 1``: Présentation générale du bot. \n ``Page 2``: Règles du jeu. \n ``Page 3``: Commandes du bot",
        inline = False
    )
    embed1.add_field(
        name = "🔖 Présentation",
        value = "``Le Loup-Garou est à l'origine un jeu de plateau, qui a ici été implémenté pour y jouer sur Discord. Le bot permet ainsi d'y jouer grâce à des channels texte privés en fonction des rôles. Le bot n'est pas entièrement automatisé et il est nécessaire d'avoir un Maître du Jeu présent pour jouer. La partie se joue dans un chat vocal dédié, mais les joueurs peuvent très bien jouer par texte dans un salon général dédié.``",
        inline = False
    )
    embed1.add_field(
        name = "📄 Navigation dans le menu",
        value = "Pour naviguer dans le menu, cliquez sur les réactions en dessous.",
        inline = False
    )
    embed1.set_footer(
        text = 'Page 1/3 • {0.name}'.format(author)
    )

    embed2 = discord.Embed(
        colour = discord.Color.dark_blue(),
        title = "Règles du jeu"
    )
    embed2.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )
    embed2.set_thumbnail(
        url='https://www.loups-garous-en-ligne.com/jeu/assets/images/carte2.png'
    )
    embed2.add_field(
        name = "📘 Déroulement du jeu",
        value = "``- Quand tous les participants se trouvent dans le channel vocal de la partie, le Maître du Jeu (MDJ) peut commencer. Chaque joueur va recevoir un rôle par message privé du bot. Une description du rôle sera donnée. Dans certains cas, un channel texte vous sera attribué, notamment pour que le MDJ communique avec vous.``\n \n ``- Lorsque la nuit tombe, tous les participants sont mute serveur, et le channel général est fermé. De même, pendant le vote les participants sont muets.`` \n \n ``- Chaque nuit, plusieurs rôles seront appelés par vocal. Ces personnes devront répondre dans leur channel respectif. A la fin de chaque jour, un vote a lieu, et tous les participants doivent voter dans le channel général quand le Maître du Jeu dit de le faire.`` \n \n ``- Certains channels ne sont pas accessibles à certains moment. Le channel des Loups n'est ouvert que pendant la nuit, contrairement à celui du couple qui n'est accessible que le jour.``",
        inline = False
    )
    embed2.add_field(
        name = "📕 Règles importantes",
        value = "**1. La dévo (dévoiler son rôle...) est totalement interdite.** \n ``La dévo comprend: dire explicitement son rôle, donner des indices très explicites sur son rôle, révéler explicitement le rôle de quelqu'un d'autre (avec le Voleur par exemple). N'hésitez pas à demander au MDJ si vous n'êtes pas sûr si ce que vous allez dire est autorisé.`` \n \n **2. L'envoi de messages privés à d'autres joueurs pendant la partie est totalement interdit.** \n ``Ainsi que les messages codés pendant la partie (langage ou références...).`` \n \n **3. Le focus est déconseillé/interdit** \n ``Par exemple le focus en tant que Sorcière avec le potion de mort, ou en étant Enfant, ou le focus de la même personne tour 1 deux parties de suite. Contactez le MDJ pour plus de précisions.`` \n \n **4. Si un Ange est dans la partie il est interdit de voter pour soi-même** \n ``Le vote au 1e tour est d'ailleurs obligatoire, et les égalités forcées sont interdites.``",
        inline = False
    )
    embed2.add_field(
        name = "📗 Informations complémentaires",
        value = "``- Vous pourrez trouver des informations concernant les règles dans le salon`` `#règles` ``sur le serveur, notamment sur l'utilisation de certains rôles et comment fonctionnent-ils.`` \n \n ``- Rendez vous dans le salon`` `#tag-roles` ``pour vous attribuez un rôle pour être notifier des parties.`` \n \n ``- Gardez un oeil sur le salon`` `#annonces` ``. C'est à cet endroit que nous notifieront les joueurs qu'une partie va commencer, et que les nouveaux rôles seront annoncés. N'hésitez pas à entrer la commande`` `.roles` ``pour connaître la liste et leurs descriptions.``",
        inline = False
    )
    embed2.set_footer(
        text = 'Page 2/3 • {0.name}'.format(author)
    )

    embed3 = discord.Embed(
        colour = discord.Color.gold(),
        title = "Commandes du Bot"
    )

    embed3.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )
    embed3.set_thumbnail(
        url='https://www.loups-garous-en-ligne.com/jeu/assets/images/carte2.png'
    )
    embed3.add_field(
        name = "🛠️ Commandes pour les Joueurs (pas de rôles requis)",
        value = "\n ``.help``: Envoie ce menu d'aide \n \n ``.roles``: Envoie la liste des rôles et leurs descriptions. \n \n Les commandes ci-dessus peuvent être exécutées par MP avec le bot directement.",
        inline = False
    )
    embed3.add_field(
        name = "🛠️ Commandes pour les Maîtres du Jeu (rôle Maître du Jeu requis)",
        value = "\n ``.setup``: Création des salons texte (obligatoire de faire cette commande avant chaque début de partie). \n \n ``.inscription``: Permet d'inscrire tous les gens de la partie ou de clear la liste d'inscription. \n \n ``.joueurs``: Affiche la liste des joueurs inscrits. \n \n ``.create <liste des rôles> <visible/cachée>``: Créer une partie. Faites ``.hcreate`` pour obtenir de l'aide sur cette commande. \n \n ``.start <couple/non>``: Démarre la partie. La variable couple dit s'il y a un couple (aléatoire seulement). \n \n ``.crypt <pourcentage>``: Définit le pourcentage de chance qu'une lettre change pour la petite-fille, le chaman, le jaloux et le 3e Oeil (par défaut: 25%). \n \n ``.freset``: Force le reset d'une partie qui permet de l'arrêter. Si aucune partie n'est en cours cette commande reset les permissions générales et certaines constantes. \n \n ``.fmenu``: Permet l'apparition de force du menu en cas de bug.",
        inline = False
    )
    embed3.set_footer(
        text = 'Page 3/3 • {0.name}'.format(author)
    )

    if ctx.channel.type is discord.ChannelType.private:
        pass
    else:
        await ctx.channel.send("<@{.id}> Le menu d'aide va vous être envoyé par MP.".format(author))

    await author.send(embed=embed1)
    await author.send(embed=embed2)
    await author.send(embed=embed3)


@client.command()
@commands.has_any_role("Maître du Jeu")
async def test(ctx):

    with open('games.json') as f:
        data = json.load(f)

    await ctx.channel.send(', '.join(data[str(ctx.author.id)]["Lroles"]))

    eliste = rdm.sample(list(emoji.UNICODE_EMOJI), 3)
    for elm in eliste:
        await ctx.channel.send(elm)


@client.command()
@commands.has_any_role("Maître du Jeu")
async def setup(ctx):

    author = ctx.author
    print("Commande .setup exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), author))

    with open("guilds.json") as f:
        d = json.load(f)
        
    if str(ctx.guild.id) in d:
        await ctx.channel.send("La commande **.setup** a déjà été exécutée sur ce serveur.")
        d[str(ctx.guild.id)]["in_game"] = False # A supprimer plus tard
        with open("guilds.json", 'w') as f:
            json.dump(d, f, indent=4)
    else:

        guild = ctx.guild
        text_channel_list = []
        channels = []

        embed = discord.Embed(
                colour = discord.Color.red(),
                title = "Commande setup"
            )

        is_channels = False

        name = 'Les Loups Garous de Thiercelieux'
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
        print(in_game)
            
        if in_game == False:

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
        
        with open('guilds.json') as json_file: 
            data = json.load(json_file) 

        data.update({str(ctx.guild.id):{"channels":channels, "in_game": False, "mdj": None, "valuepf": 25}})

        with open('guilds.json', 'w') as f:
            json.dump(data, f, indent = 4)
        
        channels = [client.get_channel(idc) for idc in channels]
        print(channels)

        await channels[0].send("Setup terminé.")
        await channels[0].send("Pour connaître la démarche pour lancer une partie, entrez la commande **.hcreate**")

        is_channels = True

    # with open('guilds.json') as f:
        # a = json.load(f)
    
    # print(a[str(ctx.guild.id)]["channels"][0])


@client.command()
@commands.has_any_role("Maître du Jeu")
async def delete(ctx):

    guild = ctx.guild

    name = 'Les Loups Garous de Thiercelieux'
    category = discord.utils.get(ctx.guild.categories, name=name)

    for channel in guild.text_channels:
        if str(channel.category) == name:
            await channel.delete()
    
    await category.delete()

    channels = []


@client.command()
async def hcreate(ctx):

    embed = discord.Embed(
        colour = discord.Color.from_rgb(0,0,120),
        title = "Aide commande .create"
    )

    embed.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed.add_field(
        name = "🔧 Avant d'utiliser la commande:",
        value = "Avant de pouvoir utiliser la commande ``.create``, il faut d'abord exécuter la commande ``.setup``, sinon une erreur vous sera renvoyée. Ces commandes ne sont exécutables que par des Maîtres du Jeu.",
        inline = False
    )


    embed.add_field(
        name = "⚙️ Utilisation de la commande:",
        value = "Les paramètres de la commande sont: une liste ``<liste de rôles>`` et un paramètre de visibilité de la composition ``<visible/cachée>``. Ce paramètre sert à dire si l'on veut que les joueurs sachents la composition ou non. Certains rôles sont interdits avec une composition cachée. \n \n La syntaxe de la liste des rôles doit être comme cela: **Role1,Role2,...,Role**. Après on peut entrer l'argument de visibilité après un espace. On arrive donc à: ``.create Role1,Role2,...,Role visible`` par exemple. \n \n La syntaxe des rôles est également importante. Certains d'entre eux ont une syntaxe raccourcie pour faciliter la création de partie. Les syntaxes des rôles se trouvent ci-dessous. Aussi, si l'on veut avoir plusieurs fois le même rôles dans la partie, il faudra renseigner plusieurs fois ce rôle (voir exemple ci-dessous).",
        inline = False
    )


    embed.add_field(
        name = "✏️ Syntaxes des rôles pour la commande:",
        value = ', '.join(liste_roles) + "\n \n Un exemple de commande .create serait donc: \n ``.create LG,LG,LGA,JDF,Voyante,Chasseur,Ours,Bouc visible`` \n Ici la partie aura 2 Loups Garous, 1 Loup Garou Anonyme, 1 Joueur de Flûte, 1 Voyante, 1 Chasseur, 1 Montreur d'Ours et 1 Bouc-émissaire, et la composition sera visible. \n \n Pour avoir une description détaillée des rôles entrez la commande ``.roles`` (où les syntaxes sont également précisées).",
        inline = False
    )

    if ctx.channel.type is discord.ChannelType.private:
        pass
    else:
        await ctx.channel.send("<@{.id}> Le menu d'aide pour la commande .create va vous être envoyé par MP.".format(ctx.author))

    await ctx.author.send(embed=embed)


@client.command()
@commands.has_any_role("Maître du Jeu")
async def create(ctx, strRole, compo):
#Permet de créer une liste de rôles pour 1 partie

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    in_game = data[gid]["in_game"]

    print("Commande .create exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), ctx.author))

    embed = discord.Embed(
        colour = discord.Color.red(),
        title = "Commande create"
    )

    embed.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )
    
    check_compo = False
    is_compo = False

    if gid in data:

        if compo == 'visible':
            is_compo = True
            check_compo = True
        elif compo == 'cachée':
            check_compo = True
        else:
            embed.set_author(
                name = "LG Bot",
                icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
            )

            embed.add_field(
                name ='.create <liste des rôles> <visible/cachée>', 
                value = "L'argument de composition n'est pas valide. Arguments valides: 'visible' ou 'cachée'. \n \n Il est également probable que __la syntaxe de la liste des rôles ne soit pas juste__. Faites ``.hcreate`` pour obtenir de l'aide sur cette commande.", 
                inline = False
            )
            
            await ctx.channel.send("⚠️ **Erreur de commande** <@{}>".format(ctx.author.id))
            await ctx.send(embed=embed)
            

        if check_compo == True:
            Lroles_dispo = []
            Lroles = strRole.split(',')
            for role in Lroles:
                if role not in liste_roles:

                    embed.add_field(
                        name ='.create <liste des rôles> <visible/cachée>', 
                        value = "**Un rôle n'est pas valide.** \n Rôle non valide: ``{}`` \n \n Pour avoir de l'aide sur cette commande et sur la syntaxe des rôles, entrez la commande ``.hcreate``.".format(role), 
                        inline = False
                    )
                    
                    await ctx.channel.send("⚠️ **Erreur de commande** <@{}>".format(ctx.author.id))
                    await ctx.send(embed=embed)

                    Lroles_dispo = []
                    check_compo = False
                    break
            
                else:
                    Lroles_dispo.append(role)

            if ('Voleur' in Lroles_dispo and 'Sectaire' in Lroles_dispo) or ('Voleur' in Lroles_dispo and 'JDF' in Lroles_dispo) or ('Voleur' in Lroles_dispo and 'Imposteur' in Lroles_dispo) or ('Voleur' in Lroles_dispo and 'Traitre' in Lroles_dispo) or ('Voleur' in Lroles_dispo and is_compo == False):
                await ctx.channel.send("Impossible d'avoir un Voleur si il y a un Abominable Sectaire / Joueur de Flûte / Imposteur / Traître dans la partie, ou si la composition est cachée. Veuillez créer un autre composition.")
                Lroles_dispo = []
                check_compo = False

            if ('Imposteur' in Lroles_dispo and 'Traitre' in Lroles_dispo):
                await ctx.channel.send("Impossible d'avoir un Imposteur et un Traître dans la même partie.")
                Lroles_dispo = []
                check_compo = False
            
            if Lroles_dispo.count('Sectaire') > 1:
                await ctx.channel.send("Impossible d'avoir plusieurs sectaires dans la même partie.")
                Lroles_dispo = []
                check_compo = False


            if 'Chaperon' in Lroles_dispo and 'Chasseur' not in Lroles_dispo:
                await ctx.channel.send("Impossible d'avoir un Chaperon Rouge sans Chasseur")
                Lroles_dispo = []
                check_compo = False
      
        if check_compo == True:   

            if len(Lroles_dispo) != 0:

                embedc = discord.Embed(
                    colour = discord.Color.dark_blue(),
                    title = "Récapitulatif des rôles"
                )

                Lr = ["__{}__".format(k) for k in Lroles_dispo]
                embedc.add_field(
                    name = "Les rôles de la partie seront:",
                    value = ', '.join(Lr),
                    inline = False
                )

                embedc.add_field(
                    name = "Composition:",
                    value = "La composition sera ``{}``".format(compo),
                    inline = False
                )
  
                embedc.set_author(
                    name = "LG Bot",
                    icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                )

                await ctx.channel.send("**Une partie a été créée par {.name}**".format(ctx.author))
                await ctx.channel.send(embed=embedc)
                await channels[1].send(embed=embedc)

                if in_game == False:

                    with open('games.json') as json_file: 
                        data = json.load(json_file) 

                    data.update({str(ctx.author.id):{"guild":ctx.guild.id,"Lp": [], "Lroles": [], "dicomembers": {},"idtoemoji": {},"dictemoji": {},"is_compo": is_compo,"game_started": False,"day": False,"is_enfant": False,"ancien_dead": False,"check_couple": False,"cpt_jour": 0,"can_vote": False}})
                    
                    with open('games.json', 'w') as f:
                        json.dump(data, f, indent = 4)

                with open('games.json') as jf:
                    gdata = json.load(jf)
                
                gdata[str(ctx.author.id)]["Lroles"] = Lroles_dispo

                with open('games.json', 'w') as f:
                    json.dump(gdata, f, indent=4)



                with open('guilds.json') as json_file:
                    data = json.load(json_file)
                
                data[gid]["in_game"] = True
                data[gid]["mdj"] = ctx.author.id

                with open('guilds.json', 'w') as f:
                    json.dump(data, f, indent=4)

                    

    else:
        embed.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )

        embed.add_field(
            name ='.create <liste des rôles> <visible/cachée>', 
            value = "La commande ``.setup`` n'a pas été exécutée.", 
            inline = False
        )
        
        await ctx.channel.send("⚠️ **Erreur de commande** <@{}>".format(ctx.author.id))
        await ctx.send(embed=embed)

    print(gdata[str(ctx.author.id)]["Lroles"])


@client.command()
@commands.has_any_role("Maître du Jeu")
async def inscription(ctx, action):
    # Permet d'inscrire automatiquement tout le monde à la partie.

    gid = str(ctx.guild.id)
    aid = str(ctx.author.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    in_game = data[gid]["in_game"]

    print("Commande .inscription {} exécutée à {} par {}.".format(action, datetime.now().strftime("%H:%M:%S"), ctx.author))


    embed = discord.Embed(
        colour = discord.Color.red(),
        title = "Commande Inscription"
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
            name = '🔈 Erreur: Channel vocal',
            value = "Le maître du jeu doit __obligatoirement__ se trouver dans un channel vocal pour exécuter cette commande.",
            inline = False
        )
        await ctx.channel.send("⚠️ **Erreur de commande** <@{}>".format(ctx.author.id))
        await ctx.channel.send(embed=embed)
    
    else:

        if len(channels) > 0:

            if in_game == True:

                Lj = [member for member in members if member not in dicop_name_to_emoji and str(member) != str(author)]
                recap = ["``{}``: {} \n".format(member, dicop_name_to_emoji[member]) for member in members if member in dicop_name_to_emoji]
                    
                if action == "create":

                    insc_loading = await ctx.channel.send("⚙️ Inscription des joueurs en cours... \nCette action peut prendre du temps.")

                    
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

                        with open('games.json') as f:
                            data = json.load(f)

                        data[aid]["idtoemoji"][str(member.id)] = emoji_p
                        data[aid]["dictemoji"][emoji_p] = member.id

                        # On se base par rapport à l'id d'un joueur
                        # client.get_user(member.id)
                        # Suppression de dicop_name_to_emoji
                        # Lp est un dico avec les member id en key
                        # dicomembers a des id en key

                        with open('games.json', 'w') as f:
                            json.dump(data, f, indent=4)


                        await member.add_roles(get(member.guild.roles, name="Joueurs Thiercelieux"))

                        await channels[0].send("**{}** a reçu l'emoji {}".format(member,emoji_p))

                        recap.append("``{}``: {} \n".format(member, emoji_p))

                    await ctx.channel.send("Inscription terminée")

                    await insc_loading.delete()

                    embedi = discord.Embed(
                        colour = discord.Color.gold(),
                        title = 'Inscription'
                    )
                    embedi.add_field(
                        name = "🖋️ Récapitulatif de l'inscription:",
                        value = ''.join(recap),
                        inline = False
                    )
                    embedi.set_author(
                        name = "LG Bot",
                        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                    )
                    embedi.set_footer(
                        text = 'Pour retirer un membre de cette liste entrez la commande .remove <nom#xxxx>'
                    )

                    await ctx.channel.send(embed=embedi)

                
                elif action == 'clear':

                    print("clear")

                    if len(dicop_name_to_emoji) == 0:
                        await ctx.channel.send("Il n'y a personne d'inscrit")

                    else:
                        dicop_id_to_emoji = {}
                        dicop_name_to_emoji = {}
                        dicop_emoji = {}

                        await ctx.channel.send("La liste des inscriptions a été réinitialisée.")
                    

                else:
                    embed.add_field(
                        name ='✏️ Erreur: Argument invalide', 
                        value = "L'argument est invalide. Veuillez vérifier que l'argument est soit 'create' ou 'clear'.", 
                        inline = False
                    )

                    await ctx.channel.send("⚠️ **Erreur de commande** <@{}>".format(ctx.author.id))
                    await ctx.send(embed=embed)

            else:
                embed.add_field(
                    name = '🔧 Erreur: Pas de partie créee',
                    value = "La commande ``.create`` n'a pas été exécutée. Veuillez créer une partie avant d'inscrire les joueurs. Vous pouvez toujours changer les rôles en exécutant la commande create à nouveau.",
                    inline = False
                )
                
                await ctx.channel.send("⚠️ **Erreur de commande** <@{}>".format(ctx.author.id))
                await ctx.channel.send(embed=embed)

        else:
            embed.add_field(
                name = "⚙️ Erreur: Les salons n'ont pas été mis en place",
                value = "La commande ``.setup`` n'a pas été exécutée. La commande ``.create`` est également nécessaire à l'exécution de cette commande.",
                inline = False
            )

            await ctx.channel.send("⚠️ **Erreur de commande** <@{}>".format(ctx.author.id))
            await ctx.channel.send(embed=embed)
    


@client.command()
@commands.has_any_role("Maître du Jeu")
async def remove(ctx, *, member : discord.User):
    
    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
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
    await ctx.channel.send("{} a été retiré de la liste des inscrits.".format(user_del))
    print("ok")

    embed = discord.Embed(
        colour = discord.Color.gold(),
        title = 'Inscription'
    )
    embed.add_field(
        name = "🖋️ Récapitulatif de l'inscription:",
        value = ''.join(rrecap),
        inline = False
    )
    embed.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )


    if user_del == None:
        ctx.channel.send("ERREUR: Cette personne n'est pas dans la liste des inscrits.")

    else:
        await ctx.channel.send(embed=embed)


@client.command()
@commands.has_any_role("Maître du Jeu")
async def joueurs(ctx):
#Affiche la liste de tous les rôles

    print("Commande .liste exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), ctx.author))

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
        gdata = json.load(gf)
    
    dicop_id_to_emoji = gdata[aid]["idtoemoji"]

    recap = []
    if len(dicop_id_to_emoji) == 0:
        await ctx.channel.send("Pas encore d'inscrits.")
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
            title = "Informations partie"
        )
        embed.add_field(
            name = "📰 Liste des joueurs:",
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

    user = ctx.author

    if ctx.channel.type is discord.ChannelType.private:
        pass
    else:
        await ctx.channel.send("<@{.id}> La liste des rôles va vous être envoyée par MP.".format(user))

    def Ldivide(L,n):

        for i in range(0, len(L), n):  
            yield L[i:i + n]

    LrV = list(Ldivide(LrVillage,(len(LrVillage)//2)+1))
    LrG = list(Ldivide(LrLG, len(LrLG)))
    LrS = list(Ldivide(LrSolo, len(LrSolo)))
    LrA = list(Ldivide(LrAutre, len(LrAutre)))

    Lall = [LrV,LrG,LrS,LrA]


    for Lgr in Lall:

        for L in Lgr:

            if Lgr == LrV:
                ecolour = discord.Color.green()
                etitle = "🏘️ Rôles du Village"

            elif Lgr == LrG:
                ecolour = discord.Color.red()
                etitle = "🐺 Rôles Loups Garous"

            elif Lgr == LrS:
                ecolour = discord.Color.default()
                etitle = "🗡️ Rôles Solo"

            elif Lgr == LrA:
                ecolour = discord.Color.from_rgb(254,254,254)
                etitle = "❓ Rôles Autre"

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
                    value = "``{}``".format(desc_roles[L[i]]),
                    inline = False
                )

            await user.send(embed=embed)

    print("Commande rôles terminée")


@client.command()
@commands.has_any_role("Maître du Jeu")
async def start(ctx, state_couple):
#Commande de départ

    gid = str(ctx.guild.id)
    aid = str(ctx.author.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    in_game = data[gid]["in_game"]

    with open('games.json') as gf:
        gdata = json.load(gf)

    Lroles_dispo = gdata[aid]["Lroles"]
    dicop_id_to_emoji = gdata[aid]["idtoemoji"]

    
    print("[{}] Commande .start {} exécutée par {}".format(datetime.now().strftime("%H:%M:%S"), state_couple, ctx.author))

    annoncef = []
    is_sect = False
    ecolour = discord.Color.red()

    # J'ai la flemme là mais je trouverais un meilleur moyen de faire ça
    # On peut pas write des emojis dans des .txt wtf

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


    if state_couple == 'couple' or state_couple == 'non':
        c_check = '✅'
    else:
        c_check = '❌'

    if roles_check == '✅' and ins_check == '✅' and create_check == '✅' and channels_check == '✅' and c_check == '✅':
        ecolour = discord.Color.green()

    embed_check = discord.Embed(
        title = "Vérification du lancement",
        colour = ecolour
    )

    embed_check.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed_check.add_field(
        name = "🗒️ Récapitulatif",
        value = "\n ``Commande .setup bien exécutée:`` {} \n \n ``Commande .create bien exécutée:`` {} \n \n ``Commande .inscription bien exécutée:`` {} \n \n ``Même nombre de rôles que de participants:`` {} \n ``({} rôles et {} participants)`` \n \n ``Paramètre du couple aléatoire correct:`` {} \n ``Paramètre entré pour la partie:`` **{}**".format(channels_check, create_check, ins_check, roles_check, len(Lroles_dispo), len(dicop_name_to_emoji), c_check, state_couple),
        inline = False
    )

    await ctx.channel.send(embed=embed_check)

    if roles_check == '✅' and ins_check == '✅' and create_check == '✅' and channels_check == '✅' and c_check == '✅' and game_started == False:
    

        await channels[1].purge(limit=50)
        #On doit faire int parce que nbplayers est un string

        #Check si on a bien entrer le bon nombre de rôles

        author = str(ctx.author)
        mdj = ctx.author

        channel = mdj.voice.channel
        members = channel.members

        members = [user for user in members if str(user) != author]
        #Enlève le MJ de la liste des joueurs

        start_time = time.time()


        await channels[1].purge(limit=50)
        await channels[2].purge(limit=50)
        

        print("Partie commencée")
        await ctx.channel.send("Une partie a commencé")

        if is_compo == False:
            await channels[1].send("_Composition cachée_")
        else:
            await channels[1].send("**Les rôles sont : **")

            embedaf = discord.Embed(
                title = "Informations partie",
                colour = discord.Color.from_rgb(50,50,50)
            )
        
            Lroles_final = list(dict.fromkeys(Lroles_dispo))
            Laff = ["``{}`` ({}) \n".format(trad_roles[k], Lroles_dispo.count(k)) if k in trad_roles else "``{}`` ({}) \n".format(k, Lroles_dispo.count(k)) for k in Lroles_final]


            if state_couple == "couple" or state_couple == "Couple":
                Laff.append("\n _+1 couple aléatoire._")
            elif 'Cupidon' in Lroles_dispo:
                Laff.append("\n _+1 couple._")
        

            embedaf.add_field(
                name = "Liste des rôles:",
                value = ''.join(Laff),
                inline = False
            )
            embedaf.set_author(
                name = "LG Bot",
                icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
            )

            print("ok")

            await channels[1].send(embed=embedaf)

        await ctx.channel.send("**Le maître de jeu est** {}.".format(author))
        await ctx.channel.send("**Les partcipants sont: **")

        compteur = 0

        Lroles_game = [k for k in Lroles_dispo]
        # Distribution des rôles

        for member in members:
        #Grosse boucle qui permet d'initialiser l'état des joueurs
            
            if str(member) != str(author):

                print(Lroles_game)
                irole = rdm.randint(0,len(Lroles_game)-1)
                role_given = Lroles_game[irole]
                Lroles_game.pop(irole)
                #Choisi un rôle au hasard et le retire de la liste
                
                if role_given in trad_roles:
                    await ctx.channel.send("{} a le rôle __{}__".format(member, trad_roles[role_given]))
                else:
                    await ctx.channel.send("{} a le rôle __{}__".format(member, role_given))

                if role_given in dicoroles:
                    if role_given == "PF" or role_given == "Chaman" or role_given == "Jaloux" or role_given == "Oeil":
                        await channels[dicoroles[role_given]].set_permissions(member, overwrite=can_see)
                    else:
                        await channels[dicoroles[role_given]].set_permissions(member, overwrite=can_talk)

                    if role_given == "IPDL" or role_given == 'LGB':
                        await channels[8].set_permissions(member, overwrite=can_talk)

                #Donne les permissions nécéssaires pour chaque joueur en fonction de son rôle (utilise le dictionnaire)
                
                embedr = discord.Embed(
                    title = "Disctribution des rôles",
                    colour = discord.Color.red()
                )

                try:
                    if role_given in trad_roles:
                        ename = "Ton rôle est: __{}__".format(trad_roles[role_given])
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
                    ctx.channel.send("{.name} n'a pas ses messages privés ouverts.".format(member))

                annoncef.append("``{0.name}`` ({1}) a le rôle __{2}__ \n".format(member, dicop_name_to_emoji[member], role_given))
                
                gdata[aid]["Lp"][str(member.id)] = [
                    str(member),                            # 0: joueur
                    role_given,                             # 1: rôle
                    'Non',                                  # 2: couple
                    'Non',                                  # 3: maitre/enfant
                    'Non',                                  # 4: charmé
                    'Non',                                  # 5: secte
                    'Non',                                  # 6: infecté
                    'Non',                                  # 7: imposteur
                    'Non',                                  # 8: rôle imposteur (LG)
                    'Non',                                  # 9: rôle traître
                    'Non',                                  # 10: peut voter
                    dicop_id_to_emoji[str(member.id)]       # 11: emoji joueur
                ]   
          
                gdata[aid]["dicomembers"][str(member.id)] = compteur
                compteur += 1

                if role_given == 'Sectaire':
                    membersect = member

                if role_given == 'Traitre':
                    membertraitre = member

                if role_given == 'Imposteur':
                    memberimp = member


                print('Terminé {}'.format(member))


        if 'Traitre' in Lroles_dispo:
            
            Lroles_traitre = [k for k in liste_roles if (k in liste_village and k not in Lroles_dispo)]
            print(Lroles_traitre)
            role_traitre = rdm.choice(Lroles_traitre)

            argr = role_traitre
            if role_traitre in trad_roles:
                argr = trad_roles[role_traitre]
            await membertraitre.send("Le rôle qui vous a été atribué est: **{}**".format(argr))
            await ctx.channel.send("Le Traître **({})** a le rôle __{}__.".format(membertraitre, argr))
            annoncef.append("\n Le traître (``{0.name}``) a le rôle {1} \n".format(membertraitre, argr))

            if role_traitre in dicoroles:
                await channels[dicoroles[role_traitre]].set_permissions(member, overwrite=can_talk)

            gdata[aid]["Lp"][str(membertraitre.id)][9] = role_traitre


        if 'Imposteur' in Lroles_dispo:

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

            embed_panel.set_author(name = "Panel de choix Imposteur")
            embed_panel.add_field(
                name ="Choix de l'imposteur",
                value = "Vous avez **30 secondes** pour choisir un rôle, sinon il vous sera attribué aléatoirement. \nRéagissez à '🥇' pour choisir le rôle **__{}__**. \nRéagissez à '🥈' pour choisir le rôle **__{}__**.".format(arg1,arg2),
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
                await memberimp.send("Vous avez choisi le rôle **{}**".format(argrole))
            except asyncio.TimeoutError:
                roleimp = rdm.choice(list(dicoimp.values()))
                argrole = roleimp
                if roleimp in trad_roles:
                    argrole = trad_roles[roleimp]
                await memberimp.send("Vous n'avez pas répondu à temps un rôle vous a été attribué au hasard. Votre rôle est: **{}**".format(argrole))
            finally:
                await channels[0].send("L'Imposteur a choisi le rôle **{}**".format(roleimp))
                annoncef.append("\n L'imposteur ({0.name}) a choisi le rôle **{1}**".format(memberimp, roleimp))
                if roleimp in dicoroles:
                    await channels[dicoroles[roleimp]].set_permissions(memberimp, overwrite=can_talk)
                    if roleimp in liste_LG:
                        gdata[aid]["Lp"][str(memberimp.id)][8] = 'LG'
                        if roleimp == 'LGB' or roleimp == 'Infect':
                            await channels[8].set_permissions(memberimp, overwrite=can_talk)
                await reaction.message.delete()

        # A FINIR/FIX
        """
        if "Sectaire" in Lroles_dispo:
            Ltemps = [k for k in Lp]
            pop_sect = int(nbp/2)
            sect = []
            stoploop = time.time() + 30 
            while len(sect) != pop_sect:
                irdm = rdm.randint(0,len(Ltemps)-1)

                if time.time() > stoploop:
                    await ctx.message.send("La création de la liste des personnes à tuer pour le sectaire a échouée. Veuillez la créer manuellement.")
                    break

                if Ltemps[irdm][1] != 'Sectaire':
                    sect.append(Ltemps[irdm][3])
                    Ltemps.pop(irdm)
                    gdata[aid]["Lp"][irdm][8] = "Secte"
            
            await ctx.channel.send("Liste des joueurs à tuer pour le sectaire: **{}**.".format(', '.join(sect)))
            await membersect.send("Liste des joueurs à tuer: {}.".format(', '.join(sect)))

            annoncef.append("\n Liste des membres à tuer pour le Sectaire: ``{}`` \n".format(', '.join(sect)))
        """
            
        temps1 = (time.time() - start_time)
        # await ctx.channel.send("Commande exécutée en {} secondes".format(temps1))

        if state_couple == 'couple':

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
            await amant1.send("Tu es en couple avec {}".format(amant2))
            await amant2.send("Tu es en couple avec {}".format(amant1))
            print("Amant 1: {}, Amant 2: {}".format(amant1,amant2))
            await ctx.channel.send("Amant 1: {}, Amant 2: {}".format(amant1,amant2))

            annoncef.append("\n❤️ Les amants sont: ``{0.name}`` et ``{1.name}``".format(amant1, amant2))


        embed = discord.Embed(
            colour = discord.Color.gold(),
            title = "Informations partie"
        )
        embed.add_field(
            name = "Distribution des rôles",
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

        with open('games.json', 'w') as f:
            json.dump(data, f, indent=4)

        await menu(ctx, ctx.author)

    
    else:

        embede = discord.Embed(
            colour = discord.Color.default(),
            title = "Erreur de lancement de partie:"
        )

        embede.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )

        embede.add_field(
            name ="Un ou plusieurs paramètres ne sont pas respectés", 
            value = "Veuillez vérifier le lancement de la partie par rapport au récapitulatif ci-dessus.", 
            inline = False)

        await ctx.channel.send(embed=embede)


@client.command()
@commands.has_any_role("Maître du Jeu")
async def fmenu(ctx):
    await menu(ctx)

# Commande pour forcer l'apparition du menu en cas de bug

async def menu(ctx):

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)
    
    aid = str(data[gid]["mdj"])

    with open('games.json') as gf:
        gdata = json.load(gf)

    game_started = gdata[aid]["game_started"]
    day = gdata[aid]["day"]

    panel = discord.Embed(
            colour = discord.Color.green()
        ) 

    emojis_action = ["🐺", "🔪", "👒", "🔇", "🔊", "🌙", "🧒", "❤️", "💤", "🕵️", "🎺", "🌞","🛑","📔"]

    if game_started == False:    # ATTENTION NE PAS OUBLIER DE CHANGER EN FALSE

        await ctx.channel.send("La partie n'a pas encore commencé. Le menu n'est pas encore disponible.")

    else:

        if day == True:
            panel.set_author(
                name="Menu d'interaction jour"
            )
            panel.add_field(
                name='🔪 Tuer une personne',
                value='Cette reaction ouvre le panel de choix pour tuer une personne.',
                inline=False
            )
            if 'IPDL' in Lroles_dispo:
                panel.add_field(
                    name='🐺 Infecter une personne',
                    value='La personne choisie sera LG à la nuit prochaine.',
                    inline=False
                )
            if 'Servante' in Lroles_dispo:
                panel.add_field(
                    name='👒 Action de la Servante',
                    value="Cette reaction fait à la fois l'action voleur et l'action kill",
                    inline=False
                )
            panel.add_field(
                name='🔇 Mute le village',
                value='Permet de mute tout le monde, notamment avant le vote.',
                inline=False
            )
            panel.add_field(
                name='🔊 Demute le village',
                value='Permet de demute tout le monde (fin de partie).',
                inline=False
            )
            panel.add_field(
                name='🌙 Passer à la nuit',
                value='Cette reaction fait changer le village de cycle.',
                inline=False
            )
            panel.add_field(
                name='📔 Lancer un vote',
                value='Cette reaction lancera un vote. Les instructions seront indiquées.',
                inline=False
            )
            panel.add_field(
                name='🛑 Arrêter la partie',
                value='Cette reaction arrête completement la partie en cours',
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
                name="Menu d'interaction nuit"
            )
            if 'Enfant' in Lroles_dispo:
                panel.add_field(
                    name="🧒 Assigner un maître à l'Enfant",
                    value="Quand le maître va mourir l'Enfant passera automatiquement LG.",
                    inline=False
                )
            if 'Cupidon' in Lroles_dispo:    
                panel.add_field(
                    name="❤️ Mettre en couple les personnes désignées par Cupidon",
                    value="Les amants ainsi que Cupidon auront accès à un channel texte.",
                    inline=False
                )
            if 'Noctambule' in Lroles_dispo:    
                panel.add_field(
                    name="💤 Choisir la personne affectée par le Noctambule",
                    value="La personne visée ne pourra pas utiliser son pouvoir cette nuit.",
                    inline=False
                )
            if 'Voleur' in Lroles_dispo:
                panel.add_field(
                    name="🕵️ Choisir la victime du Voleur",
                    value="Les rôles seront échangés.",
                    inline=False
                )
            if 'JDF' in Lroles_dispo:
                panel.add_field(
                    name="🎺 Charmer les personnes visées par le Joueur de Flûte",
                    value="Les vicitimes auront accès à un channel pour voir les autres charmés",
                    inline=False
                )
            panel.add_field(
                name="🌞 Passer au jour",
                value="Cette reaction fait changer le village de cycle.",
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

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])

    with open('games.json') as gf:
        gdata = json.load(gf)

    game_started = gdata[aid]["game_started"]
    cpt_jour = gdata[aid]["cpt_jour"]
    day = gdata[aid]["day"]
    dicomembers = gdata[aid]["dicomembers"]
    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    Lp = gdata[aid]["Lp"]

    is_cover = False
    is_devin = False

    embed = discord.Embed(
        colour = discord.Color.red(),
        title = "Commande jour"
    )

    embed.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    if game_started == True:

        if dtime == 'nuit':

            if day == True:

                gdata[aid]["cpt_jour"] += 1
                gdata[aid]["day"] = False
         
                for memberid in dicomembers:

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
                        imember = rdm.choice(list(dicomembers.keys()))
                        await channels[8].send("La couverture du LGA cette nuit est: {}.".format(Lp[imember][1]))
                        await channels[0].send("La couverture du LGA cette nuit est: {}.".format(Lp[imember][1]))
                        if cpt_jour == 1 and 'Oeil' in Lroles_dispo:
                            await channels[23].send("La couverture du LGA cette nuit est: {}.".format(Lp[dicomembers[imember]][1]))
                        is_cover = True
                    else:
                        is_cover = True 
                

                while is_devin == False:
                    if "Devin" in Lroles_dispo:
                        imember = rdm.choice(list(dicomembers.keys()))
                        if Lp[dicomembers[imember]][1] == 'Devin':
                            pass
                        else:
                            await channels[29].send("Vous devez deviner le rôle de {}.".format(str(imember)))
                            await channels[0].send("Le Devin doit deviner le rôle de {} qui est {}.".format(str(imember),Lp[dicomembers[imember]][1]))
                            if cpt_jour == 1 and 'Oeil' in Lroles_dispo:
                                await channels[23].send("Le devin doit deviner le rôle de {}.".format(str(imember)))
                            is_devin = True
                    else:
                        break
                
                embedn = discord.Embed(
                    title = "NUIT: Le village s'endort.",
                    description = "Nous sommes à la nuit **N°{}**".format(cpt_jour),
                    colour = discord.Color.dark_blue()
                )

                embedn.set_author(
                    name = "LG Bot",
                    icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                )

                await channels[2].send(embed=embedn)

                Laffichage_day = ["``{0.name}``: {1} (Rôle: __{2}__) \n".format(client.get_user(int(idm)), dicop_id_to_emoji[idm], Lp[idm][1]) for idm in dicop_id_to_emoji]

                embed = discord.Embed(
                    title = "Informations partie",
                    colour = discord.Color.gold()
                )

                embed.add_field(
                    name = "Récapitulatif des joueurs:",
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
                
                for memberid in dicomembers:

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
                    title = "JOUR: Le village se réveille.",
                    description = "Nous sommes au jour **N°{}**".format(cpt_jour),
                    colour = discord.Color.dark_gold()
                )

                embedj.set_author(
                    name = "LG Bot",
                    icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                )

                await channels[2].send(embed=embedj)

                Laffichage_day = ["``{0.name}``: {1} (Rôle: __{2}__) \n".format(client.get_user(int(idm)), dicop_id_to_emoji[idm], Lp[idm][1]) for idm in dicop_id_to_emoji]

                embed = discord.Embed(
                    title = "Informations partie",
                    colour = discord.Color.gold()
                )

                embed.add_field(
                    name = "Récapitulatif des joueurs:",
                    value = ''.join(Laffichage_day),
                    inline = False
                )
                embed.set_author(
                    name = "LG Bot",
                    icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                )

                await channels[0].send(embed=embed)

    with open('games.json', 'w') as f:
        json.dump(gdata, f, indent=4)

    await menu(ctx)


async def action_panel(ctx, action):
    # Actions: Enfant, Voleur, Infect, Kill, Noctambule, Servante

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
        gdata = json.load(gf)

    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    dicop_emoji = gdata[aid]["dictemoji"]

    d = {'Enfant': "désigner le joueur qui sera le maître de l'enfant", 'Voleur': "désigner le joueur qui sera volé", 'Infect': "désigner le joueur qui sera infecté", 'Kill': "désigner le joueur qui va mourir", 'Noctambule': "désigner le joueur visé par le Noctambule", 'Servante': "désigner le joueur visé par la Servante"}

    embed_panel = discord.Embed(
        colour = discord.Color.green()
    )

    embed_panel.set_author(
        name = "Panel de choix action {}".format(action),
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed_panel.add_field(
        name ='Les emojis des joueurs sont rappelés chaque nuit.', 
        value = "Réagissez à un émoji joueur pour **{}**. \n \nRéagissez à l'émoji ❌ pour **annuler la commande**.".format(d[action]), 
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
        await ctx.channel.send("Vous avez mis trop de temps à répondre, commande annulée.")
        await panel.delete()
        await menu(ctx)
    else:
        if str(reaction.emoji) == non:
            await ctx.channel.send("Commande annulée")
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

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
        gdata = json.load(gf)

    dicop_id_to_emoji = gdata[aid]["idtoemoji"]
    dicop_emoji = gdata[aid]["dictemoji"]

    lc = []

    embed_panel = discord.Embed(
        colour = discord.Color.from_rgb(255,0,70)
    )

    embed_panel.set_author(
        name = "Panel de choix commande cupidon",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed_panel.add_field(
        name ='Les emojis des joueurs sont rappelés chaque nuit.', 
        value = "Réagissez aux 2 émojis joueurs pour **désigner les joueurs qui seront en couple**. \n \nRéagissez à l'émoji ❌ pour **annuler la commande**.", 
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
        await ctx.channel.send("Vous avez mis trop de temps à répondre, commande annulée.")
        await current_panel.delete()
        await menu(ctx)
    else:
        if str(reaction.emoji) == non:
            await ctx.channel.send("Commande annulée")
            await reaction.message.delete()
            await menu(ctx)
        else:
            lc.append(dicop_emoji[reaction.emoji])
            reaction.message.delete()
            await ctx.channel.send("Veuillez choisir le 2e amant")
            panel2 = await ctx.channel.send(embed=embed_panel)
            for nameid in dicop_id_to_emoji:
                if nameid not in lc:
                    await panel2.add_reaction(dicop_id_to_emoji[nameid])

            def checkCupi2(reaction, user):
                return (user == mdj) and ((str(reaction.emoji) in dicop_emoji) or str(reaction.emoji) == non) and (reaction.message.id == panel2.id)

            try:
                reaction, user = await client.wait_for("reaction_add", check=checkCupi2, timeout=30.0)
            except asyncio.TimeoutError:
                await ctx.channel.send("Vous avez mis trop de temps à répondre, commande annulée.")
                await panel2.delete()
                await menu(ctx)
            else:
                lc.append(dicop_emoji[reaction.emoji])
                await cupidon_action(reaction.message, lc)



async def cupidon_action(ctx, liste_couple):

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
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
    await client.get_user(cpl1).send("Tu es en couple avec **{.name}** \nTu as maintenant accès à un channel privé avec cette personne.".format(cpl2))
    await client.get_user(cpl2).send("Tu es en couple avec **{.name}** \nTu as maintenant accès à un channel privé avec cette personne.".format(cpl1))
    await ctx.channel.send("Liste des amants: **{}** et **{}**".format(cpl1,cpl2))
    await ctx.delete()

    with open('games.json', 'w') as f:
        json.dump(gdata, f, indent=4)
    await menu(ctx)


async def enfant_action(ctx, maitreid, enfantid):

    with open('guilds.json') as f:
        data = json.load(f)

    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
        gdata = json.load(gf)

    Lp = gdata[aid]["Lp"]

    gdata[aid]["Lp"][maitreid][3] = 'Maitre'
    gdata[aid]["Lp"][enfantid][3] = 'Enfant'

    await ctx.channel.send("{} est le maître de {}.".format(client.get_user(int(maitreid)), client.get_user(int(enfantid))))
    await ctx.delete()

    with open('games.json', 'w') as jf:
        json.dump(gdata, jf, indent=4)

    await menu(ctx)


async def voleur_action(ctx, stolenid, voleurid, step):

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
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

    await stolen_name.send("Ton rôle a été volé, tu es maintenant **Voleur**")
    await voleur_name.send("Tu as volé la personne avec le rôle **{}**".format(str(role_stolen)))
    await ctx.channel.send("{} a volé le rôle de {}, qui était {}.".format(str(voleur_name),str(stolen_name),str(role_stolen)))
    await ctx.delete()

    with open('games.json', 'w') as jf:
        json.dump(gdata, jf, indent=4)

    if step == 'Voleur':
        await menu(ctx)


async def infect_action(ctx, infectid):

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
        gdata = json.load(gf)

    Lp = gdata[aid]["Lp"]
    day = gdata[aid]["day"]

    infect_name = client.get_user("infectid")

    if day == True:
        await channels[8].set_permissions(infect_name, overwrite=can_see)
    elif day == False:
        await channels[8].set_permissions(infect_name, overwrite=can_talk)

    gdata[aid]["Lp"][infectid][6] = 'Infecté'

    await infect_name.send("Tu as été infécté, tu es maintenant dans le camp des Loup-garous.")
    await ctx.channel.send("{} a été infécté.".format(str(infect_name)))
    await ctx.delete()

    with open('games.json', 'w') as jf:
        json.dump(gdata, jf, indent=4)

    await menu(ctx)


async def charm_panel(ctx):

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
        gdata = json.load(gf)

    Lp = gdata[aid]["Lp"]
    dicop_id_to_emoji = gdata[aid]["idtoemoji"]

    lc = []

    embed_panel = discord.Embed(
        colour = discord.Color.from_rgb(255,30,100)
    )

    embed_panel.set_author(
        name = "Panel de choix commande charm",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed_panel.add_field(
        name ='Les emojis des joueurs sont rappelés chaque nuit.', 
        value = "Réagissez à un ou plusieurs émoji(s) joueur(s) pour **désigner le ou les joueurs qui seront charmés**. \n \n Réagissez à l'émoji ❌ pour **annuler la commande**.", 
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
        await ctx.channel.send("Vous avez mis trop de temps à répondre, commande annulée.")
        await current_panel.delete()
        await menu(ctx)
    else:
        if str(reaction.emoji) == non:
            await ctx.channel.send("Commande annulée")
            await reaction.message.delete()
            await menu(ctx)
        else:
            lc.append(dicop_emoji[reaction.emoji])
            await reaction.message.delete()
            await ctx.channel.send("Si vous ne souhaitez charmer qu'une seule personne, réagissez à l'émoji ❌")
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
                await ctx.channel.send("Vous avez mis trop de temps à répondre, commande annulée.")
                await panel2.delete()
                await menu(ctx)
            else:
                if reaction.emoji in dicop_emoji:
                    lc.append(dicop_emoji[reaction.emoji])
                await charm_action(reaction.message, lc)


async def charm_action(ctx, liste_charm):

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
        gdata = json.load(gf)

    Lp = gdata[aid]["Lp"]

    for memberid in liste_charm:
        gdata[aid]["Lp"][str(memberid)][4] = 'Charmé'
        await channels[4].set_permissions(member, overwrite=can_see)
        await member.send("Tu as été charmé par le Joueur de flûte.")
        await ctx.channel.send("{} a été charmé".format(str(member)))

    await ctx.delete()
    with open('games.json', 'w') as jf:
        json.dump(gdata, jf, indent=4)
    await menu(ctx)


async def kill_action(ctx, killedid, step):

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
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
        await ctx.channel.send("L'ancien a été tué une fois. Entrez cette commande à nouveau pour définitivement le tuer.")

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
            await ctx.channel.send("N'oubliez pas de tuer l'autre amant si ce n'est pas déjà fait !")  
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
                    await ctx.channel.send("{} est maintenant un LG".format(memberenf))
                    break

        await channels[3].set_permissions(member, overwrite=can_talk)
        await channels[2].set_permissions(member, overwrite=can_see)

        embed = discord.Embed(
            colour = discord.Color.default(),
            title = "Un joueur est mort !"
        )

        embed.set_thumbnail(
            url = member.avatar_url
        )

        embed.set_author(
            name = "LG Bot",
            icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
        )

        if rolep in trad_roles:
            evalue = "Il était: ``{}``".format(trad_roles[rolep])

        else:
            evalue = "Il était: ``{}``".format(rolep)

        embed.add_field(
            name = "__{.name}__ est mort !".format(member),
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
        del gdata[aid]["dicomembers"][str(member.id)]
        

        print('OK {} est mort, il était {}'.format(str(member), rolep))

        if is_compo == True:
            
            gdata[aid]["Lroles"] = [k for k in Lroles_dispo if str(k) != str(rolep)]

            await channels[1].purge(limit=50)          
            
            embedaf = discord.Embed(
                colour = discord.Color.default(),
                title = "Informations partie"
            )

            Lroles_final = list(dict.fromkeys(Lroles_dispo))
            Laff = ["``{}`` ({}) \n".format(trad_roles[k], Lroles_dispo.count(k)) if k in trad_roles else "``{}`` ({}) \n".format(k, Lroles_dispo.count(k)) for k in Lroles_final]

            if check_couple == True:
                await Laff.append("\n _+ couple_")
            
            embedaf.add_field(
                name = "Liste des rôles:",
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

    with open('games.json', 'w') as jf:
        json.dump(gdata, jf, indent=4)

    await menu(ctx)


async def noctambule_action(ctx, victimeid, noctambuleid):

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    with open('games.json') as gf:
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

    await victime_name.send("Vous avez été victime du Noctambule **({})**. Vous ne pouvez pas utiliser votre pouvoir cette nuit.".format(noctambule_name))
    await ctx.channel.send("**{}** (rôle: __{}__) a été victime du Noctambule (*{}*)".format(victime_name, Lp[victimeid][1], noctambule_name))
    await ctx.delete()

    with open('games.json', 'w') as jf:
        json.dump(gdata, jf, indent=4)

    await menu(ctx)


async def vote_panel(ctx):

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    channel = author.voice.channel
    members = [member for member in channel.members if member is not author and str(Lp[str(member.id)][1]) != 'Mort']

    for member in members:
        try:
            await member.send("Le vote va commencé. Quand le Maître du Jeu annoncera le début du vote, vous allez devoir écrire par Message Privé avec le bot le nom de la personne. \n \n Pour voter pour quelqu'un, vous devrez écrire son nom de cette manière: **nom#xxxx**. Par exemple un vote valide est ``unnn#1091``.\n \n Pour voter blanc, vous pouvez écrire **blanc** ou **Blanc**. \n \n Vous n'aurez le droit de voter qu'une seule fois, donc faites le bon choix. De plus, si un Ange se trouve dans la partie, vous ne pouvez pas voter pour vous-même.")
        except:
            await ctx.channel.send("Le message d'information n'a pas pu être envoyé à {.name}".format(member))


    embed = discord.Embed(
        colour = discord.Color.green()
    )

    embed.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed.add_field(
        name = "Panel de lancement du vote",
        value = "Réagissez à l'émoji ⏱️ pour **lancer le compte à rebourd du vote**.\n \n Réagissez l'émoji ✅ pour **arrêter le vote**. \n \n Réagissez à l'émoji ❌ pour **annuler la commande**.",
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

        with open('guilds.json') as f:
            data = json.load(f)

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
@commands.has_any_role("Maître du Jeu","Développeur","Admin","Host")
async def purge(ctx, limit):
    await ctx.channel.purge(limit=int(limit))


@client.command()
@commands.has_any_role("Maître du Jeu")
async def crypt(ctx, pourcentage):

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])
    valuepf = data[gid]["valuepf"]

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
            name ='.crypt <pourcentage>', 
            value = "Le pourcentage est trop grand (ça doit être un entier positif inférieur ou égal à 100).", 
            inline = False
        )

    
        await ctx.send(embed=embed)

    else:
        data[gid]["valuepf"] = int(pourcentage)
        await ctx.channel.send("Pourcentage de changer une lettre pour la PF, le Chaman, le 3e Oeil et le Jaloux: **{}%**.".format(valuepf))


@client.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("<@{.id}> Erreur: il manque un argument à la commande. Faites .help pour vérifier les arguments de cette commande.".format(ctx.author))


@client.command()
@commands.has_any_role("Maître du Jeu")
async def freset(ctx):
# Reset de force
    await reset(ctx, ctx.author)


async def reset_panel(ctx, auth):

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])

    embed = discord.Embed(
        colour = discord.Color.from_rgb(85,0,25),
        title = 'Commande reset'
    )

    embed.set_author(
        name = "LG Bot",
        icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
    )

    embed.add_field(
        name = "⚠️ Ce choix n'est pas réversible !",
        value = "Attention: vous ne pouvez pas revenir en arrière si vous décidez d'arrêter la partie maintenant. \n \n Réagissez à l'émoji ✅ pour **confirmer votre choix d'arrêter la partie.** \n \n Réagissez à l'émoji ❌ pour **annuler l'arrêt de la partie.**",
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
        await ctx.channel.send("Vous avez mis trop de temps à répondre")
        await panel.delete()
        await menu(ctx)
    else:
        if str(reaction.emoji) == "❌":
            await ctx.channel.send("Commande annulée")
            await reaction.message.delete()
            await menu(ctx)
        else:
            await reset(ctx)


async def reset(ctx):
#Commande d'arrêt du jeu

    gid = str(ctx.guild.id)

    with open('guilds.json') as f:
        data = json.load(f)

    channels = [client.get_channel(k) for k in data[gid]["channels"]]
    aid = str(data[gid]["mdj"])
    mdj = client.get_user(data[gid]["mdj"])
    in_game = gdata[aid]["in_game"]

    with open('games.json') as gf:
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

        with open('guilds.json', 'w') as f:
            json.dump(data, f, indent=4)

        gdata.update({aid:{"guild":ctx.guild.id,"Lp": [], "Lroles": [], "dicomembers": {},"idtoemoji": {},"dictemoji": {},"is_compo": is_compo,"game_started": False,"day": False,"is_enfant": False,"ancien_dead": False,"check_couple": False,"cpt_jour": 0,"can_vote": False}})
                    
        with open('games.json', 'w') as f:
            json.dump(gdata, f, indent = 4)

        await ctx.channel.send("La partie est arrêtée")

    else:
        await ctx.channel.send("Aucune partie n'est en cours: simple reset des permissions")

        for member in members:
            await channels[2].set_permissions(member, overwrite=can_talk)
            await channels[3].set_permissions(member, overwrite=cant_talk)
            print("OK, {}".format(member))


client.run(bot_token)