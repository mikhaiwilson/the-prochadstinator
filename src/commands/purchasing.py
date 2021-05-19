from .databases import handler as database_handler
from discord.ext import commands
import discord
import os

class Purchasing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def buy(self, ctx):
        author = ctx.message.author

        buy_embed = discord.Embed(
            title = "Need more keys?",
            description = "• If you have never used The Prochadstinator before, you are entitled to 1 free usage key. You can redeem this by sending the command \"``$redeem 14FREE``\" either here in the bot's DMs or within the server.\n• Before buying, be sure that you read and understand our [Terms of Service](https://docs.google.com/document/d/e/2PACX-1vS_YlrtOZY5JaOv893Iwp1U9vmMTgNHg42Tlo3PGpEkYI1aN9IFayEKVH3XTuFohffnaJ7hCxwfGtEG/pub).\n• All purchases are ***FINAL***, but other payment methods may be occasionally accepted (keep an eye out for these in <#778697936888528896>).\n• After purchasing, you should receive an email with an order ID. Use this to redeem your usage ticket.\n• If your need help or are having any other issues with purchasing, forward an inquiry into our [contact form](https://bit.ly/contactprochadstinator).\n\n[Click me to purchase.](https://shoppy.gg/product/1mKDTJb) Thanks for helping me keep this project alive! <3",
            color = 8311585
        )
    
        try:
            await author.send(embed = buy_embed)
        except:
            await database_handler.dms_closed(ctx, author)

    @commands.command()
    async def unlocks(self, ctx):
        author = ctx.message.author
        unlocks = database_handler.get_value("unlocks", author.id)

        if unlocks == None:
            unlocks = 0

        unlocks_embed = discord.Embed(
            title = "Here you go, buddy.",
            description = "<@{}>, you have ``{}`` unlock(s) remaining.\n\nThanks for supporting The Prochadstinator. Remember, if you need more unlocks, use the command \"``$buy``\" in for more information. If you have never used The Prochadstinator before, use the command \"``$redeem 14FREE``\" to redeem your free unlock. You would be buying my breakfast (<3), getting your homework done in 15 minutes, and ultimately participating in keeping this project alive. It's a win-win-win!".format(author.id, unlocks),
            color = 8311585
        )

        await ctx.message.channel.send(embed = unlocks_embed) 

    @commands.command()
    async def getrefer(self, ctx):
        author = ctx.message.author

        if not database_handler.get_value("referrals", author.id):
            referral_code = database_handler.generate_referral(author.id)

            referral_info = {
                "referral": {
                    "code": referral_code,
                    "uses": 0
                },
                "redeemed": None
            }

            database_handler.push_key("referrals", author.id, referral_info)

        referral_info = database_handler.get_value("referrals", author.id)
        
        referral_embed = discord.Embed(
            description = "Thanks for participating in our referral program, <@{}>. The Prochadstinator's referral program rewards you with 5 unlocks for every 10 people that redeem your referral code. Your referral code wil be sent below this message.".format(author.id),
            color = 8311585
        )

        try:
            await author.send(embed = referral_embed)
            await author.send("``" + referral_info["referral"]["code"] + "``")
        except:
            await database_handler.dms_closed(ctx, author)

    @commands.command()
    async def redeemrefer(self, ctx, key):
        async def invalid_refer():
            invalid_refer_embed = discord.Embed(
                title = "We've encountered a problem.",
                description = "Yikes <@{}>, your referral code (\"``{}``\") is invalid. Please try again with another legitmate referral code. Make sure your referral code is copied with no spaces.\n\nExample:\n``$redeemrefer 1a2b3c45-6de7-8f9g-hijk-123456789m``".format(author.id, key),
                color = 15158332
            )

            await ctx.message.channel.send(embed = invalid_refer_embed)

        author = ctx.message.author

        print(key[:18])

        if int(key[:18]) == author.id:
            retard_alert = discord.Embed(
                title = "Nice try.",
                description = "Sorry buddy, but you aren't allowed to redeem your own referral code.",
                color = 15158332
            )

            await author.send(embed = retard_alert)

            return

        referrer_referral_info = database_handler.get_value("referrals", key[:18])
        author_referral_info = database_handler.get_value("referrals", author.id)

        if not author_referral_info:
            referral_code = database_handler.generate_referral(author.id)

            referral_info = {
                "referral": {
                    "code": referral_code,
                    "uses": 0
                },
                "redeemed": None
            }

            author_referral_info = referral_info

            database_handler.push_key("referrals", author.id, referral_info)     

        if not referrer_referral_info:
            await invalid_refer()    

            return

        if author_referral_info["redeemed"] == None:
            if referrer_referral_info["referral"]["code"] == key:
                referrer = await self.bot.fetch_user(int(key[:18]))
                referrer_referral_info["referral"]["uses"] = referrer_referral_info["referral"]["uses"] + 1
                author_referral_info["redeemed"] = key

                database_handler.push_key("referrals", referrer.id, referrer_referral_info)
                database_handler.push_key("referrals", author.id, author_referral_info)
                
                redeemed_embed = discord.Embed(
                    description = "Your referral code has been redeemed.",
                    color = 8311585
                )     

                await author.send(embed = redeemed_embed)    

                if ((10 - database_handler.get_value("referrals", referrer.id)["referral"]["uses"]) != 0):
                    referrer_notif = discord.Embed(
                        description = "Hey, <@{}>. Your referral code was just redeemed by <@{}>.\n\nYou currently need ``{}`` more redeem(s) before your 5 unlocks are gifted to you. Good luck!".format(referrer.id, author.id, database_handler.get_value("referrals", referrer.id)["referral"]["uses"]),
                        color = 8311585
                    )

                    await referrer.send(embed = referrer_notif) 

                if referrer_referral_info["referral"]["uses"] == 10:
                    referrer_referral_info["referral"]["uses"] = 0
                    current_referrer_unlocks = database_handler.get_value("unlocks", referrer.id)
                    new_referrer_unlocks = current_referrer_unlocks + 5

                    database_handler.push_key("unlocks", referrer.id, new_referrer_unlocks)
                    database_handler.push_key("referrals", referrer.id, referrer_referral_info)
                    database_handler.push_key("referrals", author.id, author_referral_info)
                
                    reward_embed = discord.Embed(
                        title = "Thanks for supporting The Prochadstinator!",
                        description = "Thank you, <@{}>.\n\n**You have been gifted 5 unlocks** for inviting 10 people into our Discord Server through our referral program. Keep inviting your friends, and tell them to invite theirs while they're at it!".format(referrer.id),
                        color = 8311585
                    )

                    await referrer.send(embed = reward_embed) 
            else:
                await invalid_refer() 
        else:
            refer_already_redeemed = discord.Embed(
                description = "You've already redeemed a referral code. This command is no longer available to you.",
                color = 15158332
            )

            await ctx.message.channel.send(embed = refer_already_redeemed)
       
    @commands.command()
    async def redeem(self, ctx, key):
        author = ctx.message.author  

        if not database_handler.get_value("unlocks", author.id) and key == "14FREE":
            database_handler.push_key("unlocks", author.id, 1)

            reward_embed = discord.Embed(
                title = "Your prayers have been answered.",
                description = "Congratulations <@{}>, **you have been gifted 1 free unlock.** If you need more unlocks, use the command \"``$buy``\" for more information. Legacy members will already have a predetermined number of unlocks depending on the subscription type they owned.\n\nRemember, if you want to use The Prochadstinator, **your DMs *must* be open.** I will no longer be resetting cooldowns because you have your DMs closed - it seriously only takes 5 seconds to check.".format(author.id),
                color = 8311585
            )

            await ctx.message.channel.send(embed = reward_embed)

            log_embed = discord.Embed(
                title = "Free key redeemed:",
                description = "<@{}> has redeemed their free key (\"``14FREE``\").".format(author.id), 
                color = 8311585
            )

            await database_handler.log_embed(self.bot, log_embed)

            return
         
        if not database_handler.get_value("keys", key): #Checks if order ID already exists in used-key database
            if key == "14FREE":
                free_key_used = discord.Embed(
                    title = "Wazowski, snap out of it!",
                    description = "~~Wazowski~~ <@{}>, you've already redeemed your free key. If you need more unlocks, use the command \"``$buy``\" for more information.".format(author.id),
                    color = 15158332
                )

                await ctx.message.channel.send(embed = free_key_used)
            elif database_handler.is_key_valid(key): #Checks if order ID is actually valid
                order_info = database_handler.is_key_valid(key)

                if order_info["paid_at"] == None:
                    nice_try_embed = discord.Embed(
                        title = "Oooh, he stealin...",
                        description = "Nice try, <@{}>, but you must actually pay for the key before trying to redeem it. Nice try though. Really.".format(author.id),
                        color = 15158332
                    )

                    await ctx.message.channel.send(embed = nice_try_embed)                               
                else:
                    previus_tally = int(database_handler.get_value("unlocks", author.id))
                    order_quantity = int(order_info["quantity"])
                    new_tally = previus_tally + order_quantity
                    
                    database_handler.push_key("unlocks", author.id, new_tally)
                    database_handler.push_key("keys", key, author.id)

                    key_redeemed_embed = discord.Embed(
                        title = "Seriously, thanks for supporting.",
                        description = "Hi <@{}>, your key (``{}`` unlock(s)) is valid and has been redeemed. and you now have ``{}`` unlocks. Remember, if you need more unlocks, use the command \"``$buy``\" for more information.".format(author.id, order_quantity, new_tally),
                        color = 8311585
                    )

                    await ctx.message.channel.send(embed = key_redeemed_embed)        
            else:
                invalid_key_embed = discord.Embed(
                    title = "We've encountered a problem.",
                    description = "Yikes <@{}>, your order ID (``\"{}\"``) is invalid. Please try again with another legitmate key. Make sure your order ID is copied with no spaces.\n\nExample:\n``$redeem 1a2b3c45-6de7-8f9g-hijk-123456789m``".format(author.id, key),
                    color = 15158332
                )

                await ctx.message.channel.send(embed = invalid_key_embed)
        else:
            redeemed_embed = discord.Embed(
                title = "Whoa, chill out!",
                description = "<@{}>, this order ID (``\"{}\"``) has already been claimed and redeemed. Please try again with another legitimate and unused key.".format(author.id, key),
                color = 15158332
            ) 

            await ctx.message.channel.send(embed = redeemed_embed)

def setup(bot):
    bot.add_cog(Purchasing(bot))