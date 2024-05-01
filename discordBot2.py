import discord
import obtainFrame
from discord.ext import commands

cookie = ''
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='>', intents=intents)

@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')

@client.command()
async def cmds(ctx):
    await ctx.send('```list - Lists the folders\nlist [folder] - Lists the videos of a specific folder\nframe - Obtain a random frame from a random video in a random folder\nframe [folder] - Obtain a random frame from a random video in a specific folder\nframe [folder] [video] - Obtain a random frame from a specific video```')

@client.command()
async def list(ctx, folder = None):
    message = ""

    if (folder == None):
        folders = obtainFrame.returnFolders()

        if (len(folders) <= 0):
            message = "No folders found."
        else:
            message = "```"

            for folder in folders:
                message += str(folders.index(folder) + 1) + ". " + str(folder) + "\n"

            message += "```"
    else:
        if (obtainFrame.checkForFolder(folder) == False):
            message = "Folder not found."
        else:
            videos = obtainFrame.returnVideos(folder)

            if (len(videos) <= 0):
                message = "No videos found."
            else:
                message = "```"

                for video in videos:
                    message += str(videos.index(video) + 1) + ". " + str(video).split(".")[0] + "\n"

                message += "```"

    await ctx.send(message)

@client.command()
async def frame(ctx, folder = None, video = None):
    if (len(obtainFrame.returnFolders()) <= 0):
        await ctx.send("No folders found.")
    elif (folder != None) and (obtainFrame.checkForFolder(folder) == False):
        await ctx.send("Folder not found.")
    elif (folder != None) and (video != None) and (obtainFrame.checkForVideo(folder, video) == False):
        await ctx.send("Video not found.")
    else:
        if (folder == None):
            folder = obtainFrame.chooseFolder()
        
        if (len(obtainFrame.returnVideos(folder)) <= 0):
            await ctx.send("No videos found on " + obtainFrame.returnName(folder) + ".")
        else:
            message : str

            if (video != None):
                message = obtainFrame.obtainFrame(folder, video)
            else:
                message = obtainFrame.obtainFrame(folder)
                
            with open('output.jpg', 'rb') as f:
                picture = discord.File(f)
                await ctx.send(content="Folder: " + message[0] + "\nVideo: " + message[1] + "\nTimestamp: " + str(message[2]), file=picture)

client.run(cookie)