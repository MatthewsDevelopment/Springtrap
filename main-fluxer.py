import fluxer
import asyncio
import aiohttp
from googletrans import Translator
from dotenv import load_dotenv
import os

load_dotenv('.env')
BOTPREFIX=os.getenv("FLUXERBOTPREFIX")
client = fluxer.Bot(command_prefix=BOTPREFIX, intents=fluxer.Intents.default())

@client.event
async def on_ready():
    print(f"{client.user.username} [Fluxer.app] Bot is Ready")

@client.command()
async def help(ctx):
    embed = fluxer.Embed(title=f"{client.user.username}", description=f"{BOTPREFIX}help\n{BOTPREFIX}ping\n{BOTPREFIX}say")
    await ctx.reply(content="Help menu", embeds=[embed.to_dict()])

@client.command()
async def ping(ctx):
    await ctx.reply("Pong!")

@client.command()
async def say(ctx, *, text: str):
    if not text:
        await message.reply(f"Please provide some text for me to say! Usage: `{BOTPREFIX}say <text>`")
        return
    if any(word in text for word in blockedwords):
        await message.reply("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
        return
    await ctx.reply(text)



if "__main__" == __name__:
    with open("blockedwords.txt", "r") as f:
        blockedwords = f.read().splitlines()

if __name__ == "__main__":
    TOKEN = os.getenv("FLUXERBOTTOKEN")
    client.run(TOKEN)
