from .databases import handler as database_handler
from discord.ext import commands
import discord

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Administrator")
    async def setunlocks(self, ctx, victim_id, new_unlocks):
        await self.bot.wait_until_ready()

        admin = ctx.message.author
        victim = await self.bot.fetch_user(int(victim_id))

        previous_tally = database_handler.get_value("unlocks", str(victim_id))
        database_handler.push_key("unlocks", str(victim_id), int(new_unlocks))
        new_tally = database_handler.get_value("unlocks", str(victim_id))

        unlocks_set_embed = discord.Embed(
            description = "<@{}>'s unlocks set to ``{}``.".format(victim_id, new_tally),
            color = 8311585
        )

        await ctx.message.channel.send(embed = unlocks_set_embed)
 
        try:
            notif_embed = discord.Embed(
                title = "Surprise!",
                description = "Hi <@{}>, your unlocks have been remotely set to ``{}``.\n\nIf you have any questions regarding this change, please contact an Administrator. Thanks for using The Prochadstinator!".format(victim_id, new_tally),
                color = 8311585
            )

            await victim.send(embed = notif_embed)
        except:
            dms_closed_embed = discord.Embed(
                description = " <@{}>'s unlocks set to ``{}``.\n\nHowever, this user's DMs are closed and I am unable to send them a notification of this change. Please be sure to do so manually.".format(victim_id, new_tally),
                color = 16098851
            )

            unlocks_set_embed.edit(embed = dms_closed_embed)

        log_embed = discord.Embed(
            title = "Unlocks changed:",
            description = "<@{}> has set <@{}>'s unlocks from ``{}`` to ``{}``.".format(admin.id, victim_id, previous_tally, new_tally),
            color = 8311585
        )   

        await database_handler.log_embed(self.bot, log_embed)

    @commands.command()
    @commands.has_role("Administrator")
    async def getunlocks(self, ctx, victim_id):
        current_unlocks = database_handler.get_value("unlocks", str(victim_id))

        unlock_embed = discord.Embed(
            description = "<@{}> currently has ``{}`` unlocks.\n\nIf you would like to change this value, use the command \"``$setunlocks <user id> <unlocks>``\".".format(victim_id, current_unlocks),
            color = 8311585
        )

        await ctx.message.channel.send(embed = unlock_embed)
 
def setup(bot):
    bot.add_cog(Administration(bot))