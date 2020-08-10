import discord
import asyncio
import sys
import time
import os
from discord.utils import get
from discord.ext import commands


os.chdir(os.path.dirname(__file__))

with open('token.txt' ,'r') as f:
    bot_token = f.readline()

liste_roles = ['Villageois','Voyante','Chasseur','Jaloux','Ancien','Sorcière','PF','Bouc','Idiot','Corbeau','Chaman','Renard','Ours','Soeur','Frère','Chevalier','Salvateur','LG','LGA','IPDL','LGB','Cupidon','JDF','Ange','Enfant','Voleur','Sectaire','Juge','Confesseur','Chaperon','Ankou','Dictateur','Noctambule','Oeil','Traitre','Imposteur','Faucheur','Servante','Assassin','Devin']
#Liste de tous les rôles
liste_LG = ['LG','LGA','IPDL','LGB']
liste_village = ['Villageois','Voyante','Chasseur','Ancien','Sorcière','PF','Bouc','Idiot','Corbeau','Chaman','Renard','Ours','Soeur','Frère','Chevalier','Salvateur','Cupidon','Jaloux','Chaperon','Ankou','Dictateur','Noctambule','Oeil','Faucheur']


LrVillage = ['Villageois','Voyante','Chasseur','Ancien','Sorcière','PF','Bouc','Idiot','Corbeau','Chaman','Renard','Ours','Soeur','Frère','Chevalier','Salvateur','Jaloux','Chaperon','Ankou','Dictateur','Noctambule','Oeil','Faucheur','Juge','Confesseur']
LrLG = ['LG','LGA','IPDL','Traitre']
LrSolo = ['JDF','Sectaire','Assassin','Devin','LGB','Ange']
LrAutre = ['Servante', 'Imposteur', 'Voleur', 'Enfant', 'Cupidon']

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