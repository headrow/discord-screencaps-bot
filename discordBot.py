import discord
import obtainFrame
from discord import app_commands

cookie = ''
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "list", description = "Lists the folders")
async def listFolders(interaction):
    folders = obtainFrame.returnFolders()

    if (len(folders) <= 0):
        message = "No folders found."
    else:
        message = "```"

        for folder in folders:
            message += str(folders.index(folder) + 1) + ". " + str(folder) + "\n"

        message += "```"

    await interaction.response.send_message(message)

@tree.command(name = "listv", description = "Lists the videos of a specific folder")
async def listVideos(interaction, folder: str):
    if (obtainFrame.checkForFolder(folder) == False):
        await interaction.response.send_message("Folder not found.")
    else:
        videos = obtainFrame.returnVideos(folder)

        if (len(videos) <= 0):
            message = "No videos found."
        else:
            message = "```"

            for video in videos:
                message += str(videos.index(video) + 1) + ". " + str(video).split(".")[0] + "\n"

            message += "```"

        await interaction.response.send_message(message)

@tree.command(name = "frame", description = "Obtain a random frame from a random video in a random folder")
async def sendFrame(interaction):
    if (len(obtainFrame.returnFolders()) <= 0):
        await interaction.response.send_message("No folders found.")
    else:
        folder = obtainFrame.chooseFolder()

        if (len(obtainFrame.returnVideos(folder)) <= 0):
            await interaction.response.send_message("No videos found on " + obtainFrame.returnName(folder) + ".")
        else:
            message = obtainFrame.obtainFrame(obtainFrame.chooseFolder())
            
            with open('output.jpg', 'rb') as f:
                picture = discord.File(f)
                await interaction.response.send_message(content="Folder: " + message[0] + "\nVideo: " + message[1] + "\nTimestamp: " + str(message[2]), file=picture)

@tree.command(name = "framef", description = "Obtain a random frame from a random video in a specific folder")
async def sendFrameF(interaction, folder: str):
    if (obtainFrame.checkForFolder(folder) == False):
        await interaction.response.send_message("Folder not found.")
    elif (len(obtainFrame.returnVideos(folder)) <= 0):
        await interaction.response.send_message("No videos found.")
    else:
        message = obtainFrame.obtainFrame(folder)
    
        with open('output.jpg', 'rb') as f:
            picture = discord.File(f)
            await interaction.response.send_message(content="Folder: " + message[0] + "\nVideo: " + message[1] + "\nTimestamp: " + str(message[2]), file=picture) 

@tree.command(name = "framev", description = "Obtain a random frame from a specific video")
async def sendFrameV(interaction, folder: str, video: str):
    if (obtainFrame.checkForVideo(folder, video) == False):
        await interaction.response.send_message("Video not found.")
    else:
        message = obtainFrame.obtainFrame(folder, video)
    
        with open('output.jpg', 'rb') as f:
            picture = discord.File(f)
            await interaction.response.send_message(content="Folder: " + message[0] + "\nVideo: " + message[1] + "\nTimestamp: " + str(message[2]), file=picture)

@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')
    await tree.sync()

client.run(cookie)