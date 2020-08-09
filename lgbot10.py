#-*- coding:utf-8 -*-

#================================

import discord
import asyncio
import emoji
import re
import sys
import time
import os
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

#================================


"""
Rôles à tester:
- Traître

Rôles à ajouter:


Idée de rôles:
- Devin Blanc : Chaque nuit, il connaîtra le joueur qui a été désigné par les Loups-Garous, comme la Sorcière. Cependant, il connaîtra l'identité du joueur si celui-ci s'est fait sauvé par la Sorcière, par le Salvateur, ou s'il est Ancien.


Changelog update 1.10:

- Nouvelle commande inscription ✅
    - Possibilité de retirer un membre spécifique
    - Nouveau menu


- Nouvelle commande help ✅
    - Plusieurs menu 
    - Navigation entre menus 
( A FINIR (infos...) )


- Annonces des rôles ✅
    - Nouveau menu
    - Récap tous les jours
    - Intégrer les émojis dedans


- Nouveau menu d'intéraction ✅
    - Apparait de manière constante après avoir réalisé une action 
    - Change en fonction du jour ou de la nuit
        Jour (actions possibles):
        - Tuer une personne
        - Mute tout le monde (vote)
        - Passer à la nuit
        - Servante
        - Infect
        Nuit (actions possibles):
        - Enfant sauvage
        - Noctambule
        - Cupidon
        - Voleur
        - Charmer
        - Passer au jour


- Bug fix:
    - Enfant qui ne se fait pas mute/unmute du salon LG quand il meurt
    - Enfant qui devient LG même si il est mort
    - Infecté qui ne se fait pas mute/unmute du salon LG
    - Rôles du Traître (il peut en avoir un qui est dans la partie)



Update 1.11 ?

- Stocks de données
    - Toutes les infos de parties précédentes
    - Rôles, participants...

- Fiche informations joueur
    - Données stockées dans un .txt
    - Affiche le nombre de parties
    - Affiche le dernier rôle obtenu
    - Nombre de victoires (?)




# Système de logs de parties (à finir)

cr_game = []
# Liste de str qui iront dans le compte rendu de la partie
check_file = False

while check_file == False:
    file_token = rdm.randint(1000000,9999999)
    if not os.path.isfile("{}.txt".format(file_token)):
        check_file = True

print("Token de la partie: {}".format(file_token))
# Token de la partie

cr_game.append("[{}] Génération d'un token de partie: {} \n".format(datetime.now().strftime("%H:%M:%S"),file_token))
cr_game.append("\n")
"""




# ==========================================================================================================================================================



@client.event
async def on_ready():
#Fonction initiale du bot (automatique)
#Initialisation

    global channels
    
    await client.wait_until_ready()
    await client.change_presence(activity=discord.Game(name=".help (ver. 10)"))
    print('Bot connecté {0.user}'.format(client))




# ==========================================================================================================================================================



@client.event
async def on_message(ctx):
    global day, channels, valuepf, can_see, can_talk, cant_talk, Lemojis, Lroles_dispo, Lroles_voleur, Lroles_traitre, step, id_panel

    author = ctx.author
    rolemdj = 'Maître du Jeu'
    rolebot = 'LG Bot'
    is_okmsg = True

    """
    if ctx.content.startswith('.create'):
        channel = ctx.channel
        embed1 = discord.Embed(
                colour = discord.Color.red(),
                title = "Commande create"
            )
        
        embed2 = discord.Embed(
                colour = discord.Color.red(),
                title = "Commande create"
            )

        embed1.add_field(
            name = "Ajoutez la liste des rôles.",
            value = "Le format doit être comme cela: ``Role1,Role2,Role3,...`` \n Pour voir la syntaxe des rôles, réagissez à l'emoji 📖",
            inline = False
        )
        embed2.add_field(
            name = "Choix de la visibilité de la composition",
            value = "Écrivez soit ``visible`` ou ``cachée`` pour décider de la visibilité",
            inline = False
        )

        if is_channels == True:

            e1 = await ctx.channel.send(embed=embed1)
            await e1.add_reaction("📖")

            Lroles_voleur = []
            Lroles_dispo = []
            Lroles_traitre = []

            step = "Create"
            id_panel = e1.id

            def check(m):
                global Lroles_dispo

                Lroles = m.content.split(',')
                for role in Lroles:
                    if role not in liste_roles:
                        Lroles_dispo = []
                        return False
                    else:
                        Lroles_dispo.append(role)
                return m.channel == channel

            msg = await client.wait_for('message', check=check)
            s = ', '
            await channel.send('Composition de la partie: {}'.format(s.join(Lroles_dispo)))
            """

    if ctx.channel.type is discord.ChannelType.private:
        if ctx.author.bot or ctx.content.startswith('.'):
            pass
        else:
            await ctx.channel.send("Les messages privés avec le bot sont désactivés pour l'instant.")

    else:

        if len(channels) > 0:
            try:
                #On check si l'auteur est maître du jeu
                for role in author.roles:
                    if role.name == rolemdj:
                        is_okmsg = False
                        break
            except:
                pass

            
            if is_okmsg == True:
                #Cryptage du message
                msg = ctx.content
                strm = [c for c in msg]

                # 1/4 chance qu'une lettre de fasse remplacer par un des symboles ci-dessous
                for i in range(len(strm)-1):
                    if strm[i] != ' ':
                        replace = rdm.randint(1,100)
                        if replace <= valuepf:
                            strm[i] = rdm.choice(['#','?','$','%','@','§'])


                # Cas de la PF qui reçoit les msg des LG (pas LGB ni IPDL)          
                if ctx.channel == channels[8]:
                    print("check pf")
                    if day == False:     
                        await channels[9].send(''.join(strm))

                    if 'Oeil' in Lroles_dispo and cpt_jour == 1:
                        print('oui oeil')
                        await channels[23].send("({}) ".format(ctx.channel.name) + ''.join(strm))
                
                # Cas du Chaman qui reçoit le salon des morts
                elif ctx.channel == channels[3]:
                    print("check chaman")
                    await channels[20].send(''.join(strm))
                    
                    if 'Oeil' in Lroles_dispo and cpt_jour == 1:
                        print('oui oeil')
                        await channels[23].send("({}) ".format(ctx.channel.name) + ''.join(strm))

                # Cas du Jaloux qui reçoit le salon du couple
                elif ctx.channel == channels[6]:
                    print("check jaloux")
                    if day == True:
                        await channels[21].send(''.join(strm))
                    
                    if 'Oeil' in Lroles_dispo and cpt_jour == 1:
                        print('oui oeil')
                        await channels[23].send("({}) ".format(ctx.channel.name) + ''.join(strm))


                # Cas du 3e Oeil
                elif ctx.channel in channels:
                    if ctx.channel.name == 'commandes-bot' or ctx.channel.name == 'roles-de-la-game' or ctx.channel.name == 'place-du-village' or ctx.channel.name == '3e-oeil' or ctx.channel.name == 'chaman' or ctx.channel.name == 'petite-fille':
                        pass
                    else:
                        if 'Oeil' in Lroles_dispo and cpt_jour == 1:
                            print('oui oeil')
                            await channels[23].send("({}) ".format(ctx.channel.name) + ''.join(strm))
                        

        if ctx.author.bot or str(ctx.channel.type) == "private":
            pass

        else:
            # Système d'inscription

            # Système obselète: remplacé par la commande inscription
            # J'ai le seum parce que c'était chiant à faire

            if ctx.channel.name == 'inscription':
                userid = ctx.author.id

                # On sépare les mots (on réduit à 1 max)
                Lmsg = ctx.content.split(" ")
                print(Lmsg)
                if len(Lmsg) > 1:
                    await ctx.channel.send("<@{}>".format(userid) + " Message non valide, veuillez entrer un emoji valide.")
                else:
                    # Extraction de l'emoji
                    text = emoji.demojize(ctx.content)
                    text = re.findall(r'(:[^:]*:)', text)
                    list_emoji = [emoji.emojize(x) for x in text]
                    if len(list_emoji) == 0:
                        await ctx.channel.send("<@{}>".format(userid) + "Message non valide, veuillez ne mettre qu'un seul emoji.")
                    else:
                        # Liste d'émojis bannis
                        # Pour une certaine raison tester si l'émoji se trouve dans une liste d'emojis bannis ne marche pas.
                        is_banned = False
                        b_emoji = ''
                        banned_emoji = ['✅','❌','❎','⬜','🌫️','◻️','▫️','◽','🥇','🥈']
                        for banem in banned_emoji:
                            if banem in list_emoji[0] or banem == list_emoji[0]:
                                b_emoji = banem
                                is_banned = True
                                break

                        # if ('✅' in list_emoji[0]) or ('❌' in list_emoji[0]) or ('❎' in list_emoji[0]) or ('⬜' in list_emoji[0]) or ('🌫️' in list_emoji[0]) or ('◻️' in list_emoji[0]) or ('▫️' in list_emoji[0]) or ('◽' in list_emoji[0]):
                            # await ctx.channel.send("<@{}>".format(userid) + " Message non valide, cet emoji n'est autorisé.")
                        if is_banned == True:
                            await ctx.channel.send("<@{}>".format(userid) + " Message non valide, cet emoji ({}) n'est autorisé.".format(b_emoji))
                        elif list_emoji[0] in Lemojis:
                            await ctx.channel.send("<@{}>".format(userid) + " Message non valide, cet emoji ({}) est déjà pris. Veuillez en choisir un autre.".format(list_emoji[0]))
                        elif ctx.author in dicop_name_to_emoji:
                            await ctx.channel.send("<@{}>".format(userid) + " Message non valide, vous vous êtes déjà inscrit.")
                        # On test ici si c'est bien un emoji standars (pas d'émoji customs)
                        elif list_emoji[0] not in emoji.UNICODE_EMOJI:
                            await ctx.channel.send("<@{}> Message non valide, cet emoji n'est pas valide (emojis Customs interdits)".format(userid))
                        else:
                            # Réponse positive.
                            bot_response = await ctx.channel.send("<@{}>".format(userid) + " a choisi l'emoji {} pour la partie.".format(list_emoji[0]))
                            await bot_response.add_reaction(list_emoji[0])

                            # On crée les différents dictionnaires petit à petit
                            dicop_id_to_emoji[ctx.author.id] = list_emoji[0]
                            dicop_emoji[list_emoji[0]] = [ctx.author,ctx.author.id]
                            dicop_name_to_emoji[ctx.author] = list_emoji[0]
                            Lemojis.append(list_emoji[0])

                            # await ctx.channel.set_permissions(ctx.author, overwrite=can_see)
                            await ctx.author.add_roles(get(ctx.author.guild.roles, name="Joueurs Thiercelieux"))
                            # await ctx.author.remove_roles(get(ctx.author.guild.roles, name="Joueurs Thiercelieux"))

                await ctx.delete()
   
    await client.process_commands(ctx)


# ==========================================================================================================================================================


@client.event
async def on_reaction_add(reaction, user):

    global old_step, annoncef, page, liste_charm, id_panel, Lannonce_vote, step, cpt_reaction, liste_couple, enfant_name, Lp, victime_name, noctambule_name, maitre_name, stolen_name, infect_name, charm_name, imposteur_name, killed_name, voleur_name, devo_name, servante_name, panel_author, is_enfant, p_emoji, check_couple, id_vote

    r_msg = reaction.message.id

    # Event reaction

    if user.bot:
        # Si c'est un bot
        pass

    elif user == panel_author or step == 'Vote' or step == 'Imposteur' or step == "Menu" or step == 'Reset':
        print("Reaction MDJ")
        print(r_msg,id_panel)

        if r_msg == id_panel:

            print("Reaction panel")
                
            
            if step == "Create" and reaction.emoji == '📖':
                print('yo')
                await reaction.message.channel.send("Nombre de rôles: {}".format(len(liste_roles)))
                await reaction.message.channel.send(', '.join(liste_roles))
                await reaction.message.remove_reaction(reaction, user)

            elif reaction.emoji == '✅':
                
                if (maitre_name != None or len(liste_couple) != 0 or stolen_name != None or killed_name != None or infect_name != None or len(liste_charm) != 0 or victime_name != None or devo_name != None) and game_started == True:

                    if step == 'Cupidon':
                        await cupidon_action(reaction.message, reaction, user)

                    elif step == 'Enfant':
                        await enfant_action(reaction.message)

                    elif step == 'Voleur': 
                        await voleur_action(reaction.message)

                    elif step == 'Infecté':
                        await infect_action(reaction.message)

                    elif step == 'Charmé':
                        await charm_action(reaction.message)

                    elif step == 'Kill':
                        await kill_action(reaction.message)

                    elif step == 'Noctambule':
                        await noctambule_action(reaction.message)

                    elif step == 'Servante':
                        await voleur_action(reaction.message)
                        await kill_action(reaction.message)


                elif step == 'Vote':
                    
                    print('step vote validation')
                    print(Lannonce_vote)
                    await channels[-2].send("**Récapitulatif des votes:**")
                    for msg in Lannonce_vote:
                        await channels[-2].send(msg)


                elif step == "Reset":
                    await reaction.message.delete()
                    await reaction.message.channel.send("<@{.id}> **Vous avez décidé d'arrêter la partie en cours.**".format(user))
                    await reset(reaction.message)


                else:
                    await reaction.message.channel.send("ERREUR: Vous n'avez sélectionné personne.")
                    await reaction.message.remove_reaction(reaction, user)

            elif reaction.emoji == "❌":
                await reaction.message.delete()
                cpt_reaction = 0
                await reaction.message.channel.send("Commande annulée.")
                await menu(reaction.message)


            elif reaction.emoji in dicop_emoji:

                print(cpt_reaction)
                print("Reaction emoji joueur")
                cpt_reaction += 1
                p_emoji = reaction.emoji

                if ((cpt_reaction > 1) and (step =='Servante' or step == 'Enfant' or step == 'Voleur' or step == 'Infecté' or step == 'Kill' or step == 'Noctambule')) or (cpt_reaction > 2 and (step == 'Cupidon' or step == 'Charmé')):

                    if step == 'Enfant' or step == 'Voleur' or step == 'Infecté' or step == 'Kill' or step == 'Noctambule':
                        await reaction.message.channel.send("Vous ne pouvez pas ajouter d'autres personnes.")
                        for reac in reaction.message.reactions:
                            try:
                                await reaction.message.remove_reaction(reac, user)
                            except:
                                pass

                else:
                    if step == 'Cupidon':
                        print("reaction cupi")
                        liste_couple.append(dicop_emoji[reaction.emoji][0])
                        await reaction.message.channel.send("{} a été ajouté à la liste des amants".format(dicop_emoji[reaction.emoji][0]))

                    elif step == 'Enfant':
                        print("reaction enfant")
                        maitre_name = dicop_emoji[reaction.emoji][0]     
                        print(reaction.emoji, maitre_name)
                        await reaction.message.channel.send("{} a été séléctionné en dans que Maître de l'enfant".format(str(maitre_name)))

                    elif step == 'Voleur':
                        print("reaction voleur")
                        stolen_name = dicop_emoji[reaction.emoji][0]
                        print(reaction.emoji, stolen_name)      
                        await reaction.message.channel.send("{} a été séléctionné en tant que cible du Voleur".format(str(stolen_name)))

                    elif step == 'Infecté':
                        print("reaction infect")
                        infect_name = dicop_emoji[reaction.emoji][0]      
                        print(reaction.emoji, infect_name)
                        await reaction.message.channel.send("{} a été séléctionné en tant qu'infecté".format(str(infect_name)))

                    elif step == 'Charmé':
                        print("reaction charmé")
                        liste_charm.append(dicop_emoji[reaction.emoji][0])
                        await reaction.message.channel.send("{} a été ajouté à la liste des charmés".format(dicop_emoji[reaction.emoji][0]))  

                    elif step == 'Kill':
                        print("reaction kill")
                        killed_name = dicop_emoji[reaction.emoji][0]      
                        print(reaction.emoji, killed_name)
                        await reaction.message.channel.send("{} a été séléctionné en tant que personne à tuer".format(str(killed_name)))

                    elif step == 'Noctambule':
                        print('reaction noctambule')
                        victime_name = dicop_emoji[reaction.emoji][0]
                        print(reaction.emoji, victime_name)
                        await reaction.message.channel.send("{} a été séléctionné en tant que cible du Noctambule".format(str(victime_name)))

                    elif step == 'Servante':
                        print("reaction servante")
                        devo_name = dicop_emoji[reaction.emoji][0]
                        print(reaction.emoji, devo_name)
                        await reaction.message.channel.send("{} a été séléctionné en tant que cible de la Servante Dévouée".format(str(devo_name)))

            elif step == 'Imposteur':
                print("reaction imposteur")
                pimp = Lp[dicomembers[imposteur_name]]
                roleimp = dicoimp[reaction.emoji]
                await imposteur_name.send("Le rôle choisi est **{}**".format(roleimp))
                await channels[0].send("L'Imposteur a choisi le rôle **{}**".format(roleimp))

                annoncef.append("\n L'imposteur ({0.name}) a choisi le rôle **{1}**".format(imposteur_name, roleimp))

                if roleimp in dicoroles:
                    await channels[dicoroles[roleimp]].set_permissions(imposteur_name, overwrite=can_talk)
                    if roleimp in liste_LG:
                        Lp[dicomembers[imposteur_name]][10] = 'LG'
                        if roleimp == 'LGB' or roleimp == 'Infect':
                            await channels[8].set_permissions(imposteur_name, overwrite=can_talk)
                await reaction.message.delete()

                Lp[dicomembers[imposteur_name]][11] = roleimp

            elif reaction.emoji in emojis_action:
                
                if step == "Menu":

                    if reaction.emoji == "❤️":
                        await cupidon_panel(reaction.message)

                    elif reaction.emoji == "🧒":
                        await enfant_panel(reaction.message)

                    elif reaction.emoji == "🕵️":
                        await voleur_panel(reaction.message)

                    elif reaction.emoji == "🐺":
                        await infect_panel(reaction.message)
                        
                    elif reaction.emoji == "🎺":
                        await charm_panel(reaction.message)

                    elif reaction.emoji == "👒":
                        await servante_panel(reaction.message)

                    elif reaction.emoji == "💤":
                        await noctambule_panel(reaction.message)

                    elif reaction.emoji == "🔪":
                        await kill_panel(reaction.message)

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

                    await reaction.message.delete()

            else:
                if step == "help":
                    pass
                else:
                    await reaction.message.remove_reaction(reaction, user)

        elif step == 'Vote':
            print('ok reaction mp vote')
            if reaction.emoji in dicop_emoji:
                await user.send("Vous avez voté pour {}".format(dicop_emoji[reaction.emoji][0]))
                await channels[0].send("__{}__ a voté pour **{}**".format(user, dicop_emoji[reaction.emoji][0]))
                Lannonce_vote.append("<@{}> a voté pour <@{}>".format(user.id, dicop_emoji[reaction.emoji][0]))
            else:
                await user.send("Vous avez voté blanc")
                await channels[0].send("__{}__ a voté **blanc**".format(user))
                Lannonce_vote.append("<@{}> a voté **blanc**".format(user.id))

            await reaction.message.delete()

    else:

        if reaction.emoji == "1️⃣":
            await manage_help(reaction.message, 1, user)
        elif reaction.emoji == "2️⃣":
            await manage_help(reaction.message, 2, user)
        elif reaction.emoji == "3️⃣":
            await manage_help(reaction.message, 3, user)
        elif reaction.emoji == "❌":
            await reaction.message.delete()

        elif game_started == True:
            await reaction.message.remove_reaction(reaction, user)

# ==========================================================================================================================================================


@client.event
async def on_reaction_remove(reaction,user):

    global id_panel, step, cpt_reaction, liste_couple, enfant_name, Lp, maitre_name, stolen_name, infect_name, killed_name, voleur_name, panel_author, victime_name, liste_charm, devo_name

    r_msg = reaction.message.id

    if user.bot:
        pass
    else:
        print('removed reaction')
        if (r_msg == id_panel) and (reaction.emoji in dicop_emoji):

            if reaction.emoji == '✅':
                pass

            else:
                cpt_reaction -= 1
                if step == 'Cupidon':
                    await reaction.message.channel.send("{} a été retiré de la liste des amants.".format(dicop_emoji[reaction.emoji][0]))
                    liste_couple.remove(dicop_emoji[reaction.emoji][0])

                elif step == 'Enfant':
                    await reaction.message.channel.send("{} n'est plus séléctionné.".format(maitre_name))
                    maitre_name = None

                elif step == 'Voleur':
                    await reaction.message.channel.send("{} n'est plus séléctionné.".format(stolen_name))
                    stolen_name = None

                elif step == 'Infecté':
                    await reaction.message.channel.send("{} n'est plus séléctionné.".format(infect_name))
                    infect_name = None

                elif step == 'Charmé':
                    await reaction.message.channel.send("{} n'est plus séléctionné.".format(dicop_emoji[reaction.emoji][0]))
                    liste_charm.remove(dicop_emoji[reaction.emoji][0])

                elif step == 'Kill':
                    await reaction.message.channel.send("{} n'est plus séléctionné.".format(killed_name))
                    killed_name = None

                elif step == 'Noctambule':
                    await reaction.message.channel.send("{} n'est plus séléctionné.".format(victime_name))
                    victime_name = None

                elif step == 'Servante':
                    await reaction.message.channel.send("{} n'est plus séléctionné.".format(devo_name))
                    devo_name = None


# ==========================================================================================================================================================

@client.command()
async def help(ctx):
#Commande d'aide utilisateur
#Affiche un embed

    global page, embed1, embed2, embed3, dico_embed, step, id_panel, old_step

    page = 1

    author = ctx.author
    print("Commande .help exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), author))
    

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

    # rea1 = await author.send(embed=embed1)
    # await ctx.channel.send("<@{0.id}> Le menu d'aide vous a été envoyé en message privé.".format(author))

    """
    rea1 = await ctx.channel.send(embed = embed1)
    await rea1.add_reaction("1️⃣")
    await rea1.add_reaction("2️⃣")
    await rea1.add_reaction("3️⃣")
    await rea1.add_reaction("❌")
    """
    # Help menu page scrolling stuff, will probably never use


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


    dico_embed = {
        1: embed1,
        2: embed2,
        3: embed3
    }

    # id_panel = rea1.id


async def manage_help(ctx, nb, user):
    # Help menu page scrolling stuff, will probably never use

    global page, step, id_panel

    page = nb

    await ctx.delete()

    # reaem = await user.send(embed = dico_embed[page])
    reaem = await ctx.channel.send(embed = dico_embed[page])
    await reaem.add_reaction("1️⃣")
    await reaem.add_reaction("2️⃣")
    await reaem.add_reaction("3️⃣")
    await reaem.add_reaction("❌")

    id_panel = reaem.id
    


# ==========================================================================================================================================================


@client.command()
@commands.has_any_role("Maître du Jeu")
async def test(ctx):

    eliste = rdm.sample(list(emoji.UNICODE_EMOJI), 3)
    for elm in eliste:
        await ctx.channel.send(elm)


# ==========================================================================================================================================================


@client.command()
@commands.has_any_role("Maître du Jeu")
async def info(ctx):
    global is_info

    if is_info == True:
        is_info = False
        await ctx.channel.send("Le bot n'affichera pas les informations de la partie.")
    else:
        is_info = True
        await ctx.channel.send("Le bot affichera les informations de la partie.")


# ==========================================================================================================================================================



@client.command()
@commands.has_any_role("Maître du Jeu")
async def setup(ctx):

    global channels, in_game, is_channels, text_channel_list, cant_talk, inscription_chan
    author = ctx.author
    print("Commande .setup exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), author))


    guild = ctx.guild
    text_channel_list = []

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

        overwrites_inscription = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True, mention_everyone=False, attach_files=False, embed_links=False)
        }
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, read_message_history=False, mention_everyone=False, attach_files=False, embed_links=False)
        }
        overwrites_pdv = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False, read_message_history=True, mention_everyone=False, attach_files=False, embed_links=False)
        }

        """
        if "inscription" not in text_channel_list:
            await guild.create_text_channel("inscription", category=category, overwrites=overwrites_pdv, topic="Les inscriptions se font ici.")

        inscription_chan = client.get_channel((discord.utils.get(guild.text_channels, name="inscription")).id)
        await inscription_chan.purge(limit=50)
        await inscription_chan.send("**Règles pour l'inscription:**")
        await inscription_chan.send("Pour vous inscrire vous devrez poster une emote discord (pas d'emote custom). Le bot vous préviendra si l'emote est déjà utilisée. Vous n'avez pas besoin de retenir votre emote, elle ne sert que au MDJ.")
        banned_emoji = ['✅','❌','❎','⬜','🌫️','◻️','▫️','◽','🥇','🥈']
        listToStr = ' '.join([str(elem) for elem in banned_emoji])
        await inscription_chan.send("Emojis bannis: {}".format(listToStr)) 
        """

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
    
    channels = [client.get_channel(id) for id in channels]
    print(channels)

    await channels[0].send("Setup terminé.")
    await channels[0].send("Pour commencer une partie, entrez la commande **.inscription create** lorsque tout les participants se trouvent dans le channel vocal.")

    is_channels = True



# ==========================================================================================================================================================



@client.command()
@commands.has_any_role("Maître du Jeu")
async def delete(ctx):

    global channels

    guild = ctx.guild

    name = 'Les Loups Garous de Thiercelieux'
    category = discord.utils.get(ctx.guild.categories, name=name)

    for channel in guild.text_channels:
        if str(channel.category) == name:
            await channel.delete()
    
    await category.delete()

    channels = []
    

# ==========================================================================================================================================================


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
        value = "Les paramètres de la commande sont: une liste ``<liste de rôles>`` et un paramètre de visibilité de la composition ``<visible/cachée>``. Ce paramètre sert à dire si l'on veut que les joueurs sachents la composition ou non. Certains rôles sont interdits avec une composition cachée. \n \n La syntaxe de la liste des rôles doit être comme cela: **Role1,Role2,...,Role**. Après on peut entrer l'argument de visibilité après un espace. On arrive donc à: ``.create Role1,Role2,...,Role visible`` par exemple. \n \n La syntaxe des rôles est également importantes. Certains d'entre eux ont une syntaxe raccourcie pour faciliter la création de partie. Les syntaxes des rôles se trouvent ci-dessous. Aussi, si l'on veut avoir plusieurs fois le même rôles dans la partie, il faudra renseigner plusieurs fois ce rôle (voir exemple ci-dessous).",
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


# ==========================================================================================================================================================

@client.command()
@commands.has_any_role("Maître du Jeu")
async def create(ctx, strRole, compo):
#Permet de créer une liste de rôles pour 1 partie

    global Lroles_dispo, Lroles_voleur, Lroles_traitre, in_game, is_channels, is_compo, inscription_chan, cr_game

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

    if is_channels == True:

        if compo == 'visible' or compo == 'Visible':
            is_compo = True
            check_compo = True
        elif compo == 'cachée' or compo == 'Cachée':
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
            Lroles_voleur = []
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
                    Lroles_voleur = []
                    Lroles_traitre = []
                    check_compo = False
                    break
            
                else:
                    Lroles_dispo.append(role)

            if ('Voleur' in Lroles_dispo and 'Sectaire' in Lroles_dispo) or ('Voleur' in Lroles_dispo and 'JDF' in Lroles_dispo) or ('Voleur' in Lroles_dispo and 'Imposteur' in Lroles_dispo) or ('Voleur' in Lroles_dispo and 'Traitre' in Lroles_dispo) or ('Voleur' in Lroles_dispo and is_compo == False):
                await ctx.channel.send("Impossible d'avoir un Voleur si il y a un Abominable Sectaire / Joueur de Flûte / Imposteur / Traître dans la partie, ou si la composition est cachée. Veuillez créer un autre composition.")
                Lroles_dispo = []
                Lroles_voleur = []
                Lroles_traitre = []
                check_compo = False

            if ('Imposteur' in Lroles_dispo and 'Traitre' in Lroles_dispo):
                await ctx.channel.send("Impossible d'avoir un Imposteur et un Traître dans la même partie.")
                Lroles_dispo = []
                Lroles_voleur = []
                Lroles_traitre = []
                check_compo = False
            
            if Lroles_dispo.count('Sectaire') > 1:
                await ctx.channel.send("Impossible d'avoir plusieurs sectaires dans la même partie.")
                Lroles_dispo = []
                Lroles_voleur = []
                Lroles_traitre = []
                check_compo = False


            if 'Chaperon' in Lroles_dispo and 'Chasseur' not in Lroles_dispo:
                await ctx.channel.send("Impossible d'avoir un Chaperon Rouge sans Chasseur")
                Lroles_dispo = []
                Lroles_voleur = []
                Lroles_traitre = []
                check_compo = False
      
        if check_compo == True:   
            if 'Imposteur' in Lroles_dispo:
                for role in liste_roles:
                    banned_roles = ['Traitre', 'Sectaire', 'Chasseur', 'Soeur', 'Frère', 'Voleur', 'Cupidon', 'Enfant']
                    if role in Lroles_dispo or role in banned_roles or (role == 'Chaperon' and 'Chasseur' not in Lroles_dispo):
                        pass
                    else:
                        Lroles_voleur.append(role)
                print(Lroles_voleur)
                
            if 'Traitre' in Lroles_dispo:
                for role in liste_roles:
                    banned_roles = ['Traitre', 'Sectaire', 'Chasseur', 'Soeur', 'Frère', 'Voleur', 'Cupidon', 'Enfant']
                    if role in liste_village and (role in Lroles_dispo or role in banned_roles):
                        pass
                    else:
                        Lroles_traitre.append(role) 
                print(Lroles_traitre)

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

                await ctx.channel.send(embed=embedc)
                await channels[1].send(embed=embedc)

                in_game = True

                #cr_game.append("[{}] Liste des rôles: {} \n".format(datetime.now().strftime("%H:%M:%S"),str_r))
                #cr_game.append("\n")

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

# ==========================================================================================================================================================


@client.command()
@commands.has_any_role("Maître du Jeu")
async def inscription(ctx, action):
    # Permet d'inscrire automatiquement tout le monde à la partie.

    global is_channels, inscription_chan, dicop_name_to_emoji, dicop_id_to_emoji, dicop_emoji, Lemojis, cr_game

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

                L_j_temp = [k for k in members]
                Lj = []
                L_j_tempstr = [str(k) for k in members]
                recap = []

                pprint(L_j_tempstr)

                for member in L_j_temp:
                    print(member)
                    if member in dicop_name_to_emoji:
                        print("déjà inscrit enlevé {}".format(member))
                        recap.append("``{}``: {} \n".format(member, dicop_name_to_emoji[member]))
                    elif str(member) == str(author):
                        print("author enlevé {}".format(member))
                    else:
                        Lj.append(member)
                
                print("ok ljtemp")
                    
                if action == "create":

                    insc_loading = await ctx.channel.send("Inscription des joueurs en cours...")
                    
                    print("create")

                    is_there_banned = False
                    # ex_liste = ['◽','🥇','🥈','🐝','🚙','🛏️','😎','😆','😔','👏']

                    while True:
                        eliste = rdm.sample(list(emoji.UNICODE_EMOJI), len(Lj))
                        #eliste = rdm.sample(ex_liste, len(Lj))
                        print(eliste)
                        banned_emojis = ['✅','❌','❎','⬜','🌫️','◻️','▫️','◽','🥇','🥈',"🐺", "🔪", "👒", "🔇", "🔊", "🌙", "🧒", "❤️", "💤", "🕵️", "🎺", "🌞","1️⃣","2️⃣","3️⃣","🛑"]
                        for bem in banned_emojis:
                            print(bem)
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

                        # await inscription_chan.set_permissions(member, overwrite=cant_talk)
                        await channels[1].set_permissions(member, overwrite=can_see)
                        await channels[2].set_permissions(member, overwrite=can_talk)
                        print(member)
                        if str(member) != str(author):
                            L_joueurs.append(member)
                            #Liste des joueurs que l'on va réutiliser 

                            for i in range(3,30):
                                await channels[i].set_permissions(member, overwrite=cant_talk)
                            #Enlève les permissions de tous les salons pour tous les joueurs

                        print("OK perm {}".format(member))

                        emoji_p = rdm.choice(eliste)
                        eliste.remove(emoji_p)

                        print(member, emoji_p)

                        dicop_id_to_emoji[member.id] = emoji_p
                        dicop_emoji[emoji_p] = [member,member.id]
                        dicop_name_to_emoji[member] = emoji_p
                        Lemojis.append(emoji_p)

                        await member.add_roles(get(member.guild.roles, name="Joueurs Thiercelieux"))

                        await channels[0].send("**{}** a reçu l'emoji {}".format(member,emoji_p))

                        recap.append("``{}``: {} \n".format(member, emoji_p))

                        # cr_game.append("**{}** reçu l'emoji {}".format(member,emoji_p))
                    
                    # cr_game.append("\n")

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
                        Lemojis = []

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
    

# ==========================================================================================================================================================

@client.command()
@commands.has_any_role("Maître du Jeu")
async def remove(ctx, *, member):

    global dicop_name_to_emoji, dicop_id_to_emoji, dicop_emoji, Lemojis

    member_name, member_discriminator = member.split('#')

    rrecap = []
    user_del = None

    for user in dicop_name_to_emoji:

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            user_del = user
            print("ok")

        else:
            rrecap.append("``{}``: {} \n".format(user, dicop_name_to_emoji[user]))

    del dicop_emoji[dicop_name_to_emoji[user_del]]
    del dicop_name_to_emoji[user_del]
    del dicop_id_to_emoji[user_del.id]
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


# ==========================================================================================================================================================

@client.command()
@commands.has_any_role("Maître du Jeu")
async def joueurs(ctx):
#Affiche la liste de tous les rôles

    print("Commande .liste exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), ctx.author))

    global Laffichage_joueurs

    recap = []
    if len(dicop_name_to_emoji) == 0:
        await ctx.channel.send("Pas encore d'inscrits.")
    else:
        print("ok joueurs aff")
        if len(Lp) != 0:
            for name in dicop_name_to_emoji:
                fiche_player = Lp[dicomembers[name]]
                rolep = fiche_player[1]
                if str(rolep) == 'Mort':
                    pass
                else:
                    recap.append("``{}``: {} \n".format(name, dicop_name_to_emoji[name]))
        
        else:
            for name in dicop_name_to_emoji:
                recap.append("``{}``: {} \n".format(name, dicop_name_to_emoji[name]))
    
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


# ==========================================================================================================================================================



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
                ecolour = discord.Color.blue()
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

# ==========================================================================================================================================================




@client.command()
@commands.has_any_role("Maître du Jeu")
async def start(ctx, state_couple):
#Commande de départ

    global mdj, annoncef, Lroles_dispo, Lroles_voleur, L_joueurs, dicoimp, in_game, game_started, channels, Lp, dicopmembers ,can_talk, cant_talk, is_compo, mdj, is_info, panel_author, step, id_panel, imposteur_name
    
    print("Commande .start exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), ctx.author))

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

    if len(dicop_name_to_emoji) == 0:
        ins_check = '❌'
    else:
        ins_check = '✅'

    if len(dicop_name_to_emoji) == len(Lroles_dispo):
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

        panel_author = ctx.author
        
        Lroles_final = []
        #Liste de transition (voir + bas)

        await channels[1].purge(limit=50)
        await channels[2].purge(limit=50)
        

        print("Partie commencée")
        await ctx.channel.send("Une partie a commencé")

        if is_compo == True:
            await channels[1].send("**Les rôles sont : **")
        else:
            await channels[1].send("_Composition cachée_")

        embedaf = discord.Embed(
            title = "Informations partie",
            colour = discord.Color.grey()
        )
        
        Laff = []
        for i in range(0,len(Lroles_dispo)):
            if Lroles_dispo[i] not in Lroles_final:
                if is_compo == True:
                    if Lroles_dispo[i] in trad_roles:
                        Laff.append("``{}`` ({}) \n".format(trad_roles[Lroles_dispo[i]],Lroles_dispo.count(Lroles_dispo[i])))
                    else:
                        Laff.append("``{}`` ({}) \n".format(Lroles_dispo[i],Lroles_dispo.count(Lroles_dispo[i])))
                    Lroles_final.append(Lroles_dispo[i])
            elif Lroles_dispo[i] in Lroles_final:
                Lroles_final.append(Lroles_dispo[i])



        if is_compo == True:
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

        await channels[1].send(embed=embedaf)

            
            # else:
                # await channels[1].send("_Composition cachée_")
            

        #Permet de compter les rôles (sans duplica)

        if is_info == True:
            text_to_say = ["**Récapitulatif du déroulement de la partie:**","- Chaque nuit, les loup-garous vont devoir éliminer un joueur de leur choix.","- D'autres actions peuvent se produire en fonction des différents rôles.","- La composition de la partie est accessible dans le salon rôles de la game","- Durant la nuit, les loup-garous peuvent parler entre eux mais le couple ne peut pas.","- Durant le jour, c'est l'inverse.","- A chaque jour, le village devra éliminer un joueur par le vote.","- En cas d'égalité, un vote est refait parmis les villageois qui n'ont pas voter pour les cibles étant à égalité.","- Il est bien sûr déconseillé de parler dans ce channel pendant la nuit.","- Les morts seront annoncées dans ce channel.","- Pour toute question concernant votre rôle ou tout problème, n'hésitez pas à envoyer un message privé au maître du jeu.","- Vos rôles vont être distribués chacun son tour. Pas la peine de demander pourquoi vous n'avez pas eu votre rôle."]
            for txt in text_to_say:
                await channels[2].send(txt)
            await channels[2].send("- Le maître du jeu est **{}**. Bon jeu !".format(str(author)))


        await ctx.channel.send("**Le maître de jeu est** {}.".format(author))
        await ctx.channel.send("**Les partcipants sont: **")

        compteur = 0

        for member in members:
        #Grosse boucle qui permet d'initialiser l'état des joueurs
            
            if str(member) != str(author):

                print(Lroles_final)
                irole = rdm.randint(0,len(Lroles_final)-1)
                role_given = Lroles_final[irole]
                Lroles_final.pop(irole)
                #Choisi un rôle au hasard et le retire de la liste
                
                if role_given in trad_roles:
                    await ctx.channel.send("{} a le rôle __{}__".format(member, trad_roles[role_given]))
                else:
                    await ctx.channel.send("{} a le rôle __{}__".format(member, role_given))

                if role_given in dicoroles:
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
                

                Lp.append([
                    str(member),        # Lp[i][0] = joueur#xxxx
                    role_given,         # Lp[i][1] = rôle servant pour l'affichage
                    str(member.id),     # Lp[i][2] = discord id
                    member,             # Lp[i][3] = class membre
                    'Non',              # Lp[i][4] = status couple
                    'Non',              # Lp[i][5] = status maître (ou enfant)
                    role_given,         # Lp[i][6] = rôle servant pour les perms et l'annonce de victoire        
                    'Non',              # Lp[i][7] = status charmé
                    'Non',              # Lp[i][8] = status secte
                    'Non',              # Lp[i][9] = status infecté
                    dicop_id_to_emoji[member.id], # Lp[i][10] = emoji du membre
                    'Non',              # Lp[i][10] = status imposteur (LG)
                    'Non',              # Lp[i][11] = rôle imposteur
                    'Non'               # Lp[i][12] = rôle traître
                    ])             

                dicomembers[member] = compteur
                compteur += 1

                if role_given == 'Sectaire':
                    membersect = member

                if role_given == 'Traitre':
                    membertraitre = member

                if role_given == 'Imposteur':
                    memberimp = member


                print('Terminé {}'.format(member))


        if 'Traitre' in Lroles_dispo:

            print(Lroles_traitre)
            role_traitre = rdm.choice(Lroles_traitre)

            if role_traitre in trad_roles:
                await membertraitre.send("Le rôle qui vous a été atribué est: {}".format(trad_roles[role_traitre]))
                await ctx.channel.send("Le Traître **({})** a le rôle __{}__.".format(membertraitre,trad_roles[role_traitre]))
                annoncef.append("\n Le traître (``{0.name}``) a le rôle {1} \n".format(membertraitre, trad_roles[role_traitre]))
            else:
                await membertraitre.send("Le rôle qui vous a été atribué est: {}".format(role_traitre))
                await ctx.channel.send("Le Traître **({})** a le rôle __{}__.".format(membertraitre,role_traitre))
                annoncef.append("\n Le traître (``{0.name}``) a le rôle {1} \n".format(membertraitre, role_traitre))

            if role_traitre in dicoroles:
                await channels[dicoroles[role_traitre]].set_permissions(member, overwrite=can_talk)

            Lp[dicomembers[membertraitre]][12] = role_traitre


        
        if 'Imposteur' in Lroles_dispo:

            print('Imposteur')

            Lrtemp = [k for k in Lroles_voleur]
            for role in Lrtemp:
                if (role == 'Jaloux' and state_couple == 'non'):
                    Lrtemp.remove(role)
                    break

            Lrimp = rdm.sample(Lrtemp, 2)
            role_imp1 = Lrimp[0]
            role_imp2 = Lrimp[1]

            print(role_imp1,role_imp2)

            embed_panel = discord.Embed(
                colour = discord.Color.red()
            )

            print('création panel')

            if role_imp1 in trad_roles:
                await memberimp.send("Réagissez à '🥇' pour choisir le rôle **__{}__**".format(trad_roles[role_imp1]))
            else:
                await memberimp.send("Réagissez à '🥇' pour choisir le rôle **__{}__**".format(role_imp1))
            dicoimp['🥇'] = role_imp1
            print('role 1 ok')

            if role_imp2 in trad_roles:
                await memberimp.send("Réagissez à '🥈' pour choisir le rôle **__{}__**".format(trad_roles[role_imp2]))
            else:
                await memberimp.send("Réagissez à '🥈' pour choisir le rôle **__{}__**".format(role_imp2))
            dicoimp['🥈'] = role_imp2
            print('role 2 ok')

            embed_panel.set_author(name = "Panel de choix Imposteur")
            embed_panel.add_field(name ="Choix de l'imposteur", value = "Réagissez à l'émoji correspondant", inline = False)
            current_panel = await memberimp.send(embed=embed_panel)

            await current_panel.add_reaction('🥇')
            await current_panel.add_reaction('🥈')
            
            print("send ok")

            imposteur_name = memberimp
            id_panel = current_panel.id
            step = "Imposteur"

            print(dicoimp)
            print(step)


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
                    Lp[irdm][8] = "Secte"
            
            str_s = ''
            for member in sect:
                str_s = str_s + str(member) + ', '
            str_s = str_s[:-2]
            await ctx.channel.send("Liste des joueurs à tuer pour le sectaire: **{}**.".format(str_s))
            await membersect.send("Liste des joueurs à tuer: {}.".format(str_s))

            annoncef.append("\n Liste des membres à tuer pour le Sectaire: ``{}`` \n".format(', '.join(sect)))
            

        print(Lp)
        temps1 = (time.time() - start_time)
        await ctx.channel.send("Commande exécutée en {} secondes".format(temps1))
        await ctx.channel.send("Lancement de la game terminé.") 


        if state_couple == 'couple':
            await couple(ctx)

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
        
        await ctx.channel.send(embed=embed)

        game_started = True

        await menu(ctx)

    
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




# ==========================================================================================================================================================

@client.command()
@commands.has_any_role("Maître du Jeu")
async def fmenu(ctx):

    await menu(ctx)

# Commande pour forcer l'apparition du menu en cas de bug



async def menu(ctx):

    global emojis_action, id_panel, step, game_started

    panel = discord.Embed(
            colour = discord.Color.green()
        ) 

    emojis_action = ["🐺", "🔪", "👒", "🔇", "🔊", "🌙", "🧒", "❤️", "💤", "🕵️", "🎺", "🌞","🛑"]


    if game_started == False:

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

        id_panel = msg.id
        step = 'Menu'





# ==========================================================================================================================================================


async def jour(ctx, dtime):

    global dicoroles, Lp, can_talk, cant_talk, game_started, channels, L_joueurs, day, dicomembers, cpt_jour, Laffichage_day

    author = mdj

    channel = author.voice.channel
    members = channel.members

    L_j_temp = [k for k in members]
    #Copie de members

    is_cover = False
    is_devin = False

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande jour"
        )

    Lmembers = [k for k in L_joueurs]

    if game_started == True:

        for i in range(0,len(L_j_temp)):
            if str(L_j_temp[i]) == str(author):
                L_j_temp.pop(i)
                break
    
        

        if dtime == 'nuit':
            if day == True:
                cpt_jour += 1

                day = False

                for member in L_j_temp:
                    await member.edit(mute=True)
                    await channels[2].set_permissions(member, overwrite=can_see) 
         
                for member in Lmembers:

                    if member in dicop_name_to_emoji:

                        fiche_player = Lp[dicomembers[member]]
                        rolep = fiche_player[1]
                        print(member,rolep)
                        if str(rolep) == 'Mort':
                            pass
                        else:
                            rol = Lp[dicomembers[member]][1]
                            statusc = Lp[dicomembers[member]][4]
                            status_infect = Lp[dicomembers[member]][9]
                            status_impost = Lp[dicomembers[member]][10]
                            
                            if rol == 'LG' or rol == 'LGB' or rol == 'IPDL' or rol == 'LGA' or (rol == 'Enfant' and is_enfant == True) or status_infect == 'Infecté' or (rol == 'Imposteur' and status_impost == 'LG'):
                                await channels[8].set_permissions(member, overwrite=can_talk)
                                print("{} OK a été demute de LG".format(str(member)))
                            if statusc == 'Oui':
                                await channels[6].set_permissions(member, overwrite=can_see)
                                print("{} OK a été mute de couple".format(str(member)))

                while is_cover == False:
                    if 'LGA' in Lroles_dispo:
                        ind = rdm.randint(0,len(L_j_temp)-1)
                        if Lp[dicomembers[L_j_temp[ind]]][1] == 'Mort':
                            pass
                        else:
                            await channels[8].send("La couverture du LGA cette nuit est: {}.".format(Lp[dicomembers[L_j_temp[ind]]][1]))
                            await channels[0].send("La couverture du LGA cette nuit est: {}.".format(Lp[dicomembers[L_j_temp[ind]]][1]))
                            if cpt_jour == 1 and 'Oeil' in Lroles_dispo:
                                await channels[23].send("La couverture du LGA cette nuit est: {}.".format(Lp[dicomembers[L_j_temp[ind]]][1]))
                            is_cover = True
                    else:
                        break 
                

                while is_devin == False:
                    if "Devin" in Lroles_dispo:
                        ind = rdm.randint(0,len(L_j_temp)-1)
                        if Lp[dicomembers[L_j_temp[ind]]][1] == 'Mort' or Lp[dicomembers[L_j_temp[ind]]][1] == 'Devin':
                            pass
                        else:
                            await channels[29].send("Vous devez deviner le rôle de {}.".format(Lp[dicomembers[L_j_temp[ind]]][0]))
                            await channels[0].send("Le Devin doit deviner le rôle de {} qui est {}.".format(Lp[dicomembers[L_j_temp[ind]]][0],Lp[dicomembers[L_j_temp[ind]]][1]))
                            if cpt_jour == 1 and 'Oeil' in Lroles_dispo:
                                await channels[23].send("Le devin doit deviner le rôle de {}.".format(Lp[dicomembers[L_j_temp[ind]]][0]))
                            is_devin = True
                    else:
                        break
                
                embedn = discord.Embed(
                    title = "NUIT: Le village s'endort.",
                    colour = discord.Color.dark_blue()
                )

                embedn.add_field(
                    name = "Nous sommes à la nuit __N°{}__".format(cpt_jour),
                    value = "\a",
                    inline = False
                )
                embedn.set_author(
                    name = "LG Bot",
                    icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                )

                await channels[2].send(embed=embedn)

                Laffichage_day = []
                for name in dicop_name_to_emoji:
                    fiche_player = Lp[dicomembers[name]]
                    rolep = fiche_player[1]
                    if str(rolep) == 'Mort':
                        pass
                    else:
                        Laffichage_day.append("``{0.name}``: {1} (Rôle: __{2}__) \n".format(name, dicop_name_to_emoji[name], rolep))

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

                # ====== AFFICHAGE BILAN MDJ ====== #
                
                # Ordre de passage:
                # Seulement tour 1: Cupidon, Enfant
                # Salvateur, LG, IPDL, GML, LGB, Voyante, Renard, Sorcière, Corbeau, JDF, Confesseur, Voleur
                Lannoncet1 = ["Cupidon", "Enfant"]
                Lannonce = ["Salvateur", "LG", "IPDL", "GML", "LGB", "Voyante", "Renard", "Sorcière", "Corbeau", "JDF", "Confesseur", "Voleur"]
                
                """
                await channels[0].send("Récapitulatif de ce qu'il y a à faire cette nuit:")

                if cpt_jour == 1:
                    await channels[0].send("__Rôles à ne faire que cette nuit (Cupidon dans #cupidon-et-couple et Enfant Sauvage par MP):__")
                    for role in Lannoncet1:
                        if role in Lroles_dispo:
                            if role in trad_roles:
                                await channels[0].send("**{}**".format(trad_roles[role]))
                            else:
                                await channels[0].send("**{}**".format(role))

                anno_lga_infect = False
                await channels[0].send("__Rôles à faire cette nuit:__")
                for role in Lannonce:
                    if role in Lroles_dispo:
                        if (role == 'LGA' or role == 'IPDL') and ('LG' not in Lroles_dispo):
                            if anno_lga_infect == False:
                                await channels[0].send("**Loup-garous**")
                                anno_lga_infect = True
                        if role in trad_roles:
                            await channels[0].send("**{}**".format(trad_roles[role]))
                        else:
                            await channels[0].send("**{}**".format(role))
                """


            else:
                await ctx.channel.send("ERREUR: commande erronée:")
                embed.set_author(name = "LG Bot")
                embed.add_field(name ='lg!jour <jour/nuit>', value = "Le temps est déjà la nuit ou l'argument rentré est erroné.", inline = False)
                await ctx.send(embed=embed)
        


        if dtime == 'jour':
            if day == False:
 
                day = True

                for member in L_j_temp:
                    if member in dicomembers:
                        if Lp[dicomembers[member]][1] == 'Mort':
                            pass
                        else:
                            await member.edit(mute=False)
                            await channels[2].set_permissions(member, overwrite=can_talk)
                
                for member in Lmembers:

                    if member in dicop_name_to_emoji:

                        fiche_player = Lp[dicomembers[member]]
                        rolep = fiche_player[1]
                        print(member,rolep)
                        if str(rolep) == 'Mort':
                            pass
                        else:
                            rol = Lp[dicomembers[member]][1]
                            statusc = Lp[dicomembers[member]][4]
                            status_infect = Lp[dicomembers[member]][9]
                            status_impost = Lp[dicomembers[member]][10]

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
                                    await channels[dicoroles[rol]].set_permissions(member, overwrite=can_talk)
                                    print("{} OK a été demute de {} (cas où noctambule)".format(member, channels[dicoroles[rol]]))
                            if statusc == 'Oui':
                                await channels[6].set_permissions(member, overwrite=can_talk)
                                print("{} OK a été demute de couple".format(str(member)))


                embedj = discord.Embed(
                    title = "JOUR: Le village se réveille.",
                    colour = discord.Color.dark_gold()
                )

                embedj.add_field(
                    name = "Nous sommes au jour __N°{}__".format(cpt_jour),
                    value = "\a",
                    inline = False
                )
                embedj.set_author(
                    name = "LG Bot",
                    icon_url = "https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=1024".format(client.user)
                )

                await channels[2].send(embed=embedj)

                Laffichage_day = []
                for name in dicop_name_to_emoji:
                    fiche_player = Lp[dicomembers[name]]
                    rolep = fiche_player[1]
                    if str(rolep) == 'Mort':
                        pass
                    else:
                        Laffichage_day.append("``{0.name}``: {1} (Rôle: __{2}__) \n".format(name, dicop_name_to_emoji[name], rolep))

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


            else:
                await ctx.channel.send("ERREUR: commande erronée:")
                embed.set_author(name = "LG Bot")
                embed.add_field(name ='.jour <jour/nuit>', value = "Le temps est déjà le jour ou l'argument rentré est erroné.", inline = False)
                await ctx.send(embed=embed)
    
    else:
        await ctx.channel.send("ERREUR: commande erronée:")
        embed.set_author(name = "LG Bot")
        embed.add_field(name ='.jour <jour/nuit>', value = "La partie n'a pas encore commencé.", inline = False)
        await ctx.send(embed=embed)

    await menu(ctx)


# ==========================================================================================================================================================


async def couple(ctx):

    global dicoroles, Lp, can_talk, cant_talk, game_started, channels,L_joueurs,check_couple, dicomembers, annoncef

    author = mdj

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande couple"
        )

    if game_started == True and check_couple == False:

        check_couple = True

        members = [k for k in L_joueurs]

        for member in members:
            fiche_player = Lp[dicomembers[member]]
            rolep = fiche_player[1]
            if rolep == 'Jaloux':
                members.remove(member)
                break
        
        i1 = rdm.randint(0,len(members)-1)
        if str(members[i1]) != author:
            amant1 = members[i1]
            print(Lp[dicomembers[members[i1]]])
            Lp[dicomembers[members[i1]]][4] = 'Oui'
            members.pop(i1)

        i2 = rdm.randint(0,len(members)-1)
        if str(members[i2]) != author:
            amant2 = members[i2]
            print(Lp[dicomembers[members[i2]]])
            Lp[dicomembers[members[i2]]][4] = 'Oui'
            members.pop(i2)


        await channels[6].set_permissions(amant1, overwrite=can_see)
        await channels[6].set_permissions(amant2, overwrite=can_see)
        await amant1.send("Tu es en couple avec {}".format(amant2))
        await amant2.send("Tu es en couple avec {}".format(amant1))
        print("Amant 1: {}, Amant 2: {}".format(amant1,amant2))
        await ctx.channel.send("Amant 1: {}, Amant 2: {}".format(amant1,amant2))

        annoncef.append("\n❤️ Les amants sont: ``{0.name}`` et ``{1.name}``".format(amant1, amant2))
    
    else:
        await ctx.channel.send("Il y a déjà un couple dans la partie.")


# ==========================================================================================================================================================


async def cupidon_panel(ctx):

    global dicoroles, Lp, can_talk, cant_talk, game_started, channels, L_joueurs, dicomembers, step, id_panel

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande cupidon"
        )

    embed_panel = discord.Embed(
            colour = discord.Color.orange()
        )


    if "Cupidon" in Lroles_dispo:

        if game_started == True:

            embed_panel.set_author(name = "Panel de choix commande cupidon")
            embed_panel.add_field(name ='Les emojis des joueurs sont rappelés chaque nuit.', value = "Veuillez réagir aux deux emojis qui représentent les deux personnes choisies par le Cupidon. Confirmez en réagissant à l'emoji ✅. Annulez la commande on réagissant à l'émoji ❌.", inline = False)
            current_panel = await ctx.channel.send(embed=embed_panel)

            for name in dicop_name_to_emoji:
                await current_panel.add_reaction(dicop_name_to_emoji[name])
            await current_panel.add_reaction("✅")
            await current_panel.add_reaction("❌")

            id_panel = current_panel.id
            step = 'Cupidon'
    
    else:
        await ctx.channel.send("ERREUR: commande erronée:")
        embed.set_author(name = "LG Bot")
        embed.add_field(name ='.cupidon', value = "Il n'y a pas de Cupidon dans la partie.", inline = False)
        await ctx.send(embed=embed)

    
    print("Fin commande cupidon")


async def cupidon_action(ctx, react, user_react):
# state designe si on ajoute un membre, si on valide ou si on annule
# Validation/Ajout/Annulation

    global liste_couple, cpt_reaction

    if len(liste_couple) < 2:
        await ctx.remove_reaction('✅', user_react)
        await ctx.channel.send("Vous n'avez pas sélectionné assez d'amants. Il manque {} amant(s).".format(2-cpt_reaction))
    else:
        cpl1 = liste_couple[0]
        cpl2 = liste_couple[1]
        await channels[6].set_permissions(cpl1, overwrite=can_see)
        await channels[6].set_permissions(cpl2, overwrite=can_see)
        await cpl1.send("Tu es en couple avec {}".format(cpl2))
        await cpl2.send("Tu es en couple avec {}".format(cpl1))
        await ctx.channel.send("Liste des amants: {} et {}".format(cpl1,cpl2))
        await ctx.delete()
        cpt_reaction = 0
        liste_couple = []

    await menu(ctx)



# ==========================================================================================================================================================


async def enfant_panel(ctx):

    global dicoroles, Lp, can_talk, cant_talk, game_started, channels, L_joueurs, dicomembers, enfant_name, id_panel, step

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande enfant"
        )

    embed_panel = discord.Embed(
            colour = discord.Color.orange()
        )

    if 'Enfant' in Lroles_dispo:
        if game_started == True:

            embed_panel.set_author(name = "Panel de choix commande enfant")
            embed_panel.add_field(name ='Les emojis des joueurs sont rappelés chaque nuit.', value = "Veuillez réagir à l'emoji correspondant au maître choisi par l'enfant. Confirmez en réagissant à l'emoji ✅. Annulez la commande on réagissant à l'émoji ❌.", inline = False)
            current_panel = await ctx.channel.send(embed=embed_panel)

            for name in dicop_name_to_emoji:
                fiche_player = Lp[dicomembers[name]]
                rolep = fiche_player[1]
                if str(rolep) == 'Enfant':
                    print("ok enfant name")
                    enfant_name = name
                elif str(rolep) == "Mort":
                    print("ok mort")
                    pass
                else:
                    print("ok not enfant")
                    await current_panel.add_reaction(dicop_name_to_emoji[name])
            await current_panel.add_reaction("✅")
            await current_panel.add_reaction("❌")

            id_panel = current_panel.id
            step = 'Enfant'
        
        print(id_panel, step, str(enfant_name))


    else:
        await ctx.channel.send("ERREUR: commande erronée:")
        embed.set_author(name = "LG Bot")
        embed.add_field(name ='.enfant', value = "Il n'y a pas d'Enfant Sauvage dans la partie.", inline = False)
        await ctx.send(embed=embed)

    print("Fin commande enfant")


async def enfant_action(ctx):

    global maitre_name, enfant_name, Lp, cpt_reaction, dicomembers

    fiche_maitre = Lp[dicomembers[maitre_name]]
    fiche_maitre[5] = 'Maitre'
    fiche_enfant = Lp[dicomembers[enfant_name]]
    fiche_enfant[5] = 'Enfant'
    fiche_enfant[6] = 'Villageois'
    await ctx.channel.send("{} est le maître de {}.".format(str(maitre_name), str(enfant_name)))
    await ctx.delete()
    cpt_reaction = 0
    maitre_name = None

    await menu(ctx)


# ==========================================================================================================================================================


async def voleur_panel(ctx):

    global dicoroles, Lp, can_talk, cant_talk, game_started, channels,L_joueurs, dicomembers, is_enfant, voleur_name, id_panel, step

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande voleur"
        )
    
    embed_panel = discord.Embed(
            colour = discord.Color.orange()
        )
    
    if 'Voleur' in Lroles_dispo:

        if game_started == True:

            print("ok")

            embed_panel.set_author(name = "Panel de choix commande voleur")
            embed_panel.add_field(name ='Les emojis des joueurs sont rappelés chaque nuit.', value = "Veuillez réagir à l'emoji correspondant à la personne qui a été volée. Confirmez en réagissant à l'emoji ✅. Annulez la commande on réagissant à l'émoji ❌.", inline = False)
            current_panel = await ctx.channel.send(embed=embed_panel)

            for name in dicop_name_to_emoji:
                fiche_player = Lp[dicomembers[name]]
                rolep = fiche_player[1]
                if str(rolep) == 'Voleur':
                    voleur_name = name
                elif str(rolep) == "Mort":
                    pass
                else:
                    await current_panel.add_reaction(dicop_name_to_emoji[name])
            await current_panel.add_reaction("✅")
            await current_panel.add_reaction("❌")

            id_panel = current_panel.id
            step = "Voleur"

        print(id_panel, step, str(voleur_name))

    else:
        await ctx.channel.send("ERREUR: commande erronée:")
        embed.set_author(name = "LG Bot")
        embed.add_field(name ='.voleur', value = "Il n'y a pas de Voleur dans la partie.", inline = False)
        await ctx.send(embed=embed)

    print("Fin commande voleur")


async def voleur_action(ctx):

    global stolen_name, voleur_name, Lp, cpt_reaction, servante_name, devo_name

    if step == 'Servante':
        voleur_name = servante_name
        stolen_name = devo_name

    fiche_stolen = Lp[dicomembers[stolen_name]]
    role_stolen = fiche_stolen[1]

    fiche_voleur = Lp[dicomembers[voleur_name]]
    role_voleur = fiche_voleur[1]

    fiche_stolen[1],fiche_voleur[1] = role_voleur,role_stolen

    if role_stolen == 'Enfant':
        fiche_voleur[5] = 'Enfant'
        fiche_stolen[5] = 'Non'

    if role_stolen in dicoroles:
        print(role_stolen, "voleur dicoroles")
        await channels[dicoroles[role_stolen]].set_permissions(voleur_name, overwrite=can_talk)
        await channels[dicoroles[role_stolen]].set_permissions(stolen_name, overwrite=cant_talk)
        if role_stolen == 'LGB' or role_stolen == 'IPDL' or (role_stolen == 'Enfant' and is_enfant == True) or fiche_stolen[9] == 'Infecté':
            await channels[8].set_permissions(stolen_name, overwrite=cant_talk)
            await channels[8].set_permissions(voleur_name, overwrite=can_talk)
    await channels[dicoroles[role_voleur]].set_permissions(voleur_name, overwrite=cant_talk)
    await channels[dicoroles[role_voleur]].set_permissions(stolen_name, overwrite=can_talk)

    await stolen_name.send("Ton rôle a été volé, tu es maintenant Voleur")
    await voleur_name.send("Tu as volé la personne avec le rôle {}".format(str(role_stolen)))
    await ctx.channel.send("{} a volé le rôle de {}, qui était {}.".format(str(voleur_name),str(stolen_name),str(role_stolen)))
    await ctx.delete()
    cpt_reaction = 0
    stolen_name = None
    voleur_name = None

    if step == 'Voleur':
        await menu(ctx)



# ==========================================================================================================================================================


async def infect_panel(ctx):

    global dicoroles, Lp, can_talk, cant_talk, game_started, channels, L_joueurs, dicomembers, id_panel, step, is_enfant

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande Infect"
        )

    embed_panel = discord.Embed(
            colour = discord.Color.orange()
        )

    if "IPDL" in Lroles_dispo:

        if game_started == True:

            embed_panel.set_author(name = "Panel de choix commande infect")
            embed_panel.add_field(name ='Les emojis des joueurs sont rappelés chaque nuit.', value = "Veuillez réagir à l'emoji correspondant à la personne qui sera infectée. Confirmez en réagissant à l'emoji ✅. Annulez la commande on réagissant à l'émoji ❌.", inline = False)
            current_panel = await ctx.channel.send(embed=embed_panel)

            for name in dicop_name_to_emoji:
                fiche_player = Lp[dicomembers[name]]
                rolep = fiche_player[1]
                status_infect = fiche_player[9]
                if str(rolep) == 'LG' or str(rolep) == 'LGA' or str(rolep) == 'LGB' or str(rolep) == 'IPDL' or str(rolep) == 'GML' or status_infect == 'Infecté' or str(rolep) == "Mort" or (str(rolep) == 'Enfant' and is_enfant == True):
                    pass
                else:    
                    await current_panel.add_reaction(dicop_name_to_emoji[name])
            await current_panel.add_reaction("✅")
            await current_panel.add_reaction("❌")

            id_panel = current_panel.id
            step = 'Infecté'

        print(id_panel, step)

    else:
        await ctx.channel.send("ERREUR: commande erronée:")
        embed.set_author(name = "LG Bot")
        embed.add_field(name ='.infect', value = "Il n'y a pas d'IPDL dans la partie.", inline = False)
        await ctx.send(embed=embed)

    print("Fin commande infect")


async def infect_action(ctx):

    global infect_name, cpt_reaction, Lp

    pi = Lp[dicomembers[infect_name]]

    if day == True:
        await channels[8].set_permissions(infect_name, overwrite=can_see)
    elif day == False:
        await channels[8].set_permissions(infect_name, overwrite=can_talk)

    pi[9] = 'Infecté'

    await infect_name.send("Tu as été infécté, tu es maintenant dans le camp des Loup-garous.")
    await ctx.channel.send("{} a été infécté.".format(str(infect_name)))
    await ctx.delete()
    cpt_reaction = 0
    infect_name = None

    await menu(ctx)



# ==========================================================================================================================================================


async def charm_panel(ctx):

    global dicoroles, Lp, can_talk, cant_talk, game_started, channels, L_joueurs, dicomembers, id_panel, step

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande Charm"
        )

    embed_panel = discord.Embed(
            colour = discord.Color.orange()
        )

    if "JDF" in Lroles_dispo:

        if game_started == True:

            embed_panel.set_author(name = "Panel de choix commande charm")
            embed_panel.add_field(name ='Les emojis des joueurs sont rappelés chaque nuit.', value = "Veuillez réagir à l'emoji correspondant à la personne qui sera charmée. Confirmez en réagissant à l'emoji ✅. Annulez la commande on réagissant à l'émoji ❌.", inline = False)
            current_panel = await ctx.channel.send(embed=embed_panel)

            for name in dicop_name_to_emoji:
                fiche_player = Lp[dicomembers[name]]
                rolep = fiche_player[1]
                status_charm = fiche_player[7]
                if str(rolep) == 'JDF' or status_charm == 'Charmé' or str(rolep) == "Mort":
                    pass      
                else:
                    await current_panel.add_reaction(dicop_name_to_emoji[name])
            await current_panel.add_reaction("✅")
            await current_panel.add_reaction("❌")

            id_panel = current_panel.id
            step = 'Charmé'

        print(id_panel, step)
    
    else:
        await ctx.channel.send("ERREUR: commande erronée:")
        embed.set_author(name = "LG Bot")
        embed.add_field(name ='.charm', value = "Il n'y a pas de Joueur de Flute dans la partie.", inline = False)
        await ctx.send(embed=embed)

    print("Fin commande charm")


async def charm_action(ctx):

    global liste_charm, cpt_reaction, Lp

    for member in liste_charm:
        Lp[dicomembers[member]][7] = 'Charmé'
        await channels[4].set_permissions(member, overwrite=can_see)
        await member.send("Tu as été charmé par le Joueur de flûte.")
        await ctx.channel.send("{} a été charmé".format(str(member)))

    await ctx.delete()
    cpt_reaction = 0
    liste_charm = []

    await menu(ctx)



# ==========================================================================================================================================================


async def kill_panel(ctx):
#Commande permettant de tuer un joueur

    global L_joueurs, Lroles_dispo, game_started, channels, dicoroles, can_talk, cant_talk, Lp, ancien_dead, dicomembers, is_enfant, check_couple, is_compo, id_panel, step

    print("Commande .kill exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), mdj))

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande kill"
        )

    embed_panel = discord.Embed(
            colour = discord.Color.orange()
        )

    if game_started == True:

        embed_panel.set_author(name = "Panel de choix commande kill")
        embed_panel.add_field(name ='Les emojis des joueurs sont rappelés chaque nuit.', value = "Veuillez réagir à l'emoji correspondant à la personne qui sera tuée. Confirmez en réagissant à l'emoji ✅. Annulez la commande on réagissant à l'émoji ❌.", inline = False)
        current_panel = await ctx.channel.send(embed=embed_panel)

        for name in dicop_name_to_emoji:
            fiche_player = Lp[dicomembers[name]]
            rolep = fiche_player[1]
            if str(rolep) == 'Mort':
                pass
            else:
                await current_panel.add_reaction(dicop_name_to_emoji[name])
        await current_panel.add_reaction("✅")
        await current_panel.add_reaction("❌")

        id_panel = current_panel.id
        step = 'Kill'

    print(id_panel, step)
    
    print("Fin commande kill")


async def kill_action(ctx):

    global Lp, is_enfant, cpt_reaction, p_emoji, servante_name, killed_name, devo_name, check_couple

    author = panel_author

    channel = mdj.voice.channel
    members = channel.members

    L_j_temp = [k for k in members]
    #Copie de members

    for i in range(0,len(members)):
        if str(members[i]) == str(author):
            L_j_temp.pop(i)
            break

    Lroles_aff = []
    affiche = False

    if step == "Servante":
        killed_name = devo_name

    pla = Lp[dicomembers[killed_name]]
    rolep = pla[1]
    status_couple = pla[4]
    status_maitre = pla[5]
    status_infect = pla[9]
    status_impost = pla[10]

    member = killed_name
    
    if rolep == 'Ancien' and ancien_dead == False:
        ancien_dead = True
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
            check_couple = False
        if status_infect == 'Infecté':
            await channels[8].set_permissions(member, overwrite=cant_talk)
            print("OK infect")
        if status_impost == 'LG':
            await channels[8].set_permissions(member, overwrite=cant_talk)
            print ('OK Impost LG')
        if status_maitre == 'Maitre' and is_enfant == False:
            print("OK Maitre")
            is_enfant = True
            for memberenf in L_j_temp:
                pla_en = Lp[dicomembers[memberenf]]
                status_enfant = pla_en[5]
                print(memberenf, pla_en)
                if status_enfant == 'Enfant':
                    pla_en[6] = 'LG'
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

        pla[1] = 'Mort'

        print('OK {} est mort, il était {}'.format(str(member), rolep))

        if is_compo == True:
            for i in range(0,len(Lroles_dispo)):
                print(i,Lroles_dispo[i], rolep)
                if Lroles_dispo[i] == rolep:
                    Lroles_dispo.pop(i)
                    affiche = True
                    break
            
            await channels[1].purge(limit=50)
            
            if affiche == True:
                
                embedaf = discord.Embed(
                    colour = discord.Color.grey(),
                    title = "Informations partie"
                )

                Laff = []
                for i in range(0,len(Lroles_dispo)):
                    if Lroles_dispo[i] not in Lroles_aff:
                        if Lroles_dispo[i] in trad_roles:
                            Laff.append("``{}`` ({}) \n".format(trad_roles[Lroles_dispo[i]],Lroles_dispo.count(Lroles_dispo[i])))
                        else:
                            Laff.append("``{}`` ({}) \n".format(Lroles_dispo[i],Lroles_dispo.count(Lroles_dispo[i])))
                        Lroles_aff.append(Lroles_dispo[i])
                    elif Lroles_dispo[i] in Lroles_aff:
                        Lroles_aff.append(Lroles_dispo[i])


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
            for i in range(0,len(Lroles_dispo)):
                print(i,Lroles_dispo[i], rolep)
                if Lroles_dispo[i] == rolep:
                    Lroles_dispo.pop(i)
                    break

    await ctx.delete()
    cpt_reaction = 0
    killed_name = None
    print("Fin commande kill")

    await menu(ctx)


# ==========================================================================================================================================================


async def noctambule_panel(ctx):

    global L_joueurs, Lroles_dispo, game_started, channels, dicoroles, can_talk, cant_talk, Lp, dicomembers, id_panel, step, noctambule_name

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande Notambule"
        )

    embed_panel = discord.Embed(
            colour = discord.Color.orange()
        )

    if game_started == True:

        embed_panel.set_author(name = "Panel de choix commande noctambule")
        embed_panel.add_field(name ='Les emojis des joueurs sont rappelés chaque nuit.', value = "Veuillez réagir à l'emoji correspondant à la personne qui sera visée par le Noctambule. Confirmez en réagissant à l'emoji ✅. Annulez la commande on réagissant à l'émoji ❌.", inline = False)
        current_panel = await ctx.channel.send(embed=embed_panel)

        for name in dicop_name_to_emoji:
            fiche_player = Lp[dicomembers[name]]
            rolep = fiche_player[1]
            roleimp = fiche_player[11]
            rolet = fiche_player[12]
            if str(rolep) == 'Mort':
                pass
            elif str(rolep) == 'Noctambule' or roleimp == 'Noctambule' or rolet == 'Noctambule':
                noctambule_name = name
            else:
                await current_panel.add_reaction(dicop_name_to_emoji[name])
        await current_panel.add_reaction("✅")
        await current_panel.add_reaction("❌")

        id_panel = current_panel.id
        step = 'Noctambule'

    print(id_panel, step)
    
    print("Fin commande noctambule")


async def noctambule_action(ctx):

    global Lp, victime_name, cpt_reaction, noctambule_name

    fiche_victime = Lp[dicomembers[victime_name]]
    rolevi = fiche_victime[1]
    status_couple = fiche_victime[4]
    status_maitre = fiche_victime[5]
    status_infect = fiche_victime[9]
    status_impost = fiche_victime[10]

    member = victime_name

    print("{} couple: {}".format(str(member),status_couple))
    print("{} enfant/maitre: {}".format(str(member),status_maitre))
    
    if rolevi in dicoroles:
        await channels[dicoroles[rolevi]].set_permissions(member, overwrite=cant_talk)
        print('OK dicoroles')
    if rolevi == "IPDL" or rolevi == 'LGB' or (rolevi == 'Enfant' and is_enfant == True) or status_infect == 'Infecté' or status_impost == 'LG':
        await channels[8].set_permissions(member, overwrite=cant_talk)
        print('OK LG')

    await victime_name.send("Vous avez été victime du Noctambule **({})**. Vous ne pouvez pas utiliser votre pouvoir cette nuit.".format(noctambule_name))
    await ctx.channel.send("**{}** (rôle: __{}__) a été victime du Noctambule (*{}*)".format(victime_name, rolevi, noctambule_name))
    await ctx.delete()
    cpt_reaction = 0
    noctambule_name = None
    victime_name = None
    print("Fin nomctambule")

    await menu(ctx)


# ==========================================================================================================================================================


async def servante_panel(ctx):

    global L_joueurs, Lroles_dispo, game_started, channels, dicoroles, can_talk, cant_talk, Lp, dicomembers, id_panel, step, servante_name

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande Servante"
        )

    embed_panel = discord.Embed(
            colour = discord.Color.orange()
        )

    if game_started == True:

        embed_panel.set_author(name = "Panel de choix commande servante")
        embed_panel.add_field(name ='Les emojis des joueurs sont rappelés chaque nuit.', value = "Veuillez réagir à l'emoji correspondant à la personne qui sera visée par la Servante Dévouée. Confirmez en réagissant à l'emoji ✅. Annulez la commande on réagissant à l'émoji ❌.", inline = False)
        current_panel = await ctx.channel.send(embed=embed_panel)

        for name in dicop_name_to_emoji:
            fiche_player = Lp[dicomembers[name]]
            rolep = fiche_player[1]
            roleimp = fiche_player[11]
            rolet = fiche_player[12]
            if str(rolep) == 'Mort':
                pass
            elif str(rolep) == 'Servante' or roleimp == 'Servante' or rolet == 'Servante':
                servante_name = name
            else:
                await current_panel.add_reaction(dicop_name_to_emoji[name])
        await current_panel.add_reaction("✅")
        await current_panel.add_reaction("❌")

        id_panel = current_panel.id
        step = 'Servante'

    print(id_panel, step)
    
    print("Fin commande servante")


# ==========================================================================================================================================================


async def reset_panel(ctx):

    global step, id_panel

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

    step = "Reset"
    id_panel = panel.id


# ==========================================================================================================================================================

async def vote(ctx): 

    global L_joueurs, Laffichage_vote, Lannonce_vote, Lroles_dispo, game_started, channels, dicoroles, can_talk, cant_talk, Lp, ancien_dead, dicomembers, is_enfant, check_couple, is_compo, id_panel, step, id_vote

    start_time = time.time()

    author = mdj

    channel = author.voice.channel
    members = channel.members

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande vote"
        )

    embed_panel = discord.Embed(
            colour = discord.Color.orange()
        )
    
    embed_panel_vote = discord.Embed(
            colour = discord.Color.green()
        )  

    Lannonce_vote = []
    Laffichage_vote = ""

    L_j_temp = [k for k in members]
    for i in range(0,len(members)):
        if str(members[i]) == str(author):
            L_j_temp.pop(i)
            break
            
    for name in dicop_name_to_emoji:
        fiche_player = Lp[dicomembers[name]]
        rolep = fiche_player[1]
        if str(rolep) == 'Mort':
            pass
        else:
            print(Laffichage_vote)
            Laffichage_vote = Laffichage_vote + '(**{}**: {}) '.format(str(name),dicop_name_to_emoji[name])


    if game_started == True:

        embed_panel.set_author(name = "Panel de commande vote")
        embed_panel.add_field(name ='Les emojis des joueurs sont rappelés au dessus.', value = "Quand tous les votes sont terminés, veuillez réagir à l'émoji ✅ pour arrêter le vote. Veuillez ensuite faire la commande kill pour tuer la personne votée.", inline = False)
        current_panel = await ctx.channel.send(embed=embed_panel)

        embed_panel_vote.set_author(name = "Panel de commande vote")
        embed_panel_vote.add_field(name ='Les emojis des joueurs sont rappelés au dessus.', value = "Veuillez réagir à l'emoji correspondant à la personne pour qui vous voulez voter. Réagissez à l'émoji ⬜ pour voter blanc.", inline = False)

        for member in L_j_temp:
            fiche_player = Lp[dicomembers[member]]
            rolep = fiche_player[1]
            if str(rolep) == 'Mort':
                pass
            else:
                await member.edit(mute=True)
                await member.send(Laffichage_vote)
                current_vote = await member.send(embed=embed_panel_vote)

            for name in dicop_name_to_emoji:
                fiche_player = Lp[dicomembers[name]]
                rolep = fiche_player[1]
                if str(rolep) == 'Mort':
                    pass
                else:
                    await current_vote.add_reaction(dicop_name_to_emoji[name])
            await current_vote.add_reaction("⬜")


        await current_panel.add_reaction("✅")
        
        # id_vote = current_vote.id
        id_panel = current_panel.id
        step = 'Vote'
    
    print('Fin commande vote')

    temps1 = (time.time() - start_time)

    await ctx.channel.send("Temps d'exécution: {} secondes".format(temps1))



# ==========================================================================================================================================================




@client.command()
@commands.has_any_role("Maître du Jeu")
async def listeid(ctx):

    author = str(ctx.author)

    channel = author.voice.channel
    members = channel.members

    for member in members:
        await ctx.channel.send(str(member.id))



# ==========================================================================================================================================================


async def mute(ctx, state):

    author = mdj

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


# ==========================================================================================================================================================



@client.command()
@commands.has_any_role("Maître du Jeu")
async def talk(ctx):

    print("Commande lg!talk exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), ctx.author))

    channel = ctx.author.voice.channel
    members = channel.members

    if in_game == False:
        for member in members:
            await channels[2].set_permissions(member, overwrite=can_talk)
            await channels[3].set_permissions(member, overwrite=cant_talk)
            print("OK, {}".format(member))

    else:
        await ctx.channel.send("ERREUR: Veuillez entrer la commande lg!stop avant de faire cette commande")


# ==========================================================================================================================================================


@client.command()
@commands.has_any_role("Maître du Jeu","Développeur","Admin","Host")
async def purge(ctx, limit):
    await ctx.channel.purge(limit=int(limit))


# ==========================================================================================================================================================


@client.command()
async def apply (ctx):

    if game_started == True:

        await ctx.delete()
    
    else:
        if str(ctx.channel.type) == "private":
            await ctx.channel.send("Vous avez commencé la procédure d'inscription pour devenir Host. Voulez-vous continuer ? \n" + "Répondez par **Oui** ou **Non**")

            

        else:
            await ctx.channel.send("Cette commande n'est disponible qu'en messages privés avec le bot.")




# ==========================================================================================================================================================



@client.command()
@commands.has_any_role("Maître du Jeu")
async def crypt(ctx, pourcentage):

    global valuepf

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande crypt"
        )

    if int(pourcentage) > 100:
        await ctx.channel.send("ERREUR: commande erronée:")

        embed.set_author(
            name = "LG Bot"
        )

        embed.add_field(
            name ='.crypt <pourcentage>', 
            value = "Le pourcentage est trop grand (ça doit être un entier positif inférieur ou égal à 100).", 
            inline = False
        )

        await ctx.send(embed=embed)

    else:
        valuepf = int(pourcentage)
        await ctx.channel.send("Pourcentage de changer une lettre pour la petite-fille et le chaman: **{}%**.".format(valuepf))




# ==========================================================================================================================================================


@client.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("Erreur: il manque un argument à la commande. Faites .help pour vérifier les arguments de cette commande.")
    
    elif isinstance(error, commands.CommandNotFound):
        await ctx.channel.send("Erreur: la commande entrée n'a pas été trouvée. Faites .help pour accéder à la liste des commandes.")


# ==========================================================================================================================================================


@client.command()
@commands.has_any_role("Maître du Jeu")
async def freset(ctx):

    await reset(ctx)


# ==========================================================================================================================================================


async def reset(ctx):
#Commande d'arrêt du jeu

    global mdj, old_step, annoncef, cr_game, Lroles_dispo, dicoimp, Lroles_voleur, Lroles_traitre, id_vote, Lannonce_vote, Laffichage_day, Laffichage_joueurs, Laffichage_vote, p_emoji, inscription_chan, L_joueurs, Lp, channels, Lchannels, text_channel_list, panel_author, servante_name, devo_name, liste_couple, noctambule_name, victime_name, voleur_name, enfant_name, maitre_name, infect_name, stolen_name, liste_charm, imposteur_name, killed_name, dicomembers, dicop_id_to_emoji, dicop_name_to_emoji, dicop_emoji, Lemojis, is_compo, is_channels, in_game, game_started, day, is_enfant, ancien_dead, check_couple, valuepf, cpt_jour, is_info, cpt_reaction

    try:
        author = mdj
        channel = author.voice.channel
        members = channel.members
    except:
        members = []


    """
    guild = ctx.guild

    print("Commande .reset exécutée à {} par {}.".format(datetime.now().strftime("%H:%M:%S"), ctx.author))

    author = ctx.author

    channel = ctx.author.voice.channel
    members = channel.members

    L_j_temp = [k for k in members]
    #Copie de members

    for i in range(0,len(members)):
        if str(members[i]) == str(author):
            L_j_temp.pop(i)
    """

    os.system('py csts.py')

    
    if in_game == True:

        for member in members:
            # await inscription_chan.set_permissions(member, overwrite=can_talk)
            await channels[2].set_permissions(member, overwrite=can_talk)
            await channels[3].set_permissions(member, overwrite=cant_talk)
            print("OK, {}".format(member))

        
        """
        print(cr_game)
        print("Token: {}".format(file_token))
        

        recap = open("{}.txt".format(file_token), "w") 
        for txt in cr_game:
            recap.write(txt) 
        recap.close() 


        cr_game = []
        """

        await ctx.channel.send("La partie est arrêtée")

    else:
        await ctx.channel.send("Aucune partie n'est en cours: simple reset des permissions")

        for member in members:
            # await inscription_chan.set_permissions(member, overwrite=can_talk)
            await channels[2].set_permissions(member, overwrite=can_talk)
            await channels[3].set_permissions(member, overwrite=cant_talk)
            print("OK, {}".format(member))



client.run(bot_token)




