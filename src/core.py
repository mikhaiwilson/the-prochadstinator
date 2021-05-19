from dotenv import load_dotenv
from discord.ext import commands
import os

load_dotenv(".env")

bot = commands.Bot(command_prefix = "$")

bot.load_extension("commands.purchasing")
bot.load_extension("commands.admin")
bot.load_extension("commands.unlocking")

bot.run("null")