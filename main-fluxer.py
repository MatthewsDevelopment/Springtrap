import fluxer
from fluxer.checks import has_permission
from fluxer.enums import Permissions
from fluxer import HTTPClient
import asyncio
import aiohttp
from googletrans import Translator
from dotenv import load_dotenv
import os

load_dotenv('.env')
BOTPREFIX=os.getenv("FLUXERBOTPREFIX")
BASEURL=os.getenv("FLUXERBASEURL")
client = fluxer.Bot(command_prefix=BOTPREFIX, intents=fluxer.Intents.default(), api_url=BASEURL)

@client.event
async def on_ready():
    print(f"{client.user.username} [Fluxer.app] Bot is Ready")

@client.command()
async def help(ctx):
    embed = fluxer.Embed(title=f"{client.user.username}", description=f"{BOTPREFIX}help\n{BOTPREFIX}ping\n{BOTPREFIX}say\n{BOTPREFIX}esay\n{BOTPREFIX}wsay\n{BOTPREFIX}wesay\n{BOTPREFIX}deletewebhook\n{BOTPREFIX}webhooklist\n{BOTPREFIX}translate")
    await ctx.reply(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.reply("Pong!")

@client.command()
async def say(ctx, *, message: str):
    if not message:
        await ctx.reply(f"Please provide some text for me to say! Usage: `{BOTPREFIX}say <text>`")
        return
    if "@everyone" in message.lower():
        await ctx.reply("You can not have the bot mention everyone")
        return
    if any(word in message for word in blockedwords):
        await ctx.reply("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
        return
    await ctx.reply(message)

@client.command()
@has_permission(fluxer.Permissions.KICK_MEMBERS)
async def esay(ctx, title:str, *, message:str):
    if any(word in title for word in blockedwords):
        await ctx.reply("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
        return
    if any(word in message for word in blockedwords):
        await ctx.reply("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
        return
    embed = fluxer.Embed(title=f"{title}", description=f"{message}")
    await ctx.reply(embed=embed)

@client.command()
@has_permission(fluxer.Permissions.KICK_MEMBERS)
async def wsay(ctx, webhookid:str, webhooktoken:str, *, message:str):
    if "@everyone" in message.lower():
        await ctx.reply("You can not have the bot mention everyone")
        return
    if any(word in message for word in blockedwords):
        await ctx.reply("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
        return
    await ctx._http.execute_webhook(webhookid, webhooktoken, content=f"{message}", wait=True)

@client.command()
@has_permission(fluxer.Permissions.KICK_MEMBERS)
async def wesay(ctx, webhookid:str, webhooktoken:str, *, message:str):
    if "@everyone" in message.lower():
        await ctx.reply("You can not have the bot mention everyone")
        return
    if any(word in message for word in blockedwords):
        await ctx.reply("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
        return
    embed = fluxer.Embed(description=f"{message}")
    await ctx._http.execute_webhook(webhookid, webhooktoken, embeds=[embed.to_dict()], wait=True)
    await ctx.reply("Sent the embed to the webhook")

@client.command()
@has_permission(fluxer.Permissions.KICK_MEMBERS)
async def deletewebhook(ctx, webhookid:str, webhooktoken:str):
    await client._http.delete_webhook_with_token(webhookid, webhooktoken)
    await ctx.reply(f"Webhook deleted successfully.")

@client.command()
@has_permission(fluxer.Permissions.KICK_MEMBERS)
async def webhooklist(ctx):
    try:
        webhooks = await client.fetch_guild_webhooks(ctx.guild_id)
        if not webhooks:
            await ctx.reply("No webhooks found in this server.")
            return
        response = f"Webhooks for {ctx.guild_id} (Found {len(webhooks)} webhooks):\n\n"
        for webhook in webhooks:
            response += f"• {webhook.name} - {webhook.id} {webhook.token}\n"
        await ctx.reply(response)
    except:
        embed = fluxer.Embed(title="AN ERROR HAS OCCURED", description="Either I need to have the **MANAGE_WEBHOOKS** permission to use this command or some unknown error has occured")
        await ctx.reply(embed=embed)
        

@client.command()
async def translate(ctx, lang, *, textmessage):
    translator = Translator()
    translation = translator.translate(textmessage, dest=lang)
    embed = fluxer.Embed(title="Translator (using Google Translate)", description=f"Original message: {textmessage}\n\nTranslated to {lang}: {translation.text}")
    await ctx.reply(embeds=[embed])

@client.command()
async def encoder(ctx, option="", *, textmessage:str):
    if option == "base64encode":
        encoded_message = base64.b64encode(textmessage.encode())
        embed = fluxer.Embed(title="Translator (using Google Translate)", description=f"Original message: {textmessage}\n\nEncoded message: {encoded_message.decode()}")
        await ctx.reply(embed=embed)
    if option == "base64decode":
        encoded_message = f'{textmessage}'
        decoded_message = base64.b64decode(encoded_message)
        embed = fluxer.Embed(title="Base64 Encoder", description=f"Original message: {textmessage}\n\nDecoded message: {decoded_message.decode()}")
        await ctx.reply(embed=embed)





if "__main__" == __name__:
    with open("blockedwords.txt", "r") as f:
        blockedwords = f.read().splitlines()

if __name__ == "__main__":
    TOKEN = os.getenv("FLUXERBOTTOKEN")
    client.run(TOKEN)
