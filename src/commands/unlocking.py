from discord.ext import commands
from .databases import handler as database_handler
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import random
import asyncio
import discord

options = Options()
options.headless = False
driver = webdriver.Firefox(options = options, executable_path = "C:/Users/GENESIS/Documents/the_prochadstinator/source/geckodriver.exe")

def get_quote():
    quotes = [
        "Whatever the mind of man can conceive and believe, it can achieve. – Napoleon Hill",
        "Strive not to be a success, but rather to be of value. – Albert Einstein",
        "Two roads diverged in a wood, and I—I took the one less traveled by, And that has made all the difference. – Robert Frost",
        "I attribute my success to this: I never gave or took any excuse. – Florence Nightingale"
        "The most difficult thing is the decision to act, the rest is merely tenacity. – Amelia Earhart",
        "The most common way people give up their power is by thinking they don’t have any. – Alice Walker"
        "You can never cross the ocean until you have the courage to lose sight of the shore. – Christopher Columbus",
        "Few things can help an individual more than to place responsibility on him, and to let him know that you trust him. – Booker T. Washington"
        "When one door of happiness closes, another opens, but often we look so long at the closed door that we do not see the one that has been opened for us. – Helen Keller",
        "First, have a definite, clear practical ideal; a goal, an objective. Second, have the necessary means to achieve your ends; wisdom, money, materials, and methods. Third, adjust all your means to that end. – Aristotle",
        "Trying is the first step toward failure. - Homer Simpson",
        "It’s only when you look at an ant through a magnifying glass on a sunny day that you realize how often they burst into flames. - Harry Hill",
        "Eagles may soar, but weasels don't get sucked into jet engines. - John Benfield",
        "I am free of all prejudice. I hate everyone equally. - W.C. Fields",
        "Light travels faster than sound. This is why some people appear bright until you hear them speak. - Alan Dundes",
        "Do not take life too seriously. You will never get out of it alive. - Elbert Hubbard",
        "Everything happens for a reason. Sometimes the reason is you're stupid and make bad decisions. - Marion G. Harmon",
        "He who laughs last didn’t get the joke. - Charles de Gaulle", 
        "The worst part of success is trying to find someone who is happy for you. - Bette Midler",
        "The trouble with having an open mind, of course, is that people will insist on coming along and trying to put things in it. - Terry Pratchett"
    ]
    random_quote = random.choice(quotes)

    return random_quote

class Chegg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.job_queue = {}
        self.current_job = None
        self.cooldowns = {}

    async def get_cooldown(self, user_id):
        if user_id in self.cooldowns:
            return self.cooldowns[user_id]
        else:
            return 0

    async def do_job(self, job_id):
        if (not self.current_job == None) or (len(self.job_queue) == 0):  #If there is currently being a job done in the chegg queue OR there is nothing in the queue, ignore the do_job function
            return

        self.current_job = list(self.job_queue.keys())[0] # Sets the current job to the first job in the request queue
        job_info = self.job_queue[self.current_job]

        await asyncio.sleep(random.randint(5, 10)) 

        """
            to do: log in automatically if browser is headless and being hosted non-remotely
        """


        
        #actually have unlocking shit here

        driver.get(job_info["requested_link"])

        soup = BeautifulSoup(driver.page_source, "html.parser")
        answer = soup.find(attrs = {"class": "answer-given-body ugc-base"})

        await asyncio.sleep(random.randint(3, 10))

        if answer == None:
            locked_embed = discord.Embed(
                description = "Sorry <@{}>, we could not find an answer for your question. **Your requested link may not have an answer,** or we may just be having issues with pushing the horses on our end. If this error shows up for multiple questions, contact an administrator.".format(job_id),
                color = 15158332
            )

            locked_embed.set_author(name = "Well, this is awkward.", url = "https://www.youtube.com/watch?v=e-yfYhSR7YE", icon_url = job_info["author"].avatar_url)

            await job_info["current_embed"].edit(embed = locked_embed)          
        elif hasattr(answer, "get_text") == False:
            element = driver.find_element_by_class_name("main")
            total_height = (element.size["height"] + 1000)
            driver.set_window_size(1920, total_height)
            
            await asyncio.sleep(random.randint(5, 10))
            element.screenshot("C:/Users/GENESIS/Documents/the_prochadstinator/temp/chegg/screenshot.png")     

            success_embed = discord.Embed(
                description = "Hey <@{}>. Your textbook document has been processed and its answer has been sent below. If you're on a computer and would like to see an enlarged version of the photo, simply click on it and open the original photo through the button below it. If the picture is just a loading icon, contact an Administratorr with the link you requested. Thank you for supprting The Prochadstinator!".format(job_info["author"].id),
                color = 8311585
            )

            success_embed.set_author(name = "Order up!", icon_url = job_info["author"].avatar_url)
            success_embed.add_field(name = "Requested Question", value = job_info["requested_link"], inline = False)

            await job_info["current_embed"].edit(embed = success_embed)
            await job_info["author"].send(file = discord.File("C:/Users/GENESIS/Documents/the_prochadstinator/temp/screenshot.png"))       
        else:
            answer_text = answer.get_text()
            answer_images = []

            for document_image_link in answer.find_all("img"):
                answer_images.append(document_image_link.get("src"))

            separator = "\n--> "
            separated_images = separator.join(answer_images)
            final_answer_image = ("Copy and paste the link after each arrow to view the image file.\n\n--> " + separated_images)

            if (len(answer_images) == 0):
                final_answer_image = "No images have been detected for this question."

            if (len(answer_text) < 10):
                answer_text = "No text has been detected for this question."

            with open("C:/Users/GENESIS/Documents/the_prochadstinator/temp/chegg/answer_text.txt", "w", encoding = "utf-8") as file:
                file.write(str(answer_text))
                file.close()

            with open("C:/Users/GENESIS/Documents/the_prochadstinator/temp/answer_images.txt", "w", encoding = "utf-8") as file:
                file.write(str(final_answer_image))
                file.close()

            success_embed = discord.Embed(
                title = "Yessssssir!",
                description = "Hey <@{}>. Your documents have been processed and are listed below. If the ``answer_text.txt`` file does not make any sense or is barely readable, it usually means that the answer is just a list of images.".format(job_info["author"].id),
                color = 8311585
            )

            success_embed.add_field(name = "Original question:", value = job_info["requested_link"], inline = False)

            with open("C:/Users/GENESIS/Documents/the_prochadstinator/temp/chegg/answer_text.txt", "rb") as file:
                await job_info["author"].send(file = discord.File(file, "answer_text.txt"))
                file.close()

            with open("C:/Users/GENESIS/Documents/the_prochadstinator/temp/chegg/answer_images.txt", "rb") as file:
                await job_info["author"].send(file = discord.File(file, "answer_images.txt"))     
                file.close()

            await job_info["current_embed"].edit(embed = success_embed)

        log_embed = discord.Embed(
            title = "Chegg job completed:",
            color = 8311585
        )

        log_embed.add_field(name = "Original question", value = job_info["requested_link"], inline = False)

        await database_handler.log_embed(self.bot, log_embed)
        
        self.job_queue.pop(self.current_job) # Removes the current job from the request queue
        updated_queue = list(self.job_queue.keys()) # Grabs an updated list
        self.current_job = None

        if len(updated_queue) > 0:
            await self.do_job(list(self.job_queue.keys())[0]) # Repeats this entire process for the next job in line

        return

    async def is_job_queued(self, job_id):
        if job_id in self.job_queue:
            return True
        else:
            return False

    @commands.command()
    async def chegg(self, ctx, requested_link):
        author = ctx.message.author

        if ctx.message.channel.id == 784110037060288593:
            if not await self.is_job_queued(author.id):
                if requested_link[:22] == "https://www.chegg.com/":
                    if not database_handler.get_value("unlocks", author.id) == 0 and database_handler.get_value("unlocks", author.id):
                        buffer_embed = discord.Embed(
                            title = "Please wait...",
                            url = "https://www.youtube.com/watch?v=e-yfYhSR7YE",
                            description = "Hey <@{}>. Your document has been placed in the request queue. Please allow up to 5 minutes for your documents to be processed. In the mean time, tell your friends about The Prochadstinator!\n\n\"{}\"".format(author.id, get_quote()),
                            color = 16098851
                        )  

                        try:
                            current_embed = await author.send(embed = buffer_embed)
                        except:
                            database_handler.dms_closed(ctx, author)

                            return

                        self.job_queue[author.id] = {
                            "author": author,
                            "ctx": ctx,
                            "requested_link": requested_link,
                            "current_embed": current_embed                    
                        }

                        await self.do_job(author.id)                        

                        database_handler.push_key("unlocks", author.id, (database_handler.get_value("unlocks", author.id) - 1))
                    else:
                        out_embed = discord.Embed(
                            title = "Oh no...",
                            description = "Sorry <@{}>, but you don't have enough unlocks to use this command. If you need more unlocks, use the command \"``$buy``\" for more information and knowledge about your eligibility for a free unlock.".format(author.id),
                            color = 15158332
                        )

                        out_embed.set_author(name = "Whoa there!", icon_url = author.avatar_url)

                        await ctx.message.channel.send(embed = out_embed)
                else:
                    invalid_link_embed = discord.Embed(
                        title = "Uh oh...",
                        description = "<@{}>, \"``{}``\" is not a valid Chegg link. Please try again with a valid link.".format(author.id, requested_link),
                        color = 15158332                        
                    )

                    await ctx.message.channel.send(embed = invalid_link_embed)
            else:
                debounce_embed = discord.Embed(
                    title = "Slow down!",
                    description = "<@{}>, you already have a document being processed in the Chegg request queue. Please wait until this document has been processed before requesting another unlock.".format(author.id),
                    color = 15158332                        
                ) 

                await ctx.message.channel.send(embed = debounce_embed)   
        else:
            wrong_channel_embed = discord.Embed(
                title = "Wrong channel, buddy.",
                description = "Hi <@{}>. Unfortunately, this command is only available for use in <#784110037060288593>. Please try again in the appropriate channel.".format(author.id),
                color = 15158332                  
            )

            await ctx.message.channel.send(embed = wrong_channel_embed)   

def setup(bot):
    bot.add_cog(Chegg(bot))