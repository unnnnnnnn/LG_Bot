#-*- coding:utf-8 -*-

#================================

import discord
import asyncio
from discord.utils import get
from discord.ext import commands
from dictionnaires import dicoroles, trad_roles, desc_roles
import time
import os
import random as rdm
from inspect import getsourcefile
os.chdir(os.path.dirname(getsourcefile(lambda: 0)))

client = commands.Bot(command_prefix=".")
client.remove_command("help")

#================================

liste_roles= ['Villageois','Voyante','Chasseur','Ancien','Sorcière','Petite-fille','Bouc-emissaire','Idiot','Corbeau','Chaman','Renard','Ours','Soeur','Frère','Chevalier','Salvateur','LG','LGA','Grand-loup','Infect','LGB','Cupidon','Flute','Ange','Enfant','Voleur']
#Liste de tous les rôles

Lroles_dispo = []
#Liste des rôles disponibles dans 1 partie

L_joueurs = []
#Liste des joueurs dans 1 partie (tempo)
Lp = []
#Liste finale de joueur

channels = []
#Liste des channels text du serveur

dicop = {}
#Dictionnaire de joueurs

cant_talk = discord.PermissionOverwrite()
cant_talk.send_messages = False
cant_talk.read_messages = False

can_talk = discord.PermissionOverwrite()
can_talk.send_messages = True
can_talk.read_messages = True

can_see = discord.PermissionOverwrite()
can_see.send_messages = False
can_see.read_messages = True


in_game = False
game_started = False
#Booleans qui permettent de contrôler l'état de la partie

ancien_dead = False
check_couple = False
#Permet de gérer les erreurs liées à l'ancien et au couple


@client.event
async def on_ready():
#Fonction initiale du bot (automatique)
#Permet d'init les channels text
#Initialisation

    global channels
    await client.wait_until_ready()
    channels = [
        client.get_channel(683372153684361251), #Enfant sauvage 0
        client.get_channel(683370294471163940), #Cupidon + couple 1
        client.get_channel(683104205879246908), #Salvateur  2
        client.get_channel(683024414807425044), #Loups  3
        client.get_channel(683104149918842883), #Petite fille   4
        client.get_channel(683332320014630915), #Infect    5
        client.get_channel(683332387748184084), #LGB    6
        client.get_channel(683105039941632044), #Voyante    7
        client.get_channel(683103921438457885), #Sorcière   8
        client.get_channel(683450271891718159), #Renard   9
        client.get_channel(683450890702946393), #Ancien 10
        client.get_channel(683422309624840305), #Flute  11
        client.get_channel(683352507157839886), #Voleur    12
        client.get_channel(683031195675656372), #Soeurs 13
        client.get_channel(683031221747449913), #Freres 14
        client.get_channel(683110376807858178), #Morts  15
        client.get_channel(683422350074445882), #Charmés    16
        client.get_channel(683329321737125894), #Roles de la game   17
        client.get_channel(683023423940853818), #Place du village    18
        client.get_channel(683475357265035305) #Bot test 19
    ]
    await channels[19].send("Bot connecté: {0.user}. Faites la commande .help pour afficher la liste des commandes.".format(client))
    await client.change_presence(activity=discord.Game(name="LG Bot par unnn et Davphla"))
    print('Bot connecté: {0.user}'.format(client))



@client.command()
@commands.has_any_role("Maître du Jeu","Développeur")
async def help(ctx):
#Commande d'aide utilisateur
#Affiche un embed

    if str(ctx.channel) in "bot-test":
    
        print("Help command")
        author = ctx.message.author

        embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Page d'aide"
        )

        embed.set_author(name = "Page d'aide")
        embed.set_thumbnail(url='https://www.loups-garous-en-ligne.com/jeu/assets/images/carte2.png')
        embed.add_field(name ='.help', value = "Affiche le menu d'aide", inline = False)
        embed.add_field(name ='.liste', value = 'Affiche la liste des rôles', inline = False)
        embed.add_field(name ='.create <liste role>', value = "Créer une partie", inline = False)
        embed.add_field(name ='.roleset <liste role>', value = "Redéfinir les rôles d'une partie", inline = False)
        embed.add_field(name ='.start <nombre joueurs> <maître du jeu>', value = 'Démarre la partie', inline = False)
        embed.add_field(name ='.roleremove <role> <nom#xxxx>', value = 'Enlève un rôle', inline = False)
        embed.add_field(name ='.kill <nom#xxxx>', value = 'Tue un joueur', inline = False)
        embed.add_field(name ='.roles', value = 'desc', inline = False)
        embed.add_field(name ='.getroles <nom#xxxx>', value = 'desc', inline = False)
        embed.add_field(name ='.stop', value = 'desc', inline = False)
        embed.add_field(name ='.voleur', value = 'Commande de jeu voleur (swap les rôles)', inline = False)
        embed.add_field(name ='.cupidon', value = 'Commande de jeu cupidon', inline = False)

        await ctx.send(embed=embed)


    else:
        print("Pas le bon salon")



@client.command()
@commands.has_any_role("Maître du Jeu","Développeur")
async def liste(message):
#Affiche la liste de tous les rôles

    Lrole = ''
    for k in liste_roles:
        Lrole = Lrole + k + ', '
    Lrole = Lrole[:-2]
    await message.channel.send(Lrole)


@client.command()
@commands.has_any_role("Maître du Jeu","Développeur")
async def create(ctx, strRole):
#Permet de créer une liste de rôles pour 1 partie

    global Lroles_dispo, in_game

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande create"
        )

    Lroles_dispo = []
    Lroles = strRole.split(',')
    for role in Lroles:
        if role not in liste_roles:
            await ctx.channel.send("ERREUR: commande erronée:")
            embed.set_author(name = "LG Bot")
            embed.add_field(name ='.create <liste des rôles>', value = "Un rôle n'est pas valide.", inline = False)
            await ctx.send(embed=embed)
            await ctx.channel.send("Rôle non valide: {}.".format(role))
            Lroles_dispo = []
            break
    
        else:
            Lroles_dispo.append(role)

    if len(Lroles_dispo) != 0:
        str_r = ''
        for k in Lroles_dispo:
            str_r = str_r + k + ', '
        str_r = str_r[:-2]
        await ctx.channel.send("Liste des rôles: {}.".format(str_r))

        in_game = True



@client.command()
@commands.has_any_role("Maître du Jeu","Développeur")
async def roles(message):
#Permet d'afficher la liste des rôles pour 1 partie

    global Lroles_dispo,in_game

    print(in_game)
    if in_game == True:
        str_r = ''
        for k in Lroles_dispo:
            str_r = str_r + k + ', '
        str_r = str_r[:-2]
        await message.channel.send("Liste des rôles: {}.".format(str_r))

    else:
        await message.channel.send("ERREUR: Aucune partie n'a été créée")



@client.command()
@commands.has_any_role("Maître du Jeu","Développeur")
async def start(ctx, nbplayers):
#Commande de départ

    global Lroles_dispo, L_joueurs, in_game, game_started, channels, Lp, dicop, can_talk, cant_talk
    master_in_game = False
    #Boolean d'état de jeu
    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande start"
        )

    if in_game == True and game_started == False:

        nbp = int(nbplayers)
        #On doit faire int parce que nbplayers est un string

        if nbp == len(Lroles_dispo):
        #Check si on a bien entrer le bon nombre de rôles

            author = str(ctx.message.author)

            channel = ctx.message.author.voice.channel
            members = channel.members

            L_j_nomj = [k for k in members]
            #Copie de members

            for i in range(0,len(members)):
                if str(members[i]) == str(author):
                    L_j_nomj.pop(i)

                    if nbp == len(L_j_nomj):
                        master_in_game = True
            #Enlève le MJ de la liste des joueurs
                

            if master_in_game == True:

                game_started = True
                
                Lroles_final = []
                #Liste de transition (voir + bas)

                print("Partie commencée")
                await ctx.channel.send("Une partie a commencé")
                await ctx.channel.send("**Les rôles sont : **")
                for i in range(0,len(Lroles_dispo)):
                    if Lroles_dispo[i] not in Lroles_final:
                        await ctx.channel.send("{} ({})".format(Lroles_dispo[i],Lroles_dispo.count(Lroles_dispo[i])))
                        Lroles_final.append(Lroles_dispo[i])
                    elif Lroles_dispo[i] in Lroles_final:
                        Lroles_final.append(Lroles_dispo[i])
                #Permet de compter les rôles (sans duplica)


                await ctx.channel.send("**Le maître de jeu est** {}.".format(author))

                await ctx.channel.send("**Les partcipants sont: **")

                compteur = 0

                for member in members:
                #Grosse boucle qui permet d'initialiser l'état des joueurs

                    await channels[18].set_permissions(member, overwrite=can_talk)
                    print(member)
                    if str(member) != str(author):
                        L_joueurs.append(member)
                        #Liste des joueurs que l'on va réutiliser 

                        for i in range(0,16):
                            await channels[i].set_permissions(member, overwrite=cant_talk)
                        #Enlève les permissions de tous les salons pour tous les joueurs


                        print(Lroles_final)
                        irole = rdm.randint(0,len(Lroles_final)-1)
                        role_given = Lroles_final[irole]
                        Lroles_final.pop(irole)
                        #Choisi un rôle au hasard et le retire de la liste
                        
                        await ctx.channel.send("{} a le rôle __{}__".format(member, role_given))

                        if role_given in dicoroles:
                            await channels[dicoroles[role_given]].set_permissions(member, overwrite=can_talk)

                            if role_given == "Infect" or role_given == 'LGB':
                                await channels[3].set_permissions(member, overwrite=can_talk)

                        #Donne les permissions nécéssaires pour chaque joueur en fonction de son rôle (utilise le dictionnaire)
                        
                        if role_given in trad_roles:
                            await member.send("Ton rôle est: __{}__".format(trad_roles[role_given]))
                            await member.send("``{}``".format(desc_roles[role_given]))
                        else:
                            await member.send("Ton rôle est: __{}__".format(role_given))
                            await member.send("``{}``".format(desc_roles[role_given]))
                        print("{} a le rôle {}".format(member, trad_roles[role_given]))

                        Lp.append([str(member),role_given,str(member.id)])

                        dicop[str(member.id)] = compteur
                        compteur += 1
                    

            else:
                await ctx.channel.send("ERREUR: commande erronée:")
                embed.set_author(name = "LG Bot")
                embed.add_field(name ='.start <nombre participants>', value = "Le nom du maître de jeu est erroné ou il n'est pas connecté dans le channel vocal.", inline = False)
                await ctx.send(embed=embed)

        else:
            await ctx.channel.send("ERREUR: commande erronée:")
            embed.set_author(name = "LG Bot")
            embed.add_field(name ='.start <nombre participants>', value = "Il n'y a pas le même nombre de rôles que de joueurs.", inline = False)
            await ctx.send(embed=embed)
    
    else:
        await ctx.channel.send("ERREUR: commande erronée:")
        embed.set_author(name = "LG Bot")
        embed.add_field(name ='.start <nombre participants>', value = "Aucune partie n'a été créé ou une partie est déjà en cours.", inline = False)
        await ctx.send(embed=embed)


@client.command()
@commands.has_any_role("Maître du Jeu","Développeur")
async def couple(ctx):

    global dicop, dicoroles, Lp, can_talk, cant_talk, game_started, channels,L_joueurs,check_couple

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande couple"
        )

    if game_started == True and check_couple == False:

        check_couple = True

        members = [k for k in L_joueurs]
        
        i1 = rdm.randint(0,len(members)-1)
        if str(members[i1]) != author:
            amant1 = members[i1]
            members.pop(i1)

        i2 = rdm.randint(0,len(members)-1)
        if str(members[i2]) != author:
            amant2 = members[i2]
            members.pop(i2)

        await channels[1].set_permissions(amant1, overwrite=can_talk)
        await channels[1].set_permissions(amant2, overwrite=can_talk)
        await amant1.send("Tu es en couple avec {}".format(amant2))
        await amant2.send("Tu es en couple avec {}".format(amant1))
        await ctx.channel.send("Amant 1: {}, Amant 2: {}".format(amant1,amant2))
    
    else:
        await ctx.channel.send("Il y a déjà un couple dans la partie.")


@client.command()
@commands.has_any_role("Maître du Jeu","Développeur")
async def cupidon(ctx, idcupidon, idcouple1, idcouple2):

    global dicop, dicoroles, Lp, can_talk, cant_talk, game_started, channels, L_joueurs

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande cupidon"
        )

    str_cup = str(idcupidon)
    str_c1 = str(idcouple1)
    str_c2 = str(idcouple2)

    if game_started == True:

        if str_c1 in dicop:
            cpl1 = L_joueur[dicop[str_c1]]

        if str_c2 in dicop:
            cpl2 = L_joueur[dicop[str_c2]]

        if str_c1 == str_c2:
            await ctx.channel.send("ERREUR: commande erronée:")
            embed.set_author(name = "LG Bot")
            embed.add_field(name ='.cupidon <id cupidon> <id couple 1> <id couple 2>', value = "Vérifiez que les ID sont les bons et que les deux amants ne sont pas la même personne.", inline = False)
            await ctx.send(embed=embed)

        else:
            await channels[1].set_permissions(cpl1, overwrite=can_talk)
            await channels[1].set_permissions(cpl2, overwrite=can_talk)
            await cpl1.send("Tu es en couple avec {}".format(cpl2))
            await cpl2.send("Tu es en couple avec {}".format(cpl1))
            await ctx.channel.send("Amant 1: {}, Amant 2: {}".format(cpl1,cpl2))



@client.command()
async def enfant(ctx, ide, idm):

    global dicop, dicoroles, Lp, can_talk, cant_talk, game_started, channels, L_joueurs

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande enfant"
        )

    str_ide = str(ide)
    str_idm = str(idm)

    if game_started == True:

        if str_ide in dicop:
            pe = Lp[dicop[str_ide]]
            rolee = pe[1]
            membere = L_joueurs[dicop[str_ide]]

        if str_idm in dicop:
            pm = Lp[dicop[str_idm]]
            rolem = pm[1]
            memberm = L_joueurs[dicop[str_idm]]

        if rolee == 'Enfant' and rolem == 'Mort':
            await channels[3].set_permissions(membere, overwrite=can_talk)
            await channels[0].set_permissions(membere, overwrite=cant_talk)
            await ctx.channel.send("{} est maintenant un LG".format(membere))

        else:
            await ctx.channel.send("ERREUR: commande erronée:")
            embed.set_author(name = "LG Bot")
            embed.add_field(name ='.enfant <id enfant> <id maitre>', value = "Vérifiez que les ID sont les bons et que le maître de l'enfant est bien mort.", inline = False)
            await ctx.send(embed=embed)



@client.command()
@commands.has_any_role("Maître du Jeu","Développeur")
async def voleur(ctx, idv, idc):

    global dicop, dicoroles, Lp, can_talk, cant_talk, game_started, channels,L_joueurs

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande voleur"
        )

    if game_started == True:
        
        if str_idv in dicop:
            pv = Lp[dicop[str_idv]]
            rolev = pv[1]
            memberv = L_joueurs[dicop[str_idv]]

        if str_idc in dicop:
            pc = Lp[dicop[str_idc]]
            rolec = pc[1]
            memberc = L_joueurs[dicop[str_idc]]


        pc[1],pv[1] = rolev,rolec

        if rolev != 'Voleur':
            await ctx.channel.send("ERREUR: commande erronée:")
            embed.set_author(name = "LG Bot")
            embed.add_field(name ='.voleur <id du voleur>', value = "Vérifiez que l'ID est le bon et que le joueur est bien voleur.", inline = False)
            await ctx.send(embed=embed)

        else:
            await channels[19].send("{} a volé le rôle de {}, qui était {}.".format(str(memberv),str(memberc),str(rolec)))
            await memberc.send("Ton rôle a été volé, tu es maintenant Voleur")
            await memberv.send("Tu as volé la personne avec le rôle {}".format(str(rolec)))
            if rolec in dicoroles:
                await channels[dicoroles[rolec]].set_permissions(memberv, overwrite=can_talk)
                await channels[dicoroles[rolec]].set_permissions(memberc, overwrite=cant_talk)
            await channels[dicoroles[rolev]].set_permissions(memberv, overwrite=cant_talk)
            await channels[dicoroles[rolev]].set_permissions(memberc, overwrite=can_talk)



@client.command()
@commands.has_any_role("Maître du Jeu","Développeur")
async def kill(ctx, idinp):
#Commande permettant de tuer un joueur

    global L_joueurs, Lroles_dispo, game_started, channels, dicop, dicoroles, can_talk, cant_talk, Lp, ancien_dead

    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande kill"
        )

    if game_started == True:

        str_id = str(idinp)

        if str_id in dicop:
            print('OK')
            pla = Lp[dicop[str_id]]
            rolep = pla[1]

            member = L_joueurs[dicop[str_id]]
            
            if rolep == 'Ancien' and ancien_dead == False:
                ancien_dead = True
                await ctx.message.send("L'ancien a été tué une fois. Entrez cette commande à nouveau pour définitivement le tuer.")
            
            elif rolp == 'Mort':
                await ctx.channel.send("ERREUR: commande erronée:")
                embed.set_author(name = "LG Bot")
                embed.add_field(name ='.kill <id du mort>', value = "Vérifiez que l'ID est le bon et que le joueur n'est pas déjà mort.", inline = False)
                await ctx.send(embed=embed)

            else:
                if rolep in dicoroles:
                    await channels[dicoroles[rolep]].set_permissions(member, overwrite=cant_talk)
                if rolep == "Infect" or rolep == 'LGB':
                        await channels[3].set_permissions(member, overwrite=cant_talk)
                await channels[15].set_permissions(member, overwrite=can_talk)
                await channels[18].set_permissions(member, overwrite=can_see)
                await channels[18].send("**{}** est mort ! Il était __{}__ !".format(str(member), rolep))
                await ctx.channel.send("**{}** est mort ! Il était __{}__ !".format(str(member), rolep))
                await member.edit(mute=True)
                pla[1] = 'Mort'

        else:
            await ctx.channel.send("ERREUR: commande erronée:")
            embed.set_author(name = "LG Bot")
            embed.add_field(name ='.kill <id du mort>', value = "Vérifiez que l'ID est le bon et que le joueur n'est pas déjà mort.", inline = False)
            await ctx.send(embed=embed)




@client.command()
async def listeid(ctx):

    author = str(ctx.message.author)

    channel = ctx.message.author.voice.channel
    members = channel.members

    for member in members:
        await ctx.channel.send(str(member.id))


@client.command()
async def mute(ctx, status):
    global L_joueurs

    author = ctx.message.author
    
    embed = discord.Embed(
            colour = discord.Color.red(),
            title = "Commande mute"
        )

    if status == 'Mute' or status == 'mute':
        for member in L_joueurs:
            await member.edit(mute=True)
    elif status == 'Unmute' or status == 'unmute':
        for member in L_joueurs:
            await member.edit(mute=False)
    else:
        await ctx.channel.send("ERREUR: commande erronée:")
        embed.set_author(name = "LG Bot")
        embed.add_field(name ='.mute <mute/unmute>', value = "mute: mute tous les gens du salon. unmute: les unmute", inline = False)
        await ctx.send(embed=embed)



@client.command()
async def talk(ctx):

    channel = ctx.message.author.voice.channel
    members = channel.members

    if in_game == False:
        for member in members:
            await channels[18].set_permissions(member, overwrite=can_talk)
            await channels[15].set_permissions(member, overwrite=cant_talk)
            print("OK, {}".format(member))

    else:
        await ctx.channel.send("ERREUR: Veuillez entrer la commande .stop avant de faire cette commande")



@client.command()
@commands.has_any_role("Maître du Jeu","Développeur")
async def stop(ctx):
#Commande d'arrêt du jeu

    global in_game, L_joueurs, Lroles_dispo
    
    in_game = False
    L_joueurs = []
    Lroles_dispo = []

    await ctx.channel.send("La partie est arrêtée")




client.run('NjgzNDY4NzUwNTgyMDU0OTM3.XlsBjQ.Hr2R4-sllhfeoUEYhmDCO3wSaEY')




