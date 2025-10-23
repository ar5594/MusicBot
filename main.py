import discord
from discord.ext import commands
import yt_dlp
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

ytdlp_format_options = {
    'format': 'bestaudio',
    'outtmpl': 'downloads/%(id)s.%(ext)s',
    'quiet': True,
    'no_warnings': True
}

vc_data = {}

@bot.event
async def on_ready():
    print(f"MusicBot is online as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"✅ Joined {channel.name}")
    else:
        await ctx.send("❌ You're not in a voice channel.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel.")
    else:
        await ctx.send("❌ I'm not in a voice channel.")

@bot.command()
async def play(ctx, *, url):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            return await ctx.send("❌ You're not in a voice channel.")

    await ctx.send("⏳ Downloading audio...")

    with yt_dlp.YoutubeDL(ytdlp_format_options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    ctx.voice_client.stop()
    source = discord.FFmpegPCMAudio(filename)
    ctx.voice_client.play(source, after=lambda e: print("Finished playing."))

    await ctx.send(f"▶️ Now playing: **{info['title']}**")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("⏹ Playback stopped.")

with open("token.txt") as f:
    TOKEN = f.read().strip()

bot.run(TOKEN)
