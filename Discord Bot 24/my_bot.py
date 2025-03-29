import discord
from discord.ext import commands
import requests

# Bot Prefix
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Bot Ready Message
@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} is now online!')

# Hello Command
@bot.command()
async def hello(ctx):
    await ctx.send("Hello! I am your bot. How can I help you? 😊")

# Ping Command
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Bot latency is {latency}ms')

# User Info Command
@bot.command()
async def info(ctx):
    user = ctx.author
    await ctx.send(f'👤 User: {user.name}\n🆔 ID: {user.id}')

# Server Info Command
@bot.command()
async def server(ctx):
    server_name = ctx.guild.name
    member_count = ctx.guild.member_count
    await ctx.send(f'🌍 Server Name: {server_name}\n👥 Members: {member_count}')

# Weather Command
@bot.command()
async def weather(ctx, city: str):
    api_key = "79bb702e4c15ac73429956da15eab728"  # API key dalna mat bhoolna!
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url).json()

    if response.get("cod") != 200:
        await ctx.send("❌ City not found! Please check the name.")
        return

    temp = response["main"]["temp"]
    weather_desc = response["weather"][0]["description"]
    await ctx.send(f'🌡 Temperature: {temp}°C\n🌤 Weather: {weather_desc}')

# Clear Messages Command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'🧹 Deleted {amount} messages!', delete_after=3)

# Bot Run (Replace with your actual token)
bot.run("your_secret_token_here")
