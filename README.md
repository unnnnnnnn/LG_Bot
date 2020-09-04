# 🐺 LG Bot

![Logo](https://www.loups-garous-en-ligne.com/jeu/assets/images/carte2.png)

LG Bot is a discord bot that allows members of a server to play a board game called 'Werewolf', but on discord.

## 📌 Usefull links

[**Invite LG Bot to your server**](https://discord.com/oauth2/authorize?client_id=683468750582054937&permissions=536734712&scope=bot)

## 🛠️ Player commands

* `lg!help`: Open the help menu.

* `lg!roles`: Open informations about roles.

* `lg!breport <text>`: Send a bug report, a translation error or a suggestion for the bot to the bot's admins.

## 🛠️ Admin commands

* `lg!setup`: Set all the channels up that are used to play the game.

* `lg!delete`: Delete all the text channels used to play.

* `lg!lsetting <language>`: Change the bot's language (default is english). Available languages are **french** and **english**

* `lg!crypt <value>`: Change the chance of a letter changing during message's encryption.

## 🛠️ Game Master commands

You need to have the **"LG Host"** role to use those commands

* `lg!create`: Create a game. All informations will be given once you use the command.

* `lg!sign ['clear']`: Sign everyone up to the game. Add 'clear' to clear the player list.

* `lg!remove <user>`: Remove someone from the list. You need to write it like a discord tag: Name#XXXX

* `lg!players`: Show the player list in the game.

* `lg!start ['lovers']`: Start a game. Add 'lovers' if you want to have a random Lovers couple in the game.

* `lg!revive <id>`: Revive a player that is dead.

* `lg!fmenu`: Force the apparition of the menu.

* `lg!freset`: Force the reset of a game.

## ⚙️ How to use the bot

Enter the `lg!setup` command to create the channels

If you have the role **LG Role**, use the command `lg!create` to create a game

When everyone is in a voice channel, use the `lg!sign` command to register all the players

Use the `lg!start` command to start the game

As the game master you will have access to a menu like this one:

![Menu](https://i.ibb.co/pvdr4kh/Capture.png)

You can interact with the reactions, and the menus change between night and day.

The actions done by the reactions are explained on the menus.

## ✉️ Contact me

If you have any question please contact me there:

> Twitter: `@unnnzz`
>
> Discord: `unnn#1091`

**I am still a beginner and my code is probably very messy and could be improved, so feel free to give me advices !**

## 📗 Planned updates

* `New game system (only needed channels are created)`

* `More languages`

* `Auto-game setting (basically the game would not need a Game Master to be played)`

* `Ban command (prevents from playing the game)`
