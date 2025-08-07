import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import random

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

secret_role = "Gamer"

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is ready as {bot.user}")


@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - dont use that word!")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is now assigned to {secret_role}")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} removed")
    else:
        await ctx.send("Role doesn't exist")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New Poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have permission to do that!")

@bot.tree.command(name="pingfun", description="Check if the bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong from funBot!")

@bot.tree.command(name="winpick", description="Randomly pick red or black")
async def pick(interaction: discord.Interaction):
    color = random.choice(["🔴 Red", "⚫ Black"])
    await interaction.response.send_message(f"🎯 Fkkk u got **{color}**!")


@bot.tree.command(name="blackjack", description="Get advice on whether to hit or stand")
@discord.app_commands.describe(
    dealer="Dealer's visible card (2–11, where 11 = Ace)",
    player="Your total hand value"
)
async def blackjack(interaction: discord.Interaction, dealer: int, player: int):
    # Basic strategy logic
    advice = ""

    if player >= 17:
        advice = "✅ Stand — you're high enough!"
    elif player <= 11:
        advice = "🃏 Hit — you can't bust yet!"
    elif 12 <= player <= 16:
        if dealer >= 7:
            advice = "🔥 Hit — dealer might beat you!"
        else:
            advice = "🛑 Stand — let the dealer bust!"
    else:
        advice = "🤔 Hmm... tricky. Play it safe."

    await interaction.response.send_message(
        f"Dealer has {dealer}, you have {player} → **{advice}**"
    )


bot.run(token, log_handler=handler, log_level=logging.DEBUG)