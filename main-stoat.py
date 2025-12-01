import stoat
from stoat.ext import commands
import asyncio
import aiohttp
from googletrans import Translator
from dotenv import load_dotenv
import os
import requests
import base64

load_dotenv('.env')
BOTPREFIX=os.getenv("STOATBOTPREFIX")
BASEURL=os.getenv("STOATBASEURL")
WEBSOCKETURL=os.getenv("STOATWEBSOCKETURL")
client = commands.Bot(command_prefix=BOTPREFIX, http_base=BASEURL, websocket_base=WEBSOCKETURL)
PTERODACTYL_PANELURL=os.getenv("PTERODACTYL_PANELURL")
PTERODACTYL_APIKEY=os.getenv("PTERODACTYL_APIKEY")
PANEL_SERVERID=os.getenv("PANEL_SERVERID")

def get_server_stats():
    headers = {
        'Authorization': f'Bearer {PTERODACTYL_APIKEY}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f'{PTERODACTYL_PANELURL}/api/client/servers/{PANEL_SERVERID}/resources', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@client.on(stoat.ReadyEvent)
async def on_ready(_) -> None:
    print("Springtrap [Revolt] Bot is Ready")

@client.on(commands.CommandErrorEvent)
async def on_command_error(event):
    ctx = event.context
    error = event.error
    await ctx.send(f"Something went wrong. {error}")



@client.command()
async def help(ctx):
    embed = pyvolt.SendableEmbed(title="Springtrap", description=f"{BOTPREFIX}help - This message\n{BOTPREFIX}ping - Pong\n{BOTPREFIX}args - Arguments for commands\n{BOTPREFIX}say - Make me say things\n{BOTPREFIX}esay - Make me say things in a embed\n{BOTPREFIX}msay - Send a message using Masquerade\n{BOTPREFIX}translate - Translate text to a different language\n{BOTPREFIX}encoder = Encode/Decode text\n{BOTPREFIX}systeminfo - Get resource usage of the python server")
    await ctx.channel.send(embeds=[embed])

@client.command()
async def ping(ctx):
    await ctx.channel.send('Pong!')

@client.command()
async def systeminfo(ctx):
    stats = get_server_stats()
    if stats:
        cpu = stats['attributes']['resources']['cpu_absolute']
        memory = round(stats['attributes']['resources']['memory_bytes'] / (1024 * 1024), 2)
        disk = round(stats['attributes']['resources']['disk_bytes'] / (1024 * 1024), 2)
        embed = stoat.SendableEmbed(title="Springtrap System Info", description=f"CPU Usage: {cpu}%\nRAM Usage: {memory}MB\nDisk Usage: {disk}MB")
        await ctx.channel.send(embeds=[embed])
        return
    else:
        embed = stoat.SendableEmbed(title="Springtrap System Info", description="Something went wrong")
        await ctx.channel.send(embeds=[embed])
        return None

@client.command()
async def args(ctx):
    embed = stoat.SendableEmbed(title="Arguments for Springtrap commands", description="{BOTPREFIX}say <message>\n{BOTPREFIX}esay <hexcolor> <embedtitle> <embedmessage>\n{BOTPREFIX}translate <language> <text>\n{BOTPREFIX}msay <avatarurl> <masqueradename> <text>")
    await ctx.channel.send(embeds=[embed])

@client.command()
async def say(ctx, *, message:str):
    if any(word in message for word in blockedwords):
        await ctx.channel.send("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
        return
    await ctx.channel.send(message)

@client.command()
async def esay(ctx, colorhex:str, title:str, message:str):
    if any(word in title for word in blockedwords):
        await ctx.channel.send("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
        return
    if any(word in message for word in blockedwords):
        await ctx.channel.send("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
        return
    embed = stoat.SendableEmbed(title=f"{title}", description=f"{message}", color=f'#{colorhex}')
    await ctx.channel.send(embeds=[embed])

@client.command()
async def msay(ctx, avatarurl:str, mname:str, message:str):
    if any(word in message for word in blockedwords):
        await ctx.channel.send("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
        return
    await ctx.channel.send(f'{message}', masquerade=pyvolt.MessageMasquerade(name=f'{mname}', avatar=f'{avatarurl}'))

@client.command()
@commands.server_only()
async def wsay(ctx, wname:str, message:str):
    if BASEURL == "https://beta.revolt.chat/api":
        if any(word in message for word in blockedwords):
            await ctx.channel.send("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
            return
        webhook = await client.http.create_webhook(f"{ctx.channel.id}", name=f"{wname}")
        await webhook.execute(f"{message}")
        await webhook.delete()
    else:
        await ctx.send("This command is disabled because this command uses a Revolt beta feature that only works through the beta API url. If you are the bot owner, open the .env file and put in https://beta.revolt.chat/api within REVOLTBASEURL")

@client.command()
async def translate(ctx, lang, *, textmessage):
    translator = Translator()
    translation = translator.translate(textmessage, dest=lang)
    embed = stoat.SendableEmbed(title="Translator (using Google Translate)", description=f"Original message: {textmessage}\n\nTranslated to {lang}: {translation.text}")
    await ctx.channel.send(embeds=[embed])

@client.command()
async def encoder(ctx, option="", *, textmessage:str):
    if option == "base64encode":
        encoded_message = base64.b64encode(textmessage.encode())
        embed = stoat.SendableEmbed(title="Translator (using Google Translate)", description=f"Original message: {textmessage}\n\nEncoded message: {encoded_message.decode()}")
        await ctx.channel.send(embeds=[embed])
    if option == "base64decode":
        encoded_message = f'{textmessage}'
        decoded_message = base64.b64decode(encoded_message)
        embed = stoat.SendableEmbed(title="Base64 Encoder", description=f"Original message: {textmessage}\n\nDecoded message: {decoded_message.decode()}")
        await ctx.channel.send(embeds=[embed])

@client.command()
@commands.server_only()
async def deletedwebhook(ctx, webhookurl):
    if not ctx.server.permissions_for(ctx.author).manage_server:
        embed = stoat.SendableEmbed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE SERVER** permission to use this command.")
        await ctx.channel.send(embeds=[embed])
        return
    if 'https://discord.com/api/webhooks/' in webhookurl:
        response = requests.delete(webhookurl)
        if response.status_code == 204:
            await ctx.channel.send('Webhook deleted successfully.')
        else:
            await ctx.channel.send(f'Failed to delete webhook. Status code: {response.status_code}')
        return
    else:
        await ctx.channel.send(f"You did not provide a valid webhook url\n\n{BOTPREFIX}deletewebhook <webhookurl>")

@client.command()
@commands.server_only()
async def deleterwebhook(ctx):
    await ctx.channel.send("This command is disabled because this command uses a Revolt beta feature that only works through the beta API url but not stable enough for this feature to work.")

@client.command()
@commands.server_only()
async def webhooklist(ctx):
    await ctx.channel.send("This command is disabled because this command uses a Revolt beta feature that only works through the beta API url but not stable enough for this feature to work.")

if "__main__" == __name__:
    with open("blockedwords.txt", "r") as f:
        blockedwords = f.read().splitlines()

@client.command()
@commands.is_owner()
async def status(ctx, *, statustext):
    await client.http.edit_my_user(status=stoat.UserStatusEdit(text=f"{statustext}"))
    await ctx.channel.send("Status has been changed")

@client.command()
@commands.is_owner()
async def presence(ctx, presencetype=""):
    if presencetype == "online":
        await client.http.edit_my_user(status=stoat.UserStatusEdit(presence=stoat.Presence.online))
        await ctx.channel.send("Status has been changed")
    if presencetype == "idle":
        await client.http.edit_my_user(status=stoat.UserStatusEdit(presence=stoat.Presence.idle))
        await ctx.channel.send("Status has been changed")
    if presencetype == "focus":
        await client.http.edit_my_user(status=stoat.UserStatusEdit(presence=stoat.Presence.focus))
        await ctx.channel.send("Status has been changed")
    if presencetype == "dnd":
        await client.http.edit_my_user(status=stoat.UserStatusEdit(presence=stoat.Presence.busy))
        await ctx.channel.send("Status has been changed")
    if presencetype == "invisible":
        await client.http.edit_my_user(status=stoat.UserStatusEdit(presence=stoat.Presence.invisible))
        await ctx.channel.send("Status has been changed")



client.run(os.getenv("STOATBOTTOKEN"))
