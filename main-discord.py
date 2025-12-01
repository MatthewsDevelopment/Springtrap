import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from discord import SyncWebhook
from googletrans import Translator
from dotenv import load_dotenv
import os
import json
import requests
import base64
import random
import asyncio
import aiohttp

load_dotenv('.env')
intents = discord.Intents.default()
client = discord.Client(intents=intents)
client = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)
client.remove_command("help")
PTERODACTYL_PANELURL=os.getenv("PTERODACTYL_PANELURL")
PTERODACTYL_APIKEY=os.getenv("PTERODACTYL_APIKEY")
PANEL_SERVERID=os.getenv("PANEL_SERVERID")

class SelectMenu(discord.ui.View):
    options = [
        discord.SelectOption(label="Standard Embed", value="1", description="Create a simple embed"),
        discord.SelectOption(label="Webhook", value="2", description="Create a simple embed and send through webhook")
    ]
    @discord.ui.select(placeholder="Select tool", options=options)
    async def menu_callback(self, interaction: discord.Interaction, select):
        select.disabled=True
        if select.values[0] == "1":
            await interaction.response.send_modal(embed_modal())
        elif select.values[0] == "2":
            await interaction.response.send_modal(webhookembed_modal())

class embed_modal(discord.ui.Modal, title="Embed Builder"):
    titleanswer = discord.ui.TextInput(label="Embed Title", style=discord.TextStyle.short, required=True, max_length=256)
    messageanswer = discord.ui.TextInput(label="Embed Description", style=discord.TextStyle.paragraph, required=True, max_length=4000)
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"{self.titleanswer}", description=f"{self.messageanswer}", color=(16711680))
        await interaction.response.send_message(embed=embed)

class webhookembed_modal(discord.ui.Modal, title="Embed Builder"):
    webhookanswer = discord.ui.TextInput(label="Webhook URL", style=discord.TextStyle.short, required=True, max_length=128)
    titleanswer = discord.ui.TextInput(label="Embed Title", style=discord.TextStyle.short, required=True, max_length=256)
    messageanswer = discord.ui.TextInput(label="Embed Description", style=discord.TextStyle.paragraph, required=True, max_length=4000)
    async def on_submit(self, interaction: discord.Interaction):
        webhook = SyncWebhook.from_url(f"{self.webhookanswer}")
        embed = discord.Embed(title=f"{self.titleanswer}", description=f"{self.messageanswer}", color=(16711680))
        webhook.send(embed=embed)
        await interaction.response.send_message("Sent the embed to the webhook", ephemeral=True)

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
    await client.change_presence(status=discord.Status.online)
    print('Springtrap [Discord] Bot is Ready')
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} Slash Commands successfully Synced")
    except Exception as e:
        print(e)

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Springtrap", description="help - This message\nping - Get the Latency of the Bot\nsysteminfo - Get resource usage of the python server\nsay - Make me say things\nesay - Make and send a simple embed\nwesay - Make and send a simple embed through webhook\nwsay - Make me say things through webhook\ndeletewebhook - Delete a webhook (USE RESPONSIBLY)\nwebhooklist - View the list of webhooks in the server\ntranslate - Translate text to a different language\nencoder = Encode/Decode text", color=(7864480))
    embed.add_field(name="Decimal Colors", value="When creating embeds, we use decimal colors. Here is a tool to get decimal colors: https://www.mathsisfun.com/hexadecimal-decimal-colors.html", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'PONG!\nLatency: {round(client.latency * 1000)}ms')

@client.command()
async def systeminfo(ctx):
    stats = get_server_stats()
    if stats:
        cpu = stats['attributes']['resources']['cpu_absolute']
        memory = round(stats['attributes']['resources']['memory_bytes'] / (1024 * 1024), 2)
        disk = round(stats['attributes']['resources']['disk_bytes'] / (1024 * 1024), 2)
        embed = discord.Embed(title="Springtrap System Info", description=f"CPU Usage: {cpu}%\nRAM Usage: {memory}MB\nDisk Usage: {disk}MB", color=(7864480))
        await ctx.send(embed=embed)
        return
    else:
        embed = discord.Embed(title="Springtrap System Info", description="Something went wrong", color=(7864480))
        await ctx.send(embed=embed)
        return None

@client.command()
async def say(ctx, *, message: commands.clean_content):
    if any(word in message for word in blockedwords):
        await ctx.send("I WILL NOT SAY ANYTHING THAT CONTAINS WORDS RELATED TO OR ENCOURAGES SCAMS, ILLEGAL ACTIVITIES, AND/OR SELF-HARM")
        return
    await ctx.send(f'{message}')
    await ctx.message.delete()

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What do you want me to say?")
    else:
        raise error

@client.command()
@commands.has_permissions(manage_messages=True)
async def esay(ctx, decimalcolor:int, title:str, message:str, fmessage:str = None):
    if any(word in title for word in blockedwords):
        await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
        return
    if any(word in message for word in blockedwords):
        await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
        return
    embed = discord.Embed(title=f"{title}", description=f"{message}", color=(decimalcolor))
    if fmessage:
        embed.set_footer(text=f"{fmessage}")
        if any(word in fmessage for word in blockedwords):
            await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
            return
    await ctx.send(embed=embed)
    await ctx.message.delete()
    return

@esay.error
async def esay_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_MESSAGES** permission to use this command.", color=(16711680))
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):  
        embed = discord.Embed(title="ARGUMENTS REQUIRED", description="esay <decimalcolor> <title> <message> [footer message] (Put each argument in quotes)", color=(16711680))
        await ctx.send(embed=embed)
    else:
        raise error

@client.command()
@commands.has_permissions(manage_webhooks=True)
@commands.cooldown(1, 15, commands.BucketType.user)
async def wesay(ctx, webhookurl:str,  decimalcolor:int, title:str, message:str, fmessage:str = None):
    if 'https://discord.com/api/webhooks/' in webhookurl:
        webhook = SyncWebhook.from_url(f"{webhookurl}")
        if any(word in title for word in blockedwords):
            await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
            return
        if any(word in message for word in blockedwords):
            await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
            return
        embed = discord.Embed(title=f"{title}", description=f"{message}", color=(decimalcolor))
        if fmessage:
            embed.set_footer(text=f"{fmessage}")
            if any(word in message for word in blockedwords):
                await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
                return
        webhook.send(embed=embed)
        await ctx.send("Sent the embed to the webhook")
        await ctx.message.delete()
        return
    else:
        await ctx.send("You did not provide a valid webhook url\n\nwesay <webhookurl> <title> <message> [footer message] (Put each argument in quotes)")

@wesay.error
async def wesay_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await ctx.send(embed=embed)
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa there. This command has a 15 second cooldown. Try again later.")
    if isinstance(error, commands.MissingRequiredArgument):  
        embed = discord.Embed(title="ARGUMENTS REQUIRED", description="wesay <webhookurl> <decimalcolor> <title> <message> [footer message] (Put each argument in quotes)", color=(16711680))
        await ctx.send(embed=embed)
    else:
        raise error

@client.command()
@commands.has_permissions(manage_webhooks=True)
@commands.cooldown(1, 15, commands.BucketType.user)
async def wsay(ctx, webhookurl:str, message:str):
    if 'https://discord.com/api/webhooks/' in webhookurl:
        webhook = SyncWebhook.from_url(f"{webhookurl}")
        if any(word in message for word in blockedwords):
            await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
            return
        webhook.send(f"{message}")
        await ctx.send("Sent the message to the webhook")
        await ctx.message.delete()
        return
    else:
        await ctx.send("You did not provide a valid webhook url\n\nwsay <webhookurl> <message> (Put each argument in quotes)")

@wsay.error
async def wsay_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await ctx.send(embed=embed)
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa there. This command has a 15 second cooldown. Try again later.")
    if isinstance(error, commands.MissingRequiredArgument):  
        embed = discord.Embed(title="ARGUMENTS REQUIRED", description="wsay <webhookurl> <message>", color=(16711680))
        await ctx.send(embed=embed)
    else:
        raise error

@client.command()
@commands.has_permissions(manage_messages=True)
async def editembed(ctx, msgid:int, decimalcolor:int, title:str, message:str, fmessage:str = None):
    msg = await ctx.fetch_message(msgid)
    if msg.guild.id == ctx.guild.id:
        if any(word in title for word in blockedwords):
            await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
            return
        if any(word in message for word in blockedwords):
            await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
            return
        embed = discord.Embed(title=f"{title}", description=f"{message}", color=(decimalcolor))
        if fmessage:
            embed.set_footer(text=f"{fmessage}")
            if any(word in message for word in blockedwords):
                await ctx.send("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm")
                return
        await msg.edit(embed=embed)
        await ctx.send("Successfully edited the embed")
        return
    else:
        await ctx.send("Please use a message ID of the message that I sent in this server")
        return

@editembed.error
async def editembed_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_MESSAGES** permission to use this command.", color=(16711680))
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):  
        embed = discord.Embed(title="ARGUMENTS REQUIRED", description="editembed <messageid> <decimalcolor> <title> <message> [footer message] (Put each argument in quotes)", color=(16711680))
        await ctx.send(embed=embed)
    else:
        raise error

@client.command()
@commands.has_permissions(manage_webhooks=True)
async def deletewebhook(ctx, webhookurl):
    if 'https://discord.com/api/webhooks/' in webhookurl:
        response = requests.delete(webhookurl)

        if response.status_code == 204:
            await ctx.send('Webhook deleted successfully.')
        else:
            await ctx.send(f'Failed to delete webhook. Status code: {response.status_code}')
        return
    else:
        await ctx.send("You did not provide a valid webhook url\n\ndeletewebhook <webhookurl>")

@deletewebhook.error
async def deletewebhook_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):  
        embed = discord.Embed(title="ARGUMENTS REQUIRED", description="deletewebhook <webhookurl>", color=(16711680))
        await ctx.send(embed=embed)
    else:
        raise error

@client.command()
@commands.has_permissions(manage_webhooks=True)
@commands.bot_has_permissions(manage_webhooks=True)
async def webhooklist(ctx):
    content = "\n".join([f"{w.name} - {w.url}" for w in await ctx.guild.webhooks()])
    embed = discord.Embed(title=f"Webhook urls for: {ctx.guild.name}", description=content, color=(7864480))
    await ctx.send(embed=embed)

@webhooklist.error
async def webhooklist_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await ctx.send(embed=embed)
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="I need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await ctx.send(embed=embed)
    else:
        raise error

@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def translate(ctx, lang, *, textmessage):
    translator = Translator()
    translation = translator.translate(textmessage, dest=lang)
    embed = discord.Embed(title="Translator", color=(7864480))
    embed.add_field(name="Original message", value=f'{textmessage}')
    embed.add_field(name=f"Translated to: {lang}", value=f'{translation.text}')
    embed.set_footer(text="Google Translate was used to translate the text")
    await ctx.send(embed=embed)

@translate.error
async def translate_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Whoa there. This command has a 15 second cooldown. Try again later.")
    if isinstance(error, commands.MissingRequiredArgument):  
        embed = discord.Embed(title="ARGUMENTS REQUIRED", description="translate <lang:totranslateto> <message>", color=(16711680))
        await ctx.send(embed=embed)
    else:
        raise error

@client.command()
async def encoder(ctx, option="", *, textmessage:str):
    if option == "base64encode":
        encoded_message = base64.b64encode(textmessage.encode())
        embed = discord.Embed(title="Base64 Encoder", color=(7864480))
        embed.add_field(name="Original message", value=f'{textmessage}')
        embed.add_field(name="Encoded message", value=f'{encoded_message.decode()}')
        await ctx.send(embed=embed)
    if option == "base64decode":
        encoded_message = f'{textmessage}'
        decoded_message = base64.b64decode(encoded_message)
        embed = discord.Embed(title="Base64 Encoder", color=(7864480))
        embed.add_field(name="Original message", value=f'{textmessage}')
        embed.add_field(name="Decoded message", value=f'{decoded_message.decode()}')
        await ctx.send(embed=embed)

@encoder.error
async def encoder_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):  
        embed = discord.Embed(title="ARGUMENTS REQUIRED", description="encoder <option> <message>", color=(16711680))
        embed.add_field(name="Available options", value="base64encode\nbase64decode")
        await ctx.send(embed=embed)
    else:
        raise error





@client.tree.command(name="ping", description="Get the Latency of the Bot")
async def _ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'PONG!\nLatency: {round(client.latency * 1000)}ms')

@client.tree.command(name="systeminfo", description="Get resource usage of the python server")
async def systeminfo(interaction: discord.Interaction):
    stats = get_server_stats()
    if stats:
        cpu = stats['attributes']['resources']['cpu_absolute']
        memory = round(stats['attributes']['resources']['memory_bytes'] / (1024 * 1024), 2)
        disk = round(stats['attributes']['resources']['disk_bytes'] / (1024 * 1024), 2)
        embed = discord.Embed(title="Springtrap System Info", description=f"CPU Usage: {cpu}%\nRAM Usage: {memory}MB\nDisk Usage: {disk}MB", color=(7864480))
        await interaction.response.send_message(embed=embed)
        return
    else:
        embed = discord.Embed(title="Springtrap System Info", description="Something went wrong", color=(7864480))
        await interaction.response.send_message(embed=embed)
        return None

@client.tree.command(name="esay", description="Make and send a simple embed")
@app_commands.checks.has_permissions(manage_messages=True)
async def _esay(interaction: discord.Interaction, channel:discord.TextChannel, decimalcolor:int, title:str, message:str, fmessage:str = None):
    if any(word in title for word in blockedwords):
        await interaction.response.send_message("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm", ephemeral=True)
        return
    if any(word in message for word in blockedwords):
        await interaction.response.send_message("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm", ephemeral=True)
        return
    embed = discord.Embed(title=f"{title}", description=f"{message}", color=(decimalcolor))
    if fmessage:
        embed.set_footer(text=f"{fmessage}")
        if any(word in fmessage for word in blockedwords):
            await interaction.response.send_message("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm", ephemeral=True)
            return
    await channel.send(embed=embed)
    await interaction.response.send_message("Embed sent successfully to the channel provided", ephemeral=True)
    return

@_esay.error
async def _esay_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_MESSAGES** permission to use this command.", color=(16711680))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        raise error

@client.tree.command(name="wesay", description="Make and send a simple embed through webhook")
@app_commands.checks.has_permissions(manage_webhooks=True)
async def _wesay(interaction: discord.Interaction, webhookurl:str, decimalcolor:int, title:str, message:str, fmessage:str = None):
    if 'https://discord.com/api/webhooks/' in webhookurl:
        webhook = SyncWebhook.from_url(f"{webhookurl}")
        if any(word in title for word in blockedwords):
            await interaction.response.send_message("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm", ephemeral=True)
            return
        if any(word in message for word in blockedwords):
            await interaction.response.send_message("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm", ephemeral=True)
            return
        embed = discord.Embed(title=f"{title}", description=f"{message}", color=(decimalcolor))
        if fmessage:
            embed.set_footer(text=f"{fmessage}")
            if any(word in message for word in blockedwords):
                await interaction.response.send_message("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm", ephemeral=True)
                return
        webhook.send(embed=embed)
        await interaction.response.send_message("Sent the embed to the webhook", ephemeral=True)
        return
    else:
        await interaction.response.send_message("You did not provide a valid webhook url\n\n/wesay <webhookurl> <title> <message> [footer message]")

@_wesay.error
async def _wesay_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        raise error

@client.tree.command(name="wsay", description="Make me say things through webhook")
@app_commands.checks.has_permissions(manage_webhooks=True)
async def _wsay(interaction: discord.Interaction, webhookurl:str, message:str):
    if 'https://discord.com/api/webhooks/' in webhookurl:
        webhook = SyncWebhook.from_url(f"{webhookurl}")
        if any(word in message for word in blockedwords):
            await interaction.response.send_message("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm", ephemeral=True)
            return
        webhook.send(f"{message}")
        await interaction.response.send_message("Sent the message to the webhook", ephemeral=True)
        return
    else:
        await interaction.response.send_message("You did not provide a valid webhook url\n\n/wsay <webhookurl> <message> (Put each argument in quotes)", ephemeral=True)

@_wsay.error
async def _wsay_error(ctx, error):
    if isinstance(error, app_commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        raise error

@client.tree.command(name="editembed", description="Edit an embed sent by the bot")
@app_commands.checks.has_permissions(manage_messages=True)
async def _editembed(interaction: discord.Interaction, msgid:str, decimalcolor:int, title:str, message:str, fmessage:str = None):
    msg = await interaction.channel.fetch_message(msgid)
    if msg.guild.id == interaction.guild.id:
        if any(word in title for word in blockedwords):
            await interaction.response.send_message("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm", ephemeral=True)
            return
        if any(word in message for word in blockedwords):
            await interaction.response.send_message("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm", ephemeral=True)
            return
        embed = discord.Embed(title=f"{title}", description=f"{message}", color=(decimalcolor))
        if fmessage:
            embed.set_footer(text=f"{fmessage}")
            if any(word in message for word in blockedwords):
                await interaction.response.send_message("I will not say anything that encourages or promotes scams, illegal activites, and/or self-harm", ephemeral=True)
                return
        await msg.edit(embed=embed)
        await interaction.response.send_message("Successfully edited the embed", ephemeral=True)
        return
    else:
        await interaction.response.send_message("Please use a message ID of the message that I sent in this server", ephemeral=True)
        return

@_editembed.error
async def _editembed_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_MESSAGES** permission to use this command.", color=(16711680))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        raise error

@client.tree.command(name="deletewebhook", description="Delete a webhook (USE RESPONSIBLY)")
@app_commands.checks.has_permissions(manage_webhooks=True)
async def _deletewebhook(interaction: discord.Interaction, webhookurl:str):
    if 'https://discord.com/api/webhooks/' in webhookurl:
        response = requests.delete(webhookurl)

        if response.status_code == 204:
            await interaction.response.send_message('Webhook deleted successfully.', ephemeral=True)
        else:
            await interaction.response.send_message(f'Failed to delete webhook. Status code: {response.status_code}', ephemeral=True)
        return
    else:
        await interaction.response.send_message("You did not provide a valid webhook url\n\n/deletewebhook <webhookurl>", ephemeral=True)

@_deletewebhook.error
async def _deletewebhook_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await interaction.response.send_message(embed=embed)
    else:
        raise error

@client.tree.command(name="webhooklist", description="Get a list of webhooks that is in your server")
@app_commands.checks.has_permissions(manage_webhooks=True)
@app_commands.checks.bot_has_permissions(manage_webhooks=True)
async def _webhooklist(interaction: discord.Interaction):
    content = "\n".join([f"{w.name} - {w.url}" for w in await interaction.guild.webhooks()])
    embed = discord.Embed(title=f"Webhook urls for: {interaction.guild.name}", description=content, color=(7864480))
    await interaction.response.send_message(embed=embed, ephemeral=True)

@_webhooklist.error
async def _webhooklist_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    if isinstance(error, app_commands.BotMissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="I need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        raise error

@client.tree.command(name="translate", description="Translate text to a different language")
async def _translate(interaction: discord.Interaction, lang:str, textmessage:str):
    translator = Translator()
    translation = translator.translate(textmessage, dest=lang)
    embed = discord.Embed(title="Translator", color=(7864480))
    embed.add_field(name="Original message", value=f'{textmessage}')
    embed.add_field(name=f"Translated to: {lang}", value=f'{translation.text}')
    embed.set_footer(text="Google Translate was used to translate the text")
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="encoder", description='Encode/Decode base64 text')
@app_commands.choices(option=[
    discord.app_commands.Choice(name="Base64-Encode", value=1),
    discord.app_commands.Choice(name="Base64-Decode", value=2),
])
async def _encoder(interaction: discord.Interaction, option: discord.app_commands.Choice[int], textmessage:str):
    if option.name == "Base64-Encode":
        encoded_message = base64.b64encode(textmessage.encode())
        embed = discord.Embed(title="Base64 Encoder", color=(7864480))
        embed.add_field(name="Original message", value=f'{textmessage}')
        embed.add_field(name="Encoded message", value=f'{encoded_message.decode()}')
        await interaction.response.send_message(embed=embed)
    if option.name == "Base64-Decode":
        encoded_message = f'{textmessage}'
        decoded_message = base64.b64decode(encoded_message)
        embed = discord.Embed(title="Base64 Encoder", color=(7864480))
        embed.add_field(name="Original message", value=f'{textmessage}')
        embed.add_field(name="Decoded message", value=f'{decoded_message.decode()}')
        await interaction.response.send_message(embed=embed)





@client.tree.command(name="embedtools", description='See a Discord dropdown of embed building tools with modal usage.')
@app_commands.checks.has_permissions(manage_webhooks=True)
async def _embedtools(interaction: discord.Interaction):
    await interaction.response.send_message("Select what you want to do", view=SelectMenu(), ephemeral=True)

@_embedtools.error
async def _embedtools_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to have **MANAGE_WEBHOOKS** permission to use this command.", color=(16711680))
        await interaction.response.send_message(embed=embed)
    else:
        raise error

if "__main__" == __name__:
    with open("blockedwords.txt", "r") as f:
        blockedwords = f.read().splitlines()

matthewdevstaff = [815684414045552680, 724723809218723970]

@client.command()
async def status(ctx, value="", *, statustext):
    if ctx.author.id in matthewdevstaff:
        if value == "watch":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{statustext}"))
            await ctx.send("My Status is Successfully Changed")
            return
        if value == "listen":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{statustext}"))
            await ctx.send("My Status is Successfully Changed")
            return
        if value == "play":
            await client.change_presence(activity=discord.Game(name=f"{statustext}"))
            await ctx.send("My Status is Successfully Changed")
            return
        if value == "compete":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f"{statustext}"))
            await ctx.send("My Status is Successfully Changed")
            return
        if value == "custom":
            await client.change_presence(activity=discord.CustomActivity(name=f"{statustext}"))
            await ctx.send("My Status is Successfully Changed")
            return
    else:
        await ctx.send("Only Matthews Development Staff members can use this command")
        return

@client.tree.command(name="status", description="Change the status of the bot (Bot staff only)")
@app_commands.choices(status=[
    discord.app_commands.Choice(name="Watching", value=1),
    discord.app_commands.Choice(name="Listening", value=2),
    discord.app_commands.Choice(name="Playing", value=3),
    discord.app_commands.Choice(name="Compete", value=4),
    discord.app_commands.Choice(name="Custom", value=5),
])
async def _status(interaction: discord.Interaction, status: discord.app_commands.Choice[int], statustext:str):
    if interaction.user.id in matthewdevstaff:
        if status.name == "Watching":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{statustext}"))
            await interaction.response.send_message("My Status is Successfully Changed", ephemeral=True)
            return
        if status.name == "Listening":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{statustext}"))
            await interaction.response.send_message("My Status is Successfully Changed", ephemeral=True)
            return
        if status.name == "Playing":
            await client.change_presence(activity=discord.Game(name=f"{statustext}"))
            await interaction.response.send_message("My Status is Successfully Changed", ephemeral=True)
            return
        if status.name == "Compete":
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=f"{statustext}"))
            await interaction.response.send_message("My Status is Successfully Changed", ephemeral=True)
            return
        if status.name == "Custom":
            await client.change_presence(activity=discord.CustomActivity(name=f"{statustext}"))
            await interaction.response.send_message("My Status is Successfully Changed", ephemeral=True)
            return
    else:
        await interaction.response.send_message("Only Matthews Development Staff members can use this command", ephemeral=True)
        return





TOKEN = os.getenv("DISCORDBOTTOKEN")
client.run(TOKEN)
