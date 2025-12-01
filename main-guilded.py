import guilded
from guilded.ext import commands
from guilded import Webhook
import requests
import aiohttp
from googletrans import Translator
import base64
import random
import json
from dotenv import load_dotenv
import os

load_dotenv()
client = guilded.Client()
BOTPREFIX=os.getenv("GUILDEDBOTPREFIX")
client = commands.Bot(command_prefix=BOTPREFIX)
client.remove_command("help")
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

@client.event
async def on_ready():
    print("Springtrap [Guilded] Bot is Ready")

@client.command()
async def help(ctx):
    embed = guilded.Embed(title="Springtrap", description=f"{BOTPREFIX}help - This message\n{BOTPREFIX}ping - Get the Latency of the Bot\n{BOTPREFIX}systeminfo - Get resource usage of the python server\n{BOTPREFIX}say - Make me say things\n{BOTPREFIX}esay - Make and send a simple embed\n{BOTPREFIX}wesay - Make and send a simple embed through webhook\n{BOTPREFIX}translate - Translate text to a different language\n{BOTPREFIX}encoder = Encode/Decode text", color=(7864480))
    embed.add_field(name="Tools", value=f"{BOTPREFIX}args - Arguments for the say commands", inline=False)
    embed.add_field(name="Decimal Colors", value="When creating embeds, we use decimal colors. Here is a tool to get decimal colors: https://www.mathsisfun.com/hexadecimal-decimal-colors.html", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'PONG!\nLatency: {round(client.latency * 1000)}ms')

@client.command()
async def args(ctx):
    embed = guilded.Embed(title="Arguments for Springtrap commands", color=(7864480))
    embed.add_field(name="esay args", value=f"{BOTPREFIX}esay <decimalcolor> <embedtitle> <embedmessage>", inline=False)
    embed.add_field(name="wesay args", value="{BOTPREFIX}wesay <webhookurl> <decimalcolor> <embedtitle> <embedmessage>", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def say(ctx, *, message):
    await ctx.send(f'{message}')
    await ctx.message.delete()

@client.command()
@commands.has_server_permissions(manage_messages=True)
async def esay(ctx, decimalcolor:int, title:str, message:str):
    if any(word in title for word in blockedwords):
        await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
        return
    if any(word in message for word in blockedwords):
        await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
        return
    embed = guilded.Embed(title=f"{title}", description=f'{message}', color=(decimalcolor))
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command()
async def wesay(ctx, webhookurl:str, decimalcolor:int, title:str, message:str):
    if ctx.author.server_permissions.manage_webhooks:
        if any(word in title for word in blockedwords):
            await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
            return
        if any(word in message for word in blockedwords):
            await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
            return
        if 'https://media.guilded.gg/webhooks/' in webhookurl:
            embed = guilded.Embed(title=f"{title}", description=f'{message}', color=(decimalcolor))
            async with aiohttp.ClientSession() as session:
                webhook = guilded.Webhook.from_url(f'{webhookurl}', session=session)
                await webhook.send(embed=embed)
                await ctx.message.delete()
        else:
            await ctx.send("This is not a Guilded webhook url")
    else:
        embed = guilded.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await ctx.send(embed=embed)

@client.command()
async def translate(ctx, lang, *, textmessage):
    translator = Translator()
    translation = translator.translate(textmessage, dest=lang)
    embed = guilded.Embed(title="Translator", color=(7864480))
    embed.add_field(name="Original message", value=f'{textmessage}')
    embed.add_field(name=f"Translated to: {lang}", value=f'{translation.text}')
    embed.set_footer(text="Google Translate was used to translate the text")
    await ctx.send(embed=embed)

@client.command()
async def encoder(ctx, option="", *, textmessage:str):
    if option == "base64encode":
        encoded_message = base64.b64encode(textmessage.encode())
        embed = guilded.Embed(title="Base64 Encoder", color=(7864480))
        embed.add_field(name="Original message", value=f'{textmessage}')
        embed.add_field(name="Encoded message", value=f'{encoded_message.decode()}')
        await ctx.send(embed=embed)
        return
    if option == "base64decode":
        encoded_message = f'{textmessage}'
        decoded_message = base64.b64decode(encoded_message)
        embed = guilded.Embed(title="Base64 Encoder", color=(7864480))
        embed.add_field(name="Original message", value=f'{textmessage}')
        embed.add_field(name="Decoded message", value=f'{decoded_message.decode()}')
        await ctx.send(embed=embed)
        return
    else:
        embed = guilded.Embed(title="ARGUMENTS REQUIRED/INVALID", description=f"{BOTPREFIX}encoder <option> <message>", color=(16711680))
        embed.add_field(name="Available options", value="base64encode\nbase64decode")
        await ctx.send(embed=embed)
        return

if "__main__" == __name__:
    with open("blockedwords.txt", "r") as f:
        blockedwords = f.read().splitlines()





client.run(os.getenv("GUILDEDBOTTOKEN"))
