# Springtrap

> [!CAUTION]
> The Guilded bot is deprecated and will no longer work after Guilded shuts down on December 19th, 2025. Code will remain up for legacy reasons.

Springtrap is an embed builder (that can be sent through the bot or webhook), webhook deleter, and translator bot for Discord, Guilded, and Stoat.chat. This bot includes a filter to prevent the bots from saying bad and illegal stuff.

With the Discord bot, it supports both mention prefix and slash commands.

For Stoat.chat users: Our Stoat bot is not available on any 3rd party instances. To use Springtrap on a 3rd party instance, you will need to self host the bot yourself. Make sure the Stoat instance you are using is using Stoat v0.7 or newer for this to work.

## Original Bots:

[Discord Bot](https://discord.com/oauth2/authorize?client_id=844448961195409418&permissions=0&integration_type=0&scope=bot+applications.commands) - [Revolt Bot](https://app.revolt.chat/bot/01H96QS2SJP1NCVDMQZFMZKMYP)

[Discord Server](https://discord.gg/VBJyndbKC2) - [Stoat Server](https://rvlt.gg/fSfKknAw)

## Setup Guide:

1. Fork/Download this source code
2. Create a Discord, Guilded, and/or Stoat bot
- For Discord: Create a Discord bot in https://discord.com/developers/applications
- For Guilded: Head to your server and go to your bot settings
- For Stoat: Head to https://app.revolt.chat/settings/bots and create a bot by clicking "Create a bot" (if using a 3rd party instance, app.revolt.chat would be the domain of your instance)
3. Fill in everything in the .env.example file and rename .env.example to .env
- DISCORDBOTTOKEN= -> Your Discord bot token
- GUILDEDBOTTOKEN= -> Your Guilded bot token
- GUILDEDBOTPREFIX= -> Prefix for the Guilded bot
- STOATBOTTOKEN= -> Your Stoat bot token
- STOATBOTPREFIX= -> Prefix for the Stoat bot
- STOATBASEURL= -> The base API url if the Stoat instance (Defaults to normal Stoat instance if left blank)
- STOATWEBSOCKETBASE= -> The websocket base. Can be found in the ws part in the base api url (Defaults to normal Stoat instance if left blank)
- LAUNCHMODE=0 -> Refer to the modes section below
- PTERODACTYL_PANELURL= -> (Optional) Pterodactyle panel url (include the https:// or http://
- PTERODACTYL_APIKEY= -> (Optional) Your Pterodactyle API key
- PANEL_SERVERID= -> (Optional) The server idea for the Pterodactyle server
4. Install everything from requirements.txt (Command is: pip install -r requirements.txt)
5. Run the Bot (Command is: python main.py)

NEVER SHARE YOUR TOKENS WITH ANYONE!

MODES:

- 0 = Discord+Stoat Bot
- 1 = Discord Bot Only
- 2 = Stoat Bot Only
- 3 = Discord, Guilded, and Stoat Bot
- 4 = Guilded Bot Only
- 5 = Discord and Guildeds Bot

## WARNING:

THIS SOFTWARE IS PROVIDED AS-IS WITHOUT WARRENTY OF ANY KIND and it is to be used at your own risk. The Creator of this source code will NOT be liable for any damages caused from using the software. We will also not cover any hosting fees.