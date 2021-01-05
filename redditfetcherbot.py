import discord # import the discord api
from random import randint # random number generator
import json # to interpret the json data from reddits api
import urllib.request # to get the json data from reddits api

with open("pid.txt", "w") as f: # put the pid of the bot in a file incase it is run as pyw
    from os import getpid
    print("pid of program is %d" % getpid())
    f.write(str(getpid()))
    f.close()

def GetRandomImage(subreddit): # function that returns a url for the bot to use
    url = "https://www.reddit.com/r/{}.json?limit=102".format(subreddit) # url
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36/8mqQhSuL-09" # the user agent in the request, so reddit leaves us alone
    encountered_error = False # since we cant exit() we will set a flag by default is False
    error_message = "" # the error message for the bot to tell the user
    return_url = "" # the url to return to the user
    image_author = "" # the reddit user who made the post
    perma_link = "" # the link to the reddit post
    nsfw = False # whether or not the reddit post is nsfw

    req = urllib.request.Request(url, data=None, headers={"User-Agent": user_agent}) # the request to pass through
    try:
        jsonString = urllib.request.urlopen(req) # make the url request
    except urllib.error.HTTPError as reason: # if reddit is upsetti

        error_message = reason # encountered a http error, set the flag and the error message
        encountered_error = True

    if encountered_error == False: # a http error was not encountered
        urls = []

        # decode the json data
        jsonString = jsonString.read()
        jsonString = jsonString.decode("utf-8")
        jsonDict = json.loads(jsonString)

        if jsonDict["data"]["dist"] == 0: # check whether or not the subreddit exists
            error_message = "Error Subreddit does not exist"
            encountered_error = True
        else:
            validEnds = (".jpg",".png",".gif",".vgif") # make sure we are receiving the correct file types

            for postID in range(jsonDict["data"]["dist"]):
                if jsonDict["data"]["children"][postID]["data"]["url"].endswith(validEnds): # only add the correct urls
                    urls.append(jsonDict["data"]["children"][postID]["data"]["url"])

            if len(urls) == 0: # check whether or not the subreddit contains any images
                encountered_error = True
                error_message = "No images found"

            else:
                postID = randint(0, len(urls)-1) # get a post id to use
                return_url = urls[postID] # determine the return url
                image_author = jsonDict["data"]["children"][postID]["data"]["author"] # get the image author
                perma_link = "https://reddit.com"+jsonDict["data"]["children"][postID]["data"]["permalink"] # get the perma link to the post
                nsfw = jsonDict["data"]["children"][postID]["data"]["over_18"] # get whether or not the post is nsfw

    return return_url, encountered_error, error_message, image_author, perma_link, nsfw # return of the data



class MyClient(discord.Client): # initalize the client
    async def on_ready(self):
        print("logged on as", self.user)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="!rf subreddit")) # set the status message

    async def on_message(self, message): # get the message
        if message.author == self.user: # do not reply to ourself
            return


        if message.content.startswith("!rf"): # if the message starts with !rf then get ready
            subreddit = message.content.split(" ")[1] # get the subreddit text
            await message.channel.send("Fetching random image from r/%s" % subreddit, delete_after=3) # tell the user the image is being fetched, then delete the message after 3 seconds

            result = GetRandomImage(subreddit) # get the data

            if result[1] == True: # if the error flag is set True
                await message.channel.send("The bot encountered the following error: %s" % result[2]) # return the error

            elif message.channel.is_nsfw() == False and result[5]: # if the post is nsfw and the channel is not, then send the url to post but not the image
                await message.channel.send("This post is nsfw, however this channel is not. Only the link will be sent")
                title = "By u/"+result[3] # set the embed title
                embedRF = discord.Embed(title=title, url=result[4]) # create the embed
                await message.channel.send(embed=embedRF) # send the embed

            else: # if no other cases were found
                title = "By u/"+result[3] # set the title
                embedRF = discord.Embed(title=title, url=result[4]) # create the embed
                embedRF.set_image(url=result[0]) # set the image for the embed
                await message.channel.send(embed=embedRF) # send the embed


client = MyClient() # get the client

with open("discordBotSecret.txt", "r") as f: # get the discord bot secret from the file (because this is on github)
    client.run(f.read()) # run the client with our secret code
    f.close()
