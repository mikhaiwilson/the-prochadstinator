import json
import os
import requests
import uuid
import discord

async def log_embed(bot, embed_object):
    channel = await bot.fetch_channel(791878275621191690)

    await channel.send(embed = embed_object)

def generate_referral(id):
    return str(id) + str(uuid.uuid4())

async def dms_closed(ctx, author):
    dms_closed_embed = discord.Embed(
        title = "This might be a problem...",
        description = "<@{}>, in order for this command to work, your DMs must be open. Please open your DMs and try using this command again.".format(author.id),
        color = 15158332
    )

    await ctx.message.channel.send(embed = dms_closed_embed)    

def is_key_valid(key):
    url = "https://shoppy.gg/api/v1/orders/{}".format(str(key))
    headers = {
        "User-Agent": "The Prochadstinator/V2.0",
        "Authorization": "null"
    }
    response = requests.get(url, headers = headers)

    #print("GET response:", response)

    json_response = response.json()
    
    if response:
        return json_response
    else:
        return None

def get_value(database, key):
    # Returns the value of key if it exists or False if it doesn't
    with open("C:/Users/GENESIS/Documents/the_prochadstinator/source/commands/databases/{}.json".format(database), "r") as json_database:
        database_dict = json.load(json_database)
        json_database.close()

    if str(key) in database_dict:
        return database_dict[str(key)]
    else:
        return None

def push_key(database, key, value):
    # Pushes key into database with value as value

    with open("C:/Users/GENESIS/Documents/the_prochadstinator/source/commands/databases/{}.json".format(database), "r") as json_database:
        database_dict = json.load(json_database)
        json_database.close()

    database_dict[str(key)] = value

    with open("C:/Users/GENESIS/Documents/the_prochadstinator/source/commands/databases/{}.json".format(database), "w") as json_database:
        json.dump(database_dict, json_database) 
        json_database.close()