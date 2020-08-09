import discord
import asyncio
import sys
import time
import os
from discord.utils import get
from discord.ext import commands


liste_roles = ['Villageois','Voyante','Chasseur','Jaloux','Ancien','Sorcière','PF','Bouc','Idiot','Corbeau','Chaman','Renard','Ours','Soeur','Frère','Chevalier','Salvateur','LG','LGA','IPDL','LGB','Cupidon','JDF','Ange','Enfant','Voleur','Sectaire','Juge','Confesseur','Chaperon','Ankou','Dictateur','Noctambule','Oeil','Traitre','Imposteur','Faucheur','Servante','Assassin','Devin']
#Liste de tous les rôles
liste_LG = ['LG','LGA','IPDL','LGB']
liste_village = ['Villageois','Voyante','Chasseur','Ancien','Sorcière','PF','Bouc','Idiot','Corbeau','Chaman','Renard','Ours','Soeur','Frère','Chevalier','Salvateur','Cupidon','Jaloux','Chaperon','Ankou','Dictateur','Noctambule','Oeil','Faucheur']


LrVillage = ['Villageois','Voyante','Chasseur','Ancien','Sorcière','PF','Bouc','Idiot','Corbeau','Chaman','Renard','Ours','Soeur','Frère','Chevalier','Salvateur','Jaloux','Chaperon','Ankou','Dictateur','Noctambule','Oeil','Faucheur','Juge','Confesseur']
LrLG = ['LG','LGA','IPDL','Traitre']
LrSolo = ['JDF','Sectaire','Assassin','Devin','LGB','Ange']
LrAutre = ['Servante', 'Imposteur', 'Voleur', 'Enfant', 'Cupidon']


# Liste des catégories de rôles

Lroles_dispo = []
#Liste des rôles disponibles dans 1 partie
Lroles_voleur = []
#Liste des rôles disponnibles pour l'imposteur/mîme/voleur thierc
Lroles_traitre = []
#Liste des rôles disponnibles pour le traître
dicoimp = {}

L_joueurs = []
#Liste des joueurs dans 1 partie (tempo)
Lp = []
#Liste finale de joueur

channels = []
Lchannels = []
text_channel_list = []
emojis_action = []
#Liste des channels text du serveur


dicomembers = {}
#Dictionnaire de joueurs (class members)


dicop_id_to_emoji = {}
dicop_name_to_emoji = {}
dicop_emoji = {}
Lemojis = []

inscription_chan = None

liste_couple = []
liste_charm = []
enfant_name = None
maitre_name = None
voleur_name = None
stolen_name = None
infect_name = None
charm_name = None
killed_name = None
panel_author = None
imposteur_name = None
noctambule_name = None
victime_name = None
servante_name = None
devo_name = None

is_compo = False
is_channels = False
in_game = False
game_started = False
day = True
is_enfant = False
#Booleans qui permettent de contrôler l'état de la partie

ancien_dead = False
check_couple = False
#Permet de gérer les erreurs liées à l'ancien et au couple

valuepf = 25
#Pourcentage par défaut que une lettre change pour la petite-fille

cpt_jour = 0
#Compteur de jour

is_info = False

id_panel = 0
id_vote = 0
step = ''
old_step = ''
# steps: Cupidon, Enfant, Voleur, Infecté, Charmé, Kill
cpt_reaction = 0

Lannonce_vote = []
# Liste pour annonce vote
Laffichage_vote = ""
# str annonce vote
Laffichage_joueurs = ""
# str affichage joueur commande liste
Laffichage_day = ""
# str affichage joueurs chaque jour

cant_talk = discord.PermissionOverwrite()
# Permission (ne peut pas voir le salon)
cant_talk.send_messages = False
cant_talk.read_messages = False
cant_talk.read_message_history = False

can_talk = discord.PermissionOverwrite()
# Permission (voit le salon et peut parler)
can_talk.send_messages = True
can_talk.read_messages = True

can_see = discord.PermissionOverwrite()
# Permissions (voit le salon mais ne peut pas parler)
can_see.send_messages = False
can_see.read_messages = True

annoncef = []

mdj = None

print("Les constantes sont à l'état initial")