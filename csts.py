import discord
import asyncio
import sys
import time
import os
from discord.utils import get
from discord.ext import commands


os.chdir(os.path.dirname(__file__))

with open('token.txt' ,'r') as f:
    TOKEN = f.readline()


liste_roles_fr = ['Villageois','Voyante','Chasseur','Jaloux','Ancien','Sorcière','PF','Bouc','Idiot','Corbeau','Chaman','Renard','Ours','Soeur','Frère','Chevalier','Salvateur','LG','LGA','IPDL','LGB','Cupidon','JDF','Ange','Enfant','Voleur','Sectaire','Juge','Confesseur','Chaperon','Ankou','Dictateur','Noctambule','Oeil','Traitre','Imposteur','Faucheur','Servante','Assassin','Devin']
liste_roles_en = ['Villager','Oracle','Hunter','Jealous','Ancient','Witch','Girl','Scapegoat','Idiot','Crow','Shaman','Fox','Bear','Sister','Brother','Knight','Guard','Werewolf','AW','WF','WW','Cupid','PP','Angel','Child','Thief','Sectarian','Juge','Confessor','RRH','Ankou','Dictator','Owl','Eye','Traitor','Impostor','Reaper','Servant','Assassin','Diviner']
#Liste de tous les rôles

liste_LG_fr = ['LG','LGA','IPDL','LGB']
liste_LG_en = ["Werewolf", "AW", "WF", "WW", 'Traitor']

liste_village_fr = ['Villageois','Voyante','Chasseur','Ancien','Sorcière','PF','Bouc','Idiot','Corbeau','Chaman','Renard','Ours','Soeur','Frère','Chevalier','Salvateur','Cupidon','Jaloux','Chaperon','Ankou','Dictateur','Noctambule','Oeil','Faucheur']
liste_village_en = ['Villager','Oracle','Hunter','Jealous','Ancient','Witch','Girl','Scapegoat','Idiot','Crow','Shaman','Fox','Bear','Sister','Brother','Knight','Guard','Juge','Confessor','RRH','Ankou','Dictator','Owl','Eye','Reaper']


LrVillage_fr = ['Villageois','Voyante','Chasseur','Ancien','Sorcière','PF','Bouc','Idiot','Corbeau','Chaman','Renard','Ours','Soeur','Frère','Chevalier','Salvateur','Jaloux','Chaperon','Ankou','Dictateur','Noctambule','Oeil','Faucheur','Juge','Confesseur']
LrVillage_en = ['Villager','Oracle','Hunter','Jealous','Ancient','Witch','Girl','Scapegoat','Idiot','Crow','Shaman','Fox','Bear','Sister','Brother','Knight','Guard','Juge','Confessor','RRH','Ankou','Dictator','Owl','Eye','Reaper']

LrLG_fr = ['LG','LGA','IPDL','Traitre']
LrLG_en = ["Werewolf", "AW", "WF", 'Traitor']

LrSolo_fr = ['JDF','Sectaire','Assassin','Devin','LGB','Ange']
LrSolo_en = ['PP', 'Sectarian', 'Assassin', 'Diviner', 'WW', 'Angel']

LrAutre_fr = ['Servante', 'Imposteur', 'Voleur', 'Enfant', 'Cupidon']
LrAutre_en = ['Servant', 'Impostor', 'Thief', 'Child', 'Cupid']


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

ok = "✅"
non = "❌"