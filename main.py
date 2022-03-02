import discord
from discord.ext import commands
import music

cogs = [music]
print(len(cogs))

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run("NjY2NDIxODA2NDI4ODQ4MTMx.Xhz7rA.FJtzolEsYmVXDEOF_kebYgFXW9E")
